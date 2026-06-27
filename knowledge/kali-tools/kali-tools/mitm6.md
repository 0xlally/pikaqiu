# mitm6

**Category**: NTLM relay, coercion, and ADCS relay chains

**Purpose**: IPv6 DNS poisoning to capture or relay Windows authentication.

**When to use**: Use when NTLM relay, ADCS web enrollment, IPv6 poisoning, EFSRPC/MS-RPRN coercion, or machine account abuse is in scope.

## Commands
- `mitm6`

## First Commands
- `mitm6 -d DOMAIN`
- `mitm6 --domain DOMAIN --host-allowlist HOST`

## Notes
Usually paired with ntlmrelayx; scope carefully.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
