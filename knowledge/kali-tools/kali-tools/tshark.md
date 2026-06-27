# tshark

**Category**: Packet capture and protocol analysis

**Purpose**: CLI packet capture and protocol analysis.

**When to use**: Use when traffic evidence, protocol debugging, credentials in transit, or pcap analysis matters.

## Commands
- `tshark`

## First Commands
- `tshark -i any -a duration:30 -w capture.pcap`
- `tshark -r capture.pcap -Y 'http || dns || kerberos || ldap || smb2'`

## Notes
Prefer tshark in containers; Wireshark GUI may not be practical.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
