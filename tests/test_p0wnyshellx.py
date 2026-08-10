"""Offline test suite for p0wnyShellX.

Covers: generation invariants, seed determinism, theme/transport matrix,
optional features, and the whole optional LLM layer (parser, validators,
denylist, provider dispatch, fallback, caching, prompt context) with a
mocked HTTP backend.
"""
import io
import shutil
import subprocess
import urllib.error

import pytest

from conftest import make_args

HAVE_PHP = shutil.which("php") is not None


def gen(px, **kw):
    return px.generate(make_args(px, **kw), info=io.StringIO())


# ── Core generation ──────────────────────────────────────────────────────────

def test_default_build_contains_core(px):
    php = gen(px)
    assert "<?php" in php and "function " in php
    auth = gen(px, no_auth=False)   # hex fallback keeps this php-free
    assert "session_name('" in auth  # per-build session cookie name


def test_seed_determinism(px):
    assert gen(px, seed=42) == gen(px, seed=42)


def test_two_unseeded_runs_differ(px):
    assert gen(px) != gen(px)


@pytest.mark.parametrize("theme", ["infra-dark", "corporate-blue", "matrix",
                                   "zabbix", "ctos", "fsociety", "russia",
                                   "korea", "france", "usa", "redux",
                                   "poly", "none"])
def test_all_themes_build(px, theme):
    php = gen(px, theme=theme)
    assert "<?php" in php


@pytest.mark.parametrize("transport", ["plain", "mimic", "rc4"])
def test_all_transports_build(px, transport):
    php = gen(px, transport=transport)
    assert "<?php" in php
    if transport == "rc4":
        assert "tEnc" in php and "tDec" in php


def test_mimic_replaces_plain_param_names(px):
    ctx = px.generate_transport_context(__import__("random").Random(1), "mimic")
    plain = {"cmd", "cwd", "filename", "type", "path", "file"}
    assert not plain & {ctx["p_cmd"], ctx["p_cwd"], ctx["p_filename"],
                        ctx["p_filetype"], ctx["p_path"], ctx["p_file"]}


def test_junk_bounds(px):
    no_junk = gen(px, junk=0, seed=7)
    with_junk = gen(px, junk=60, seed=7)
    assert with_junk.count("function ") > no_junk.count("function ")


def test_optional_features_compiled_in(px):
    php = gen(px, revshell=True, clearlog=True, portscan=True, pingsweep=True, seed=3)
    bare = gen(px, seed=3)
    # optional routes exist only when requested (search the shuffled case labels)
    assert len(php) > len(bare)


def test_no_auth_has_no_login(px):
    php = gen(px, no_auth=True)
    assert "password_verify" not in php


@pytest.mark.skipif(not HAVE_PHP, reason="php CLI not available")
@pytest.mark.parametrize("kw", [{}, {"theme": "poly"}, {"theme": "none"},
                                {"transport": "rc4"}, {"transport": "mimic"},
                                {"revshell": True, "portscan": True}])
