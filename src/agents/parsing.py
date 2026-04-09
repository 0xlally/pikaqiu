from __future__ import annotations

import json
import re
from typing import Any

from core.models import (
    ActResult,
    AgentRuntimeRequest,
    ConclusionRecord,
    EvidenceRecord,
    NodeStatus,
    NodeType,
    ObjectInventoryEntry,
    ParsedActResult,
    RequestGraphEntry,
    RetryCandidate,
    SessionBundle,
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

HTTP_METHOD_PATTERN = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\b", flags=re.IGNORECASE)

OBJECT_CANDIDATE_PATTERNS = [
    re.compile(r"(?i)\b(?:user|account|order|file|doc|resource|item|tenant|object)[_-]?id\b\s*[:=]\s*[\"']?([A-Za-z0-9_-]{2,64})"),
    re.compile(r"(?i)(?:https?://[^\s'\"<>`]+)?/api/[A-Za-z0-9._~!$&()*+,;=:@%/-]*/([A-Za-z0-9_-]{2,64})"),
]

CREDENTIAL_LINE_HINT_PATTERN = re.compile(r"(?i)(credential|账号|密码|登录|login|auth|default)")


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
            node_type=node.node_type,
            raw_output=act_result.raw_output,
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

        events = self._extract_json_events(raw_output)
        merged = "\n".join([raw_output or "", summary or ""])
        if re.search(r"(?i)(flag\{[^}\n]{1,256}\}|ctf\{[^}\n]{1,256}\}|flag[:=]\s*[^\s\n]{1,256})", merged):
            return NodeStatus.DONE

        if node_type != NodeType.TEST:
            return NodeStatus.DONE

        statuses = [int(code) for code in re.findall(r"(?im)\bstatus\s*[:=]\s*(\d{3})\b", raw_output or "")]
        has_success_status = any(200 <= code < 400 for code in statuses)
        has_5xx_status = any(500 <= code < 600 for code in statuses)
        statuses_all_404 = bool(statuses) and all(code == 404 for code in statuses)
        event_http_statuses = [
            int(item.get("status"))
            for item in events
            if str(item.get("status") or "").lstrip("-").isdigit() and int(item.get("status")) >= 100
        ]

        status_200_count_match = re.search(r'"status_200_count"\s*:\s*(\d+)', raw_output or "")
        status_200_count = int(status_200_count_match.group(1)) if status_200_count_match else None
        anomaly_targets = self._extract_object_inventory(raw_output)

        if any(str(item.get("event") or "") == "fallback_needs_materials" for item in events):
            return NodeStatus.TODO

        if self._has_auth_wall_signal(raw_output, events):
            return NodeStatus.TODO

        if self._has_semantic_failure_signal(raw_output, events):
            return NodeStatus.TODO

        if statuses and not has_success_status and not statuses_all_404:
            return NodeStatus.TODO
        if (
            status_200_count is not None
            and status_200_count <= 0
            and (statuses or event_http_statuses)
            and not statuses_all_404
        ):
            return NodeStatus.TODO
        if has_5xx_status and anomaly_targets:
            return NodeStatus.TODO

        return NodeStatus.DONE

    def _has_auth_wall_signal(self, raw_output: str, events: list[dict[str, Any]]) -> bool:
        if any(str(item.get("event") or "") == "auth_wall_detected" for item in events):
            return True
        statuses = [int(item.get("status")) for item in events if str(item.get("status") or "").isdigit()]
        if statuses and all(status in (401, 403) for status in statuses):
            return True
        if re.search(r"(?i)(unauthorized|forbidden|login required|请先登录)", raw_output or ""):
            return True
        return False

    def _has_semantic_failure_signal(self, raw_output: str, events: list[dict[str, Any]]) -> bool:
        summary_events = [item for item in events if str(item.get("event") or "") == "summary"]
        observed_http_statuses = [
            int(item.get("status"))
            for item in events
            if str(item.get("status") or "").lstrip("-").isdigit() and int(item.get("status")) >= 100
        ]
        observed_all_404 = bool(observed_http_statuses) and all(code == 404 for code in observed_http_statuses)
        for item in summary_events:
            tested = int(item.get("tested_count") or 0)
            success_200 = int(item.get("status_200_count") or 0)
            if tested > 0 and success_200 == 0 and observed_http_statuses and not observed_all_404:
                return True

        probe_events = [item for item in events if str(item.get("event") or "") in {"object_probe", "retry_candidate_probe"}]
        if probe_events:
            statuses = [int(item.get("status") or -1) for item in probe_events]
            if all(status >= 500 or status < 0 for status in statuses):
                return True
        return False

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

        credential_hints = self._extract_credential_materials(raw)
        for item in credential_hints[:4]:
            add("credential_material", item)

        jwt_tokens: list[str] = []
        for token in re.findall(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9._-]{8,}\.[A-Za-z0-9._-]{8,}\b", raw_with_command):
            if token not in jwt_tokens:
                jwt_tokens.append(token)
        for token in jwt_tokens[:4]:
            add("jwt_material", token)

        return evidence, evidence_index, evidence_contents

    def _extract_json_events(self, raw_output: str) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for line in (raw_output or "").splitlines():
            text = line.strip()
            if not text or not text.startswith("{") or not text.endswith("}"):
                continue
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and payload.get("event"):
                events.append(payload)
        return events

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
        node_type: NodeType,
        raw_output: str,
    ) -> StateTableDelta:
        default_refs = [item for ids in evidence_index.values() for item in ids][:3]
        events = self._extract_json_events(raw_output)
        request_templates = self._build_request_templates(executed_command, evidence_contents, raw_output)
        object_inventory_entries = self._build_object_inventory_entries(raw_output, events)
        object_inventory_values = self._flatten_object_inventory_values(object_inventory_entries)
        request_graph_entries = self._build_request_graph_entries(
            node_id=node_id,
            evidence_contents=evidence_contents,
            events=events,
        )
        flow_graph = self._build_flow_graph(
            node_title=node_title,
            api_paths=evidence_contents.get("api_path", []),
            request_graph_entries=request_graph_entries,
        )
        retry_candidates = self._build_retry_candidates(
            node_id=node_id,
            node_title=node_title,
            family_id=family_id,
            node_type=node_type,
            raw_output=raw_output,
            object_inventory=object_inventory_values,
            request_templates=request_templates,
            events=events,
        )
        session_bundles = self._build_session_bundles(
            node_id=node_id,
            raw_output=raw_output,
            request_templates=request_templates,
            evidence_contents=evidence_contents,
            events=events,
        )

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
        reusable_artifacts.extend(
            [
                StateItem(
                    title="请求模板",
                    content=f"{item.get('method', 'GET')} {item.get('path', '')}".strip(),
                    refs=evidence_index.get("api_path", [])[:3] or default_refs,
                    source=node_id,
                )
                for item in request_templates[:8]
                if item.get("path")
            ]
        )

        workflow_prerequisites = [
            StateItem(
                title="对象清单",
                content=target,
                refs=evidence_index.get("api_path", [])[:3] or default_refs,
                source=node_id,
            )
            for target in object_inventory_values[:10]
        ]
        for edge in flow_graph.get("edges", [])[:10]:
            src = str(edge.get("from") or "")
            dst = str(edge.get("to") or "")
            if not src or not dst:
                continue
            workflow_prerequisites.append(
                StateItem(
                    title="流程关系",
                    content=f"{src} -> {dst}",
                    refs=evidence_index.get("api_path", [])[:3] or default_refs,
                    source=node_id,
                )
            )

        session_risks = [
            StateItem(
                title=f"风险提示：{family_id}",
                content=risk_text,
                refs=default_refs,
                source=node_id,
            )
        ]
        if retry_candidates:
            session_risks.append(
                StateItem(
                    title="frontier_queue",
                    content=f"待重试项 {len(retry_candidates)} 条（anomaly_retry）",
                    refs=default_refs,
                    source=node_id,
                )
            )

        notes: list[str] = []
        if trace_content:
            notes.append(trace_content)
        notes.append(f"request_templates={json.dumps(request_templates[:20], ensure_ascii=False)}")
        notes.append(f"object_inventory={json.dumps(object_inventory_values[:20], ensure_ascii=False)}")
        notes.append(f"flow_graph={json.dumps(flow_graph, ensure_ascii=False)}")
        if retry_candidates:
            notes.append(
                "frontier_queue="
                + json.dumps(
                    [
                        {
                            "id": item.id,
                            "retry_key": item.id,
                            "kind": "anomaly_retry",
                            "status": item.status,
                            "reason": item.retry_reason,
                            "method": item.method,
                            "path": item.path,
                            "retries_left": max(item.max_attempts - item.times_attempted, 0),
                            "needs_retry": item.status != "consumed",
                            "family_id": family_id,
                        }
                        for item in retry_candidates[:20]
                    ],
                    ensure_ascii=False,
                )
            )

        return StateTableDelta(
            identities=identities,
            session_materials=session_materials,
            key_entrypoints=key_entrypoints,
            workflow_prerequisites=workflow_prerequisites,
            reusable_artifacts=reusable_artifacts,
            session_risks=session_risks,
            session_bundles=session_bundles,
            request_graph=request_graph_entries,
            object_inventory=object_inventory_entries,
            retry_candidates=retry_candidates,
            notes=notes,
        )

    def _extract_credential_materials(self, raw_output: str) -> list[str]:
        materials: list[str] = []

        users = re.findall(
            r"(?im)[\"']?(?:username|user_name|user|account|login|email)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_.@+-]{2,64})",
            raw_output,
        )
        passwords = re.findall(
            r"(?im)[\"']?(?:password|passwd|pass|pwd)[\"']?\s*[:=]\s*[\"']?([^\s,;\"']{2,64})",
            raw_output,
        )

        for index, username in enumerate(users[:6]):
            if index >= len(passwords):
                break
            password = passwords[index]
            if self._is_valid_credential_pair(username, password):
                candidate = f"{username}:{password}"
                if candidate not in materials:
                    materials.append(candidate)

        for line in raw_output.splitlines():
            if not CREDENTIAL_LINE_HINT_PATTERN.search(line):
                continue
            pair_match = re.search(r"([A-Za-z0-9_.@+-]{2,64})\s*[:/]\s*([^\s,;\"']{2,64})", line)
            if not pair_match:
                continue
            username = pair_match.group(1)
            password = pair_match.group(2)
            if not self._is_valid_credential_pair(username, password):
                continue
            candidate = f"{username}:{password}"
            if candidate not in materials:
                materials.append(candidate)

        return materials[:4]

    def _is_valid_credential_pair(self, username: str, password: str) -> bool:
        normalized_user = username.strip().lower()
        normalized_password = password.strip()
        if not normalized_user or not normalized_password:
            return False
        if normalized_user in {
            "http",
            "https",
            "url",
            "status",
            "content-type",
            "authorization",
            "bearer",
            "host",
            "date",
            "token",
        }:
            return False
        if normalized_password.lower().startswith(("http://", "https://")):
            return False
        if re.search(r"\s", normalized_password):
            return False
        if len(normalized_user) < 2 or len(normalized_password) < 2:
            return False
        return True

    def _build_request_templates(
        self,
        executed_command: str,
        evidence_contents: dict[str, list[str]],
        raw_output: str,
    ) -> list[dict[str, str]]:
        templates: list[dict[str, str]] = []
        api_paths = evidence_contents.get("api_path", [])

        method = "GET"
        method_match = HTTP_METHOD_PATTERN.search(executed_command or "")
        if method_match:
            method = method_match.group(1).upper()

        for path in api_paths[:8]:
            templates.append({"method": method, "path": path, "source": "api_path"})

        for method_value, path in re.findall(
            r"(?i)\b(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\b\s+(?:https?://[^\s'\"<>`]+)?(/api/[A-Za-z0-9._~!$&()*+,;=:@%/-]*)",
            raw_output,
        ):
            entry = {"method": method_value.upper(), "path": path, "source": "raw_output"}
            if entry not in templates:
                templates.append(entry)

        return templates[:12]

    def _build_request_graph_entries(
        self,
        *,
        node_id: str,
        evidence_contents: dict[str, list[str]],
        events: list[dict[str, Any]],
    ) -> list[RequestGraphEntry]:
        entries: list[RequestGraphEntry] = []
        seen: set[tuple[str, str, int, str]] = set()

        def add_entry(path: str, *, url: str = "", status: int = 0, event: str = "", links: list[str] | None = None) -> None:
            normalized_path = str(path or "").strip()
            if not normalized_path:
                return
            key = (normalized_path, str(url or "").strip(), int(status or 0), event)
            if key in seen:
                return
            seen.add(key)

            param_keys: list[str] = []
            if "?" in normalized_path:
                query = normalized_path.split("?", 1)[1]
                for segment in query.split("&"):
                    name = segment.split("=", 1)[0].strip()
                    if name and name not in param_keys:
                        param_keys.append(name)

            entries.append(
                RequestGraphEntry(
                    url=str(url or ""),
                    path=normalized_path,
                    status_code=int(status or 0),
                    links=list(dict.fromkeys(links or []))[:20],
                    discovered_params={"query": param_keys} if param_keys else {},
                    source_node_id=node_id,
                )
            )

        for path in evidence_contents.get("api_path", [])[:20]:
            add_entry(path, event="api_path")

        for item in events:
            event = str(item.get("event") or "").strip()
            path = str(item.get("path") or "").strip()
            url = str(item.get("url") or "").strip()
            status = int(item.get("status") or 0) if str(item.get("status") or "").isdigit() else 0
            links = [str(item.get("path") or "").strip()] if event == "discovered_endpoint" else []
            if event == "discovered_endpoint":
                discovered = str(item.get("path") or "").strip()
                add_entry(discovered, event=event)
                continue
            if event in {
                "post_login_recon",
                "object_probe",
                "retry_candidate_probe",
                "login_page_probe",
                "login_replay",
                "session_recipe_replay",
                "anomaly_retry",
            } and path:
                add_entry(path, url=url, status=status, event=event, links=links)

        return entries[:60]

    def _build_object_inventory_entries(self, raw_output: str, events: list[dict[str, Any]]) -> list[ObjectInventoryEntry]:
        grouped: dict[str, list[str]] = {}

        def add(object_type: str, value: str, *, source_path: str = "", method: str = "regex") -> None:
            normalized = str(value or "").strip().strip("，。！？；,:;)")
            if len(normalized) < 2:
                return
            bucket = grouped.setdefault(object_type, [])
            if normalized not in bucket:
                bucket.append(normalized)

        for value in self._extract_object_inventory(raw_output):
            add(self._infer_object_type(value), value, method="raw_output")

        for item in events:
            for key in ("candidate_value", "base_value", "target"):
                value = str(item.get(key) or "").strip()
                if not value:
                    continue
                add(self._infer_object_type(value), value, source_path=str(item.get("path") or ""), method="event")

        entries: list[ObjectInventoryEntry] = []
        for object_type, values in grouped.items():
            entries.append(
                ObjectInventoryEntry(
                    object_type=object_type,
                    values=values[:30],
                    extraction_method="regex+event",
                    confidence=0.75 if len(values) > 1 else 0.6,
                )
            )
        return entries[:20]

    def _flatten_object_inventory_values(self, entries: list[ObjectInventoryEntry]) -> list[str]:
        values: list[str] = []
        for entry in entries:
            for value in entry.values:
                if value not in values:
                    values.append(value)
        return values[:40]

    def _build_retry_candidates(
        self,
        *,
        node_id: str,
        node_title: str,
        family_id: str,
        node_type: NodeType,
        raw_output: str,
        object_inventory: list[str],
        request_templates: list[dict[str, str]],
        events: list[dict[str, Any]],
    ) -> list[RetryCandidate]:
        candidates: list[RetryCandidate] = []
        seen: set[str] = set()

        def add_candidate(method: str, path: str, payload: dict[str, Any], reason: str, statuses: list[int] | None = None) -> None:
            normalized_method = str(method or "GET").upper()
            normalized_path = str(path or "").strip()
            if not normalized_path:
                return
            key = f"{normalized_method} {normalized_path} {json.dumps(payload, sort_keys=True, ensure_ascii=False)}"
            if key in seen:
                return
            seen.add(key)
            candidates.append(
                RetryCandidate(
                    method=normalized_method,
                    path=normalized_path,
                    params_or_body=payload,
                    retry_reason=reason,
                    times_attempted=0,
                    max_attempts=3,
                    last_statuses=list(statuses or []),
                    source_node_id=node_id,
                    status="pending",
                )
            )

        legacy_queue = self._build_anomaly_retry_frontier_queue(
            node_id=node_id,
            node_title=node_title,
            family_id=family_id,
            node_type=node_type,
            raw_output=raw_output,
            object_inventory=object_inventory,
            request_templates=request_templates,
        )
        for item in legacy_queue:
            command = str(item.get("command") or "")
            method = "GET"
            path = str(item.get("endpoint") or "").strip()
            match = re.match(r"(?i)\s*(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s+([^\s]+)", command)
            if match:
                method = match.group(1).upper()
                if not path:
                    path = match.group(2)
            add_candidate(method, path, {"target": str(item.get("target") or "")}, str(item.get("reason") or "anomaly_retry"), [500])

        for event in events:
            event_name = str(event.get("event") or "")
            if event_name not in {"anomaly_retry", "object_probe", "retry_candidate_probe"}:
                continue
            status = int(event.get("status") or -1) if str(event.get("status") or "").lstrip("-").isdigit() else -1
            if status < 500:
                continue
            method = str(event.get("method") or "GET").upper()
            path = str(event.get("path") or "").strip()
            payload = {
                "candidate_value": str(event.get("candidate_value") or ""),
                "base_value": str(event.get("base_value") or ""),
                "mutation_type": str(event.get("mutation_type") or ""),
            }
            payload = {k: v for k, v in payload.items() if v}
            add_candidate(method, path, payload, f"{event_name}_status_{status}", [status])

        return candidates[:30]

    def _build_session_bundles(
        self,
        *,
        node_id: str,
        raw_output: str,
        request_templates: list[dict[str, str]],
        evidence_contents: dict[str, list[str]],
        events: list[dict[str, Any]],
    ) -> list[SessionBundle]:
        base_url = ""
        for item in events:
            candidate = str(item.get("base_url") or "").strip()
            if candidate:
                base_url = candidate
                break

        if not base_url:
            url_line = re.search(r"(?im)^url:([^\n]+)", raw_output or "")
            if url_line:
                url = url_line.group(1).strip()
                match = re.match(r"(?i)(https?://[^/]+)", url)
                if match:
                    base_url = match.group(1)

        login_recipes: list[dict[str, Any]] = []
        for item in request_templates:
            method = str(item.get("method") or "GET").upper()
            path = str(item.get("path") or "").strip()
            if not path:
                continue
            if any(token in path.lower() for token in ("login", "signin", "password", "auth")):
                login_recipes.append({"method": method, "path": path})

        for item in events:
            if str(item.get("event") or "") != "login_replay":
                continue
            path = str(item.get("path") or "").strip()
            method = str(item.get("method") or "POST").upper()
            payload_keys = item.get("payload_keys") if isinstance(item.get("payload_keys"), list) else []
            payload = {str(key): "<filled_by_act>" for key in payload_keys[:6]}
            if path:
                login_recipes.append({"method": method, "path": path, "payload": payload})

        jwt = ""
        for token in re.findall(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9._-]{8,}\.[A-Za-z0-9._-]{8,}\b", raw_output or ""):
            jwt = token
            break

        headers: dict[str, str] = {}
        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"

        identity = ""
        credentials = self._extract_credential_materials(raw_output)
        if credentials:
            identity = credentials[0].split(":", 1)[0]

        has_login_signal = any(
            str(item.get("event") or "") in {"login_replay", "login_try", "session_recipe_replay", "post_login_recon"}
            for item in events
        )
        if not (base_url or login_recipes or headers or has_login_signal):
            return []

        return [
            SessionBundle(
                base_url=base_url,
                cookies={},
                headers=headers,
                login_recipes=login_recipes[:20],
                current_identity=identity or None,
                authenticated_page_fingerprint=(evidence_contents.get("login_surface") or [""])[0][:160] or None,
                source_node_id=node_id,
            )
        ]

    def _infer_object_type(self, value: str) -> str:
        lowered = str(value or "").lower()
        if "tenant" in lowered:
            return "tenant_id"
        if "user" in lowered:
            return "user_id"
        if "order" in lowered:
            return "order_id"
        if re.fullmatch(r"\d+", lowered):
            return "object_id"
        return "generic"

    def _extract_object_inventory(self, raw_output: str) -> list[str]:
        inventory: list[str] = []
        for pattern in OBJECT_CANDIDATE_PATTERNS:
            for match in pattern.findall(raw_output or ""):
                if isinstance(match, tuple):
                    value = next((item for item in match if item), "")
                else:
                    value = match
                candidate = str(value).strip().strip("，。！？；,:;)")
                if len(candidate) < 2:
                    continue
                if candidate not in inventory:
                    inventory.append(candidate)
        return inventory[:16]

    def _build_flow_graph(
        self,
        *,
        node_title: str,
        api_paths: list[str],
        request_graph_entries: list[RequestGraphEntry],
    ) -> dict[str, Any]:
        nodes = [node_title]
        edges: list[dict[str, str]] = []
        for path in api_paths[:8]:
            if path not in nodes:
                nodes.append(path)
            edges.append({"from": node_title, "to": path, "relation": "touches"})
        for entry in request_graph_entries[:20]:
            path = entry.path
            if not path:
                continue
            if path not in nodes:
                nodes.append(path)
            edges.append({"from": node_title, "to": path, "relation": "observed"})
        return {
            "nodes": nodes[:20],
            "edges": edges[:20],
        }

    def _build_anomaly_retry_frontier_queue(
        self,
        *,
        node_id: str,
        node_title: str,
        family_id: str,
        node_type: NodeType,
        raw_output: str,
        object_inventory: list[str],
        request_templates: list[dict[str, str]],
    ) -> list[dict[str, Any]]:
        if node_type != NodeType.TEST:
            return []

        statuses = [int(code) for code in re.findall(r"(?im)\bstatus\s*[:=]\s*(\d{3})\b", raw_output or "")]
        has_5xx = any(500 <= code < 600 for code in statuses)
        if not has_5xx:
            return []

        targets = object_inventory[:6]
        if not targets:
            return []

        queue: list[dict[str, Any]] = []
        for index, target in enumerate(targets):
            template = request_templates[index] if index < len(request_templates) else {}
            method = str(template.get("method") or "GET").upper()
            path = str(template.get("path") or "")
            queue.append(
                {
                    "id": f"{node_id}-anomaly-retry-{index + 1}",
                    "retry_key": f"{node_id}:anomaly_retry:{target}",
                    "type": "anomaly_retry",
                    "status": "retry",
                    "needs_retry": True,
                    "retries_left": 2,
                    "node_id": node_id,
                    "node_title": node_title,
                    "title": f"{node_title} - anomaly retry {target}",
                    "target": target,
                    "endpoint": path,
                    "command": f"{method} {path}".strip(),
                    "reason": f"5xx 响应命中可疑对象 {target}，需要 anomaly_retry 二次验证。",
                    "description": f"对象 {target} 在测试链路中触发 5xx，需继续验证稳定复现与可利用性。",
                    "test_family_id": family_id,
                }
            )

        return queue[:10]

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
