# ysoserial

**Category**: Exploit frameworks, payloads, deserialization, and local privesc enumeration

**Purpose**: Generate Java deserialization payloads.

**When to use**: Use after confirming a vulnerable service, exploit module, deserialization sink, or local shell.

## Commands
- `ysoserial`

## Paths
- `/opt/exploit-tools/ysoserial-all.jar`

## First Commands
- `ysoserial CommonsCollections1 'id' | base64 -w0`
- `ysoserial --help`

## Notes
Understand whether output execution is local payload generation or remote target execution.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