def test_generated_php_lints(px, kw, tmp_path):
    kw.setdefault("seed", 11)
    php = gen(px, **kw)
    f = tmp_path / "shell.php"
    f.write_text(php)
    r = subprocess.run(["php", "-l", str(f)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.skipif(not HAVE_PHP, reason="php CLI not available")
def test_auth_build_embeds_bcrypt(px):
    php = gen(px, no_auth=False, seed=5)
    assert "$2y$12$" in php and "password_verify" in php


# ── LLM layer ────────────────────────────────────────────────────────────────

def test_llm_spec_parsing(px):
    p = px.LLMProvider("ollama")
    assert p.provider == "ollama" and p.model == "llama3.2"
    p = px.LLMProvider("ollama:qwen2.5")
    assert p.model == "qwen2.5"
    with pytest.raises(ValueError):
        px.LLMProvider("bogus")


def test_parse_llm_list_formats(px):
    assert px._parse_llm_list('["a", "b"]') == ["a", "b"]
    assert px._parse_llm_list('```json\n["a", "b"]\n```') == ["a", "b"]
    assert px._parse_llm_list('Sure! Here you go:\n["a", "b"]') == ["a", "b"]
    assert px._parse_llm_list("1. alpha\n2. beta\n- gamma") == ["alpha", "beta", "gamma"]


def _fake_llm(px, items):
    """LLMProvider whose _raw returns a canned JSON list; records prompts."""
    prov = px.LLMProvider("ollama")
    prov.prompts = []
    prov._raw = lambda prompt: (prov.prompts.append(prompt),
                                __import__("json").dumps(items))[1]
    return prov


def test_variants_validates_atoms(px):
    prov = _fake_llm(px, ["fetchClusterStatus", "1bad", "has space",
                          "dropTable(); DELETE", "syncData", "a" * 60, "fetchClusterStatus"])
    out = prov.variants("func_names", 10, __import__("random").Random(1))
    assert out == ["fetchClusterStatus", "syncData"]   # invalid + duplicate filtered


def test_variants_denylist(px):
    prov = _fake_llm(px, ["decodePayloadBase64", "runShellCmd", "execReport",
                          "fetchPickingList"])
    out = prov.variants("func_names", 10, __import__("random").Random(1))
    assert out == ["fetchPickingList"]


def test_variants_fallback_on_network_error(px, monkeypatch):
    prov = px.LLMProvider("ollama")

    def boom(prompt):
        raise urllib.error.URLError("down")

    prov._raw = boom
    assert prov.variants("func_names", 10, __import__("random").Random(1)) == []


def test_variants_cached(px):
    calls = []
    prov = px.LLMProvider("ollama")
    prov._raw = lambda p: (calls.append(p), '["alphaOne","betaTwo"]')[1]
    rng = __import__("random").Random(1)
    assert prov.variants("func_names", 5, rng) == ["alphaOne", "betaTwo"]
    assert prov.variants("func_names", 5, rng) == ["alphaOne", "betaTwo"]
    assert len(calls) == 1


def test_company_context_reaches_prompt(px):
    prov = px.LLMProvider("ollama", company="Acme Logistics", context="freight, France")
    prov._raw = lambda prompt: (setattr(prov, "seen", prompt), '["fetchPickingList"]')[1]
    prov.variants("func_names", 5, __import__("random").Random(1))
    assert "Acme Logistics" in prov.seen and "freight, France" in prov.seen


def test_llm_names_land_in_build(px):
    prov = _fake_llm(px, ["fetchPickingList", "reconcileFreightManifest",
                          "validateContainerRouting", "auditWarehouseStock"])
    info = io.StringIO()
    # junk=200 draws most of the augmented pool, so LLM names are certain to appear
    php = px.generate(make_args(px, llm_provider=prov, seed=9, junk=200), info=info)
    assert any(n in php for n in ("fetchPickingList", "reconcileFreightManifest",
                                  "validateContainerRouting", "auditWarehouseStock"))
    assert "static pools only" not in info.getvalue()


def test_llm_failure_builds_anyway(px):
    prov = px.LLMProvider("ollama")

    def boom(prompt):
        raise urllib.error.URLError("down")

    prov._raw = boom
    info = io.StringIO()
    php = px.generate(make_args(px, llm_provider=prov, seed=9), info=info)
    assert "<?php" in php
    assert "static pools only" in info.getvalue()


def test_static_pools_never_mutated(px):
    before = (len(px.PHP_FUNC_POOL), len(px.MIMIC_PARAM_POOL), len(px.POLY_APP_NAMES))
    prov = _fake_llm(px, ["fetchPickingList", "brandNewParam", "FleetOps Console"])
    px.generate(make_args(px, llm_provider=prov, seed=9), info=io.StringIO())
    after = (len(px.PHP_FUNC_POOL), len(px.MIMIC_PARAM_POOL), len(px.POLY_APP_NAMES))
    assert before == after
