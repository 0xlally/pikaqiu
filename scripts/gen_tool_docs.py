"""Generate Kali tool documentation from the running sandbox container and bundle as a ZIP."""
from __future__ import annotations
import io
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent.parent

TOOLS: dict[str, list[str]] = {
    # Network scanning
    "nmap":               ["nmap"],
    "masscan":            ["masscan"],
    # Web directory enumeration
    "gobuster":           ["gobuster"],
    "ffuf":               ["/root/go/bin/ffuf", "ffuf"],
    "feroxbuster":        ["feroxbuster"],
    "dirb":               ["dirb"],
    "dirsearch":          ["dirsearch", "/usr/lib/python3/dist-packages/dirsearch/dirsearch.py"],
    "wfuzz":              ["wfuzz"],
    "nikto":              ["nikto"],
    # Web utilities
    "curl":               ["curl"],
    "httpx":              ["/root/go/bin/httpx", "httpx"],
    "whatweb":            ["whatweb"],
    "wpscan":             ["wpscan"],
    # Vulnerability / exploitation
    "sqlmap":             ["sqlmap"],
    "nuclei":             ["/root/go/bin/nuclei", "nuclei"],
    "commix":             ["commix"],
    # Brute force / password
    "hydra":              ["hydra"],
    "medusa":             ["medusa"],
    "john":               ["john"],
    "hashcat":            ["hashcat"],
    # Post-exploitation / pivoting
    "netcat-nc":          ["nc"],
    "socat":              ["socat"],
    "msfvenom":           ["msfvenom"],
    # Impacket
    "impacket-secretsdump": ["impacket-secretsdump"],
    "impacket-psexec":    ["impacket-psexec"],
    "impacket-smbexec":   ["impacket-smbexec"],
    "impacket-wmiexec":   ["impacket-wmiexec"],
    "impacket-getTGT":    ["impacket-getTGT"],
    "impacket-GetNPUsers": ["impacket-GetNPUsers"],
    "impacket-GetUserSPNs": ["impacket-GetUserSPNs"],
    "impacket-smbclient": ["impacket-smbclient"],
    # CrackMapExec / NetExec
    "crackmapexec":       ["crackmapexec", "cme"],
    "netexec":            ["netexec", "nxc"],
    # DNS
    "dnsenum":            ["dnsenum"],
    "dnsrecon":           ["dnsrecon"],
    "dig":                ["dig"],
    # Misc
    "netdiscover":        ["netdiscover"],
    "whois":              ["whois"],
    "enum4linux":         ["enum4linux"],
    "smbclient":          ["smbclient"],
    "rpcclient":          ["rpcclient"],
}

CONTAINER = "pikaqiu-sandbox-1"


def _run_help_capture(path: str) -> str:
    script = (
        f"{{ {path} --help 2>&1 || {path} -h 2>&1; }} | head -100; "
        f"echo ''; echo 'BINARY_PATH:'; which {path} 2>/dev/null || echo 'not in PATH'"
    )
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "bash", "-c", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=15,
    )
    return (result.stdout or "").strip()


def get_tool_help(tool_name: str, paths: list[str]) -> tuple[str, str] | None:
    for path in paths:
        try:
            output = _run_help_capture(path)
            if output and len(output) > 60 and "not found" not in output.split("\n")[0]:
                return path, output
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    return None


def generate_markdown(tool_name: str, binary_path: str, raw_help: str) -> str:
    lines = raw_help.splitlines()
    # Extract binary path from last lines
    bin_path_line = ""
    clean_lines = []
    for ln in lines:
        if ln.startswith("BINARY_PATH:"):
            continue
        clean_lines.append(ln)
        if ln.startswith("/") and tool_name.split("-")[-1].lower() in ln.lower():
            bin_path_line = ln.strip()

    help_text = "\n".join(clean_lines).strip()
    return f"""# {tool_name}

**Binary**: `{bin_path_line or binary_path}`

## Help Output

```
{help_text}
```
"""


def main() -> None:
    out_dir = ROOT / "knowledge"
    out_zip = out_dir / "kali-tools.zip"

    print(f"Generating tool docs from container '{CONTAINER}'...")
    results: dict[str, str] = {}
    missing: list[str] = []

    for tool_name, paths in TOOLS.items():
        found = get_tool_help(tool_name, paths)
        if found:
            binary_path, raw_help = found
            md = generate_markdown(tool_name, binary_path, raw_help)
            results[tool_name] = md
            print(f"  ✓ {tool_name} ({len(raw_help)} chars)")
        else:
            missing.append(tool_name)
            print(f"  ✗ {tool_name}: not found in container")

    print(f"\nBuilding ZIP: {out_zip.name}")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for tool_name, md in results.items():
            zf.writestr(f"kali-tools/{tool_name}.md", md.encode("utf-8"))
        # Also write a summary index
        index_lines = ["# Kali Tool Reference Index\n"]
        for tool_name in sorted(results):
            index_lines.append(f"- [{tool_name}](kali-tools/{tool_name}.md)")
        if missing:
            index_lines.append("\n## Not Found In Container")
            for t in missing:
                index_lines.append(f"- {t}")
        zf.writestr("kali-tools/INDEX.md", "\n".join(index_lines).encode("utf-8"))

    out_zip.write_bytes(buf.getvalue())
    print(f"Wrote {out_zip} ({out_zip.stat().st_size // 1024} KB, {len(results)} tools)")
    print(f"Missing: {missing}")


if __name__ == "__main__":
    main()
