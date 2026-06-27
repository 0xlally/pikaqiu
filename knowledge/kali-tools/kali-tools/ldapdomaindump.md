# ldapdomaindump

**Category**: Active Directory, Kerberos, LDAP, and SMB enumeration

**Purpose**: Dump LDAP domain users, groups, computers, ACL-related data, and trusts.

**When to use**: Use when a Windows domain, SMB, LDAP, Kerberos, domain credentials, or internal Windows hosts are discovered.

## Commands
- `ldapdomaindump`

## First Commands
- `ldapdomaindump -u DOMAIN\\USER -p PASS DC_IP -o ldapdump`

## Notes
Good after obtaining valid domain credentials.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
