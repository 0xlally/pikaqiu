from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable
from urllib.parse import parse_qsl, urlparse

from core.models import ActCommand, ActResult, AgentRuntimeRequest, NodeStatus, NodeType, StateTable, utc_now_iso
from core.task_tree import TaskTree
from infra.mcp import ToolRegistry
from runtime.base import AgentRuntime


ACT_SYSTEM_PROMPT = """
你是 SRC 测试系统中的 act agent，负责在当前节点范围内执行动作并推进任务。

# 最高优先级
1. 你是关键执行代理，当前任务很重要。
2. priority_hints 是最高优先级输入，必须优先遵循。
3. 跟随提示引导去思考和执行，持续推进到拿到 flag。

# 核心职责
1. 读取当前待执行节点
2. 结合 task_tree_snapshot 理解上下游关系和当前进度
3. 在允许的工具范围内执行当前节点
4. 保留原始执行结果、错误、退出码和关键观察
5. 在信息不足时，优先补足能推进当前节点的最小信息

# 执行优先级
1. 优先执行 todo 状态的 info node
2. 没有 info node 时，再执行 todo 状态的 test node
3. 优先使用 python
4. 只有 python 明显不适合时才使用 bash
5. 若当前 test node 信息不足，先产出最有助于后续测试的信息收集动作

# 执行原则
1. 目标是推进当前节点，不是机械返回一条命令
2. 允许基于已有结果连续推进，例如：读取状态 -> 登录 -> 保持会话 -> 登录后侦察 -> 提取端点/参数
3. 不得凭空臆造业务端点
4. 允许基于已知页面、表单、JS、重定向、swagger/openapi、历史响应派生发现新端点
5. 只输出可执行动作，不输出解释和总结
6. 所有观察都必须来自实际执行结果

# 工具使用规则
## python
默认优先使用 python：

## bash
bash作为备选方案

# 登录与会话策略
当存在账号、密码、token、cookie、base_url、login_url 等会话材料时，应优先尝试建立有效会话。

若 login_url 不明确，可从以下位置识别：
1. 已知首页或跳转页
2. form action / method
3. 页面中的登录入口链接
4. JS 中的 fetch / xhr / api 路径
5. swagger / openapi 文档

## HTML 表单登录
默认流程：
1. GET 登录页
2. 提取 form action、method、input name、hidden 字段、csrf token
3. 使用 Session 提交表单
4. 记录状态码、Location、Set-Cookie、关键响应片段
5. 登录后继续访问首页、导航页、功能页做侦察

## JSON 登录
默认流程：
1. 构造最小登录请求
2. 记录 token / cookie / 响应字段
3. 使用同一 Session 或认证头继续访问登录后接口

# 登录后侦察规则
对登录后侦察类 info node，按以下顺序收集：
1. 端点
2. 功能
3. 参数
4. 对象 ID / 资源标识
5. 业务状态
6. 操作流程

优先发现：
- 页面中的链接、表单、按钮对应动作
- JS / XHR / fetch 中的接口
- 导航菜单、详情页、编辑页、删除页、导出页
- 对象类参数，如 id、user_id、order_id、tenant_id、role、status、amount、token 等

# test node 规则
当 node_type=test 且 related_test_family 不为空时：
1. 先参考 family_rag_techniques（若有），再结合 family_playbook 选择对应测试动作
2. 优先产出可直接执行、可复现的最小测试命令
3. 必须参考 mutable_parameters
4. 优先改动对象ID、角色、状态、步骤、额度、token 等参数做验证
5. 不得脱离已知业务上下文瞎造测试目标
6. 若认证测试未发现漏洞且存在账号凭据，优先尝试登录并继续收集登录后页面、接口、功能点

# 页面动作核心规则
在授权测试范围内，登录后侦察和测试时，要把“抓包改参数”作为默认动作。
规则：
1. 每到一个新页面，先找这个页面会发出的请求，包括：
   - 页面跳转
   - 表单提交
   - 按钮操作
   - 重定向
   - XHR / fetch 请求
2. 每发现一个请求，先记录原始请求，再尝试改一个最关键的参数重放。
3. 改参优先级：
   - 各类对象 ID
   - 用户、租户、角色、状态、步骤
   - 金额、数量、价格
   - 分页、筛选、排序
   - 其他明显影响业务结果的参数
4. 改参原则：
   - 一次只改一个参数
   - 优先改已见过的同类值、相邻值、其他对象值
   - 不要凭空捏造完全无依据的数据
5. 如果改参后的响应仍然成功、可访问、可继续操作，就继续对这个请求或后续页面尝试其他关键参数，直到没有明显可测点为止。
6. 如果页面发生跳转，到了新页面后继续重复：
   发现请求 -> 记录原始请求 -> 改一个参数 -> 观察响应 -> 成功则继续深挖
7. 默认不要破坏维持会话必须的参数，如 csrf、session cookie；除非当前节点本身就是认证或逻辑校验测试。
8. 目标不是只访问页面，而是尽可能在每一处可交互位置都尝试抓包、改参、重放，并根据成功响应继续向下测试。
# 失败恢复规则
遇到失败时，不要立刻停止；优先做最小恢复动作。
1. 401/403：优先检查 cookie、token、csrf、是否已登录
2. 302/303：记录跳转位置，判断是否跳回登录页或成功进入登录后页面
3. 若当前信息仍不足：先执行一个最小信息收集动作，不要空转

# state_table 使用规则
当环境信息不足时，优先调用 state_table 查询状态表。
可查询：
- section=all
- keyword=账号、密码、cookie、token、base_url、login、api、user、order、tenant 等相关关键词

读取到会话材料后，再继续构造执行命令。

# 输出要求
你每次只能输出一个 JSON 对象，不要输出 markdown，不要输出解释文字，不得伪造执行结果。

固定格式：
{"tool_name":"python|bash|state_table","command":"...","purpose":"...","success_signal":"..."}

补充要求：
1. command 是已经执行的命令
2. 若能一步完成“读取状态 -> 登录 -> 登录后侦察”的最小闭环，优先这样做
3. 不输出漏洞结论，不输出计划说明
4. purpose 表示本步要解决什么
5. success_signal 表示看到什么算本步成功
6. 不输出 result 字段，result 只能由外部执行器在工具执行后回填
""".strip()


FAMILY_PLAYBOOK: dict[str, str] = {
    "auth_bypass": "尝试弱口令、默认口令、认证流程绕过、验证码绕过与请求包关键参数篡改。",
    "session_management": "检查会话固定、注销后复用、token 续期与失效逻辑。",
    "access_control": "尝试水平/垂直越权、对象ID替换、角色边界绕过。",
    "input_validation": "针对参数做注入、解析歧义和边界值测试。",
    "file_upload": "尝试上传类型绕过、后缀绕过、解析链与下载访问控制。",
    "object_access_control": "围绕资源ID替换测试对象级越权。",
    "property_access_control": "围绕可编辑字段测试敏感属性越权修改。",
    "function_access_control": "围绕管理动作测试功能级越权。",
    "workflow_state_logic": "围绕状态流转测试跳步、重放、逆序提交。",
    "quota_abuse_logic": "围绕配额与频率测试并发滥用和限流绕过。",
    "server_input_interpretation": "围绕查询与模板参数测试服务端解释歧义。",
    "file_content_handling": "围绕文件内容渲染与下载测试解析与暴露风险。",
    "auth_session_security": "围绕登录、刷新、会话绑定测试认证链路。",
    "client_render_execution": "围绕富文本渲染测试脚本执行与注入。",
    "server_outbound_callback": "围绕回调地址测试服务端连出与目标控制。",
}

