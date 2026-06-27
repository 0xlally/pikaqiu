# rg

**Category**: Local source, filesystem, and artifact search

**Purpose**: Fast recursive text and file-name search.

**When to use**: Use when challenge files, extracted source, logs, mounted volumes, or a shell/RCE filesystem need fast focused search.

## Commands
- `rg`

## First Commands
- `rg -n "flag|password|secret|token" .`
- `rg --files . | rg -i 'flag|config|env|backup'`

## Notes
Prefer rg for focused local searches. The sandbox flag path dictionary is `/opt/pikaqiu-tools/flag-paths.txt`.

## Captured Help
No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.
