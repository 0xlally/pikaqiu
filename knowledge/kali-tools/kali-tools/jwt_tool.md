# jwt_tool

**Category**: Credentials, password attacks, and token testing

**Purpose**: Decode, tamper, test, and crack JWT tokens.

**When to use**: Use when credentials, hashes, JWTs, login forms, Kerberos users, or password spraying opportunities are discovered.

## Commands
- `jwt_tool`

## First Commands
- `jwt_tool TOKEN`
- `jwt_tool TOKEN -M at`
- `jwt_tool TOKEN -C -d /usr/share/wordlists/rockyou.txt`

## Notes
Use after decoding claims and identifying alg/kid/jku/x5u or weak HS secrets.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
