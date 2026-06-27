# kerberoast

**Category**: Active Directory, Kerberos, LDAP, and SMB enumeration

**Purpose**: Enumerate SPNs and request Kerberoast hashes.

**When to use**: Use when a Windows domain, SMB, LDAP, Kerberos, domain credentials, or internal Windows hosts are discovered.

## Commands
- `impacket-GetUserSPNs`
- `GetUserSPNs.py`

## First Commands
- `impacket-GetUserSPNs DOMAIN/USER:PASS -dc-ip DC_IP -request -outputfile spn.hashes`

## Notes
Crack returned hashes with the hashcat mode indicated by the hash format.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
