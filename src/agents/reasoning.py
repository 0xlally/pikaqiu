from __future__ import annotations

import json
import re
from typing import Any

from core.mapping import TestFamilyMapper
from core.models import (
    AgentRuntimeRequest,
    FeaturePoint,
    NodeType,
    ParsedActResult,
    ReasoningPlan,
    StateTable,
    TestFamilyRecommendation,
    TaskNode,
)
from core.state_table import StateTableStore
from core.task_tree import TaskTree
from infra.mcp import ToolRegistry
from reasoning.engine import FeatureReasoningEngine
from reasoning.models import ParsingObservation, ReasoningFeatureDecision
from runtime.base import AgentRuntime


TASK_TREE_NODE_FIELDS = [
    "id",
    "title",
    "node_type",
    "status",
    "parent_id",
    "source",
    "related_feature_id",
    "related_test_family",
    "notes",
    "evidence_refs",
]


REASONING_SYSTEM_PROMPT = """
你是 SRC 测试系统中的 reasoning agent，负责全局规划与任务树演进。

核心职责：
1. 基于功能点和现有任务树规划下一步测试。
2. 结合 parsing 输出更新状态，并补充必要的 info/test 节点。
3. 保持任务树去重，优先高价值、可执行、可验证路径。

硬性规则：
1. 先做功能点到测试家族映射，再创建 test 节点。
2. 不重复创建同一功能点 + 同一测试家族节点。
3. 信息不足时先补信息收集节点，不做武断漏洞结论。
4. 结论必须来自已有证据，不得捏造事实。
5. 当有外部提示（planning_hint）时，优先把提示转成可执行工作流节点。

输出风格：
1. 保持简洁、可追踪，便于写入节点 notes。
2. 用步骤化表达下一步计划，不输出与当前目标无关内容。
""".strip()


MAX_TASK_TREE_CONTEXT_NODES = 120

AUTH_LOGIN_FAMILY_IDS = {
    "auth_bypass",
    "auth_session_security",
    "session_management",
}

VULNERABILITY_SIGNAL_PATTERN = re.compile(
    r"bypass|idor|sqli|ssti|ssrf|xss|rce|越权|绕过|注入|漏洞|命中\s*flag|flag\{",
    flags=re.IGNORECASE,
)

MAPPING_GENERIC_TERMS = {
    "id",
    "api",
    "query",
    "parameter",
    "input",
    "admin",
    "user",
    "token",
    "status",
    "role",
    "file",
}

HINT_FAMILY_ALIASES: dict[str, list[str]] = {
    "auth_bypass": ["认证", "登录", "绕过", "auth", "login", "bypass", "captcha", "otp"],
    "session_management": ["会话", "token", "session", "refresh", "fixation", "注销"],
    "access_control": ["越权", "权限", "access control", "idor", "authorization"],
    "input_validation": ["注入", "输入", "参数", "sqli", "ssti", "ssrf", "xss"],
    "file_upload": ["上传", "附件", "file", "upload", "import", "preview"],
}

REASONING_TO_BASE_FAMILY_IDS: dict[str, list[str]] = {
    "object_access_control": ["access_control"],
    "property_access_control": ["access_control"],
    "function_access_control": ["access_control"],
    "workflow_state_logic": ["access_control"],
    "quota_abuse_logic": ["input_validation"],
    "server_input_interpretation": ["input_validation"],
    "file_content_handling": ["file_upload", "input_validation"],
    "auth_session_security": ["auth_bypass", "session_management"],
    "client_render_execution": ["input_validation", "file_upload"],
    "server_outbound_callback": ["input_validation"],
}

ENGINE_CONFIDENCE_THRESHOLD = 0.55
MAPPING_RELATIVE_SCORE_THRESHOLD = 0.45
MAX_RECOMMENDED_FAMILIES = 3

WORKFLOW_HINT_STAGE_RULES: list[dict[str, Any]] = [
    {
        "stage_id": "recon",
        "title": "Exploit Workflow：入口与资产侦察",
        "node_type": NodeType.INFO,
        "related_test_family": None,
        "description": "基于提示梳理页面、接口、对象、参数与可达路径，形成后续利用链输入。",
        "keywords": ["侦察", "枚举", "入口", "资产", "api", "endpoint", "页面", "recon", "discover"],
    },
    {
        "stage_id": "auth",
        "title": "Exploit Workflow：认证与会话突破",
        "node_type": NodeType.TEST,
        "related_test_family": "auth_bypass",
        "description": "围绕登录、验证码、OTP、Token 签发与刷新链路尝试绕过与状态篡改。",
        "keywords": ["登录", "认证", "auth", "token", "session", "captcha", "otp", "jwt", "会话"],
    },
    {
        "stage_id": "access",
        "title": "Exploit Workflow：授权边界突破",
        "node_type": NodeType.TEST,
        "related_test_family": "access_control",
        "description": "围绕对象 ID、角色与租户边界验证水平/垂直越权路径。",
        "keywords": ["越权", "权限", "idor", "authorization", "access control", "role", "tenant"],
    },
    {
        "stage_id": "input",
        "title": "Exploit Workflow：输入点利用验证",
        "node_type": NodeType.TEST,
        "related_test_family": "input_validation",
        "description": "围绕参数和请求体执行注入/解析歧义测试，验证可利用输入点。",
        "keywords": ["注入", "参数", "输入", "payload", "fuzz", "sqli", "ssti", "ssrf", "xss", "rce"],
    },
    {
        "stage_id": "file",
        "title": "Exploit Workflow：文件链路利用验证",
        "node_type": NodeType.TEST,
        "related_test_family": "file_upload",
        "description": "围绕上传、解析、预览、下载链路验证类型混淆和执行面。",
        "keywords": ["上传", "附件", "file", "upload", "import", "preview", "解析", "download"],
    },
    {
        "stage_id": "proof",
        "title": "Exploit Workflow：利用链闭环与取证",
        "node_type": NodeType.INFO,
        "related_test_family": None,
        "description": "整合命中证据、关键 payload 与复现步骤，收敛到可交付利用链。",
        "keywords": ["利用", "workflow", "exploit", "链路", "拿到flag", "flag", "proof", "复现"],
    },
]

