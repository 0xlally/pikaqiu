from __future__ import annotations

import subprocess
import sys
from typing import Protocol

from core.models import StrictModel


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


class ToolRegistry:
    """按名称分发工具。"""

    def __init__(self, tools: list[MCPTool]) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def run(self, tool_name: str, command: str) -> ToolExecutionOutput:
        try:
            return self.tools[tool_name].run(command)
        except KeyError as exc:
            raise KeyError(f"未知工具：{tool_name}") from exc
