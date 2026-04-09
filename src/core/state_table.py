from __future__ import annotations

from pathlib import Path
from typing import Any

from core.models import (
    ObjectInventoryEntry,
    RequestGraphEntry,
    RetryCandidate,
    SessionBundle,
    StateItem,
    StateTable,
    StateTableDelta,
    utc_now_iso,
)


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

        filtered_identities = [item for item in delta.identities if self._is_identity_material(item)]
        self.model.identities = self._merge_items(self.model.identities, filtered_identities)
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
        self.model.session_bundles = self._merge_structured_models(
            self.model.session_bundles,
            delta.session_bundles,
            key_getter=lambda item: item.id,
        )
        self.model.request_graph = self._merge_structured_models(
            self.model.request_graph,
            delta.request_graph,
            key_getter=lambda item: f"{item.source_node_id or '-'}::{item.path.strip().lower()}::{item.body_hash}",
        )
        self.model.object_inventory = self._merge_object_inventory(
            self.model.object_inventory,
            delta.object_inventory,
        )
        self.model.retry_candidates = self._merge_structured_models(
            self.model.retry_candidates,
            delta.retry_candidates,
            key_getter=lambda item: f"{item.method.upper()}::{item.path.strip().lower()}::{item.retry_reason}::{item.source_node_id or '-'}",
        )
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
        lines.extend(self._structured_count_lines("session_bundles", len(self.model.session_bundles)))
        lines.extend(self._structured_count_lines("request_graph", len(self.model.request_graph)))
        lines.extend(self._structured_count_lines("object_inventory", len(self.model.object_inventory)))
        lines.extend(self._structured_count_lines("retry_candidates", len(self.model.retry_candidates)))
        lines.extend(self._note_lines(self.model.notes))
        return "\n".join(lines).strip() + "\n"

    def save_session_bundle(self, bundle: SessionBundle | dict[str, Any]) -> SessionBundle:
        model = bundle if isinstance(bundle, SessionBundle) else SessionBundle.model_validate(bundle)
        model.last_successful_login_at = model.last_successful_login_at or utc_now_iso()
        self.model.session_bundles = self._merge_structured_models(
            self.model.session_bundles,
            [model],
            key_getter=lambda item: item.id,
        )
        return model

    def get_latest_session_bundle(self, base_url: str | None = None) -> SessionBundle | None:
        bundles = self.model.session_bundles
        if base_url:
            bundles = [item for item in bundles if item.base_url == base_url]
        if not bundles:
            return None
        return sorted(bundles, key=lambda item: item.last_successful_login_at, reverse=True)[0]

    def list_session_bundles(self) -> list[SessionBundle]:
        return list(self.model.session_bundles)

    def save_request_graph(self, node_id: str, graph_entry: RequestGraphEntry | dict[str, Any]) -> RequestGraphEntry:
        model = graph_entry if isinstance(graph_entry, RequestGraphEntry) else RequestGraphEntry.model_validate(graph_entry)
        if not model.source_node_id:
            model.source_node_id = node_id
        self.model.request_graph = self._merge_structured_models(
            self.model.request_graph,
            [model],
            key_getter=lambda item: f"{item.source_node_id or '-'}::{item.path.strip().lower()}::{item.body_hash}",
        )
        return model

    def list_recent_request_graph(self, limit: int = 40) -> list[RequestGraphEntry]:
        if limit <= 0:
            return []
        return self.model.request_graph[-limit:]

    def save_object_ids(
        self,
        object_type: str,
        values: list[str],
        source_path: str,
        extraction_method: str,
        confidence: float,
    ) -> ObjectInventoryEntry:
        model = ObjectInventoryEntry(
            object_type=object_type or "generic",
            values=[item for item in values if item],
            source_path=source_path,
            extraction_method=extraction_method,
            confidence=max(0.0, min(float(confidence), 1.0)),
            last_seen_at=utc_now_iso(),
        )
        self.model.object_inventory = self._merge_object_inventory(self.model.object_inventory, [model])
        return model

    def get_object_candidates(self, object_type: str | None = None) -> list[str]:
        values: list[str] = []
        for item in self.model.object_inventory:
            if object_type and item.object_type != object_type:
                continue
            for value in item.values:
                normalized = value.strip()
                if normalized and normalized not in values:
                    values.append(normalized)
        return values

    def save_retry_candidate(self, candidate: RetryCandidate | dict[str, Any]) -> RetryCandidate:
        model = candidate if isinstance(candidate, RetryCandidate) else RetryCandidate.model_validate(candidate)
        self.model.retry_candidates = self._merge_structured_models(
            self.model.retry_candidates,
            [model],
            key_getter=lambda item: f"{item.method.upper()}::{item.path.strip().lower()}::{item.retry_reason}::{item.source_node_id or '-'}",
        )
        return model

    def list_retry_candidates(self, status: str | None = None) -> list[RetryCandidate]:
        if not status:
            return list(self.model.retry_candidates)
        lowered = status.strip().lower()
        return [item for item in self.model.retry_candidates if item.status.strip().lower() == lowered]

    def mark_retry_candidate_consumed(self, candidate_id: str) -> bool:
        for item in self.model.retry_candidates:
            if item.id != candidate_id:
                continue
            item.status = "consumed"
            return True
        return False

    def get_exploit_frontiers(self) -> dict[str, Any]:
        pending_retries = [item for item in self.model.retry_candidates if item.status.lower() != "consumed"]
        object_values = self.get_object_candidates()
        latest_bundle = self.get_latest_session_bundle()
        return {
            "pending_retry_candidates": pending_retries,
            "object_candidates": object_values,
            "has_session_bundle": latest_bundle is not None,
            "session_bundle_id": latest_bundle.id if latest_bundle else None,
            "request_graph_count": len(self.model.request_graph),
        }

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

    def _merge_structured_models(self, current: list[Any], incoming: list[Any], *, key_getter) -> list[Any]:
        merged = list(current)
        seen = {key_getter(item): item for item in current}
        for item in incoming:
            key = key_getter(item)
            if key in seen:
                existing = seen[key]
                index = merged.index(existing)
                merged[index] = item
                seen[key] = item
                continue
            merged.append(item)
            seen[key] = item
        return merged

    def _merge_object_inventory(
        self,
        current: list[ObjectInventoryEntry],
        incoming: list[ObjectInventoryEntry],
    ) -> list[ObjectInventoryEntry]:
        merged = list(current)
        by_key: dict[str, ObjectInventoryEntry] = {
            f"{item.object_type}::{item.source_path}::{item.extraction_method}": item
            for item in current
        }

        for item in incoming:
            key = f"{item.object_type}::{item.source_path}::{item.extraction_method}"
            existing = by_key.get(key)
            if existing is None:
                merged.append(item)
                by_key[key] = item
                continue

            for value in item.values:
                if value not in existing.values:
                    existing.values.append(value)
            existing.confidence = max(existing.confidence, item.confidence)
            existing.last_seen_at = item.last_seen_at
        return merged

    def _is_identity_material(self, item: StateItem) -> bool:
        title = item.title.lower()
        content = item.content.lower()
        if not content.strip():
            return False
        noise_markers = ["query_", "family_", "debug", "trace", "retriever_called", "query_count"]
        if any(marker in content for marker in noise_markers):
            return False
        semantic_markers = ["username", "password", "账号", "密码", "token", "cookie", "session"]
        if any(marker in title or marker in content for marker in semantic_markers):
            return True
        if re_match := (":" in item.content and len(item.content.split(":", 1)[0].strip()) >= 2):
            return bool(re_match)
        return False

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

    def _structured_count_lines(self, title: str, count: int) -> list[str]:
        lines = [f"## {title}"]
        lines.append(f"- count: {count}")
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
