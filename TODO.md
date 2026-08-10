# TODO / Roadmap

**Project goal: full Weevely parity** — one generator that covers both the browser-terminal and the CLI-framework use cases, so the two tools no longer have to be combined.

## Planned (Weevely parity gaps)

- [ ] Obfuscated HTTP protocol — XOR+gzip+base64 for request and response payloads (à la Weevely), making POST body opaque to WAF inspection
- [ ] Non-interactive CLI client — scripted, pipeable command execution against a deployed shell (automation, à la Weevely client); the browser stays the primary interface, the CLI is for tooling chains
- [ ] SQL console module — interactive SQL queries against databases reachable from the target (à la `:sql_console`)
- [ ] Proxy/pivot module — route operator traffic through the target host (à la `:net_proxy`)

## Low priority / won't implement soon

- [ ] `disable_functions` bypass via mod_cgi — requires Apache + mod_cgi enabled + `AllowOverride FileInfo` + a web-writable directory. All four conditions are rarely met simultaneously in production environments, making this bypass mostly theoretical in practice.

## Done

- [x] Polymorphic generator — unique PHP file on every run (function names, routing tokens, junk, exec order)
- [x] bcrypt password hashing at generation time — no plaintext ever stored in the output file
- [x] Seed reproducibility — deterministic builds with `--seed`
- [x] Random routing tokens — replaces static `?feature=shell`
- [x] Random PHP/JS/HTML function and variable names — 250+ business name pool
- [x] Dynamic junk functions — 20–80 decoy PHP functions per run, 20 body templates
- [x] Shuffled exec fallback chain — exec/shell_exec/system/passthru/popen order varies per run
- [x] CSS camouflage themes — infra-dark, corporate-blue, matrix
- [x] CI — polymorphism validation, bcrypt verification, PHP lint, static signature detection
- [x] GitHub Releases — auto-generate 3 example shells (one per theme) on version tag push
- [x] GitHub Pages — interactive command builder at franckferman.github.io/p0wnyShellX
- [x] Built-in reverse shell — `revshell <IP> <PORT>` command, multi-method (bash, python3, perl, php) fallback chain
- [x] Log clearing — `clearlog <file> <pattern>` strips matching lines in-place from any readable/writable file
- [x] Internal port scan — `portscan <ip[-range]> <port[s]>` TCP scan via fsockopen from the target host
- [x] UTF-8 output — `b64u()` helper using `decodeURIComponent(escape(atob(s)))` fixes mojibake on non-ASCII command output
- [x] Optional LLM pool augmentation (v3.0.0) — `--llm provider[:model]` (ollama local, or anthropic/openai/deepseek/kimi via env keys): fresh function names, app names, mimic params and junk words per build; atoms-only validation + denylist; silent static-pool fallback
- [x] Target-context camouflage (v3.0.0) — `--company` / `--context`: names generated in the target organization's vocabulary
- [x] Per-build session cookie name (v3.0.0) — random plausible name instead of `PHPSESSID`
- [x] Offline pytest suite (v3.0.0) — 40 tests: generation invariants, seed determinism, theme/transport matrix, `php -l`, full LLM layer with mocked HTTP
