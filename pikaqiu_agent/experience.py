from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any


PREFERRED_EXPERIENCE_REFS = {
    "experience/okk/pentest_methodology.md",
    "experience/okk/agent_execution_protocols.md",
    "experience/okk/observability_and_runtime.md",
    "experience/rules/mistakes.md",
    "experience/rules/hunting.md",
    "experience/rules/techniques.md",
    "experience/rules/waf-bypass-protocol.md",
}


def distilled_experience_root(workspace_root: Path) -> Path:
    return workspace_root / ".pikaqiu_agent" / "experience_distilled"


def build_experience_query(mission: dict[str, Any], memory: dict[str, Any]) -> str:
    idea = memory.get("idea_board") if isinstance(memory.get("idea_board"), dict) else {}
    board = memory.get("memory_board") if isinstance(memory.get("memory_board"), dict) else {}
    pieces = [
        mission.get("target", ""),
        mission.get("goal", ""),
        " ".join(str(item) for item in mission.get("domains", [])),
        idea.get("active_direction", ""),
        idea.get("primary_hypothesis", ""),
        idea.get("risk_or_blocker", ""),
        " ".join(str(item) for item in board.get("facts", [])[:6]),
        " ".join(str(item) for item in board.get("constraints", [])[:4]),
    ]
    return " ".join(str(piece) for piece in pieces if str(piece).strip())


def search_experience(workspace_root: Path, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
    tokens = _query_tokens(query)
    scored: list[tuple[float, Path, str, str]] = []
    for root, source in _experience_sources(workspace_root):
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            rel = _experience_rel(workspace_root, path, source)
            if not rel:
                continue
            text = _read_text(path)
            haystack = f"{rel}\n{text[:12000]}".lower()
            score = 0.0
            for token in tokens:
                token_l = token.lower()
                if token_l in rel.lower():
                    score += 4.0
                if token_l in haystack:
                    score += 1.0
            if rel in PREFERRED_EXPERIENCE_REFS:
                score += 0.25
            if source == "distilled" and "source_mission_id" in text:
                score += 0.2
            if score > 0 or not tokens:
                scored.append((score, path, source, _snippet(text, tokens)))
    scored.sort(key=lambda item: (item[0], item[2] == "distilled", -len(str(item[1]))), reverse=True)
    return [
        {
            "path": _experience_rel(workspace_root, path, source),
            "source": source,
            "distilled": source == "distilled",
            "score": round(score, 3),
            "snippet": snippet,
            "source_mission_id": _extract_source_mission_id(_read_text(path)) if source == "distilled" else "",
        }
        for score, path, source, snippet in scored[:limit]
    ]


def load_experience(workspace_root: Path, rel_path: str, *, max_chars: int) -> dict[str, Any]:
    target = resolve_experience_path(workspace_root, rel_path)
    if not target:
        return {"ok": False, "path": rel_path, "error": "path must stay inside an experience root and point to a markdown file"}
    text = _read_text(target)
    truncated = len(text) > max_chars
    if truncated:
        text = text[:max_chars] + "\n... [truncated]"
    source = "distilled" if _is_under(target, distilled_experience_root(workspace_root)) else "manual"
    return {
        "ok": True,
        "path": _experience_rel(workspace_root, target, source),
        "source": source,
        "distilled": source == "distilled",
        "truncated": truncated,
        "content": text,
        "source_mission_id": _extract_source_mission_id(text) if source == "distilled" else "",
    }


def resolve_experience_path(workspace_root: Path, rel_path: str) -> Path | None:
    raw = str(rel_path or "").strip().replace("\\", "/")
    if not raw:
        return None
    candidates: list[Path] = []
    if raw.startswith("experience/"):
        candidates.append(workspace_root / raw)
        candidates.append(workspace_root / raw[len("experience/") :])
    elif raw.startswith(".pikaqiu_agent/experience_distilled/"):
        candidates.append(workspace_root / raw)
    elif raw.startswith("experience_distilled/"):
        candidates.append(workspace_root / ".pikaqiu_agent" / raw)
    else:
        candidates.append(workspace_root / "experience" / raw)
        candidates.append(distilled_experience_root(workspace_root) / raw)

    roots = [(workspace_root / "experience").resolve(), distilled_experience_root(workspace_root).resolve()]
    for candidate in candidates:
        target = candidate.resolve()
        if not target.is_file() or target.suffix.lower() != ".md":
            continue
        if any(_is_under(target, root) for root in roots):
            return target
    return None


def format_experience_hints(results: list[dict[str, Any]], *, limit: int = 3) -> str:
    rows = [row for row in results if row.get("snippet")][:limit]
    if not rows:
        return ""
    lines = ["## Distilled Experience Hints"]
    for row in rows:
        marker = "distilled" if row.get("distilled") else "manual"
        source_id = f" source_mission_id={row.get('source_mission_id')}" if row.get("source_mission_id") else ""
        lines.append(
            f"- [{marker}] {row.get('path')} score={row.get('score')}{source_id}: {row.get('snippet')}"
        )
    return "\n".join(lines)


def write_distilled_experience(
    workspace_root: Path,
    *,
    mission: dict[str, Any],
    markdown: str,
) -> Path:
    root = distilled_experience_root(workspace_root)
    root.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    slug = _slug(mission.get("name") or mission.get("target") or "mission")
    mission_id = str(mission.get("id") or "")[:8] or "unknown"
    path = root / f"{now}-{slug}-{mission_id}.md"
    path.write_text(markdown.strip() + "\n", encoding="utf-8")
    return path


def _experience_sources(workspace_root: Path) -> list[tuple[Path, str]]:
    return [
        ((workspace_root / "experience").resolve(), "manual"),
        (distilled_experience_root(workspace_root).resolve(), "distilled"),
    ]


def _experience_rel(workspace_root: Path, path: Path, source: str) -> str:
    try:
        if source == "distilled":
            rel = path.resolve().relative_to(workspace_root.resolve())
        else:
            rel = path.resolve().relative_to(workspace_root.resolve())
    except ValueError:
        return ""
    return rel.as_posix()


def _read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _clean_text(value: Any, limit: int = 1200) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def _snippet(text: str, tokens: list[str], limit: int = 500) -> str:
    if not text:
        return ""
    lower = text.lower()
    pos = -1
    for token in tokens:
        pos = lower.find(token.lower())
        if pos >= 0:
            break
    if pos < 0:
        return _clean_text(text[:limit], limit)
    start = max(0, pos - 160)
    return _clean_text(text[start : start + limit], limit)


def _query_tokens(query: str) -> list[str]:
    seen: set[str] = set()
    tokens: list[str] = []
    for token in re.findall(r"[A-Za-z0-9_.:+/-]+|[\u4e00-\u9fff]{2,}", query.lower()):
        token = token.strip()
        if len(token) < 2 or token in seen:
            continue
        seen.add(token)
        tokens.append(token)
        if len(tokens) >= 16:
            break
    return tokens


def _extract_source_mission_id(text: str) -> str:
    match = re.search(r"source_mission_id\s*[:=]\s*`?([A-Za-z0-9_.:-]+)`?", text)
    return match.group(1) if match else ""


def _slug(value: Any) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "").strip().lower()).strip("-")
    return text[:48] or "mission"


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
