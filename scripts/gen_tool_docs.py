"""Generate sandbox tool documentation from tool_catalog.json.

The generated ZIP is indexed by the PikaQiu knowledge base. If the sandbox is
running, this script also captures each CLI tool's --help/-h output.
"""
from __future__ import annotations

import io
import json
import shlex
import subprocess
import zipfile
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).parent.parent
CATALOG_PATH = ROOT / "scripts" / "sandbox-tools" / "tool_catalog.json"
CONTAINER = "pikaqiu-sandbox-1"


FALLBACK_TOOLS: dict[str, list[str]] = {
    "nmap": ["nmap"],
    "ffuf": ["ffuf"],
    "sqlmap": ["sqlmap"],
    "nuclei": ["nuclei"],
    "hydra": ["hydra"],
    "hashcat": ["hashcat"],
    "netexec": ["netexec", "nxc"],
    "smbmap": ["smbmap"],
    "impacket-GetNPUsers": ["impacket-GetNPUsers"],
    "impacket-GetUserSPNs": ["impacket-GetUserSPNs"],
    "impacket-secretsdump": ["impacket-secretsdump"],
    "searchsploit": ["searchsploit"],
}


def load_catalog() -> dict[str, Any]:
    if not CATALOG_PATH.is_file():
        return {}
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def iter_catalog_tools(catalog: dict[str, Any]) -> Iterable[tuple[dict[str, Any], dict[str, Any]]]:
    for category in catalog.get("categories", []):
        for tool in category.get("tools", []):
            yield category, tool


def fallback_catalog() -> dict[str, Any]:
    return {
        "categories": [
            {
                "id": "fallback",
                "title": "Fallback Kali tools",
                "when": "Fallback list used when tool_catalog.json is missing.",
                "tools": [
                    {"name": name, "commands": commands, "purpose": "Kali sandbox tool"}
                    for name, commands in FALLBACK_TOOLS.items()
                ],
            }
        ]
    }


def _run_help_capture(command: str) -> str:
    quoted = shlex.quote(command)
    script = (
        f"({quoted} --help 2>&1 || {quoted} -h 2>&1 || {quoted} help 2>&1 || true) | head -160; "
        "echo ''; echo 'BINARY_PATH:'; "
        f"command -v {quoted} 2>/dev/null || echo {quoted}"
    )
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-lc", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=20,
    )
    return (result.stdout or "").strip()


def get_tool_help(commands: list[str]) -> tuple[str, str] | None:
    for command in commands:
        try:
            output = _run_help_capture(command)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
        first_line = output.splitlines()[0] if output else ""
        if output and len(output) > 40 and "not found" not in first_line.lower():
            return command, output
    return None


def _bullet_lines(values: list[str]) -> str:
    if not values:
        return ""
    return "\n".join(f"- `{value}`" for value in values)


def _plain_bullets(values: list[str]) -> str:
    if not values:
        return ""
    return "\n".join(f"- {value}" for value in values)


def generate_markdown(
    *,
    category: dict[str, Any],
    tool: dict[str, Any],
    binary_path: str = "",
    raw_help: str = "",
) -> str:
    name = tool.get("name", "unknown-tool")
    commands = [str(item) for item in tool.get("commands", [])]
    paths = [str(item) for item in tool.get("paths", [])]
    first_commands = [str(item) for item in tool.get("first_commands", [])]
    notes = tool.get("notes", "")
    purpose = tool.get("purpose", "")
    category_title = category.get("title", category.get("id", "uncategorized"))
    when = category.get("when", "")

    parts = [
        f"# {name}",
        "",
        f"**Category**: {category_title}",
    ]
    if purpose:
        parts.extend(["", f"**Purpose**: {purpose}"])
    if when:
        parts.extend(["", f"**When to use**: {when}"])
    if commands:
        parts.extend(["", "## Commands", _bullet_lines(commands)])
    if paths:
        parts.extend(["", "## Paths", _bullet_lines(paths)])
    if first_commands:
        parts.extend(["", "## First Commands", _bullet_lines(first_commands)])
    if notes:
        parts.extend(["", f"## Notes\n{notes}"])
    if binary_path:
        parts.extend(["", f"**Detected binary**: `{binary_path}`"])
    if raw_help:
        clean_help = raw_help.strip()
        parts.extend(["", "## Captured Help", "```", clean_help, "```"])
    else:
        parts.extend([
            "",
            "## Captured Help",
            "No live help output was captured. Start with the commands above, or run the tool with `-h`/`--help` in the sandbox.",
        ])

    return "\n".join(parts).strip() + "\n"


def main() -> None:
    catalog = load_catalog() or fallback_catalog()
    out_dir = ROOT / "knowledge"
    out_zip = out_dir / "kali-tools.zip"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating tool docs from catalog: {CATALOG_PATH}")
    print(f"Attempting live help capture from container '{CONTAINER}'...")

    results: dict[str, str] = {}
    captured: list[str] = []
    catalog_only: list[str] = []

    for category, tool in iter_catalog_tools(catalog):
        name = str(tool.get("name", "unknown-tool"))
        commands = [str(item) for item in tool.get("commands", [])]
        found = get_tool_help(commands) if commands else None
        if found:
            binary_path, raw_help = found
            captured.append(name)
            print(f"  capture: {name}")
            md = generate_markdown(
                category=category,
                tool=tool,
                binary_path=binary_path,
                raw_help=raw_help,
            )
        else:
            catalog_only.append(name)
            print(f"  catalog: {name}")
            md = generate_markdown(category=category, tool=tool)
        results[name] = md

    index_lines = [
        "# Kali Tool Reference Index",
        "",
        "Generated from `scripts/sandbox-tools/tool_catalog.json`.",
        "",
        "## Tools",
    ]
    for tool_name in sorted(results):
        index_lines.append(f"- [{tool_name}](kali-tools/{tool_name}.md)")
    if captured:
        index_lines.extend(["", "## Live Help Captured", _plain_bullets(sorted(captured))])
    if catalog_only:
        index_lines.extend(["", "## Catalog Only", _plain_bullets(sorted(catalog_only))])

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for tool_name, md in results.items():
            zf.writestr(f"kali-tools/{tool_name}.md", md.encode("utf-8"))
        zf.writestr("kali-tools/INDEX.md", "\n".join(index_lines).encode("utf-8"))

    out_zip.write_bytes(buf.getvalue())
    print(f"Wrote {out_zip} ({out_zip.stat().st_size // 1024} KB, {len(results)} tools)")
    print(f"Live help captured: {len(captured)}")
    print(f"Catalog-only docs: {len(catalog_only)}")


if __name__ == "__main__":
    main()
