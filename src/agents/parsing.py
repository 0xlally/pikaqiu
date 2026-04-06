from __future__ import annotations

from core.models import (
    ActResult,
    AgentRuntimeRequest,
    ConclusionRecord,
    EvidenceRecord,
    ParsedActResult,
    StateItem,
    StateTableDelta,
)
from core.task_tree import TaskTree
from runtime.base import AgentRuntime


PARSING_SYSTEM_PROMPT = """
你是SRC测试系统中的 parsing agent。

你的职责：
1. 压缩 act agent 的原始输出。
2. 提取高价值事实，形成结构化结果。
3. 分离保存证据和结论。

你不能做的事：
1. 不做漏洞判断。
2. 不判断测试家族。
3. 不创建 test node。
4. 不把未经证实的猜测写成事实。

输出要求：
1. evidence 只保存原始证据或引用。
2. conclusion 只能引用 evidence id。
3. state_delta 只保留高价值上下文。
""".strip()


RISK_HINTS = {
    "auth_bypass": "认证链路值得继续验证绕过、状态篡改和边界切换。",
    "session_management": "会话签发、续期、失效和值绑定值得继续验证。",
    "access_control": "对象和角色授权边界值得继续验证越权路径。",
    "input_validation": "请求参数值得继续验证注入和解析歧义。",
    "file_upload": "上传链路值得继续验证内容识别和落盘暴露。",
}


class ParsingAgent:
    """压缩 act 输出并产出证据、结论和状态增量的 parsing agent。"""

    def __init__(self, runtime: AgentRuntime) -> None:
        self.runtime = runtime

    def parse(self, act_result: ActResult, task_tree: TaskTree) -> ParsedActResult:
        """把工具输出整理成可回填任务树和状态表的结构。"""
        node = task_tree.get_node(act_result.node_id)
        trace = self.runtime.run(
            AgentRuntimeRequest(
                agent_name="parsing",
                system_prompt=PARSING_SYSTEM_PROMPT,
                user_prompt=f"请压缩节点 {node.id} 的执行结果：{node.title}",
                context={
                    "node_id": node.id,
                    "node_title": node.title,
                    "tool_name": act_result.tool_name,
                    "exit_code": act_result.exit_code,
                },
            )
        )

        summary = f"{node.title} 执行完成，退出码为 {act_result.exit_code}。"
        evidence = EvidenceRecord(
            source="act",
            content=act_result.raw_output,
            tool_name=act_result.tool_name,
            node_id=node.id,
        )
        conclusion = ConclusionRecord(
            title=f"{node.title} 的执行摘要",
            summary=summary,
            evidence_ids=[evidence.id],
            source_node_id=node.id,
        )
        risk_text = RISK_HINTS.get(node.test_family_id or "", "当前表面值得继续人工复核。")

        return ParsedActResult(
            node_id=node.id,
            summary=summary,
            evidence=[evidence],
            conclusions=[conclusion],
            state_delta=StateTableDelta(
                key_entrypoints=[
                    StateItem(
                        title=node.title,
                        content=node.description[:160],
                        refs=[evidence.id],
                        source=node.id,
                    )
                ],
                session_risks=[
                    StateItem(
                        title=f"风险提示：{node.test_family_id or 'generic'}",
                        content=risk_text,
                        refs=[evidence.id],
                        source=node.id,
                    )
                ],
                notes=[trace.content] if trace.content else [],
            ),
        )
