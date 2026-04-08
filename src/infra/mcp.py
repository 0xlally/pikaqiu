from __future__ import annotations

import json
import subprocess
import sys
from typing import Callable, Protocol

from core.models import StateItem, StateTable, StrictModel


class ToolExecutionOutput(StrictModel):
    """工具执行后的统一结果。"""

    tool_name: str
    command: str
    stdout: str
    stderr: str
    exit_code: int


class MCPTool(Protocol):
    """act agent 使用的最小工具协议。"""

    name: str

    def run(self, command: str) -> ToolExecutionOutput:
        """执行命令并返回结构化结果。"""


def _run_process(tool_name: str, argv: list[str], command: str) -> ToolExecutionOutput:
    result = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        check=False,
    )
    return ToolExecutionOutput(
        tool_name=tool_name,
        command=command,
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
        exit_code=result.returncode,
    )


class PythonMCPTool:
    """执行内联 Python 代码。"""

    name = "python"

    def run(self, command: str) -> ToolExecutionOutput:
        return _run_process("python", [sys.executable, "-c", command], command)


class BashMCPTool:
    """执行 bash 命令，面向 Kali 容器环境。"""

    name = "bash"

    def run(self, command: str) -> ToolExecutionOutput:
        return _run_process("bash", ["bash", "-lc", command], command)


class StateTableQueryMCPTool:
    """查询状态表快照的轻量MCP工具。"""

    name = "state_table"

    def __init__(self, state_provider: Callable[[], StateTable]) -> None:
        self.state_provider = state_provider

    def run(self, command: str) -> ToolExecutionOutput:
        section, keyword = self._parse_command(command)
        table = self.state_provider()
        payload = self._query(table, section=section, keyword=keyword)
        return ToolExecutionOutput(
            tool_name=self.name,
            command=command,
            stdout=json.dumps(payload, ensure_ascii=False),
            stderr="",
            exit_code=0,
        )

    def _parse_command(self, command: str) -> tuple[str, str]:
        section = "all"
        keyword = ""
        for part in command.split(";"):
            key, sep, value = part.partition("=")
            if sep == "":
                continue
            lowered_key = key.strip().lower()
            lowered_value = value.strip()
            if lowered_key == "section" and lowered_value:
                section = lowered_value
            if lowered_key == "keyword":
                keyword = lowered_value
        return section, keyword

    def _query(self, table: StateTable, *, section: str, keyword: str) -> dict[str, object]:
        normalized_keyword = keyword.strip().lower()
        selected_sections = self._select_sections(table, section)

        result: dict[str, object] = {}
        for name, items in selected_sections.items():
            if name == "notes":
                filtered_notes = self._filter_notes(items, normalized_keyword)
                result[name] = filtered_notes
                continue
            filtered_items = self._filter_items(items, normalized_keyword)
            result[name] = [self._serialize_item(item) for item in filtered_items]

        return {
            "query": {
                "section": section,
                "keyword": keyword,
            },
            "result": result,
        }

    def _select_sections(self, table: StateTable, section: str) -> dict[str, list[StateItem] | list[str]]:
        sections: dict[str, list[StateItem] | list[str]] = {
            "identities": table.identities,
            "session_materials": table.session_materials,
            "key_entrypoints": table.key_entrypoints,
            "workflow_prerequisites": table.workflow_prerequisites,
            "reusable_artifacts": table.reusable_artifacts,
            "session_risks": table.session_risks,
            "notes": table.notes,
        }
        normalized_section = section.strip().lower()
        if normalized_section == "all":
            return sections
        if normalized_section in sections:
            return {normalized_section: sections[normalized_section]}
        return sections

    def _filter_items(self, items: list[StateItem], keyword: str) -> list[StateItem]:
        if not keyword:
            return items[:30]
        filtered: list[StateItem] = []
        for item in items:
            text = f"{item.title} {item.content}".lower()
            if keyword in text:
                filtered.append(item)
        return filtered[:30]

    def _filter_notes(self, notes: list[str], keyword: str) -> list[str]:
        if not keyword:
            return notes[-30:]
        filtered = [note for note in notes if keyword in note.lower()]
        return filtered[-30:]

    def _serialize_item(self, item: StateItem) -> dict[str, object]:
        return {
            "title": item.title,
            "content": item.content,
            "refs": item.refs,
            "source": item.source,
        }


class ToolRegistry:
    """按名称分发工具。"""

    def __init__(self, tools: list[MCPTool]) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def run(self, tool_name: str, command: str) -> ToolExecutionOutput:
        try:
            return self.tools[tool_name].run(command)
        except KeyError as exc:
            raise KeyError(f"未知工具：{tool_name}") from exc
