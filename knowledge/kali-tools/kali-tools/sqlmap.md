# sqlmap

**Category**: Web discovery, fuzzing, and vulnerability checks

**Purpose**: SQL injection detection, exploitation, database enumeration, and dump automation.

**When to use**: Use when the target exposes HTTP/HTTPS, APIs, parameters, directories, virtual hosts, known products, or reflected input.

## Commands
- `sqlmap`

## First Commands
- `sqlmap -u 'http://TARGET/item?id=1' --batch --level 2 --risk 1`
- `sqlmap -r request.txt --batch --current-user --current-db`

## Notes
Use a captured request file when cookies, POST bodies, or custom headers matter.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
