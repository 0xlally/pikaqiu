# nmap

**Category**: Web discovery, fuzzing, and vulnerability checks

**Purpose**: Port scanning, service/version detection, OS hints, and NSE enumeration.

**When to use**: Use when the target exposes HTTP/HTTPS, APIs, parameters, directories, virtual hosts, known products, or reflected input.

## Commands
- `nmap`

## First Commands
- `nmap -sV -sC -Pn -oN nmap.txt TARGET`
- `nmap --script vuln -Pn TARGET`

## Notes
Avoid full port scans when the mission already gives a precise URL/port unless there is evidence of more services.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
