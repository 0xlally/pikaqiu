from __future__ import annotations

import csv
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Iterable


_FLAG_COUNT_SUFFIX_RE = re.compile(r"\s+\(\d+/\d+\)\s*$")
_EXPECTED_CAPTURED_RE = re.compile(r"^- Expected flags: (.*?), captured flags: \d+\s*$", re.M)


def flag_from_event_content(content: Any) -> str:
    first_line = str(content or "").strip().splitlines()
    if not first_line:
        return ""
    return _FLAG_COUNT_SUFFIX_RE.sub("", first_line[0]).strip()


def captured_flags_from_events(events: Iterable[dict[str, Any]]) -> list[str]:
    flags: list[str] = []
    seen: set[str] = set()
    for event in events:
        if event.get("type") != "flag":
            continue
        flag = flag_from_event_content(event.get("content"))
        if not flag and isinstance(event.get("metadata"), dict):
            flag = str(event["metadata"].get("flag") or "").strip()
        if not flag:
            continue
        key = flag.lower()
        if key in seen:
            continue
        seen.add(key)
        flags.append(flag)
    return flags


def normalize_mission_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    flags = captured_flags_from_events(payload.get("events") or [])
    count = len(flags)
    payload["captured_flags"] = flags
    payload["captured_flag_count"] = count
    for key in ("mission", "experiment"):
        section = payload.get(key)
        if isinstance(section, dict):
            section["captured_flags"] = flags
            section["captured_flag_count"] = count
            if key == "experiment":
                section["flag_count"] = count
                if count and not str(section.get("outcome") or "").strip():
                    section["outcome"] = "success"
    return payload, flags


def normalize_mission_log_export_dir(export_dir: str | Path) -> dict[str, dict[str, Any]]:
    root = Path(export_dir)
    json_dir = root / "json"
    markdown_dir = root / "markdown"
    summaries: dict[str, dict[str, Any]] = {}

    for json_path in sorted(json_dir.glob("*.json")):
        payload = json.loads(json_path.read_text(encoding="utf-8-sig"))
        payload, flags = normalize_mission_payload(payload)
        json_path.write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        mission = payload.get("mission") if isinstance(payload.get("mission"), dict) else {}
        summaries[json_path.name] = {
            "name": str(mission.get("name") or json_path.stem),
            "id": str(mission.get("id") or ""),
            "flags": flags,
            "count": len(flags),
        }
        _update_markdown_file(markdown_dir / f"{json_path.stem}.md", flags)

    rows = _update_index_json(root / "index.json", summaries)
    _update_index_csv(root / "index.csv", summaries)
    _update_readme(root / "README.md", rows)
    return summaries


def _path_name(value: Any) -> str:
    text = str(value or "")
    if "\\" in text:
        return PureWindowsPath(text).name
    return PurePosixPath(text).name


def _summary_for_entry(entry: dict[str, Any], summaries: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    json_name = _path_name(entry.get("json"))
    if json_name in summaries:
        return summaries[json_name]
    entry_id = str(entry.get("id") or "")
    entry_name = str(entry.get("name") or "")
    for summary in summaries.values():
        if entry_id and summary.get("id") == entry_id:
            return summary
        if entry_name and summary.get("name") == entry_name:
            return summary
    return None


def _update_index_json(index_path: Path, summaries: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if not index_path.exists():
        return []
    rows = json.loads(index_path.read_text(encoding="utf-8-sig"))
    if not isinstance(rows, list):
        return []
    for entry in rows:
        if not isinstance(entry, dict):
            continue
        summary = _summary_for_entry(entry, summaries)
        if not summary:
            continue
        flags = list(summary["flags"])
        entry["captured_flags"] = int(summary["count"])
        entry["captured_flag_count"] = int(summary["count"])
        entry["captured_flag_values"] = flags
    index_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return rows


def _update_index_csv(index_path: Path, summaries: dict[str, dict[str, Any]]) -> None:
    if not index_path.exists():
        return
    with index_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    for extra in ("captured_flag_count", "captured_flag_values"):
        if extra not in fieldnames:
            fieldnames.append(extra)
    for row in rows:
        summary = _summary_for_entry(row, summaries)
        if not summary:
            continue
        row["captured_flags"] = str(summary["count"])
        row["captured_flag_count"] = str(summary["count"])
        row["captured_flag_values"] = ";".join(summary["flags"])
    with index_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _update_readme(readme_path: Path, rows: list[dict[str, Any]]) -> None:
    if not readme_path.exists() or not rows:
        return
    original = readme_path.read_text(encoding="utf-8")
    exported = ""
    for line in original.splitlines():
        if line.startswith("Exported at:"):
            exported = line
            break
    lines = ["# PikaQiu Mission Log Export", ""]
    if exported:
        lines.extend([exported, ""])
    lines.extend([
        "| Name | Status | Target | Events | Command Events | Captured Flags |",
        "|---|---|---|---:|---:|---:|",
    ])
    for row in rows:
        count = row.get("captured_flag_count", row.get("captured_flags", 0))
        lines.append(
            f"| {row.get('name', '')} | {row.get('status', '')} | `{row.get('target', '')}` | "
            f"{row.get('events', 0)} | {row.get('command_events', 0)} | {count} |"
        )
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _update_markdown_file(markdown_path: Path, flags: list[str]) -> None:
    if not markdown_path.exists():
        return
    text = markdown_path.read_text(encoding="utf-8")
    count = len(flags)
    text = _EXPECTED_CAPTURED_RE.sub(rf"- Expected flags: \1, captured flags: {count}", text)
    text = re.sub(r"^- Captured flag values: .*\n?", "", text, count=1, flags=re.M)
    if flags:
        values = ", ".join(f"`{flag}`" for flag in flags)
        marker = f"- Expected flags: "
        idx = text.find(marker)
        if idx != -1:
            line_end = text.find("\n", idx)
            if line_end != -1:
                text = text[: line_end + 1] + f"- Captured flag values: {values}\n" + text[line_end + 1 :]
    markdown_path.write_text(text, encoding="utf-8")
