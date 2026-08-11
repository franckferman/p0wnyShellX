"""Runtime end-to-end tests: build real shells, serve them with `php -S`,
and drive them through the actual HTTP protocol — login, command exec, cwd
persistence, all three transports, and the optional feature commands.

`php -l` proves syntax; this suite proves the shell *works*.
Skipped entirely when no php CLI is available.
"""
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from shellx_client import Protocol, ShellxClient  # noqa: E402

HAVE_PHP = shutil.which("php") is not None
pytestmark = pytest.mark.skipif(not HAVE_PHP, reason="php CLI not available")

PASSWORD = "Runt1meTest!"
USER = "operator"


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _build(tmp_path: Path, name: str, *extra: str) -> Path:
    out = tmp_path / name
    subprocess.run(
        [sys.executable, str(ROOT / "p0wnyShellX.py"), "-p", PASSWORD, "-u", USER,
         "--client-config", str(out) + ".json", "-o", str(out), *extra],
        check=True, capture_output=True)
    return out


@pytest.fixture(scope="module")
def server(tmp_path_factory):
    """php -S serving a dir with one shell per transport + one full-featured."""
    tmp = tmp_path_factory.mktemp("runtime")
    shells = {
        "plain": _build(tmp, "plain.php"),
        "mimic": _build(tmp, "mimic.php", "--transport", "mimic"),
        "rc4":   _build(tmp, "rc4.php", "--transport", "rc4"),
        "full":  _build(tmp, "full.php", "--revshell", "--clearlog",
                        "--portscan", "--pingsweep", "--sql", "--fetch"),
    }
    port = _free_port()
    proc = subprocess.Popen(["php", "-S", f"127.0.0.1:{port}", "-t", str(tmp)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(base + "/plain.php", timeout=1)
            break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        pytest.fail("php -S did not come up")
    yield base, shells
    proc.kill()


def _client(base, shell_path, via="sidecar"):
    proto = (Protocol.from_shell_file(str(shell_path)) if via == "shell"
             else Protocol.from_sidecar(str(shell_path) + ".json"))
    return ShellxClient(f"{base}/{shell_path.name}", proto, timeout=15)


@pytest.mark.parametrize("transport", ["plain", "mimic", "rc4"])
@pytest.mark.parametrize("via", ["shell", "sidecar"])
def test_login_and_exec(server, transport, via):
    base, shells = server
    c = _client(base, shells[transport], via=via)

    # Wrong password must be rejected (and slow — random 400-700ms sleep)
    assert not c.login(USER, "wrong-password")
    # Right password
    assert c.login(USER, PASSWORD)
    out = c.exec("id")
    assert "uid=" in out


@pytest.mark.parametrize("transport", ["plain", "mimic", "rc4"])
def test_cwd_persistence(server, transport):
    base, shells = server
    c = _client(base, shells[transport])
    assert c.login(USER, PASSWORD)
    c.exec("cd /tmp")
    assert c.exec("pwd").strip() == "/tmp"


def test_unauthenticated_ajax_cannot_execute(server):
    """Critical: the auth gate must run before the route dispatcher."""
    base, shells = server
    c = _client(base, shells["plain"])
    # No login — a direct AJAX hit must not return a command response.
    try:
        out = c.exec("id")
    except Exception:
        out = ""  # protocol garbage (login HTML) is a pass
    assert "uid=" not in out


def test_clearlog(server, tmp_path):
    base, shells = server
    c = _client(base, shells["full"])
    assert c.login(USER, PASSWORD)
    target = tmp_path / "fake_access.log"
    target.write_text("10.0.0.1 GET /ok\n192.168.1.5 GET /shell.php\n10.0.0.2 GET /ok2\n")
    out = c.exec(f"clearlog {target} 192\\.168")
    assert "Removed 1/3" in out
    assert "192.168" not in target.read_text()


def test_portscan_localhost(server):
    base, shells = server
    port = base.rsplit(":", 1)[1]
    c = _client(base, shells["full"])
    assert c.login(USER, PASSWORD)
    out = c.exec(f"portscan 127.0.0.1 {port} --fast")
    assert port in out and "open" in out.lower()  # the php -S port itself
    out2 = c.exec("portscan 127.0.0.1 1 --fast")
    assert "No open ports" in out2                # closed-port path


def test_pingsweep_localhost(server):
    base, shells = server
    port = base.rsplit(":", 1)[1]
    c = _client(base, shells["full"])
    assert c.login(USER, PASSWORD)
    out = c.exec(f"pingsweep 127.0.0.1 --ports {port} --fast")
    assert "127.0.0.1" in out and "up" in out.lower()


# ── fetch module (pivot recon) ───────────────────────────────────────────────

@pytest.fixture(scope="module")
def content_server(tmp_path_factory):
    """A plain HTTP server hosting a marker file — the 'internal' resource."""
    import functools
    import http.server
    import threading
    tmp = tmp_path_factory.mktemp("content")
    (tmp / "secret.txt").write_text("INTERNAL-PORTAL-MARKER-42")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def test_fetch_through_target(server, content_server):
    base, shells = server
    c = _client(base, shells["full"])
    assert c.login(USER, PASSWORD)
    out = c.exec(f"fetch {content_server}/secret.txt")
    assert "INTERNAL-PORTAL-MARKER-42" in out


def test_fetch_fsockopen_fallback(server, content_server, tmp_path):
    """Same fetch, but with allow_url_fopen=0 → a fallback path must serve it.

    Locally (no curl extension) this exercises the raw fsockopen path; in CI
    (curl present) it exercises the curl path. Either way the content must
    come through when fopen is unavailable.
    """
    base, shells = server
    src = tmp_path / "nofopen.php"
    shutil.copy(shells["full"], src)
    port = _free_port()
    proc = subprocess.Popen(
        ["php", "-d", "allow_url_fopen=0", "-S", f"127.0.0.1:{port}", "-t", str(tmp_path)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1)
        c = ShellxClient(f"http://127.0.0.1:{port}/nofopen.php",
                         Protocol.from_sidecar(str(shells["full"]) + ".json"), timeout=15)
        assert c.login(USER, PASSWORD)
        out = c.exec(f"fetch {content_server}/secret.txt")
        assert "INTERNAL-PORTAL-MARKER-42" in out
        assert any(engine in out for engine in ("fsockopen", "curl"))
    finally:
        proc.kill()


# ── sql module (PDO) ─────────────────────────────────────────────────────────

HAVE_PDO_SQLITE = HAVE_PHP and b"pdo_sqlite" in subprocess.run(
    ["php", "-m"], capture_output=True).stdout.lower()


@pytest.mark.skipif(not HAVE_PDO_SQLITE, reason="pdo_sqlite not available locally (covered in CI)")
def test_sql_console_sqlite(server, tmp_path):
    import sqlite3
    db = tmp_path / "app.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE users (id INTEGER, login TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'admin'), (2, 'jdoe')")
    conn.commit()
    conn.close()

    base, shells = server
    c = _client(base, shells["full"])
    assert c.login(USER, PASSWORD)
    out = c.exec(f'sql sqlite:{db} "SELECT * FROM users ORDER BY id"')
    assert "admin" in out and "jdoe" in out and "login" in out
    out2 = c.exec(f"sql sqlite:{db} \"UPDATE users SET login='root' WHERE id=2\"")
    assert "1 row(s) affected" in out2
