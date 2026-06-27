# nuclei

**Category**: Web discovery, fuzzing, and vulnerability checks

**Purpose**: Template-based vulnerability, exposure, and misconfiguration detection.

**When to use**: Use when the target exposes HTTP/HTTPS, APIs, parameters, directories, virtual hosts, known products, or reflected input.

## Commands
- `nuclei`

## First Commands
- `nuclei -u http://TARGET -severity medium,high,critical`
- `nuclei -u http://TARGET -tags cve,exposure,misconfig`

## Notes
Use findings as leads; verify manually before relying on them.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
