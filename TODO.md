# TODO / Roadmap

## Planned

- [ ] Obfuscated HTTP protocol — XOR+gzip+base64 for request and response payloads (à la Weevely), making POST body opaque to WAF inspection
- [ ] Built-in reverse shell — `revshell <IP> <PORT>` command inside the terminal, multi-method (bash, python3, perl, php) with automatic fallback
- [ ] Log clearing — `clearlog /var/log/apache2/access.log <pattern>` to strip matching lines in-place
- [ ] Internal port scan — `portscan 10.0.0.1-254 22,80,443` for lateral movement recon from the target host

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
