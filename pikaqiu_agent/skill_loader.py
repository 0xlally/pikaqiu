from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_VALID_SKILL_ID = re.compile(r"^[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class Skill:
    id: str
    name: str
    description: str
    path: str
    prompt: str
    tags: list[str] = field(default_factory=list)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(
        self,
        *,
        include_prompt: bool = False,
        include_references: bool = False,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "path": self.path,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }
        if include_prompt:
            data["prompt"] = self.prompt
        if include_references:
            data["references"] = SkillLoader.reference_manifest_for_path(Path(self.path))
        return data


class SkillLoader:
    """Loads SKILL.md files under the configured skills directory."""

    def __init__(self, workspace_root: Path, skills_dir: str = "./skills") -> None:
        self.workspace_root = workspace_root
        skills_path = Path(skills_dir)
        if not skills_path.is_absolute():
            skills_path = workspace_root / skills_path
        self.skills_root = skills_path.resolve()
        self._skills: dict[str, Skill] = {}
        self._errors: list[str] = []

    def refresh(self) -> dict[str, Any]:
        self._skills = {}
        self._errors = []

        if not self.skills_root.exists():
            return self.stats(status="no_skills_dir")
        if not self.skills_root.is_dir():
            self._errors.append(f"skills path is not a directory: {self.skills_root}")
            return self.stats(status="invalid_skills_dir")

        for skill_file in sorted(self.skills_root.rglob("SKILL.md")):
            self._load_skill_file(skill_file)

        return self.stats(status="ready")

    def stats(self, *, status: str = "ready") -> dict[str, Any]:
        enabled = sum(1 for skill in self._skills.values() if skill.enabled)
        return {
            "status": status,
            "skills_dir": str(self.skills_root),
            "total": len(self._skills),
            "enabled": enabled,
            "errors": list(self._errors),
        }

    def list_skills(
        self,
        *,
        include_prompt: bool = False,
        include_references: bool = False,
    ) -> list[dict[str, Any]]:
        return [
            skill.to_dict(include_prompt=include_prompt, include_references=include_references)
            for skill in sorted(self._skills.values(), key=lambda item: item.id)
        ]

    def catalog(self, *, limit: int = 50) -> list[dict[str, Any]]:
        items = []
        for skill in sorted(self._skills.values(), key=lambda item: item.id):
            if not skill.enabled:
                continue
            items.append({
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "tags": skill.tags,
            })
            if len(items) >= limit:
                break
        return items

    def resolve(self, skill_ids: list[str] | None) -> tuple[list[Skill], list[str]]:
        skills: list[Skill] = []
        missing: list[str] = []
        for raw_id in skill_ids or []:
            skill_id = str(raw_id).strip()
            if not skill_id:
                continue
            skill = self._skills.get(skill_id)
            if not skill or not skill.enabled:
                missing.append(skill_id)
                continue
            skills.append(skill)
        return skills, missing

    def get_skill(self, skill_id: str) -> Skill | None:
        skill = self._skills.get(str(skill_id).strip())
        if not skill or not skill.enabled:
            return None
        return skill

    def search(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        tokens = self._query_tokens(query)
        if not tokens:
            return []
        scored: list[tuple[float, Skill]] = []
        for skill in self._skills.values():
            if not skill.enabled:
                continue
            haystack = " ".join([
                skill.id,
                skill.name,
                skill.description,
                " ".join(skill.tags),
            ]).lower()
            score = 0.0
            for token in tokens:
                if token in skill.id.lower():
                    score += 4.0
                if token in skill.name.lower():
                    score += 3.0
                if token in " ".join(skill.tags).lower():
                    score += 2.0
                if token in haystack:
                    score += 1.0
            if score > 0:
                scored.append((score, skill))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {**skill.to_dict(include_prompt=False), "score": score}
            for score, skill in scored[: max(1, min(int(limit), 20))]
        ]

    def read_reference(self, skill_id: str, relative_path: str, *, max_chars: int = 20000) -> str:
        skill = self.get_skill(skill_id)
        if not skill:
            return f"[skill_read_reference] Unknown skill: {skill_id}"

        root = Path(skill.path).resolve()
        target = (root / relative_path).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            return "[skill_read_reference] Invalid reference path"

        if not target.is_file():
            return f"[skill_read_reference] File not found: {relative_path}"

        text = self._read_text(target)
        if len(text) > max_chars:
            text = text[:max_chars] + "\n... [truncated]"
        return text

    def _load_skill_file(self, skill_file: Path) -> None:
        skill_dir = skill_file.parent
        try:
            raw = self._read_text(skill_file).strip()
            metadata, body = self._split_frontmatter(raw)
        except Exception as exc:
            self._errors.append(f"skipped {skill_dir.name}: {exc}")
            logger.warning("Failed to load skill %s: %s", skill_file, exc)
            return

        if not body:
            self._errors.append(f"skipped {skill_dir.name}: SKILL.md body is empty")
            return

        skill_id = str(metadata.get("id") or skill_dir.name).strip()
        if not _VALID_SKILL_ID.fullmatch(skill_id):
            self._errors.append(f"skipped {skill_dir.name}: invalid skill id '{skill_id}'")
            return
        if skill_id in self._skills:
            self._errors.append(f"skipped {skill_dir.name}: duplicate skill id '{skill_id}'")
            return

        tags = self._as_str_list(metadata.get("tags", []))
        self._skills[skill_id] = Skill(
            id=skill_id,
            name=str(metadata.get("name") or skill_id).strip(),
            description=str(metadata.get("description") or "").strip(),
            path=str(skill_dir),
            prompt=body,
            tags=tags,
            enabled=self._as_bool(metadata.get("enabled", True)),
            metadata=metadata,
        )

    @staticmethod
    def _split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
        if not raw.startswith("---"):
            return {}, raw
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.S)
        if not match:
            return {}, raw
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("PyYAML is required to parse SKILL.md frontmatter") from exc
        data = yaml.safe_load(match.group(1)) or {}
        if not isinstance(data, dict):
            raise ValueError("SKILL.md frontmatter must be a YAML object")
        return data, match.group(2).strip()

    @staticmethod
    def _read_text(path: Path) -> str:
        for encoding in ("utf-8", "utf-8-sig", "gb18030"):
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        return path.read_text(encoding="utf-8", errors="replace")

    @staticmethod
    def _as_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() not in {"0", "false", "no", "off", ""}
        return bool(value)

    @staticmethod
    def _as_str_list(value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in re.split(r"[, ]+", value) if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return [str(value).strip()] if str(value).strip() else []

    @staticmethod
    def _query_tokens(query: str) -> list[str]:
        tokens = re.findall(r"[A-Za-z0-9_.:+-]+|[\u4e00-\u9fff]{2,}", query.lower())
        seen: set[str] = set()
        result: list[str] = []
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            result.append(token)
            if len(result) >= 20:
                break
        return result

    @staticmethod
    def reference_manifest_for_path(skill_path: Path, *, limit: int = 80) -> list[dict[str, Any]]:
        root = skill_path.resolve()
        if not root.is_dir():
            return []
        files: list[dict[str, Any]] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name == "SKILL.md":
                continue
            try:
                rel = path.relative_to(root).as_posix()
            except ValueError:
                continue
            files.append({"path": rel, "size": path.stat().st_size})
            if len(files) >= limit:
                break
        return files