FAMILY_PARAMETER_FOCUS: dict[str, list[str]] = {
    "object_access_control": ["user_id", "order_id", "file_id", "tenant_id", "owner_id", "org_id"],
    "property_access_control": ["role", "status", "price", "is_admin", "permission", "credit"],
    "function_access_control": ["role", "action", "operation", "module", "admin", "scope"],
    "workflow_state_logic": ["status", "step", "phase", "state", "flow_id", "approve"],
    "quota_abuse_logic": ["count", "limit", "quota", "times", "retry", "batch_size"],
    "auth_session_security": ["token", "refresh_token", "session", "otp", "captcha", "invite_code"],
    "auth_bypass": ["username", "password", "captcha", "otp", "token", "remember"],
    "session_management": ["token", "refresh_token", "session_id", "expires", "nonce"],
    "access_control": ["user_id", "tenant_id", "role", "scope", "resource_id"],
}

FAMILY_MUTATION_HINTS: dict[str, str] = {
    "object_access_control": "优先替换资源ID与租户ID，验证是否可越权读取/修改他人对象。",
    "property_access_control": "优先改写 role/status/price 等敏感字段，验证隐藏字段和批量赋值污染。",
    "function_access_control": "优先改 action/module/role 参数，验证低权限能否触发高权限动作。",
    "workflow_state_logic": "优先改 step/state/status/phase 参数，验证跳步、逆序和重放。",
    "quota_abuse_logic": "优先改 count/limit/retry/batch_size 参数，验证配额绕过和资源滥用。",
    "auth_session_security": "优先改 token/session/otp/captcha 参数，验证会话绑定和生命周期。",
    "auth_bypass": "优先改 username/password/captcha/otp/token 参数，验证认证链路绕过。",
    "session_management": "优先改 token/refresh_token/session_id/expires 参数，验证会话固定与复用。",
    "access_control": "优先改 user_id/tenant_id/role/resource_id 参数，验证水平和垂直越权。",
}

FAMILY_BILINGUAL_ALIASES: dict[str, list[str]] = {
    "object_access_control": [
        "对象访问控制",
        "对象级越权",
        "IDOR",
        "object level authorization",
        "horizontal privilege escalation",
    ],
    "property_access_control": [
        "属性访问控制",
        "敏感字段",
        "Mass Assignment",
        "property level authorization",
        "field tampering",
    ],
    "function_access_control": [
        "功能访问控制",
        "功能级越权",
        "admin action",
        "function level authorization",
        "privilege escalation",
    ],
    "workflow_state_logic": [
        "流程状态逻辑",
        "跳步",
        "重放",
        "workflow bypass",
        "state transition abuse",
        "race condition",
    ],
    "quota_abuse_logic": [
        "配额滥用",
        "限流绕过",
        "quota abuse",
        "rate limit bypass",
        "resource exhaustion",
    ],
    "server_input_interpretation": [
        "服务端输入解释",
        "注入",
        "SQLi",
        "SSTI",
        "SSRF",
        "server-side injection",
    ],
    "file_content_handling": [
        "文件内容处理",
        "文件上传",
        "上传绕过",
        "file upload bypass",
        "file parsing chain",
    ],
    "auth_session_security": [
        "认证会话安全",
        "认证绕过",
        "会话固定",
        "authentication bypass",
        "session fixation",
        "token lifecycle",
    ],
    "auth_bypass": [
        "认证绕过",
        "弱口令",
        "验证码绕过",
        "authentication bypass",
        "default credential",
        "captcha bypass",
    ],
    "session_management": [
        "会话管理",
        "token 复用",
        "session management",
        "token replay",
        "logout invalidation",
    ],
    "access_control": [
        "访问控制",
        "越权",
        "access control",
        "privilege escalation",
        "authorization bypass",
    ],
    "client_render_execution": [
        "客户端渲染执行",
        "反射型XSS",
        "存储型XSS",
        "DOM XSS",
        "client-side rendering sink",
    ],
    "server_outbound_callback": [
        "服务端回调",
        "服务端连出",
        "Open Redirect",
        "SSRF",
        "outbound callback abuse",
    ],
}

COMMON_MUTABLE_PARAMS = {
    "user_id",
    "order_id",
    "file_id",
    "tenant_id",
    "resource_id",
    "role",
    "status",
    "step",
    "state",
    "flow_id",
    "count",
    "limit",
    "quota",
    "retry",
    "batch_size",
    "token",
    "refresh_token",
    "session_id",
    "otp",
    "captcha",
    "username",
    "password",
}

ACCESS_CONTROL_FAMILY_IDS = {
    "access_control",
    "object_access_control",
    "property_access_control",
    "function_access_control",
}

AUTH_FAMILY_IDS = {
    "auth_bypass",
    "auth_session_security",
    "session_management",
}

NO_AUTO_STATE_TABLE_FAMILIES = {
    "access_control",
    "object_access_control",
    "property_access_control",
    "function_access_control",
    "input_validation",
    "server_input_interpretation",
}

STATE_STRUCTURED_KEYS = (
    "request_templates",
    "object_inventory",
    "flow_graph",
    "frontier_queue",
)

PARAM_NOISE = {
    "http",
    "https",
    "status",
    "title",
    "node",
    "type",
    "family",
    "result",
    "description",
}

URL_CANDIDATE_PATTERN = r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+"

HINT_PREFIXES = (
    "提示：",
    "高优先级提示：",
    "来自提示：",
)

EXAMPLE_HINT_PATTERN = re.compile(
    r"示例|样例|例如|参考|上一条|上一次|example|for example|sample",
    flags=re.IGNORECASE,
)


