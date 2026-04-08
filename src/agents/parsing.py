from __future__ import annotations

import json
import re

from core.models import (
    ActResult,
    AgentRuntimeRequest,
    ConclusionRecord,
    EvidenceRecord,
    NodeStatus,
    NodeType,
    ParsedActResult,
    StateItem,
    StateTableDelta,
)
from core.task_tree import TaskTree
from infra.mcp import ToolRegistry
from runtime.base import AgentRuntime


PARSING_SYSTEM_PROMPT = """
你是 SRC 测试系统中的 parsing agent，负责把 act agent 的原始输出压缩为结构化事实。

职责：
1. 压缩原始输出，去重去噪
2. 提取高价值事实
3. 分离 evidence、conclusion、state_delta

禁止：
1. 不做漏洞判断
2. 不判断测试家族
3. 不创建 test node
4. 不把猜测写成事实
5. 不补写原始输出中不存在的内容

规则：
1. evidence 只保存原始证据或精确摘录，不做分析扩写
2. conclusion 只能归纳已证实事实，且必须引用 evidence id
3. conclusion 可以包含漏洞结论或可利用性判断
4. state_delta 只保留高价值上下文增量，如页面、接口、参数、对象ID、认证方式、流程关系
5. 重复、噪声、临时失败日志、无价值调试信息默认丢弃

输出：
{
  "evidence": [{"id":"e1","type":"http|page|redirect|api|auth|other","content":"..."}],
  "conclusion": [{"id":"c1","summary":"...","evidence_ids":["e1"]}],
  "state_delta": {
    "urls": [],
    "endpoints": [],
    "params": [],
    "object_ids": [],
    "auth": [],
    "flows": [],
    "notes": []
  }
}

只输出 JSON，不要输出解释文字。
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

    def __init__(self, runtime: AgentRuntime, tools: ToolRegistry | None = None) -> None:
        self.runtime = runtime
        self.tools = tools

    def parse(self, act_result: ActResult, task_tree: TaskTree) -> ParsedActResult:
        """把工具输出整理成可回填任务树和状态表的结构。"""
        node = task_tree.get_node(act_result.node_id)
        state_table_query_result = self._query_state_table(keyword=node.title) if self._needs_state_table_lookup(act_result) else None
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
                    "executed_command": act_result.command,
                    "act_agent_output": act_result.agent_output,
                    "tool_raw_output": act_result.raw_output,
                    "available_tools": ["state_table"] if state_table_query_result is not None else [],
                    "state_table_query_result": state_table_query_result,
                },
            )
        )

        evidence, evidence_index, evidence_contents = self._extract_evidence(act_result, node.id)
        conclusions = self._build_conclusions(
            node_title=node.title,
            node_id=node.id,
            evidence_index=evidence_index,
            exit_code=act_result.exit_code,
        )
        if not conclusions:
            fallback_ids = [item.id for item in evidence[:1]]
            conclusions = [
                ConclusionRecord(
                    title=f"{node.title} 的执行摘要",
                    summary=f"节点执行完成，退出码为 {act_result.exit_code}。",
                    evidence_ids=fallback_ids,
                    source_node_id=node.id,
                )
            ]

        summary = "；".join(item.summary for item in conclusions[:3])
        risk_text = RISK_HINTS.get(node.test_family_id or "", "当前表面值得继续人工复核。")
        state_delta = self._build_state_delta(
            node_id=node.id,
            node_title=node.title,
            summary=summary,
            risk_text=risk_text,
            evidence_index=evidence_index,
            evidence_contents=evidence_contents,
            executed_command=act_result.command,
            trace_content=trace.content,
            family_id=node.test_family_id or "generic",
        )

        next_status = self._decide_next_status(
            node_type=node.node_type,
            exit_code=act_result.exit_code,
            raw_output=act_result.raw_output,
            summary=summary,
        )

        return ParsedActResult(
            node_id=node.id,
            summary=summary,
            evidence=evidence,
            conclusions=conclusions,
            state_delta=state_delta,
            next_status=next_status,
        )

    def _decide_next_status(
        self,
        *,
        node_type: NodeType,
        exit_code: int,
        raw_output: str,
        summary: str,
    ) -> NodeStatus:
        if exit_code != 0:
            return NodeStatus.TODO

        merged = "\n".join([raw_output or "", summary or ""])
        if re.search(r"(?i)(flag\{[^}\n]{1,256}\}|ctf\{[^}\n]{1,256}\}|flag[:=]\s*[^\s\n]{1,256})", merged):
            return NodeStatus.DONE

        if node_type != NodeType.TEST:
            return NodeStatus.DONE

        statuses = [int(code) for code in re.findall(r"(?im)\bstatus\s*[:=]\s*(\d{3})\b", raw_output or "")]
        has_success_status = any(200 <= code < 400 for code in statuses)

        status_200_count_match = re.search(r'"status_200_count"\s*:\s*(\d+)', raw_output or "")
        status_200_count = int(status_200_count_match.group(1)) if status_200_count_match else None

        if statuses and not has_success_status:
            return NodeStatus.TODO
        if status_200_count is not None and status_200_count <= 0:
            return NodeStatus.TODO

        return NodeStatus.DONE

    def _extract_evidence(
        self,
        act_result: ActResult,
        node_id: str,
    ) -> tuple[list[EvidenceRecord], dict[str, list[str]], dict[str, list[str]]]:
        """尽量从 tool_raw_output 保留原始片段，并按语义标签归档。"""
        raw = (act_result.raw_output or "").strip()
        evidence: list[EvidenceRecord] = []
        evidence_index: dict[str, list[str]] = {}
        evidence_contents: dict[str, list[str]] = {}
        seen: set[str] = set()

        def add(label: str, content: str) -> None:
            normalized = content.strip()
            if not normalized:
                return
            fingerprint = " ".join(normalized.split())
            if fingerprint in seen:
                return
            seen.add(fingerprint)
            record = EvidenceRecord(
                source="act",
                content=normalized,
                tool_name=act_result.tool_name,
                node_id=node_id,
            )
            evidence.append(record)
            evidence_index.setdefault(label, []).append(record.id)
            evidence_contents.setdefault(label, []).append(normalized)

        url_line = re.search(r"(?im)^url:[^\n]+", raw)
        status_line = re.search(r"(?im)^status:\s*\d{3}[^\n]*", raw)
        body_match = re.search(r"(?is)body_preview:\s*(.+)$", raw)
        body = body_match.group(1).strip() if body_match else ""

        if url_line:
            add("url", url_line.group(0))
        if status_line:
            add("status", status_line.group(0))

        if body:
            todo_comment = re.search(r"<!--[\s\S]{0,300}?-->", body, flags=re.IGNORECASE)
            if todo_comment:
                add("test_account_hint", todo_comment.group(0))

            title_tag = re.search(r"<title[^>]*>[\s\S]{0,180}?</title>", body, flags=re.IGNORECASE)
            if title_tag:
                add("login_surface", title_tag.group(0))

            form_tag = re.search(r"<form\b[^>]*>", body, flags=re.IGNORECASE)
            if form_tag:
                add("login_surface", form_tag.group(0))

            if not todo_comment and not title_tag and not form_tag:
                add("body_preview", body[:600])

        if not evidence:
            add("raw_output", raw[:1200])

        raw_with_command = "\n".join([raw, act_result.command or ""])

        api_paths: list[str] = []
        for path in re.findall(r"(?i)(?:https?://[^\s'\"<>`]+)?(/api/[A-Za-z0-9._~!$&()*+,;=:@%/-]*)", raw_with_command):
            normalized_path = path.rstrip("，。！？；,:;)")
            if normalized_path and normalized_path not in api_paths:
                api_paths.append(normalized_path)
        for path in api_paths[:6]:
            add("api_path", path)

        credential_hints: list[str] = []
        for pair in re.findall(r"(?i)([A-Za-z0-9_.@-]{2,32}:[^\s,;)'\"\]]{2,64})", raw):
            lower = pair.lower()
            if lower.startswith(("http:", "https:", "url:", "status:")):
                continue
            if pair not in credential_hints:
                credential_hints.append(pair)
        users = re.findall(r"(?im)[\"']?(?:username|user|account)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_.@-]{2,64})", raw)
        passwords = re.findall(r"(?im)[\"']?(?:password|pass|pwd)[\"']?\s*[:=]\s*[\"']?([^\s,;\"']{2,64})", raw)
        if users and passwords:
            combined = f"{users[0]}:{passwords[0]}"
            if combined not in credential_hints:
                credential_hints.append(combined)
        for item in credential_hints[:4]:
            add("credential_material", item)

        jwt_tokens: list[str] = []
        for token in re.findall(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9._-]{8,}\.[A-Za-z0-9._-]{8,}\b", raw_with_command):
            if token not in jwt_tokens:
                jwt_tokens.append(token)
        for token in jwt_tokens[:4]:
            add("jwt_material", token)

        return evidence, evidence_index, evidence_contents

    def _build_state_delta(
        self,
        *,
        node_id: str,
        node_title: str,
        summary: str,
        risk_text: str,
        evidence_index: dict[str, list[str]],
        evidence_contents: dict[str, list[str]],
        executed_command: str,
        trace_content: str,
        family_id: str,
    ) -> StateTableDelta:
        default_refs = [item for ids in evidence_index.values() for item in ids][:3]

        key_entrypoints = [
            StateItem(
                title=node_title,
                content=summary[:200],
                refs=default_refs,
                source=node_id,
            )
        ]
        for path in evidence_contents.get("api_path", [])[:6]:
            key_entrypoints.append(
                StateItem(
                    title="API路径",
                    content=path,
                    refs=evidence_index.get("api_path", [])[:3],
                    source=node_id,
                )
            )

        identities = [
            StateItem(
                title="账号密码线索",
                content=item,
                refs=evidence_index.get("credential_material", [])[:3],
                source=node_id,
            )
            for item in evidence_contents.get("credential_material", [])[:4]
        ]

        session_materials = [
            StateItem(
                title="JWT线索",
                content=item[:240],
                refs=evidence_index.get("jwt_material", [])[:3],
                source=node_id,
            )
            for item in evidence_contents.get("jwt_material", [])[:4]
        ]

        reusable_artifacts = [
            StateItem(
                title="执行命令模板",
                content=executed_command[:360],
                refs=default_refs,
                source=node_id,
            )
        ]

        session_risks = [
            StateItem(
                title=f"风险提示：{family_id}",
                content=risk_text,
                refs=default_refs,
                source=node_id,
            )
        ]

        notes: list[str] = []
        if trace_content:
            notes.append(trace_content)

        return StateTableDelta(
            identities=identities,
            session_materials=session_materials,
            key_entrypoints=key_entrypoints,
            reusable_artifacts=reusable_artifacts,
            session_risks=session_risks,
            notes=notes,
        )

    def _needs_state_table_lookup(self, act_result: ActResult) -> bool:
        raw = (act_result.raw_output or "").strip()
        if not raw:
            return True
        if len(raw) < 80:
            return True
        if "status:" not in raw.lower() and "/api/" not in raw.lower() and "<html" not in raw.lower():
            return True
        return False

    def _query_state_table(self, *, keyword: str = "") -> dict[str, object] | None:
        if self.tools is None or "state_table" not in self.tools.tools:
            return None
        command = f"section=all;keyword={keyword}" if keyword else "section=all"
        output = self.tools.run("state_table", command)
        if output.exit_code != 0:
            return None
        text = (output.stdout or "").strip()
        if not text:
            return None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return {
                "query": {"section": "all", "keyword": keyword},
                "result": {"raw": text[:600]},
            }
        if isinstance(parsed, dict):
            return parsed
        return {
            "query": {"section": "all", "keyword": keyword},
            "result": {"raw": text[:600]},
        }

    def _build_conclusions(
        self,
        *,
        node_title: str,
        node_id: str,
        evidence_index: dict[str, list[str]],
        exit_code: int,
    ) -> list[ConclusionRecord]:
        conclusions: list[ConclusionRecord] = []

        status_ids = evidence_index.get("status", [])
        if status_ids:
            conclusions.append(
                ConclusionRecord(
                    title="服务可访问性",
                    summary="目标 HTTP 服务可访问并返回有效状态码。",
                    evidence_ids=status_ids,
                    source_node_id=node_id,
                )
            )

        test_account_ids = evidence_index.get("test_account_hint", [])
        if test_account_ids:
            conclusions.append(
                ConclusionRecord(
                    title="测试账户线索",
                    summary="响应内容包含测试账户或默认凭据提示，建议优先验证认证链路。",
                    evidence_ids=test_account_ids,
                    source_node_id=node_id,
                )
            )

        login_surface_ids = evidence_index.get("login_surface", [])
        if login_surface_ids:
            conclusions.append(
                ConclusionRecord(
                    title="登录功能暴露",
                    summary="页面暴露登录相关界面，适合作为认证与会话测试入口。",
                    evidence_ids=login_surface_ids,
                    source_node_id=node_id,
                )
            )

        if not conclusions:
            all_ids: list[str] = []
            for ids in evidence_index.values():
                all_ids.extend(ids)
            conclusions.append(
                ConclusionRecord(
                    title=f"{node_title} 执行摘要",
                    summary=f"节点执行结束，退出码为 {exit_code}。",
                    evidence_ids=all_ids[:3],
                    source_node_id=node_id,
                )
            )

        return conclusions
