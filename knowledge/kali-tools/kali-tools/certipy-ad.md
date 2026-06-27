# certipy-ad

**Category**: Active Directory, Kerberos, LDAP, and SMB enumeration

**Purpose**: ADCS enumeration and exploitation.

**When to use**: Use when a Windows domain, SMB, LDAP, Kerberos, domain credentials, or internal Windows hosts are discovered.

## Commands
- `certipy-ad`
- `certipy`

## First Commands
- `certipy-ad find -u USER@DOMAIN -p PASS -dc-ip DC_IP -vulnerable -stdout`
- `certipy-ad req -u USER@DOMAIN -p PASS -ca CA_NAME -template TEMPLATE -dc-ip DC_IP`

## Notes
Use for ESC templates, enrollment agents, relay to ADCS, and certificate authentication.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
