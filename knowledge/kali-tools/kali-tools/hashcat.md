# hashcat

**Category**: Credentials, password attacks, and token testing

**Purpose**: Offline hash cracking with many hash modes.

**When to use**: Use when credentials, hashes, JWTs, login forms, Kerberos users, or password spraying opportunities are discovered.

## Commands
- `hashcat`

## First Commands
- `hashcat --help | grep -i ntlm`
- `hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt`

## Notes
Identify the hash mode first; use rockyou or focused wordlists before mask attacks.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
