"""Shared fixtures for p0wnyShellX tests.

Every test is offline: the autouse fixture makes any real HTTP call raise, so
an un-mocked LLM provider fails loudly instead of hitting the network in CI.
"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load():
    spec = importlib.util.spec_from_file_location("p0wnyShellX", ROOT / "p0wnyShellX.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def px():
    """The p0wnyShellX module, loaded once per test session."""
    return _load()


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    import urllib.request

    def _blocked(*args, **kwargs):
        raise AssertionError("real network call attempted in a test (mock it)")

    monkeypatch.setattr(urllib.request, "urlopen", _blocked)


def make_args(px, **kw):
    """Minimal argparse-like namespace accepted by generate()."""
    import argparse
    defaults = dict(password="TestPass123!", user="sysadmin", output="shell.php",
                    stdout=True, junk=None, theme=None, seed=None, no_junk=False,
                    transport="plain", no_auth=True, revshell=False, clearlog=False,
                    portscan=False, pingsweep=False, sql=False, fetch=False,
                    outdir=None, llm=None, company=None, context=None,
                    client_config=None, llm_provider=None)
    defaults.update(kw)
    return argparse.Namespace(**defaults)
