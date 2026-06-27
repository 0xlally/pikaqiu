# smbmap

**Category**: Active Directory, Kerberos, LDAP, and SMB enumeration

**Purpose**: Enumerate SMB shares, permissions, and accessible files.

**When to use**: Use when a Windows domain, SMB, LDAP, Kerberos, domain credentials, or internal Windows hosts are discovered.

## Commands
- `smbmap`

## First Commands
- `smbmap -H TARGET`
- `smbmap -H TARGET -u USER -p PASS -R`

## Notes
Use before recursive downloads; capture readable shares and interesting files.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
