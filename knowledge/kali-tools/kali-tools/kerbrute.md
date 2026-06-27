# kerbrute

**Category**: Credentials, password attacks, and token testing

**Purpose**: Kerberos user enumeration and password spraying.

**When to use**: Use when credentials, hashes, JWTs, login forms, Kerberos users, or password spraying opportunities are discovered.

## Commands
- `kerbrute`

## First Commands
- `kerbrute userenum -d DOMAIN users.txt --dc DC_IP`
- `kerbrute passwordspray -d DOMAIN users.txt 'Password123' --dc DC_IP`

## Notes
Prefer userenum before spraying; keep lockout risk in mind for authorized ranges.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
