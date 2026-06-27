# ffuf

**Category**: Web discovery, fuzzing, and vulnerability checks

**Purpose**: High-speed directory, file, parameter, API, and virtual-host fuzzing.

**When to use**: Use when the target exposes HTTP/HTTPS, APIs, parameters, directories, virtual hosts, known products, or reflected input.

## Commands
- `ffuf`

## First Commands
- `ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc all`
- `ffuf -u http://IP/ -H 'Host: FUZZ.domain.local' -w vhosts.txt`

## Notes
Always establish baseline filters such as -fs, -fw, -fc, or -mc after a short test.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
