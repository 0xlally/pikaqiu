from __future__ import annotations

from typing import Protocol

from core.models import AgentRuntimeRequest, AgentRuntimeResponse


class AgentRuntime(Protocol):
    """agent 运行时的统一边界。"""

    def run(self, request: AgentRuntimeRequest) -> AgentRuntimeResponse:
        """执行一轮 agent 调用并返回结果。"""
