# netexec

**Category**: Active Directory, Kerberos, LDAP, and SMB enumeration

**Purpose**: Enumerate and manage SMB/LDAP/WinRM/MSSQL/SSH services and AD environments.

**When to use**: Use when a Windows domain, SMB, LDAP, Kerberos, domain credentials, or internal Windows hosts are discovered.

## Commands
- `netexec`
- `nxc`

## First Commands
- `netexec smb TARGET -u USER -p PASS --shares`
- `netexec ldap DC_IP -u USER -p PASS --users --groups`

## Notes
Use for quick domain/service posture and credential validation.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
