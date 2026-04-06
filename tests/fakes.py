from __future__ import annotations

from core.models import AgentRuntimeRequest, AgentRuntimeResponse


class FakeRuntime:
    """测试用假运行时。"""

    def run(self, request: AgentRuntimeRequest) -> AgentRuntimeResponse:
        return AgentRuntimeResponse(
            agent_name=request.agent_name,
            content=f"fake::{request.agent_name}",
            raw={"provider": "fake"},
        )