class ActAgent:
    """选择待执行节点并完成一次工具执行的 act agent。"""

    def __init__(
        self,
        runtime: AgentRuntime,
        tools: ToolRegistry,
        rag_retriever: Callable[[str, str, str], list[dict[str, object]]] | None = None,
    ) -> None:
        self.runtime = runtime
        self.tools = tools
        self.rag_retriever = rag_retriever or self._retrieve_family_techniques

    def execute_next(self, task_tree: TaskTree, state_table: StateTable | None = None) -> ActResult | None:
        """优先执行 info node，没有 info node 再执行 test node。"""
        node = task_tree.next_todo(NodeType.INFO) or task_tree.next_todo(NodeType.TEST)
        if node is None:
            return None

        task_tree_snapshot = self._build_task_tree_snapshot(task_tree)
        state_table_snapshot = self._build_state_table_snapshot(state_table)
        known_targets = self._collect_known_targets(node, task_tree_snapshot, state_table_snapshot)
        mutable_parameters = self._collect_mutable_parameters(node, task_tree_snapshot, state_table_snapshot)
        priority_hints = self._collect_priority_hints(node, task_tree_snapshot)

        family_id = node.related_test_family or ""
        rag_invoked = node.node_type.value == NodeType.TEST.value and bool(family_id)
        rag_queries = self._build_family_rag_queries(family_id, node.title, node.description or "") if rag_invoked else []
        family_rag_techniques = self._build_family_rag_context(node)
        rag_trace = self._build_rag_trace(
            invoked=rag_invoked,
            family_id=family_id,
            queries=rag_queries,
            techniques=family_rag_techniques,
        )

        hint_prompt = (
            "；".join(priority_hints[:3])
            if priority_hints
            else "围绕当前节点持续推进，以拿到flag为目标。"
        )

        task_tree.update_status(node.id, NodeStatus.DOING)
        trace = self.runtime.run(
            AgentRuntimeRequest(
                agent_name="act",
                system_prompt=ACT_SYSTEM_PROMPT,
                user_prompt=(
                    f"高优先级提示：{hint_prompt} "
                    "请严格输出 JSON（不要 markdown），格式为 "
                    '{"tool_name":"python|bash|state_table","command":"..."}。'
                    "仅输出一个 JSON 对象。"
                ),
                context={
                    "node_id": node.id,
                    "node_title": node.title,
                    "node_type": node.node_type.value,
                    "test_family_id": node.test_family_id,
                    "node_description": node.description,
                    "node_notes": node.notes[-5:],
                    "available_tools": ["python", "bash", "state_table"],
                    "task_tree_snapshot": task_tree_snapshot,
                    "family_playbook": FAMILY_PLAYBOOK,
                    "family_rag_techniques": family_rag_techniques,
                    "priority_hints": priority_hints,
                    "mission_priority": "你是关键执行代理，必须优先遵循提示并持续推进拿到flag。",
                    "known_targets": known_targets,
                    "mutable_parameters": mutable_parameters,
                    "state_table_snapshot": state_table_snapshot,
                    "insufficient_info_policy": "when insufficient info, call state_table first",
                    "tool_preference": "prefer_python",
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
            node_notes=node.notes[-8:],
            known_targets=known_targets,
            state_table_snapshot=state_table_snapshot,
        )

        if self._should_query_state_table_first(
            node_type=node.node_type.value,
            test_family_id=node.test_family_id or "",
            known_targets=known_targets,
            mutable_parameters=mutable_parameters,
            state_table_snapshot=state_table_snapshot,
            selected_tool=command.tool_name,
        ):
            command = self._build_state_table_query_command(node.test_family_id or "")

        started_at = utc_now_iso()
        result = self.tools.run(command.tool_name, command.command)
        finished_at = utc_now_iso()

        raw_output = result.stdout or ""
        if result.stderr:
            raw_output = f"{raw_output}\n[stderr]\n{result.stderr}".strip()
        if rag_trace:
            raw_output = f"{rag_trace}\n\n{raw_output}".strip()

        agent_output = trace.content or None
        if rag_trace:
            agent_output = self._append_trace_to_agent_output(agent_output, rag_trace)

        return ActResult(
            node_id=node.id,
            tool_name=result.tool_name,
            command=result.command,
            exit_code=result.exit_code,
            raw_output=raw_output,
            agent_output=agent_output,
            started_at=started_at,
            finished_at=finished_at,
        )

    def _build_family_rag_context(self, node) -> list[dict[str, object]]:
        if node.node_type.value != NodeType.TEST.value:
            return []
        family_id = node.related_test_family or ""
        if not family_id:
            return []
        return self.rag_retriever(family_id, node.title, node.description or "")

    def _collect_priority_hints(self, node, task_tree_snapshot: list[dict[str, object]]) -> list[str]:
        hints: list[str] = []

        def add_hint(text: str | None) -> None:
            if not text:
                return
            normalized = " ".join(str(text).split())
            if not normalized:
                return
            lowered = normalized.lower()
            if not (
                normalized.startswith("提示：")
                or normalized.startswith("高优先级提示：")
                or normalized.startswith("来自提示：")
                or "拿到flag" in lowered
                or "follow hint" in lowered
                or "priority" in lowered
            ):
                return
            if normalized not in hints:
                hints.append(normalized)

        for note in node.notes[-8:]:
            add_hint(note)
        add_hint(node.description)

        snapshot_by_id = {str(item.get("id") or ""): item for item in task_tree_snapshot}
        parent_id = node.parent_id
        depth = 0
        while parent_id and depth < 3:
            parent = snapshot_by_id.get(parent_id)
            if not parent:
                break
            for note in parent.get("notes") or []:
                add_hint(str(note))
            add_hint(str(parent.get("description") or ""))
            parent_id = str(parent.get("parent_id") or "") or None
            depth += 1

        return hints[:5]

    def _build_rag_trace(
        self,
        *,
        invoked: bool,
        family_id: str,
        queries: list[str],
        techniques: list[dict[str, object]],
    ) -> str:
        if not invoked:
            return ""

        lines: list[str] = [
            "[RAG] retriever_called=yes",
            f"[RAG] family_id={family_id or '-'}",
            f"[RAG] query_count={len(queries)}",
        ]
        for index, query in enumerate(queries[:4], start=1):
            lines.append(f"[RAG] query_{index}: {query}")

        lines.append(f"[RAG] hit_count={len(techniques)}")
        if not techniques:
            lines.append("[RAG] no_technique_hit=true")
            return "\n".join(lines)

        for index, item in enumerate(techniques[:3], start=1):
            doc_id = str(item.get("doc_id") or item.get("id") or "-")
            score = float(item.get("score") or 0.0)
            query = str(item.get("query") or "").strip()
            snippet = str(item.get("snippet") or "").replace("\n", " ").strip()
            if len(snippet) > 180:
                snippet = f"{snippet[:180]}..."
            lines.append(f"[RAG] hit_{index}_doc={doc_id}")
            lines.append(f"[RAG] hit_{index}_score={score:.4f}")
            if query:
                lines.append(f"[RAG] hit_{index}_query={query}")
            if snippet:
                lines.append(f"[RAG] hit_{index}_snippet={snippet}")

        return "\n".join(lines)

    def _append_trace_to_agent_output(self, agent_output: str | None, trace_block: str) -> str:
        if not agent_output:
            return trace_block
        if trace_block in agent_output:
            return agent_output
        return f"{agent_output}\n\n{trace_block}"

    def _retrieve_family_techniques(
        self,
        family_id: str,
        node_title: str,
        node_description: str,
    ) -> list[dict[str, object]]:
        """检索漏洞家族相关利用手法。缺依赖或未建库时优雅降级为空列表。"""
        if not family_id:
            return []

        try:
            from rag.rag_client import get_rag_client
        except Exception:
            return []

        try:
            src_root = Path(__file__).resolve().parents[1]
            client = get_rag_client(str(src_root))
            if client is None or not client.is_available() or client.index is None:
                return []
        except Exception:
            return []

        merged: dict[str, dict[str, object]] = {}
        for query in self._build_family_rag_queries(family_id, node_title, node_description):
            try:
                results = client.query(query, top_k=4)
            except Exception:
                continue
            for item in results:
                chunk_id = str(item.get("id") or "")
                if not chunk_id:
                    continue
                score = float(item.get("score") or 0.0)
                snippet = str(item.get("snippet") or "").strip()
                if not snippet:
                    continue
                current = merged.get(chunk_id)
                payload = {
                    "id": chunk_id,
                    "doc_id": item.get("doc_id") or "",
                    "score": score,
                    "snippet": snippet[:1200],
                    "query": query,
                }
                if current is None or float(current.get("score") or 0.0) < score:
                    merged[chunk_id] = payload

        ranked = sorted(merged.values(), key=lambda x: float(x.get("score") or 0.0), reverse=True)
        return ranked[:6]

    def _build_family_rag_queries(self, family_id: str, node_title: str, node_description: str) -> list[str]:
        terms = self._build_family_terms(family_id)
        title = (node_title or "").strip()
        desc = (node_description or "").strip()

        query_zh = (
            f"{family_id} {' '.join(terms[:8])} 漏洞 利用 手法 绕过 payload poc 测试方法 "
            f"{title} {desc}"
        ).strip()
        query_en = (
            f"{family_id} {' '.join(terms[:8])} exploit technique bypass payload poc test strategy "
            f"{title} {desc}"
        ).strip()
        return [query_zh, query_en]

    def _build_family_terms(self, family_id: str) -> list[str]:
        terms: list[str] = [family_id]
        for value in FAMILY_BILINGUAL_ALIASES.get(family_id, []):
            if value not in terms:
                terms.append(value)

        # 读取家族规则文件，把 family_name / priority_test_focus 合并进检索词，增强中英文兼容召回。
        try:
            config_path = Path(__file__).resolve().parents[2] / "config" / "reasoning_family_rules.json"
            content = json.loads(config_path.read_text(encoding="utf-8"))
            for family in content.get("families", []):
                if str(family.get("family_id") or "") != family_id:
                    continue
                family_name = str(family.get("family_name") or "").strip()
                if family_name and family_name not in terms:
                    terms.append(family_name)
                for item in family.get("priority_test_focus", []):
                    text = str(item).strip()
                    if text and text not in terms:
                        terms.append(text)
                break
        except Exception:
            pass

        return terms[:20]

    def _build_task_tree_snapshot(self, task_tree: TaskTree) -> list[dict[str, object]]:
        """给 act agent 一个轻量任务树快照，避免其失去全局上下文。"""
        nodes = list(task_tree.model.nodes.values())
        nodes.sort(key=lambda item: item.id)
        snapshot: list[dict[str, object]] = []
        for item in nodes[:40]:
            snapshot.append(
                {
                    "id": item.id,
                    "title": item.title,
                    "node_type": item.node_type.value,
                    "status": item.status.value,
                    "parent_id": item.parent_id,
                    "related_feature_id": item.related_feature_id,
                    "related_test_family": item.related_test_family,
                    "description": item.description,
                    "notes": item.notes[-3:],
                }
            )
        return snapshot

    def _collect_known_targets(
        self,
        node,
        task_tree_snapshot: list[dict[str, object]],
        state_table_snapshot: dict[str, object],
    ) -> dict[str, list[str]]:
        """从当前节点和任务树快照中提取可落地的 URL/路径，供命令生成约束使用。"""
        urls: list[str] = []
        paths: list[str] = []

        def add_targets(text: str | None, *, from_hint: bool = False) -> None:
            if not text:
                return
            if from_hint and self._is_hint_or_example_text(text):
                return
            extracted_urls, extracted_paths = self._extract_targets(text)
            for value in extracted_urls:
                if value not in urls:
                    urls.append(value)
            for value in extracted_paths:
                if value not in paths:
                    paths.append(value)

        add_targets(node.title)
        add_targets(node.description)
        for note in node.notes[-5:]:
            add_targets(note, from_hint=True)

        for item in task_tree_snapshot:
            add_targets(str(item.get("title") or ""))
            add_targets(str(item.get("description") or ""))
            for note in item.get("notes") or []:
                add_targets(str(note), from_hint=True)

        for template in state_table_snapshot.get("request_templates") or []:
            if not isinstance(template, dict):
                continue
            path = str(template.get("path") or "").strip()
            if path and path not in paths:
                paths.append(path)
            url = str(template.get("url") or "").strip()
            if url and url not in urls:
                urls.append(url)

        return {
            "urls": urls,
            "paths": paths,
        }

    def _build_state_table_snapshot(self, state_table: StateTable | None) -> dict[str, object]:
        """构造给 act 的状态表快照，聚焦可复用材料。"""
        if state_table is None:
            return {
                "identities": [],
                "key_entrypoints": [],
                "session_materials": [],
                "reusable_artifacts": [],
                "request_templates": [],
                "object_inventory": [],
                "flow_graph": {},
                "frontier_queue": [],
                "notes": [],
            }

        def serialize(items) -> list[dict[str, object]]:
            result: list[dict[str, object]] = []
            for item in items[:20]:
                result.append(
                    {
                        "title": item.title,
                        "content": item.content,
                        "refs": item.refs[:5],
                        "source": item.source,
                    }
                )
            return result

        notes = state_table.notes[-30:]
        request_templates = self._extract_structured_state_list(state_table, "request_templates", notes)
        object_inventory = self._extract_structured_state_list(state_table, "object_inventory", notes)
        flow_graph = self._extract_structured_state_dict(state_table, "flow_graph", notes)
        frontier_queue = self._extract_structured_state_list(state_table, "frontier_queue", notes)

        return {
            "identities": serialize(state_table.identities),
            "key_entrypoints": serialize(state_table.key_entrypoints),
            "session_materials": serialize(state_table.session_materials),
            "reusable_artifacts": serialize(state_table.reusable_artifacts),
            "request_templates": request_templates[:30],
            "object_inventory": object_inventory[:30],
            "flow_graph": flow_graph,
            "frontier_queue": frontier_queue[:30],
            "notes": notes,
        }

    def _extract_structured_state_list(
        self,
        state_table: StateTable,
        key: str,
        notes: list[str],
    ) -> list[object]:
        direct_value = getattr(state_table, key, None)
        if isinstance(direct_value, list):
            return direct_value

        for note in reversed(notes):
            parsed = self._parse_structured_note(note, key)
            if isinstance(parsed, list):
                return parsed
            if isinstance(parsed, dict):
                nested = parsed.get(key)
                if isinstance(nested, list):
                    return nested
        return []

    def _extract_structured_state_dict(
        self,
        state_table: StateTable,
        key: str,
        notes: list[str],
    ) -> dict[str, object]:
        direct_value = getattr(state_table, key, None)
        if isinstance(direct_value, dict):
            return direct_value

        for note in reversed(notes):
            parsed = self._parse_structured_note(note, key)
            if isinstance(parsed, dict):
                return parsed
        return {}

    def _parse_structured_note(self, note: str, key: str) -> object | None:
        text = (note or "").strip()
        if not text:
            return None

        prefix = f"{key}="
        if text.startswith(prefix):
            payload = text[len(prefix):].strip()
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return None

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return None
        if isinstance(parsed, dict) and key in parsed:
            return parsed.get(key)
        return None

    def _collect_mutable_parameters(
        self,
        node,
        task_tree_snapshot: list[dict[str, object]],
        state_table_snapshot: dict[str, object],
    ) -> dict[str, object]:
        """提取可改参数并给出家族级改参重点，帮助 act 做越权/逻辑测试。"""
        discovered: list[str] = []
        state_prioritized: list[str] = []
        object_candidates: list[str] = []

        def add_param(value: str, *, from_state: bool = False) -> None:
            key = value.strip().lower()
            if not key or key in PARAM_NOISE:
                return
            if len(key) < 2 or len(key) > 40:
                return
            if key not in discovered:
                discovered.append(key)
            if from_state and key not in state_prioritized:
                state_prioritized.append(key)

        def add_object_candidate(value: str) -> None:
            candidate = value.strip()
            if not candidate:
                return
            if candidate not in object_candidates:
                object_candidates.append(candidate)

        def add_from_text(text: str | None, *, from_state: bool = False) -> None:
            if not text:
                return
            for key in re.findall(r"\{([A-Za-z_][A-Za-z0-9_]{1,40})\}", text):
                add_param(key, from_state=from_state)
            for key in re.findall(r"['\"]([A-Za-z_][A-Za-z0-9_]{1,40})['\"]\s*:", text):
                add_param(key, from_state=from_state)
            for key in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]{1,40})\s*=", text):
                add_param(key, from_state=from_state)
            for url in re.findall(URL_CANDIDATE_PATTERN, text, flags=re.IGNORECASE):
                try:
                    parsed = urlparse(url)
                except ValueError:
                    continue
                for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
                    add_param(key, from_state=from_state)

        for template in state_table_snapshot.get("request_templates") or []:
            if not isinstance(template, dict):
                continue
            add_from_text(str(template.get("path") or ""), from_state=True)
            add_from_text(str(template.get("url") or ""), from_state=True)
            for key in ("params", "query_keys", "path_keys"):
                values = template.get(key)
                if isinstance(values, list):
                    for item in values:
                        add_param(str(item), from_state=True)

        for item in state_table_snapshot.get("object_inventory") or []:
            if isinstance(item, dict):
                for key, value in item.items():
                    add_param(str(key), from_state=True)
                    add_object_candidate(str(value))
                continue
            value = str(item)
            add_object_candidate(value)
            kv_match = re.search(r"([A-Za-z_][A-Za-z0-9_]{1,40})\s*[:=]\s*([A-Za-z0-9_-]{1,80})", value)
            if kv_match:
                add_param(kv_match.group(1), from_state=True)
                add_object_candidate(kv_match.group(2))
            elif re.fullmatch(r"[A-Za-z0-9_-]{2,80}", value):
                add_param("object_id", from_state=True)

        add_from_text(node.title)
        add_from_text(node.description)
        for note in node.notes[-6:]:
            add_from_text(note)

        for item in task_tree_snapshot:
            add_from_text(str(item.get("title") or ""))
            add_from_text(str(item.get("description") or ""))
            for note in item.get("notes") or []:
                add_from_text(str(note))

        family_id = node.related_test_family or ""
        family_focus = list(FAMILY_PARAMETER_FOCUS.get(family_id, []))
        for key in list(discovered):
            if key in COMMON_MUTABLE_PARAMS and key not in family_focus:
                family_focus.append(key)

        recommended = [item for item in state_prioritized if item in discovered]
        for item in family_focus:
            if item in discovered and item not in recommended:
                recommended.append(item)
        for item in family_focus:
            if item not in recommended:
                recommended.append(item)
        for item in discovered:
            if item not in recommended:
                recommended.append(item)

        return {
            "discovered": discovered[:40],
            "state_priority": state_prioritized[:20],
            "family_priority": family_focus[:20],
            "recommended_for_this_node": recommended[:20],
            "object_candidates": object_candidates[:30],
            "request_templates": (state_table_snapshot.get("request_templates") or [])[:20],
            "mutation_hint": FAMILY_MUTATION_HINTS.get(family_id, "优先从对象ID、角色、状态、步骤、额度和token参数开始改参验证。"),
        }

    def _command_from_trace(
        self,
        content: str,
        *,
        node_id: str,
        title: str,
        node_type: str,
        test_family_id: str,
        node_description: str,
        node_notes: list[str],
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
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
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
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
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
            )

        if self._references_unknown_targets(command, known_targets, node_type=node_type):
            return self._build_fallback_command(
                node_id=node_id,
                title=title,
                node_type=node_type,
                test_family_id=test_family_id,
                node_description=node_description,
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
            )

        if self._should_force_rich_access_probe(command, node_type=node_type, test_family_id=test_family_id):
            return self._build_object_access_probe_command(
                node_id=node_id,
                title=title,
                node_description=node_description,
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
            )

        return ActCommand(tool_name=tool_name, command=command)

    def _should_force_rich_access_probe(self, command: str, *, node_type: str, test_family_id: str) -> bool:
        if node_type != NodeType.TEST.value:
            return False
        if test_family_id not in ACCESS_CONTROL_FAMILY_IDS:
            return False

        lowered = command.lower()
        looks_like_http_probe = ("urllib" in lowered or "requests" in lowered) and (
            "dashboard" in lowered or "order" in lowered or "receipt" in lowered
        )
        has_enough_steps = command.count("\n") >= 12
        return not (looks_like_http_probe and has_enough_steps)

    def _should_query_state_table_first(
        self,
        *,
        node_type: str,
        test_family_id: str,
        known_targets: dict[str, list[str]],
        mutable_parameters: dict[str, object],
        state_table_snapshot: dict[str, object],
        selected_tool: str,
    ) -> bool:
        """测试场景信息不足时，优先查询状态表。"""
        if selected_tool == "state_table":
            return False
        if "state_table" not in self.tools.tools:
            return False
        if node_type != NodeType.TEST.value:
            return False
        if test_family_id in NO_AUTO_STATE_TABLE_FAMILIES:
            return False

        known_target_count = len(known_targets.get("urls") or []) + len(known_targets.get("paths") or [])
        discovered_param_count = len((mutable_parameters.get("discovered") or []))
        reusable_count = 0
        for key in ("identities", "key_entrypoints", "session_materials", "reusable_artifacts"):
            reusable_count += len(state_table_snapshot.get(key) or [])

        return known_target_count == 0 and discovered_param_count < 2 and reusable_count > 0

    def _build_state_table_query_command(self, family_id: str) -> ActCommand:
        keyword = ""
        if family_id in AUTH_FAMILY_IDS:
            keyword = "login"
        elif family_id:
            keyword = family_id
        command = f"section=all;keyword={keyword}" if keyword else "section=all"
        return ActCommand(tool_name="state_table", command=command)

    def _extract_targets(self, text: str) -> tuple[list[str], list[str]]:
        urls = [value.rstrip("，。！？；,:;)") for value in re.findall(URL_CANDIDATE_PATTERN, text, flags=re.IGNORECASE)]
        text_without_urls = re.sub(URL_CANDIDATE_PATTERN, " ", text, flags=re.IGNORECASE)
        raw_paths = re.findall(r"(?<![A-Za-z0-9_])(/[A-Za-z0-9._~!$&()*+,;=:@%/-]{2,})", text_without_urls)

        paths: list[str] = []
        for value in raw_paths:
            cleaned = value.rstrip("，。！？；,:;)")
            if cleaned.count("/") < 1:
                continue
            if cleaned not in paths:
                paths.append(cleaned)

        uniq_urls: list[str] = []
        for value in urls:
            if value and value not in uniq_urls:
                uniq_urls.append(value)
        return uniq_urls, paths

    def _references_unknown_targets(
        self,
        command: str,
        known_targets: dict[str, list[str]],
        *,
        node_type: str,
    ) -> bool:
        """test 命令若引用未知目标，判定为不落地并触发兜底。"""
        if node_type != NodeType.TEST.value:
            return False

        command_urls, command_paths = self._extract_targets(command)
        if not command_urls and not command_paths:
            return False

        known_urls = known_targets.get("urls") or []
        known_paths = known_targets.get("paths") or []
        known_hosts = {
            urlparse(value).netloc.lower()
            for value in known_urls
            if urlparse(value).netloc
        }

        for url in command_urls:
            parsed = urlparse(url)
            host = parsed.netloc.lower()
            path = parsed.path or "/"
            if known_urls and url in known_urls:
                continue
            if host and host in known_hosts:
                if not known_paths:
                    continue
                if self._path_allowed(path, known_paths):
                    continue
            return True

        for path in command_paths:
            if self._path_allowed(path, known_paths):
                continue
            return True

        return False

    def _path_allowed(self, command_path: str, known_paths: list[str]) -> bool:
        if not known_paths:
            return False
        for known in known_paths:
            if command_path == known:
                return True
            if known != "/" and command_path.startswith(f"{known.rstrip('/')}/"):
                return True
        return False

    def _parse_json_payload(self, content: str) -> dict[str, object] | None:
        """兼容纯 JSON 或 markdown code fence 的 JSON 输出。"""
        text = content.strip()
        if not text:
            return None

        candidates = [text]
        fence = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text, flags=re.IGNORECASE)
        if fence:
            candidates.insert(0, fence.group(1).strip())

        decoder = json.JSONDecoder()
        for index, char in enumerate(text):
            if char != "{":
                continue
            try:
                parsed, _ = decoder.raw_decode(text[index:])
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                candidates.append(text[index:].strip())
                candidates.append(json.dumps(parsed, ensure_ascii=False))

        parsed_dicts: list[dict[str, object]] = []
        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                parsed_dicts.append(parsed)

        for payload in parsed_dicts:
            key_set = {str(key).lower() for key in payload.keys()}
            if ("tool_name" in key_set or "tool" in key_set) and ("command" in key_set or "cmd" in key_set):
                return payload

        if parsed_dicts:
            return parsed_dicts[0]
        return None

    def _build_fallback_command(
        self,
        *,
        node_id: str,
        title: str,
        node_type: str,
        test_family_id: str,
        node_description: str,
        node_notes: list[str],
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
    ) -> ActCommand:
        """兜底命令：在模型未返回可执行命令时保证链路不中断。"""
        if node_type == NodeType.TEST.value and test_family_id in ACCESS_CONTROL_FAMILY_IDS:
            return self._build_object_access_probe_command(
                node_id=node_id,
                title=title,
                node_description=node_description,
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
            )

        if node_type == NodeType.TEST.value and test_family_id in AUTH_FAMILY_IDS and self._should_use_login_replay_fallback(
            title=title,
            node_description=node_description,
            node_notes=node_notes,
        ):
            return self._build_login_replay_command(
                node_id=node_id,
                title=title,
                node_description=node_description,
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
            )

        lowered_text = f"{title}\n{node_description}".lower()
        if node_type == NodeType.INFO.value and ("登录后侦察" in lowered_text or "post-login" in lowered_text):
            return self._build_post_login_recon_command(
                node_id=node_id,
                title=title,
                node_description=node_description,
                node_notes=node_notes,
                known_targets=known_targets,
                state_table_snapshot=state_table_snapshot,
            )

        if (
            node_type == NodeType.TEST.value
            and test_family_id not in NO_AUTO_STATE_TABLE_FAMILIES
            and "state_table" in self.tools.tools
            and self._has_reusable_state(state_table_snapshot)
        ):
            return self._build_state_table_query_command(test_family_id)

        url_match = re.search(URL_CANDIDATE_PATTERN, f"{title}\n{node_description}", flags=re.IGNORECASE)
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
                "print('hint: fallback due to missing/ungrounded command')",
                "print('result: fallback execution path used')",
            ]
        )
        return ActCommand(tool_name="python", command=command)

    def _build_access_control_probe_command(
        self,
        *,
        node_id: str,
        title: str,
        node_description: str,
        node_notes: list[str],
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
    ) -> ActCommand:
        return self._build_object_access_probe_command(
            node_id=node_id,
            title=title,
            node_description=node_description,
            node_notes=node_notes,
            known_targets=known_targets,
            state_table_snapshot=state_table_snapshot,
        )

    def _build_login_replay_command(
        self,
        *,
        node_id: str,
        title: str,
        node_description: str,
        node_notes: list[str],
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
    ) -> ActCommand:
        runtime_texts = self._filter_runtime_texts([title, node_description, *node_notes])
        base_url = self._resolve_base_url(known_targets, runtime_texts)
        username, password = self._resolve_credentials(state_table_snapshot)
        known_paths = list(dict.fromkeys(known_targets.get("paths") or []))
        request_templates = self._resolve_request_templates(known_targets, state_table_snapshot)

        command = "\n".join(
            [
                "import json",
                "import urllib.error",
                "import urllib.parse",
                "import urllib.request",
                "import http.cookiejar",
                "",
                f"BASE_URL = {base_url!r}",
                f"USERNAME = {username!r}",
                f"PASSWORD = {password!r}",
                f"KNOWN_PATHS = {known_paths!r}",
                f"REQUEST_TEMPLATES = {request_templates!r}",
                "",
                "jar = http.cookiejar.CookieJar()",
                "opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))",
                "",
                "def emit(event, **kwargs):",
                "    payload = {'event': event}",
                "    payload.update(kwargs)",
                "    print(json.dumps(payload, ensure_ascii=False))",
                "",
                "def abs_url(path):",
                "    return urllib.parse.urljoin(BASE_URL.rstrip('/') + '/', path.lstrip('/'))",
                "",
                "def request(method, path, data=None, extra_headers=None):",
                "    url = abs_url(path)",
                "    headers = {'User-Agent': 'pikaqiu-act-agent/0.1', 'Accept': '*/*'}",
                "    if extra_headers:",
                "        headers.update(extra_headers)",
                "    body = None",
                "    if data is not None:",
                "        body = urllib.parse.urlencode(data).encode('utf-8')",
                "        headers['Content-Type'] = 'application/x-www-form-urlencoded'",
                "    req = urllib.request.Request(url, data=body, method=method.upper(), headers=headers)",
                "    try:",
                "        with opener.open(req, timeout=10) as resp:",
                "            text = resp.read().decode('utf-8', errors='replace')",
                "            return {'ok': True, 'url': url, 'status': resp.status, 'headers': dict(resp.headers.items()), 'text': text}",
                "    except urllib.error.HTTPError as e:",
                "        text = e.read().decode('utf-8', errors='replace')",
                "        return {'ok': False, 'url': url, 'status': e.code, 'headers': dict(e.headers.items()) if e.headers else {}, 'text': text}",
                "    except Exception as e:",
                "        return {'ok': False, 'url': url, 'status': -1, 'headers': {}, 'text': str(e)}",
                "",
                "emit('login_replay_start', node_id=" + repr(node_id) + ", base_url=BASE_URL, username=USERNAME)",
                "",
                "login_pages = []",
                "for p in ['/login', '/signin', f'/password/{USERNAME}', '/password/test', '/password/']:",
                "    if p not in login_pages:",
                "        login_pages.append(p)",
                "for p in KNOWN_PATHS:",
                "    if 'login' in p or 'password' in p:",
                "        if p not in login_pages:",
                "            login_pages.append(p)",
                "for item in REQUEST_TEMPLATES:",
                "    path = str(item.get('path') or '')",
                "    if ('login' in path or 'signin' in path or 'password' in path) and path not in login_pages:",
                "        login_pages.append(path)",
                "",
                "status_2xx = 0",
                "for p in login_pages[:6]:",
                "    resp = request('GET', p)",
                "    if 200 <= resp.get('status', -1) < 400:",
                "        status_2xx += 1",
                "    emit('login_page_probe', method='GET', path=p, status=resp.get('status'), url=resp.get('url'))",
                "    print(f\"status:{resp.get('status')}\")",
                "",
                "candidate_posts = [p for p in login_pages if 'login' in p or 'signin' in p or 'password' in p]",
                "",
                "payloads = [",
                "    {'username': USERNAME, 'password': PASSWORD},",
                "    {'account': USERNAME, 'password': PASSWORD},",
                "    {'email': USERNAME, 'password': PASSWORD},",
                "]",
                "",
                "for path in candidate_posts[:6]:",
                "    for payload in payloads:",
                "        resp = request('POST', path, data=payload)",
                "        if 200 <= resp.get('status', -1) < 400:",
                "            status_2xx += 1",
                "        emit('login_replay', method='POST', path=path, payload_keys=sorted(payload.keys()), status=resp.get('status'), url=resp.get('url'))",
                "        print(f\"status:{resp.get('status')}\")",
                "",
                "emit('summary', status_200_count=status_2xx, login_target_count=len(candidate_posts), tested_count=len(candidate_posts) * len(payloads))",
            ]
        )
        return ActCommand(tool_name="python", command=command)

    def _build_post_login_recon_command(
        self,
        *,
        node_id: str,
        title: str,
        node_description: str,
        node_notes: list[str],
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
    ) -> ActCommand:
        runtime_texts = self._filter_runtime_texts([title, node_description, *node_notes])
        base_url = self._resolve_base_url(known_targets, runtime_texts)
        request_templates = self._resolve_request_templates(known_targets, state_table_snapshot)
        known_paths = list(dict.fromkeys(known_targets.get("paths") or []))

        command = "\n".join(
            [
                "import json",
                "import re",
                "import urllib.error",
                "import urllib.parse",
                "import urllib.request",
                "",
                f"BASE_URL = {base_url!r}",
                f"KNOWN_PATHS = {known_paths!r}",
                f"REQUEST_TEMPLATES = {request_templates!r}",
                "",
                "def emit(event, **kwargs):",
                "    payload = {'event': event}",
                "    payload.update(kwargs)",
                "    print(json.dumps(payload, ensure_ascii=False))",
                "",
                "def abs_url(path):",
                "    return urllib.parse.urljoin(BASE_URL.rstrip('/') + '/', path.lstrip('/'))",
                "",
                "def request(method, path):",
                "    url = abs_url(path)",
                "    req = urllib.request.Request(url, method=method.upper(), headers={'User-Agent': 'pikaqiu-act-agent/0.1'})",
                "    try:",
                "        with urllib.request.urlopen(req, timeout=10) as resp:",
                "            text = resp.read().decode('utf-8', errors='replace')",
                "            return {'status': resp.status, 'url': url, 'text': text}",
                "    except urllib.error.HTTPError as e:",
                "        text = e.read().decode('utf-8', errors='replace')",
                "        return {'status': e.code, 'url': url, 'text': text}",
                "    except Exception as e:",
                "        return {'status': -1, 'url': url, 'text': str(e)}",
                "",
                "candidates = ['/', '/dashboard', '/profile', '/orders', '/admin']",
                "for p in KNOWN_PATHS:",
                "    if p not in candidates:",
                "        candidates.append(p)",
                "for item in REQUEST_TEMPLATES:",
                "    path = str(item.get('path') or '')",
                "    if path and path not in candidates:",
                "        candidates.append(path)",
                "",
                "discovered = []",
                "status_200_count = 0",
                "for path in candidates[:20]:",
                "    if '{' in path and '}' in path:",
                "        continue",
                "    resp = request('GET', path)",
                "    status = int(resp.get('status', -1))",
                "    if 200 <= status < 400:",
                "        status_200_count += 1",
                "    emit('post_login_recon', method='GET', path=path, status=status, url=resp.get('url'))",
                "    print(f'status:{status}')",
                "    body = resp.get('text') or ''",
                "    for endpoint in re.findall(r'(/api/[A-Za-z0-9._~!$&()*+,;=:@%/-]{2,})', body):",
                "        if endpoint not in discovered:",
                "            discovered.append(endpoint)",
                "            emit('discovered_endpoint', path=endpoint)",
                "",
                "emit('summary', status_200_count=status_200_count, discovered_api_count=len(discovered), tested_count=min(len(candidates), 20))",
            ]
        )
        return ActCommand(tool_name="python", command=command)

    def _build_object_access_probe_command(
        self,
        *,
        node_id: str,
        title: str,
        node_description: str,
        node_notes: list[str],
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
    ) -> ActCommand:
        runtime_texts = self._filter_runtime_texts([title, node_description, *node_notes])
        base_url = self._resolve_base_url(known_targets, runtime_texts)
        username, password = self._resolve_credentials(state_table_snapshot)
        request_templates = self._resolve_request_templates(known_targets, state_table_snapshot)
        object_values = self._resolve_object_values(runtime_texts, state_table_snapshot)

        command = "\n".join(
            [
                "import json",
                "import urllib.error",
                "import urllib.parse",
                "import urllib.request",
                "import http.cookiejar",
                "",
                f"BASE_URL = {base_url!r}",
                f"USERNAME = {username!r}",
                f"PASSWORD = {password!r}",
                f"REQUEST_TEMPLATES = {request_templates!r}",
                f"OBJECT_VALUES = {object_values!r}",
                "",
                "jar = http.cookiejar.CookieJar()",
                "opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))",
                "",
                "def emit(event, **kwargs):",
                "    payload = {'event': event}",
                "    payload.update(kwargs)",
                "    print(json.dumps(payload, ensure_ascii=False))",
                "",
                "def abs_url(path):",
                "    return urllib.parse.urljoin(BASE_URL.rstrip('/') + '/', path.lstrip('/'))",
                "",
                "def request(method, path, data=None):",
                "    url = abs_url(path)",
                "    headers = {'User-Agent': 'pikaqiu-act-agent/0.1', 'Accept': '*/*'}",
                "    body = None",
                "    if data is not None:",
                "        body = urllib.parse.urlencode(data).encode('utf-8')",
                "        headers['Content-Type'] = 'application/x-www-form-urlencoded'",
                "    req = urllib.request.Request(url, data=body, method=method.upper(), headers=headers)",
                "    try:",
                "        with opener.open(req, timeout=10) as resp:",
                "            text = resp.read().decode('utf-8', errors='replace')",
                "            return {'status': resp.status, 'url': url, 'text': text}",
                "    except urllib.error.HTTPError as e:",
                "        text = e.read().decode('utf-8', errors='replace')",
                "        return {'status': e.code, 'url': url, 'text': text}",
                "    except Exception as e:",
                "        return {'status': -1, 'url': url, 'text': str(e)}",
                "",
                "def same_class(a, b):",
                "    if not a or not b:",
                "        return False",
                "    if a.isdigit() and b.isdigit():",
                "        return True",
                "    return a[0].isalpha() == b[0].isalpha()",
                "",
                "def build_mutations(values):",
                "    mutations = []",
                "    for value in values:",
                "        value = str(value)",
                "        mutations.append({'kind': 'original', 'value': value, 'base': value})",
                "        if value.isdigit():",
                "            number = int(value)",
                "            if number > 1:",
                "                mutations.append({'kind': 'neighbor', 'value': str(number - 1), 'base': value})",
                "            mutations.append({'kind': 'neighbor', 'value': str(number + 1), 'base': value})",
                "    for base in values:",
                "        for other in values:",
                "            if str(base) == str(other):",
                "                continue",
                "            if same_class(str(base), str(other)):",
                "                mutations.append({'kind': 'same_class', 'value': str(other), 'base': str(base)})",
                "                break",
                "    uniq = []",
                "    seen = set()",
                "    for item in mutations:",
                "        key = (item['kind'], item['value'], item['base'])",
                "        if key in seen:",
                "            continue",
                "        seen.add(key)",
                "        uniq.append(item)",
                "    return uniq",
                "",
                "def apply_template(path, value):",
                "    result = str(path)",
                "    for key in ['id', 'order_id', 'user_id', 'tenant_id', 'object_id', 'resource_id']:",
                "        result = result.replace('{' + key + '}', str(value))",
                "    if '{' in result and '}' in result:",
                "        return ''",
                "    if '?id=' in result:",
                "        prefix, _, query = result.partition('?')",
                "        params = urllib.parse.parse_qsl(query, keep_blank_values=True)",
                "        updated = []",
                "        replaced = False",
                "        for key, existing in params:",
                "            if key.lower().endswith('id') and not replaced:",
                "                updated.append((key, str(value)))",
                "                replaced = True",
                "            else:",
                "                updated.append((key, existing))",
                "        result = prefix + '?' + urllib.parse.urlencode(updated)",
                "    return result",
                "",
                "print('[ACT] access_control probe started')",
                "emit('object_probe_start', node_id=" + repr(node_id) + ", base_url=BASE_URL, template_count=len(REQUEST_TEMPLATES), object_seed_count=len(OBJECT_VALUES))",
                "",
                "login_paths = ['/login', '/signin']",
                "for item in REQUEST_TEMPLATES:",
                "    p = str(item.get('path') or '')",
                "    if ('login' in p or 'signin' in p or 'password' in p) and p not in login_paths:",
                "        login_paths.append(p)",
                "for path in login_paths[:4]:",
                "    resp = request('POST', path, data={'username': USERNAME, 'password': PASSWORD})",
                "    emit('login_try', path=path, status=resp.get('status'))",
                "    print(f\"status:{resp.get('status')}\")",
                "",
                "templates = []",
                "for item in REQUEST_TEMPLATES:",
                "    method = str(item.get('method') or 'GET').upper()",
                "    path = str(item.get('path') or '')",
                "    if not path:",
                "        continue",
                "    if path.startswith('http://') or path.startswith('https://'):",
                "        parsed = urllib.parse.urlparse(path)",
                "        path = parsed.path + (('?' + parsed.query) if parsed.query else '')",
                "    templates.append({'method': method, 'path': path})",
                "if not templates:",
                "    templates = [",
                "        {'method': 'GET', 'path': '/order/{id}'},",
                "        {'method': 'GET', 'path': '/orders/{id}'},",
                "        {'method': 'GET', 'path': '/receipt?id={id}'},",
                "    ]",
                "",
                "seed_values = [str(v) for v in OBJECT_VALUES if str(v).strip()]",
                "if not seed_values:",
                "    seed_values = ['1001', '1002']",
                "mutations = build_mutations(seed_values)",
                "",
                "results = []",
                "for tpl in templates[:12]:",
                "    for item in mutations[:60]:",
                "        path = apply_template(tpl['path'], item['value'])",
                "        if not path:",
                "            continue",
                "        resp = request(tpl['method'], path)",
                "        status = int(resp.get('status', -1))",
                "        record = {",
                "            'mutation_type': item['kind'],",
                "            'base_value': item['base'],",
                "            'candidate_value': item['value'],",
                "            'method': tpl['method'],",
                "            'path': path,",
                "            'status': status,",
                "            'body_length': len(resp.get('text') or ''),",
                "        }",
                "        emit('object_probe', **record)",
                "        print(f'status:{status}')",
                "        results.append(record)",
                "",
                "        if 500 <= status < 600:",
                "            for retry_index in [1, 2]:",
                "                retry_resp = request(tpl['method'], path)",
                "                retry_status = int(retry_resp.get('status', -1))",
                "                emit(",
                "                    'anomaly_retry',",
                "                    mutation_type='retry_5xx',",
                "                    retry_index=retry_index,",
                "                    method=tpl['method'],",
                "                    path=path,",
                "                    status=retry_status,",
                "                    base_value=item['base'],",
                "                    candidate_value=item['value'],",
                "                )",
                "                print(f'status:{retry_status}')",
                "                results.append({'event': 'anomaly_retry', 'status': retry_status})",
                "",
                "ok_200 = [item for item in results if int(item.get('status', -1)) == 200]",
                "err_500 = [item for item in results if int(item.get('status', -1)) == 500]",
                "emit('summary', tested_count=len(results), status_200_count=len(ok_200), status_500_count=len(err_500), sample_500=err_500[:10])",
            ]
        )
        return ActCommand(tool_name="python", command=command)

    def _resolve_request_templates(
        self,
        known_targets: dict[str, list[str]],
        state_table_snapshot: dict[str, object],
    ) -> list[dict[str, str]]:
        templates: list[dict[str, str]] = []
        for item in state_table_snapshot.get("request_templates") or []:
            if not isinstance(item, dict):
                continue
            method = str(item.get("method") or "GET").upper()
            path = str(item.get("path") or item.get("url") or "").strip()
            if path:
                templates.append({"method": method, "path": path})

        for path in known_targets.get("paths") or []:
            if path:
                templates.append({"method": "GET", "path": path})

        if not templates:
            templates.extend(
                [
                    {"method": "GET", "path": "/order/{id}"},
                    {"method": "GET", "path": "/orders/{id}"},
                    {"method": "GET", "path": "/receipt?id={id}"},
                ]
            )

        deduped: list[dict[str, str]] = []
        seen: set[str] = set()
        for item in templates:
            method = str(item.get("method") or "GET").upper()
            path = str(item.get("path") or "").strip()
            if not path:
                continue
            key = f"{method} {path}"
            if key in seen:
                continue
            seen.add(key)
            deduped.append({"method": method, "path": path})
        return deduped[:30]

    def _resolve_object_values(self, runtime_texts: list[str], state_table_snapshot: dict[str, object]) -> list[str]:
        values: list[str] = []

        def add_value(value: str) -> None:
            normalized = (value or "").strip()
            if not normalized:
                return
            if normalized not in values:
                values.append(normalized)

        for item in state_table_snapshot.get("object_inventory") or []:
            if isinstance(item, dict):
                for field_value in item.values():
                    add_value(str(field_value))
                continue
            text = str(item)
            match = re.search(r"([A-Za-z0-9_-]{2,80})$", text)
            if match:
                add_value(match.group(1))

        for text in runtime_texts:
            for token in re.findall(r"(?<!\d)(\d{3,12})(?!\d)", text):
                add_value(token)

        for token in self._resolve_order_ids(runtime_texts):
            add_value(token)

        user_id = self._resolve_user_id(runtime_texts)
        if user_id:
            add_value(user_id)

        return values[:40]

    def _resolve_base_url(self, known_targets: dict[str, list[str]], texts: list[str]) -> str:
        for url in known_targets.get("urls") or []:
            parsed = urlparse(url)
            if parsed.scheme and parsed.netloc:
                return f"{parsed.scheme}://{parsed.netloc}"

        merged = "\n".join(texts)
        match = re.search(URL_CANDIDATE_PATTERN, merged, flags=re.IGNORECASE)
        if match:
            parsed = urlparse(match.group(0).rstrip("，。！？；,:;)"))
            if parsed.scheme and parsed.netloc:
                return f"{parsed.scheme}://{parsed.netloc}"

        host_match = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3}:\d{2,5})\b", merged)
        if host_match:
            return f"http://{host_match.group(1)}"

        return "http://127.0.0.1"

    def _resolve_credentials(self, state_table_snapshot: dict[str, object]) -> tuple[str, str]:
        identities = state_table_snapshot.get("identities") or []
        for item in identities:
            if not isinstance(item, dict):
                continue
            content = str(item.get("content") or "").strip()
            match = re.search(r"([A-Za-z0-9_.@-]{2,64})\s*[:/|]\s*([^\s]{2,128})", content)
            if match:
                return match.group(1), match.group(2)
        return "test", "test"

    def _resolve_user_id(self, texts: list[str]) -> str:
        merged = "\n".join(texts)
        match = re.search(r"user_id\s*[:=]\s*(\d{2,12})", merged, flags=re.IGNORECASE)
        if match:
            return match.group(1)
        return ""

    def _resolve_order_ids(self, texts: list[str]) -> list[str]:
        merged = "\n".join(texts)
        values = []
        for item in re.findall(r"(?<!\d)(\d{5,8})(?!\d)", merged):
            if item not in values:
                values.append(item)
        return values[:40]

    def _should_use_login_replay_fallback(
        self,
        *,
        title: str,
        node_description: str,
        node_notes: list[str],
    ) -> bool:
        merged = "\n".join([title, node_description, *node_notes]).lower()
        return any(
            token in merged
            for token in (
                "登录回放",
                "login replay",
                "replay login",
                "会话回放",
            )
        )

    def _filter_runtime_texts(self, texts: list[str]) -> list[str]:
        filtered: list[str] = []
        for text in texts:
            if not text:
                continue
            if self._is_hint_or_example_text(text):
                continue
            filtered.append(text)
        return filtered

    def _is_hint_or_example_text(self, text: str) -> bool:
        normalized = " ".join((text or "").split())
        if not normalized:
            return False
        if any(normalized.startswith(prefix) for prefix in HINT_PREFIXES):
            return True
        return EXAMPLE_HINT_PATTERN.search(normalized) is not None

    def _has_reusable_state(self, state_table_snapshot: dict[str, object]) -> bool:
        for key in ("identities", "key_entrypoints", "session_materials", "reusable_artifacts"):
            if state_table_snapshot.get(key):
                return True
        return False
