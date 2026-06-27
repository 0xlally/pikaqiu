# hydra

**Category**: Credentials, password attacks, and token testing

**Purpose**: Online authentication brute force and password spraying across many protocols.

**When to use**: Use when credentials, hashes, JWTs, login forms, Kerberos users, or password spraying opportunities are discovered.

## Commands
- `hydra`

## First Commands
- `hydra -L users.txt -P passwords.txt TARGET ssh -V -f`
- `hydra -l USER -P passwords.txt TARGET http-post-form '/login:user=^USER^&pass=^PASS^:F=Invalid'`

## Notes
Use carefully with small lists and clear failure markers to avoid wasting rounds.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
