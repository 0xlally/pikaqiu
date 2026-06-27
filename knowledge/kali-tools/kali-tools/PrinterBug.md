# PrinterBug

**Category**: NTLM relay, coercion, and ADCS relay chains

**Purpose**: MS-RPRN printer bug coercion.

**When to use**: Use when NTLM relay, ADCS web enrollment, IPv6 poisoning, EFSRPC/MS-RPRN coercion, or machine account abuse is in scope.

## Commands
- `printerbug`

## Paths
- `/opt/ad-tools/krbrelayx/printerbug.py`

## First Commands
- `printerbug DOMAIN/USER:PASS@TARGET LISTENER`

## Notes
Wrapper runs the krbrelayx printerbug script.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
