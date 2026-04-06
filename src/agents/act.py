from __future__ import annotations

import json
import re

from core.models import ActCommand, ActResult, AgentRuntimeRequest, NodeStatus, NodeType, utc_now_iso
from core.task_tree import TaskTree
from infra.mcp import ToolRegistry
from runtime.base import AgentRuntime


ACT_SYSTEM_PROMPT = """
你是SRC测试系统中的 act agent。

你的职责：
1. 读取当前待执行节点。
2. 当前节点可能是 info node，也可能是 test node。
3. 在允许的工具范围内执行当前节点。
4. 保留原始执行结果、错误、退出码和关键观察。

你不能做的事：
1. 不判断功能点。
2. 不判断测试家族。
3. 不更新状态表。
4. 不把猜测写成事实。

执行顺序：
1. 优先执行 todo 状态的 info node。
2. 没有 info node 时，再执行 todo 状态的 test node。

输出要求：
1. 简要说明为什么选择这个工具。
2. 如果调用了工具，保留原始工具结果。
3. 不输出漏洞结论。
""".strip()


class ActAgent:
    """选择待执行节点并完成一次工具执行的 act agent。"""

    def __init__(self, runtime: AgentRuntime, tools: ToolRegistry) -> None:
        self.runtime = runtime
        self.tools = tools

    def execute_next(self, task_tree: TaskTree) -> ActResult | None:
        """优先执行 info node，没有 info node 再执行 test node。"""
        node = task_tree.next_todo(NodeType.INFO) or task_tree.next_todo(NodeType.TEST)
        if node is None:
            return None

        task_tree.update_status(node.id, NodeStatus.DOING)
        trace = self.runtime.run(
            AgentRuntimeRequest(
                agent_name="act",
                system_prompt=ACT_SYSTEM_PROMPT,
                user_prompt=(
                    "请严格输出 JSON（不要 markdown），格式为 "
                    '{"tool_name":"python|bash","command":"..."}。'
                    "仅输出一个 JSON 对象。"
                ),
                context={
                    "node_id": node.id,
                    "node_title": node.title,
                    "node_type": node.node_type.value,
                    "test_family_id": node.test_family_id,
                    "node_description": node.description,
                    "available_tools": ["python", "bash"],
                },
            )
        )
        command = self._command_from_trace(
            trace.content,
            node_id=node.id,
            title=node.title,
            node_type=node.node_type.value,
            test_family_id=node.test_family_id or "",
            node_description=node.description,
        )

        started_at = utc_now_iso()
        result = self.tools.run(command.tool_name, command.command)
        finished_at = utc_now_iso()

        raw_output = result.stdout or ""
        if result.stderr:
            raw_output = f"{raw_output}\n[stderr]\n{result.stderr}".strip()
        if trace.content:
            raw_output = f"{raw_output}\n[agent_trace]\n{trace.content}".strip()

        return ActResult(
            node_id=node.id,
            tool_name=result.tool_name,
            command=result.command,
            exit_code=result.exit_code,
            raw_output=raw_output,
            started_at=started_at,
            finished_at=finished_at,
        )

    def _command_from_trace(
        self,
        content: str,
        *,
        node_id: str,
        title: str,
        node_type: str,
        test_family_id: str,
        node_description: str,
    ) -> ActCommand:
        """从模型输出中提取工具命令，失败时回退到本地兜底命令。"""
        payload = self._parse_json_payload(content)
        if payload is None:
            return self._build_fallback_command(
                node_id=node_id,
                title=title,
                node_type=node_type,
                test_family_id=test_family_id,
                node_description=node_description,
            )

        tool_name = str(payload.get("tool_name") or payload.get("tool") or "").strip().lower()
        command = str(payload.get("command") or payload.get("cmd") or "").strip()
        if tool_name not in self.tools.tools or not command:
            return self._build_fallback_command(
                node_id=node_id,
                title=title,
                node_type=node_type,
                test_family_id=test_family_id,
                node_description=node_description,
            )
        return ActCommand(tool_name=tool_name, command=command)

    def _parse_json_payload(self, content: str) -> dict[str, object] | None:
        """兼容纯 JSON 或 markdown code fence 的 JSON 输出。"""
        text = content.strip()
        if not text:
            return None

        candidates = [text]
        fence = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text, flags=re.IGNORECASE)
        if fence:
            candidates.insert(0, fence.group(1).strip())

        object_match = re.search(r"(\{[\s\S]*\})", text)
        if object_match:
            candidates.append(object_match.group(1).strip())

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
        return None

    def _build_fallback_command(
        self,
        *,
        node_id: str,
        title: str,
        node_type: str,
        test_family_id: str,
        node_description: str,
    ) -> ActCommand:
        """兜底命令：在模型未返回可执行命令时保证链路不中断。"""
        url_match = re.search(r"https?://[^\s,;，；。！？]+", f"{title}\n{node_description}")
        if url_match:
            url = url_match.group(0).rstrip("，。！？；,:;)")
            command = "\n".join(
                [
                    "import urllib.request",
                    f"url = {url!r}",
                    "request = urllib.request.Request(url, headers={'User-Agent': 'pikaqiu-agent/0.1'})",
                    "with urllib.request.urlopen(request, timeout=8) as response:",
                    "    body = response.read(600).decode('utf-8', errors='replace')",
                    "    print(f'url:{url}')",
                    "    print(f'status:{response.status}')",
                    "    print('body_preview:')",
                    "    print(body)",
                ]
            )
            return ActCommand(tool_name="python", command=command)

        command = "\n".join(
            [
                "print(" + repr(f"type:{node_type}") + ")",
                "print(" + repr(f"family:{test_family_id or '-'}") + ")",
                "print(" + repr(f"node:{node_id}") + ")",
                "print(" + repr(f"title:{title}") + ")",
                "print('result: fallback execution path used')",
            ]
        )
        return ActCommand(tool_name="python", command=command)