WORKFLOW_HINT_DEFAULT_STAGE_IDS = ["recon", "input", "proof"]


class ReasoningAgent:
    """负责全局规划、任务树扩展和结构化事实吸收的 reasoning agent。"""

    def __init__(
        self,
        runtime: AgentRuntime,
        mapper: TestFamilyMapper,
        feature_engine: FeatureReasoningEngine | None = None,
        tools: ToolRegistry | None = None,
    ) -> None:
        self.runtime = runtime
        self.mapper = mapper
        self.feature_engine = feature_engine
        self.tools = tools
        self.last_ingest_trace: str | None = None

    def plan_feature(
        self,
        feature: FeaturePoint,
        task_tree: TaskTree,
        planning_hint: str | None = None,
    ) -> ReasoningPlan:
        """根据功能点规划任务；信息不足时先只创建 info node。"""
        normalized_hint = self._normalize_text(planning_hint)
        feature_for_mapping = self._feature_with_hint(feature, normalized_hint)

        should_defer_test_nodes = self._should_collect_info_first(feature, normalized_hint)
        state_table_query_result = self._query_state_table(keyword=feature.name) if should_defer_test_nodes else None

        family_catalog = [
            {
                "id": family.id,
                "name": family.name,
                "description": family.description,
            }
            for family in self.mapper.config.families
        ]
        trace = self.runtime.run(
            AgentRuntimeRequest(
                agent_name="reasoning",
                system_prompt=REASONING_SYSTEM_PROMPT,
                user_prompt=f"请围绕功能点规划测试覆盖：{feature.description}",
                context={
                    "task_tree_node_fields": TASK_TREE_NODE_FIELDS,
                    "mapping_requirement": "必须先做功能点到漏洞家族映射，再创建 test 节点。",
                    "dedupe_requirement": "创建新节点前先比对任务树，避免重复创建同功能点同测试家族节点。",
                    "family_catalog": family_catalog,
                    "info_node_definition": "只做信息收集，不做漏洞结论和测试家族判断。",
                    "test_node_definition": "围绕功能点和测试家族展开验证，必须写 related_feature_id 和 related_test_family。",
                    "task_tree_snapshot": self._build_task_tree_snapshot(task_tree, focus_feature_id=feature.id),
                    "planning_hint": normalized_hint,
                    "available_tools": ["state_table"] if state_table_query_result is not None else [],
                    "state_table_query_result": state_table_query_result,
                },
            )
        )

        info_node = self._find_existing_info_node(task_tree, feature)
        canonical_feature_id = feature.id
        if info_node is None:
            info_node = task_tree.add_node(
                TaskNode(
                    kind=NodeType.INFO,
                    title=f"功能点：{feature.name}",
                    description=feature.description,
                    related_feature_id=feature.id,
                    source="reasoning",
                    notes=[
                        *([trace.content] if trace.content else []),
                        *([f"提示：{normalized_hint}"] if normalized_hint else []),
                    ],
                )
            )
        else:
            canonical_feature_id = info_node.related_feature_id or feature.id
            info_node.related_feature_id = canonical_feature_id
            if feature.description and not info_node.description:
                info_node.description = feature.description
            if trace.content and trace.content not in info_node.notes:
                info_node.notes.append(trace.content)
            if normalized_hint:
                hint_note = f"提示：{normalized_hint}"
                if hint_note not in info_node.notes:
                    info_node.notes.append(hint_note)

        feature_for_plan = feature.model_copy(update={"id": canonical_feature_id})

        recommendations = self.mapper.recommend(feature_for_mapping)
        recommendations = self._prioritize_and_filter_recommendations(
            feature_for_mapping,
            recommendations,
            planning_hint=normalized_hint,
        )
        if should_defer_test_nodes:
            return ReasoningPlan(
                feature_point=feature_for_plan,
                info_node=info_node,
                recommended_families=[],
                test_nodes=[],
                trace=trace.content,
            )

        test_nodes: list[TaskNode] = []
        for item in recommendations:
            existing_test_node = self._find_existing_test_node(task_tree, canonical_feature_id, item.family.id)
            if existing_test_node is not None:
                test_nodes.append(existing_test_node)
                continue

            matched = ", ".join(item.matched_terms[:6]) or "无直接命中词"
            node = TaskNode(
                kind=NodeType.TEST,
                title=f"测试 {item.family.name}",
                description=f"围绕功能点“{feature.name}”覆盖 {item.family.description}。",
                parent_id=info_node.id,
                related_feature_id=canonical_feature_id,
                test_family_id=item.family.id,
                source="reasoning",
                notes=[
                    f"漏洞家族：{item.family.id}",
                    f"命中词：{matched}",
                    *([f"高优先级提示：{normalized_hint}"] if normalized_hint else []),
                ],
                metadata={
                    "matched_terms": matched,
                    "matched_rule_ids": item.matched_rule_ids,
                    "mapping_score": item.score,
                },
            )
            task_tree.add_node(node)
            test_nodes.append(node)

        return ReasoningPlan(
            feature_point=feature_for_plan,
            info_node=info_node,
            recommended_families=recommendations,
            test_nodes=test_nodes,
            trace=trace.content,
        )

    def ingest_parsed_result(
        self,
        parsed_result: ParsedActResult,
        task_tree: TaskTree,
        state_store: StateTableStore,
        planning_hint: str | None = None,
    ) -> StateTable:
        """reasoning agent 只吸收 parsing agent 压缩后的结果。"""
        normalized_hint = self._normalize_text(planning_hint)
        source_node = task_tree.get_node(parsed_result.node_id)
        updated_state = state_store.apply_delta(parsed_result.state_delta)
        needs_lookup = not parsed_result.evidence or len(parsed_result.summary.strip()) < 20
        state_table_query_result = self._query_state_table(keyword=source_node.title) if needs_lookup else None
        trace = self.runtime.run(
            AgentRuntimeRequest(
                agent_name="reasoning",
                system_prompt=REASONING_SYSTEM_PROMPT,
                user_prompt=f"请吸收节点 {parsed_result.node_id} 的 parsing 结果并更新全局计划。",
                context={
                    "node_id": parsed_result.node_id,
                    "summary": parsed_result.summary,
                    "planning_hint": normalized_hint,
                    "task_tree_node_fields": TASK_TREE_NODE_FIELDS,
                    "source_node": self._serialize_node(source_node),
                    "task_tree_snapshot": self._build_task_tree_snapshot(
                        task_tree,
                        focus_feature_id=source_node.related_feature_id,
                        focus_node_id=source_node.id,
                    ),
                    "state_table_snapshot": self._build_state_table_snapshot(updated_state),
                    "available_tools": ["state_table"] if state_table_query_result is not None else [],
                    "state_table_query_result": state_table_query_result,
                },
            )
        )
        self.last_ingest_trace = trace.content or None
        task_tree.apply_parsed_result(parsed_result)
        self._expand_test_nodes_from_parsed(parsed_result, source_node, task_tree)
        self._expand_test_nodes_from_hint(
            planning_hint=normalized_hint,
            source_node=source_node,
            task_tree=task_tree,
            parsed_result=parsed_result,
        )
        self._expand_workflow_nodes_from_hint(
            planning_hint=normalized_hint,
            source_node=source_node,
            task_tree=task_tree,
            parsed_result=parsed_result,
        )
        self._ensure_retry_frontier_test_nodes(
            source_node=source_node,
            task_tree=task_tree,
            state_table=updated_state,
        )
        self._maybe_schedule_post_login_recon(
            parsed_result=parsed_result,
            source_node=source_node,
            task_tree=task_tree,
            state_table=updated_state,
        )
        return updated_state

    def _expand_test_nodes_from_parsed(
        self,
        parsed_result: ParsedActResult,
        source_node: TaskNode,
        task_tree: TaskTree,
    ) -> None:
        feature_id = source_node.related_feature_id or self._find_related_feature_id_from_ancestors(task_tree, source_node)
        if not feature_id:
            return

        existing_family_ids = {
            node.related_test_family
            for node in task_tree.model.nodes.values()
            if node.node_type == NodeType.TEST and node.related_feature_id == feature_id and node.related_test_family
        }

        observation_text = self._build_observation_text(parsed_result)
        if not observation_text:
            return

        derived_feature = FeaturePoint.from_description(observation_text)
        recommendations = self.mapper.recommend(derived_feature)
        recommendations = self._prioritize_and_filter_recommendations(
            derived_feature,
            recommendations,
            planning_hint="",
        )

        matched_terms_by_family: dict[str, str] = {}
        candidate_family_ids = [item.family.id for item in recommendations]
        for item in recommendations:
            matched_terms_by_family[item.family.id] = ", ".join(item.matched_terms[:6]) or "无直接命中词"

        if not candidate_family_ids:
            return

        parent_id = self._find_feature_info_node_id(task_tree, feature_id) or source_node.id
        for family_id in candidate_family_ids:
            if family_id in existing_family_ids:
                continue
            family = self.mapper.family_by_id.get(family_id)
            if family is None:
                continue
            if self._find_existing_test_node(task_tree, feature_id, family_id) is not None:
                existing_family_ids.add(family_id)
                continue

            matched_terms = matched_terms_by_family.get(family_id, "来自 parsing 证据的启发式命中")
            task_tree.create_node(
                title=f"测试 {family.name}",
                node_type=NodeType.TEST,
                source="reasoning",
                parent_id=parent_id,
                related_feature_id=feature_id,
                related_test_family=family_id,
                notes=[f"漏洞家族：{family_id}", f"命中词：{matched_terms}"],
                evidence_refs=[item.id for item in parsed_result.evidence[:3]],
                description=f"依据 parsing 证据补充测试：{family.description}",
            )
            existing_family_ids.add(family_id)

    def _build_observation_text(self, parsed_result: ParsedActResult) -> str:
        parts = [parsed_result.summary]
        parts.extend(item.content for item in parsed_result.evidence[:6])
        parts.extend(item.summary for item in parsed_result.conclusions[:6])
        normalized = [" ".join(part.split()) for part in parts if part and part.strip()]
        return "\n".join(normalized)

    def _should_collect_info_first(self, feature: FeaturePoint, planning_hint: str | None = None) -> bool:
        """输入过于稀疏时，先做信息侦察，避免强行创建 test 节点。"""
        hint = self._normalize_text(planning_hint)
        if hint and self._hint_has_actionable_signal(hint):
            return False

        normalized = self._normalize_text(feature.description)
        if not normalized:
            return True

        url_only = re.fullmatch(
            r"https?://[^\s,;，；。！？]+(?:\s*[，,;；]\s*拿到flag给我)?",
            normalized,
            flags=re.IGNORECASE,
        )
        if url_only:
            return True

        stripped = re.sub(r"https?://[^\s,;，；。！？]+", " ", normalized, flags=re.IGNORECASE)
        stripped = stripped.replace("拿到flag给我", " ")
        sparse_tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]{1,}|[\u4e00-\u9fff]{2,}", stripped)

        has_actionable_signal = re.search(
            r"login|signin|auth|token|session|captcha|otp|admin|upload|download|parameter|endpoint|api/|登录|认证|会话|权限|上传|下载|参数|接口",
            normalized,
            flags=re.IGNORECASE,
        )
        return len(sparse_tokens) <= 2 and has_actionable_signal is None

    def _hint_has_actionable_signal(self, hint: str) -> bool:
        hint_tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]{1,}|[\u4e00-\u9fff]{2,}", hint)
        if not hint_tokens:
            return False
        return (
            re.search(
                r"login|signin|auth|token|session|captcha|otp|admin|upload|download|parameter|endpoint|api/|idor|sqli|ssti|ssrf|xss|rce|登录|认证|会话|权限|上传|下载|参数|接口|越权|注入|漏洞",
                hint,
                flags=re.IGNORECASE,
            )
            is not None
        )

    def _feature_with_hint(self, feature: FeaturePoint, planning_hint: str) -> FeaturePoint:
        if not planning_hint:
            return feature
        merged = f"{feature.description}\n提示：{planning_hint}".strip()
        return feature.model_copy(update={"description": merged})

    def _expand_test_nodes_from_hint(
        self,
        *,
        planning_hint: str,
        source_node: TaskNode,
        task_tree: TaskTree,
        parsed_result: ParsedActResult,
    ) -> None:
        """根据外部提示继续扩展测试节点，帮助 reasoning 在信息不足时继续规划。"""
        if not planning_hint:
            return

        feature_id = source_node.related_feature_id or self._find_related_feature_id_from_ancestors(task_tree, source_node)
        if not feature_id:
            return

        parent_id = self._find_feature_info_node_id(task_tree, feature_id) or source_node.id
        hinted_feature = FeaturePoint.from_description(planning_hint)
        recommendations = self.mapper.recommend(hinted_feature)
        recommendations = self._prioritize_and_filter_recommendations(
            hinted_feature,
            recommendations,
            planning_hint=planning_hint,
        )
        if not recommendations:
            return

        for item in recommendations:
            family_id = item.family.id
            if self._find_existing_test_node(task_tree, feature_id, family_id) is not None:
                continue

            matched = ", ".join(item.matched_terms[:6]) or "无直接命中词"
            task_tree.create_node(
                title=f"测试 {item.family.name}",
                node_type=NodeType.TEST,
                source="reasoning_hint",
                parent_id=parent_id,
                related_feature_id=feature_id,
                related_test_family=family_id,
                notes=[
                    f"漏洞家族：{family_id}",
                    f"命中词：{matched}",
                    f"来自提示：{planning_hint}",
                ],
                evidence_refs=[item.id for item in parsed_result.evidence[:3]],
                description=f"依据提示补充测试：{item.family.description}",
            )

    def _expand_workflow_nodes_from_hint(
        self,
        *,
        planning_hint: str,
        source_node: TaskNode,
        task_tree: TaskTree,
        parsed_result: ParsedActResult,
    ) -> None:
        """根据 planning_hint 直接扩展 exploit workflow 节点，而不只做家族映射。"""
        normalized_hint = self._normalize_text(planning_hint)
        if not normalized_hint:
            return

        feature_id = source_node.related_feature_id or self._find_related_feature_id_from_ancestors(task_tree, source_node)
        if not feature_id:
            return

        parent_id = self._find_feature_info_node_id(task_tree, feature_id) or source_node.id
        evidence_refs = [item.id for item in parsed_result.evidence[:3]]
        stage_specs = self._select_workflow_stage_specs(normalized_hint)

        for spec in stage_specs:
            stage_id = str(spec.get("stage_id") or "").strip()
            if not stage_id:
                continue
            if self._find_existing_workflow_hint_node(task_tree, feature_id, stage_id):
                continue

            family_id = spec.get("related_test_family")
            if spec.get("node_type") == NodeType.TEST and not family_id:
                family_id = self._infer_family_id_from_text(
                    f"{normalized_hint}\n{spec.get('title', '')}\n{spec.get('description', '')}",
                    fallback_family_id=source_node.related_test_family,
                )

            node = TaskNode(
                title=str(spec.get("title") or "Exploit Workflow：补充节点"),
                node_type=spec.get("node_type") or NodeType.INFO,
                source="reasoning_workflow_hint",
                parent_id=parent_id,
                related_feature_id=feature_id,
                related_test_family=family_id,
                notes=[
                    f"来自提示：{normalized_hint}",
                    *([f"漏洞家族：{family_id}"] if family_id else []),
                    "按 exploit workflow 推进：先验证可达性，再验证可利用性与影响。",
                ],
                evidence_refs=evidence_refs,
                description=str(spec.get("description") or ""),
                metadata={"workflow_stage_id": stage_id, "trigger": "planning_hint"},
            )
            task_tree.add_node(node)

    def _select_workflow_stage_specs(self, planning_hint: str) -> list[dict[str, Any]]:
        normalized_hint = self._normalize_text(planning_hint).lower()
        if not normalized_hint:
            return []

        selected: list[dict[str, Any]] = []
        for spec in WORKFLOW_HINT_STAGE_RULES:
            keywords = [self._normalize_text(str(item)).lower() for item in spec.get("keywords", [])]
            if any(self._contains_term(normalized_hint, keyword) for keyword in keywords if keyword):
                selected.append(spec)

        if selected:
            selected_stage_ids = {str(item.get("stage_id") or "") for item in selected}
            has_test_stage = any(item.get("node_type") == NodeType.TEST for item in selected)
            if "recon" not in selected_stage_ids:
                recon_stage = next((item for item in WORKFLOW_HINT_STAGE_RULES if item.get("stage_id") == "recon"), None)
                if recon_stage is not None:
                    selected.insert(0, recon_stage)
            if has_test_stage and "proof" not in selected_stage_ids:
                proof_stage = next((item for item in WORKFLOW_HINT_STAGE_RULES if item.get("stage_id") == "proof"), None)
                if proof_stage is not None:
                    selected.append(proof_stage)
            return selected

        if not self._hint_has_actionable_signal(normalized_hint):
            return []

        default_specs: list[dict[str, Any]] = []
        default_ids = set(WORKFLOW_HINT_DEFAULT_STAGE_IDS)
        for spec in WORKFLOW_HINT_STAGE_RULES:
            if spec.get("stage_id") in default_ids:
                default_specs.append(spec)
        return default_specs

    def _find_existing_workflow_hint_node(self, task_tree: TaskTree, feature_id: str, stage_id: str) -> TaskNode | None:
        for node in task_tree.model.nodes.values():
            if node.source != "reasoning_workflow_hint":
                continue
            if node.related_feature_id != feature_id:
                continue
            existing_stage_id = str(node.metadata.get("workflow_stage_id", "")).strip()
            if existing_stage_id == stage_id:
                return node
        return None

    def _infer_family_id_from_text(self, text: str, fallback_family_id: str | None = None) -> str | None:
        normalized = self._normalize_text(text)
        if normalized:
            inferred = self._infer_hint_family_ids(normalized)
            for family_id in inferred:
                if family_id in self.mapper.family_by_id:
                    return family_id

            derived_feature = FeaturePoint.from_description(normalized)
            recommendations = self.mapper.recommend(derived_feature)
            if recommendations:
                return recommendations[0].family.id

        if fallback_family_id and fallback_family_id in self.mapper.family_by_id:
            return fallback_family_id
        return None

    def _ensure_retry_frontier_test_nodes(
        self,
        *,
        source_node: TaskNode,
        task_tree: TaskTree,
        state_table: StateTable,
    ) -> None:
        retry_items = self._extract_frontier_retry_items(state_table)
        if not retry_items:
            return

        feature_id = source_node.related_feature_id or self._find_related_feature_id_from_ancestors(task_tree, source_node)
        if not feature_id:
            return

        parent_id = self._find_feature_info_node_id(task_tree, feature_id) or source_node.parent_id or source_node.id
        for item in retry_items:
            retry_key = self._normalize_text(str(item.get("retry_key") or "")).lower()
            family_id = item.get("family_id") or self._infer_family_id_from_text(
                f"{item.get('title', '')}\n{item.get('description', '')}",
                fallback_family_id=source_node.related_test_family,
            )
            title = str(item.get("title") or "测试 Frontier 待重试项").strip()
            description = str(item.get("description") or "来自 state_table.frontier_queue 的待重试任务").strip()

            if self._find_corresponding_frontier_test_node(
                task_tree,
                feature_id=feature_id,
                retry_key=retry_key,
                title=title,
                family_id=family_id,
            ) is not None:
                continue

            notes = [
                "来自 state_table.frontier_queue 的待重试项。",
                *([f"漏洞家族：{family_id}"] if family_id else []),
            ]
            if item.get("reason"):
                notes.append(f"待重试原因：{item['reason']}")

            task_tree.add_node(
                TaskNode(
                    title=title,
                    node_type=NodeType.TEST,
                    source="reasoning_frontier_retry",
                    parent_id=parent_id,
                    related_feature_id=feature_id,
                    related_test_family=family_id,
                    notes=notes,
                    description=description,
                    metadata={
                        "frontier_retry_key": retry_key,
                        "frontier_status": item.get("status"),
                    },
                )
            )

    def _extract_frontier_retry_items(self, state_table: StateTable) -> list[dict[str, Any]]:
        candidates = self._to_frontier_candidates(getattr(state_table, "frontier_queue", None))

        if not candidates:
            for note in reversed(state_table.notes[-20:]):
                candidates = self._parse_frontier_candidates_from_note(note)
                if candidates:
                    break

        normalized_items: list[dict[str, Any]] = []
        for index, item in enumerate(candidates):
            normalized = self._normalize_frontier_retry_item(item, index)
            if normalized is not None:
                normalized_items.append(normalized)
        return normalized_items

    def _to_frontier_candidates(self, raw_queue: Any) -> list[Any]:
        if raw_queue is None:
            return []
        if isinstance(raw_queue, list):
            return raw_queue
        if isinstance(raw_queue, tuple):
            return list(raw_queue)
        if isinstance(raw_queue, dict):
            for key in ("frontier_queue", "queue", "items", "retry_items"):
                value = raw_queue.get(key)
                if isinstance(value, list):
                    return value
            return [raw_queue]
        return []

    def _parse_frontier_candidates_from_note(self, note: str) -> list[Any]:
        text = self._normalize_text(note)
        if not text:
            return []

        if "frontier_queue=" in text:
            payload_text = text.split("frontier_queue=", 1)[1].strip()
            try:
                payload = json.loads(payload_text)
            except Exception:
                return []
            return self._to_frontier_candidates(payload)

        try:
            payload = json.loads(text)
        except Exception:
            payload = None

        if isinstance(payload, dict) and "frontier_queue" in payload:
            return self._to_frontier_candidates(payload.get("frontier_queue"))
        if isinstance(payload, list):
            return payload

        if re.search(r"待重试|retry", text, flags=re.IGNORECASE):
            return [text]
        return []

    def _normalize_frontier_retry_item(self, item: Any, index: int) -> dict[str, Any] | None:
        if isinstance(item, str):
            text = self._normalize_text(item)
            if not text:
                return None
            if re.search(r"待重试|retry|pending", text, flags=re.IGNORECASE) is None:
                return None
            return {
                "retry_key": f"frontier-{index}-{text[:48].lower()}",
                "title": f"测试待重试项 #{index + 1}",
                "description": text,
                "family_id": None,
                "reason": text,
                "status": "retry",
            }

        if not isinstance(item, dict):
            return None

        status = self._normalize_text(
            str(item.get("status") or item.get("state") or item.get("retry_status") or item.get("node_status") or "")
        ).lower()
        should_retry = bool(item.get("needs_retry") or item.get("need_retry") or item.get("retry"))
        if not should_retry and re.search(r"retry|pending|todo|待重试", status, flags=re.IGNORECASE) is None:
            retries_left = item.get("retries_left")
            try:
                retries_left_int = int(retries_left)
            except Exception:
                retries_left_int = 0
            if retries_left_int <= 0:
                return None

        title = self._normalize_text(
            str(item.get("title") or item.get("node_title") or item.get("name") or item.get("target") or item.get("endpoint") or "")
        )
        if not title:
            title = f"测试待重试项 #{index + 1}"

        description = self._normalize_text(
            str(item.get("description") or item.get("reason") or item.get("error") or item.get("command") or title)
        )
        family_id = self._normalize_text(
            str(item.get("related_test_family") or item.get("test_family_id") or item.get("family_id") or "")
        )
        if family_id and family_id not in self.mapper.family_by_id:
            family_id = ""

        retry_key = self._normalize_text(
            str(item.get("id") or item.get("retry_key") or item.get("node_id") or f"frontier-{index}-{title.lower()}")
        ).lower()

        return {
            "retry_key": retry_key,
            "title": title,
            "description": description,
            "family_id": family_id or None,
            "reason": self._normalize_text(str(item.get("reason") or item.get("error") or "")),
            "status": status or "retry",
        }

    def _find_corresponding_frontier_test_node(
        self,
        task_tree: TaskTree,
        *,
        feature_id: str,
        retry_key: str,
        title: str,
        family_id: str | None,
    ) -> TaskNode | None:
        normalized_title = self._normalize_text(title).lower()
        for node in task_tree.model.nodes.values():
            if node.node_type != NodeType.TEST:
                continue
            if node.related_feature_id != feature_id:
                continue

            node_retry_key = self._normalize_text(str(node.metadata.get("frontier_retry_key") or "")).lower()
            if retry_key and node_retry_key and node_retry_key == retry_key:
                return node

            if family_id and node.related_test_family == family_id and node.source == "reasoning_frontier_retry":
                if normalized_title and self._normalize_text(node.title).lower() == normalized_title:
                    return node

            if normalized_title and self._normalize_text(node.title).lower() == normalized_title:
                return node

        return None

    def _find_feature_info_node_id(self, task_tree: TaskTree, feature_id: str) -> str | None:
        for node in task_tree.model.nodes.values():
            if node.node_type == NodeType.INFO and node.related_feature_id == feature_id:
                return node.id
        return None

    def _find_existing_info_node(self, task_tree: TaskTree, feature: FeaturePoint) -> TaskNode | None:
        expected_title = f"功能点：{feature.name}"
        normalized_description = self._normalize_text(feature.description)

        for node in task_tree.model.nodes.values():
            if node.node_type != NodeType.INFO:
                continue
            if node.title == expected_title:
                return node
            if normalized_description and self._normalize_text(node.description) == normalized_description:
                return node
        return None

    def _find_existing_test_node(self, task_tree: TaskTree, feature_id: str, family_id: str) -> TaskNode | None:
        for node in task_tree.model.nodes.values():
            if node.node_type != NodeType.TEST:
                continue
            if node.related_feature_id != feature_id:
                continue
            if node.related_test_family != family_id:
                continue
            return node
        return None

    def _find_related_feature_id_from_ancestors(self, task_tree: TaskTree, source_node: TaskNode) -> str | None:
        current_parent_id = source_node.parent_id
        while current_parent_id:
            parent = task_tree.model.nodes.get(current_parent_id)
            if parent is None:
                return None
            if parent.related_feature_id:
                return parent.related_feature_id
            current_parent_id = parent.parent_id
        return None

    def _build_task_tree_snapshot(
        self,
        task_tree: TaskTree,
        focus_feature_id: str | None = None,
        focus_node_id: str | None = None,
    ) -> dict[str, Any]:
        nodes = list(task_tree.model.nodes.values())
        pending_nodes = [node for node in nodes if node.status.value != "done"]
        focus_nodes = [
            node
            for node in nodes
            if focus_feature_id is not None and node.related_feature_id == focus_feature_id
        ]
        if not focus_nodes and focus_node_id is not None:
            focus_nodes = [node for node in nodes if node.id == focus_node_id or node.parent_id == focus_node_id]

        existing_test_signatures = sorted(
            {
                f"{node.related_feature_id}:{node.related_test_family}"
                for node in nodes
                if node.node_type == NodeType.TEST and node.related_feature_id and node.related_test_family
            }
        )

        return {
            "summary": {
                "nodeCount": len(nodes),
                "pendingCount": len(pending_nodes),
                "infoTodoCount": len([node for node in pending_nodes if node.node_type == NodeType.INFO]),
                "testTodoCount": len([node for node in pending_nodes if node.node_type == NodeType.TEST]),
            },
            "focusFeatureId": focus_feature_id,
            "focusNodeId": focus_node_id,
            "focusNodes": [self._serialize_node(node) for node in focus_nodes[:MAX_TASK_TREE_CONTEXT_NODES]],
            "pendingNodes": [self._serialize_node(node) for node in pending_nodes[:MAX_TASK_TREE_CONTEXT_NODES]],
            "existingTestSignatures": existing_test_signatures[:MAX_TASK_TREE_CONTEXT_NODES],
        }

    def _serialize_node(self, node: TaskNode) -> dict[str, Any]:
        return {
            "id": node.id,
            "title": node.title,
            "node_type": node.node_type.value,
            "status": node.status.value,
            "parent_id": node.parent_id,
            "source": node.source,
            "related_feature_id": node.related_feature_id,
            "related_test_family": node.related_test_family,
            "child_ids": list(node.child_ids),
            "evidence_refs": list(node.evidence_refs),
            "notes": list(node.notes[-3:]),
        }

    def _normalize_text(self, text: str | None) -> str:
        if not text:
            return ""
        return " ".join(text.split())

    def _prioritize_and_filter_recommendations(
        self,
        feature: FeaturePoint,
        recommendations: list[TestFamilyRecommendation],
        *,
        planning_hint: str,
    ) -> list[TestFamilyRecommendation]:
        if not recommendations:
            return []

        hint_family_ids = self._infer_hint_family_ids(planning_hint)
        engine_family_ids = self._infer_engine_family_ids(feature, planning_hint)
        max_score = max(item.score for item in recommendations)
        score_threshold = max(2, int(max_score * MAPPING_RELATIVE_SCORE_THRESHOLD))

        ranked: list[tuple[int, TestFamilyRecommendation]] = []
        for item in recommendations:
            family_id = item.family.id
            hinted = family_id in hint_family_ids
            approved_by_engine = (not engine_family_ids) or family_id in engine_family_ids
            if not approved_by_engine and not hinted:
                continue

            if item.score < score_threshold and not hinted:
                continue

            adjusted_score = item.score
            if hinted:
                adjusted_score += max(2, max_score // 2)
            if self._is_generic_match_only(item.matched_terms):
                adjusted_score -= 1

            ranked.append((adjusted_score, item))

        if not ranked:
            if engine_family_ids:
                engine_only = [item for item in recommendations if item.family.id in engine_family_ids]
                if engine_only:
                    return engine_only[:1]
            return recommendations[:1]

        ranked.sort(key=lambda pair: (-pair[0], -pair[1].score, pair[1].family.name.lower()))
        filtered = [item for _, item in ranked]
        return filtered[:MAX_RECOMMENDED_FAMILIES]

    def _infer_hint_family_ids(self, planning_hint: str) -> set[str]:
        normalized_hint = self._normalize_text(planning_hint).lower()
        if not normalized_hint:
            return set()

        matched: set[str] = set()
        for family in self.mapper.config.families:
            terms = [family.id.lower(), family.name.lower(), *HINT_FAMILY_ALIASES.get(family.id, [])]
            for term in terms:
                normalized_term = term.lower().strip()
                if not normalized_term:
                    continue
                if self._contains_term(normalized_hint, normalized_term):
                    matched.add(family.id)
                    break
        return matched

    def _infer_engine_family_ids(self, feature: FeaturePoint, planning_hint: str) -> set[str]:
        if self.feature_engine is None:
            return set()

        observation_notes = [feature.description]
        if planning_hint:
            observation_notes.append(planning_hint)

        try:
            decision = self.feature_engine.analyze(ParsingObservation(notes=observation_notes))
        except Exception:
            return set()

        matched: set[str] = set()
        for mapping in decision.family_mapping:
            if mapping.confidence < ENGINE_CONFIDENCE_THRESHOLD:
                continue

            if not mapping.family_scores:
                matched.update(self._normalize_engine_family_ids(mapping.primary_family_id))
                continue

            primary_score = int(mapping.family_scores.get(mapping.primary_family_id, 0))
            keep_threshold = max(2, primary_score - 2)
            for family_id, score in mapping.family_scores.items():
                if int(score) >= keep_threshold:
                    matched.update(self._normalize_engine_family_ids(family_id))

        return matched

    def _normalize_engine_family_ids(self, family_id: str) -> set[str]:
        normalized = REASONING_TO_BASE_FAMILY_IDS.get(family_id, [family_id])
        return {item for item in normalized if item in self.mapper.family_by_id}

    def _is_generic_match_only(self, matched_terms: list[str]) -> bool:
        normalized = [item.strip().lower() for item in matched_terms if item and item.strip()]
        if not normalized:
            return False
        return all(item in MAPPING_GENERIC_TERMS for item in normalized)

    def _contains_term(self, text: str, term: str) -> bool:
        if re.search(r"[A-Za-z0-9_]", term):
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(term.lower())}(?![A-Za-z0-9_])"
            return re.search(pattern, text, flags=re.IGNORECASE) is not None
        return term in text

    def _build_state_table_snapshot(self, state_table: StateTable) -> dict[str, Any]:
        def serialize_items(items) -> list[dict[str, Any]]:
            return [
                {
                    "title": item.title,
                    "content": item.content,
                    "refs": item.refs[:5],
                    "source": item.source,
                }
                for item in items[:20]
            ]

        frontier_queue = self._to_frontier_candidates(getattr(state_table, "frontier_queue", None))

        return {
            "identities": serialize_items(state_table.identities),
            "key_entrypoints": serialize_items(state_table.key_entrypoints),
            "session_materials": serialize_items(state_table.session_materials),
            "reusable_artifacts": serialize_items(state_table.reusable_artifacts),
            "notes": state_table.notes[-20:],
            "frontier_queue": frontier_queue[:20],
        }

    def _maybe_schedule_post_login_recon(
        self,
        *,
        parsed_result: ParsedActResult,
        source_node: TaskNode,
        task_tree: TaskTree,
        state_table: StateTable,
    ) -> None:
        """认证测试未见漏洞且有账号时，补充登录后逐端点侦察节点。"""
        if source_node.node_type != NodeType.TEST:
            return
        if (source_node.related_test_family or "") not in AUTH_LOGIN_FAMILY_IDS:
            return
        if self._has_vulnerability_signal(parsed_result):
            return
        if not self._has_login_credentials(state_table):
            return
        if not self._has_login_entrypoint(state_table):
            return

        feature_id = source_node.related_feature_id or self._find_related_feature_id_from_ancestors(task_tree, source_node)
        if not feature_id:
            return
        if self._has_existing_post_login_recon_node(task_tree, feature_id):
            return

        parent_id = self._find_feature_info_node_id(task_tree, feature_id) or source_node.parent_id or source_node.id
        task_tree.create_node(
            title="登录后侦察：逐端点逐功能信息收集",
            node_type=NodeType.INFO,
            source="reasoning_post_login",
            parent_id=parent_id,
            related_feature_id=feature_id,
            notes=[
                "认证测试未发现明确漏洞，且状态表存在可用账号。",
                "使用账号登录后，逐个端点和功能记录页面、接口、参数、对象、流程事实。",
            ],
            evidence_refs=[item.id for item in parsed_result.evidence[:5]],
            description="登录后继续侦察，逐端点逐功能分析，补充可复用信息（页面/API/对象/流程/参数）。",
        )

    def _has_vulnerability_signal(self, parsed_result: ParsedActResult) -> bool:
        texts = [parsed_result.summary]
        texts.extend(item.summary for item in parsed_result.conclusions)
        texts.extend(item.content for item in parsed_result.evidence[:8])
        combined = "\n".join(texts)
        return bool(VULNERABILITY_SIGNAL_PATTERN.search(combined))

    def _has_login_credentials(self, state_table: StateTable) -> bool:
        for item in state_table.identities:
            content = item.content.lower()
            if ":" in item.content:
                return True
            if "username" in content and "password" in content:
                return True
        return False

    def _has_login_entrypoint(self, state_table: StateTable) -> bool:
        for item in state_table.key_entrypoints:
            content = item.content.lower()
            if any(term in content for term in ("/login", "signin", "auth", "token", "登录")):
                return True
        return False

    def _has_existing_post_login_recon_node(self, task_tree: TaskTree, feature_id: str) -> bool:
        for node in task_tree.model.nodes.values():
            if node.node_type != NodeType.INFO:
                continue
            if node.related_feature_id != feature_id:
                continue
            if node.source != "reasoning_post_login":
                continue
            return True
        return False

    def _query_state_table(self, *, keyword: str = "") -> dict[str, Any] | None:
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
        except Exception:
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

    def analyze_structured_observation(self, observation: ParsingObservation) -> ReasoningFeatureDecision:
        """从 parsing agent 的结构化事实中识别功能点并映射测试家族。"""
        if self.feature_engine is None:
            raise ValueError("未配置功能点推理引擎")

        self.runtime.run(
            AgentRuntimeRequest(
                agent_name="reasoning",
                system_prompt=REASONING_SYSTEM_PROMPT,
                user_prompt="请根据 parsing agent 的结构化事实识别功能点并映射测试家族。",
                context={
                    "observation_sections": list(observation.sections().keys()),
                    "task_tree_node_fields": TASK_TREE_NODE_FIELDS,
                },
            )
        )
        return self.feature_engine.analyze(observation)
