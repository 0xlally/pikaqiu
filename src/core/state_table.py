from __future__ import annotations

from pathlib import Path
from typing import Any

from core.models import StateItem, StateTable, StateTableDelta


class StateTableStore:
    """高价值状态表的可变封装。"""

    def __init__(self, model: StateTable | None = None) -> None:
        self.model = model or StateTable()

    def merge(self, incoming: StateTable | StateTableDelta | dict[str, Any]) -> StateTable:
        """合并整表、增量或普通字典到当前状态。"""
        if isinstance(incoming, StateTable):
            delta = StateTableDelta.model_validate(incoming.model_dump())
        elif isinstance(incoming, StateTableDelta):
            delta = incoming
        else:
            delta = StateTableDelta.model_validate(incoming)

        self.model.identities = self._merge_items(self.model.identities, delta.identities)
        self.model.session_materials = self._merge_items(self.model.session_materials, delta.session_materials)
        self.model.key_entrypoints = self._merge_items(self.model.key_entrypoints, delta.key_entrypoints)
        self.model.workflow_prerequisites = self._merge_items(
            self.model.workflow_prerequisites,
            delta.workflow_prerequisites,
        )
        self.model.reusable_artifacts = self._merge_items(
            self.model.reusable_artifacts,
            delta.reusable_artifacts,
        )
        self.model.session_risks = self._merge_items(self.model.session_risks, delta.session_risks)
        self.model.notes = self._merge_notes(self.model.notes, delta.notes)
        return self.model

    def update(self, **sections: list[StateItem] | list[str]) -> StateTable:
        """按关键字参数更新一个或多个分区。"""
        return self.merge(sections)

    def apply_delta(self, delta: StateTableDelta) -> StateTable:
        """兼容旧调用方式。"""
        return self.merge(delta)

    def save_json(self, path: str | Path) -> Path:
        """把状态表序列化到 JSON 文件。"""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.model.model_dump_json(indent=2), encoding="utf-8")
        return target

    @classmethod
    def load_json(cls, path: str | Path) -> "StateTableStore":
        """从 JSON 文件加载状态表。"""
        data = Path(path).read_text(encoding="utf-8")
        return cls(StateTable.model_validate_json(data))

    def to_markdown(self) -> str:
        """导出为适合其他 agent 直接读取的 markdown 快照。"""
        lines = ["# 状态表", ""]
        lines.extend(self._section_lines("identities", self.model.identities))
        lines.extend(self._section_lines("session_materials", self.model.session_materials))
        lines.extend(self._section_lines("key_entrypoints", self.model.key_entrypoints))
        lines.extend(self._section_lines("workflow_prerequisites", self.model.workflow_prerequisites))
        lines.extend(self._section_lines("reusable_artifacts", self.model.reusable_artifacts))
        lines.extend(self._section_lines("session_risks", self.model.session_risks))
        lines.extend(self._note_lines(self.model.notes))
        return "\n".join(lines).strip() + "\n"

    def _merge_items(self, current: list[StateItem], incoming: list[StateItem]) -> list[StateItem]:
        """按标题和内容去重，避免状态表膨胀。"""
        seen = {self._item_key(item) for item in current}
        merged = list(current)
        for item in incoming:
            key = self._item_key(item)
            if key in seen:
                continue
            merged.append(item)
            seen.add(key)
        return merged

    def _merge_notes(self, current: list[str], incoming: list[str]) -> list[str]:
        """保留唯一备注。"""
        seen = {item.strip().lower() for item in current}
        merged = list(current)
        for note in incoming:
            key = note.strip().lower()
            if not key or key in seen:
                continue
            merged.append(note)
            seen.add(key)
        return merged

    def _item_key(self, item: StateItem) -> str:
        return f"{item.title.strip().lower()}::{item.content.strip().lower()}"

    def _section_lines(self, title: str, items: list[StateItem]) -> list[str]:
        lines = [f"## {title}"]
        if not items:
            lines.append("- none")
            lines.append("")
            return lines
        for item in items:
            lines.append(f"- {item.title}: {item.content}")
            lines.append(f"  refs: {', '.join(item.refs) or '-'}")
            lines.append(f"  source: {item.source or '-'}")
        lines.append("")
        return lines

    def _note_lines(self, notes: list[str]) -> list[str]:
        lines = ["## notes"]
        if not notes:
            lines.append("- none")
            lines.append("")
            return lines
        for note in notes:
            lines.append(f"- {note}")
        lines.append("")
        return lines
