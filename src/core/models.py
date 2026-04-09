from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
import re
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


def new_id() -> str:
    """生成本地状态对象使用的短 id。"""
    return uuid4().hex[:12]


def utc_now_iso() -> str:
    """返回 UTC ISO 时间戳。"""
    return datetime.now(timezone.utc).isoformat()


class StrictModel(BaseModel):
    """全项目统一的 Pydantic 基类。"""

    model_config = ConfigDict(extra="forbid")


class NodeType(str, Enum):
    INFO = "info"
    TEST = "test"


class NodeStatus(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class EvidenceRecord(StrictModel):
    """证据单独存储，永远不和结论混写。"""

    id: str = Field(default_factory=new_id)
    kind: str = "tool_output"
    source: str
    content: str
    tool_name: str | None = None
    node_id: str | None = None
    created_at: str = Field(default_factory=utc_now_iso)


class ConclusionRecord(StrictModel):
    """结论只引用证据 id，不内嵌原始证据全文。"""

    id: str = Field(default_factory=new_id)
    title: str
    summary: str
    evidence_ids: list[str] = Field(default_factory=list)
    source_node_id: str | None = None
    created_at: str = Field(default_factory=utc_now_iso)


class StateItem(StrictModel):
    """适合人和 agent 同时读写的小型上下文条目。"""

    id: str = Field(default_factory=new_id)
    title: str
    content: str
    refs: list[str] = Field(default_factory=list)
    source: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_fields(cls, data: Any) -> Any:
        """兼容旧字段名，减少其余模块改动。"""
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "content" not in normalized and "summary" in normalized:
            normalized["content"] = normalized.pop("summary")
        if "refs" not in normalized and "evidence_ids" in normalized:
            normalized["refs"] = normalized.pop("evidence_ids")
        if "source" not in normalized and "source_node_id" in normalized:
            normalized["source"] = normalized.pop("source_node_id")
        return normalized

    @property
    def summary(self) -> str:
        return self.content

    @summary.setter
    def summary(self, value: str) -> None:
        self.content = value

    @property
    def evidence_ids(self) -> list[str]:
        return self.refs

    @evidence_ids.setter
    def evidence_ids(self, value: list[str]) -> None:
        self.refs = value

    @property
    def source_node_id(self) -> str | None:
        return self.source

    @source_node_id.setter
    def source_node_id(self, value: str | None) -> None:
        self.source = value


class SessionBundle(StrictModel):
    """可复用登录态与请求材料。"""

    id: str = Field(default_factory=new_id)
    base_url: str = ""
    cookies: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)
    login_recipes: list[dict[str, Any]] = Field(default_factory=list)
    csrf_tokens: dict[str, str] = Field(default_factory=dict)
    current_identity: str | None = None
    authenticated_page_fingerprint: str | None = None
    last_successful_login_at: str = Field(default_factory=utc_now_iso)
    source_node_id: str | None = None


class RequestGraphEntry(StrictModel):
    """页面/请求图中的单条记录。"""

    id: str = Field(default_factory=new_id)
    url: str = ""
    path: str = ""
    referer: str = ""
    title: str = ""
    status_code: int = 0
    body_hash: str = ""
    links: list[str] = Field(default_factory=list)
    forms: list[dict[str, Any]] = Field(default_factory=list)
    discovered_params: dict[str, list[str]] = Field(default_factory=dict)
    discovered_object_ids: dict[str, list[str]] = Field(default_factory=dict)
    auth_wall_markers: list[str] = Field(default_factory=list)
    source_node_id: str | None = None
    created_at: str = Field(default_factory=utc_now_iso)


class ObjectInventoryEntry(StrictModel):
    """业务对象库存条目。"""

    id: str = Field(default_factory=new_id)
    object_type: str = "generic"
    values: list[str] = Field(default_factory=list)
    source_path: str = ""
    extraction_method: str = "unknown"
    confidence: float = 0.5
    last_seen_at: str = Field(default_factory=utc_now_iso)


class RetryCandidate(StrictModel):
    """可重放/重试利用候选。"""

    id: str = Field(default_factory=new_id)
    method: str = "GET"
    path: str = ""
    params_or_body: dict[str, Any] = Field(default_factory=dict)
    required_session_bundle_id: str | None = None
    retry_reason: str = "flaky"
    times_attempted: int = 0
    max_attempts: int = 3
    last_statuses: list[int] = Field(default_factory=list)
    source_node_id: str | None = None
    status: str = "pending"
    created_at: str = Field(default_factory=utc_now_iso)


class StateTable(StrictModel):
    """只保存高价值上下文的精简状态表。"""

    identities: list[StateItem] = Field(default_factory=list)
    session_materials: list[StateItem] = Field(default_factory=list)
    key_entrypoints: list[StateItem] = Field(default_factory=list)
    workflow_prerequisites: list[StateItem] = Field(default_factory=list)
    reusable_artifacts: list[StateItem] = Field(default_factory=list)
    session_risks: list[StateItem] = Field(default_factory=list)
    session_bundles: list[SessionBundle] = Field(default_factory=list)
    request_graph: list[RequestGraphEntry] = Field(default_factory=list)
    object_inventory: list[ObjectInventoryEntry] = Field(default_factory=list)
    retry_candidates: list[RetryCandidate] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_fields(cls, data: Any) -> Any:
        """兼容旧字段名，允许平滑加载历史 JSON。"""
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "identities" not in normalized and "identity_materials" in normalized:
            normalized["identities"] = normalized.pop("identity_materials")
        if "key_entrypoints" not in normalized and "key_entries" in normalized:
            normalized["key_entrypoints"] = normalized.pop("key_entries")
        if "workflow_prerequisites" not in normalized and "flow_prerequisites" in normalized:
            normalized["workflow_prerequisites"] = normalized.pop("flow_prerequisites")
        if "session_risks" not in normalized and "risk_hints" in normalized:
            normalized["session_risks"] = normalized.pop("risk_hints")
        if "retry_candidates" not in normalized and "frontier_queue" in normalized:
            normalized["retry_candidates"] = normalized.pop("frontier_queue")
        return normalized

    @property
    def identity_materials(self) -> list[StateItem]:
        return self.identities

    @identity_materials.setter
    def identity_materials(self, value: list[StateItem]) -> None:
        self.identities = value

    @property
    def key_entries(self) -> list[StateItem]:
        return self.key_entrypoints

    @key_entries.setter
    def key_entries(self, value: list[StateItem]) -> None:
        self.key_entrypoints = value

    @property
    def flow_prerequisites(self) -> list[StateItem]:
        return self.workflow_prerequisites

    @flow_prerequisites.setter
    def flow_prerequisites(self, value: list[StateItem]) -> None:
        self.workflow_prerequisites = value

    @property
    def risk_hints(self) -> list[StateItem]:
        return self.session_risks

    @risk_hints.setter
    def risk_hints(self, value: list[StateItem]) -> None:
        self.session_risks = value


class StateTableDelta(StrictModel):
    """状态表的增量更新载荷。"""

    identities: list[StateItem] = Field(default_factory=list)
    session_materials: list[StateItem] = Field(default_factory=list)
    key_entrypoints: list[StateItem] = Field(default_factory=list)
    workflow_prerequisites: list[StateItem] = Field(default_factory=list)
    reusable_artifacts: list[StateItem] = Field(default_factory=list)
    session_risks: list[StateItem] = Field(default_factory=list)
    session_bundles: list[SessionBundle] = Field(default_factory=list)
    request_graph: list[RequestGraphEntry] = Field(default_factory=list)
    object_inventory: list[ObjectInventoryEntry] = Field(default_factory=list)
    retry_candidates: list[RetryCandidate] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_fields(cls, data: Any) -> Any:
        """兼容旧字段名，保证旧写入侧不立刻失效。"""
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "identities" not in normalized and "identity_materials" in normalized:
            normalized["identities"] = normalized.pop("identity_materials")
        if "key_entrypoints" not in normalized and "key_entries" in normalized:
            normalized["key_entrypoints"] = normalized.pop("key_entries")
        if "workflow_prerequisites" not in normalized and "flow_prerequisites" in normalized:
            normalized["workflow_prerequisites"] = normalized.pop("flow_prerequisites")
        if "session_risks" not in normalized and "risk_hints" in normalized:
            normalized["session_risks"] = normalized.pop("risk_hints")
        if "retry_candidates" not in normalized and "frontier_queue" in normalized:
            normalized["retry_candidates"] = normalized.pop("frontier_queue")
        return normalized

    @property
    def identity_materials(self) -> list[StateItem]:
        return self.identities

    @identity_materials.setter
    def identity_materials(self, value: list[StateItem]) -> None:
        self.identities = value

    @property
    def key_entries(self) -> list[StateItem]:
        return self.key_entrypoints

    @key_entries.setter
    def key_entries(self, value: list[StateItem]) -> None:
        self.key_entrypoints = value

    @property
    def flow_prerequisites(self) -> list[StateItem]:
        return self.workflow_prerequisites

    @flow_prerequisites.setter
    def flow_prerequisites(self, value: list[StateItem]) -> None:
        self.workflow_prerequisites = value

    @property
    def risk_hints(self) -> list[StateItem]:
        return self.session_risks

    @risk_hints.setter
    def risk_hints(self, value: list[StateItem]) -> None:
        self.session_risks = value


class FeaturePoint(StrictModel):
    """功能点或攻击面的轻量表示。"""

    id: str = Field(default_factory=new_id)
    name: str
    description: str
    entry_points: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    objects: list[str] = Field(default_factory=list)
    flow_steps: list[str] = Field(default_factory=list)
    key_parameters: list[str] = Field(default_factory=list)

    @classmethod
    def from_description(cls, description: str) -> "FeaturePoint":
        """在没有 LLM 时，基于自由文本构造一个最小功能点。"""
        cleaned = " ".join(description.strip().split())
        sentences = [part.strip() for part in re.split(r"[!?;。！？；]", cleaned) if part.strip()]
        urls = cls._extract_urls(cleaned)

        name = sentences[0][:48] if sentences else cleaned[:48]
        if urls:
            parsed = urlparse(urls[0])
            if parsed.netloc:
                name = parsed.netloc

        role_candidates = ["admin", "administrator", "user", "guest", "manager", "管理员", "用户", "访客"]
        object_candidates = ["account", "session", "token", "order", "file", "report", "invoice", "user"]
        params = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{1,31}\b", cleaned)
        paths = re.findall(r"/[A-Za-z0-9_./-]+", cleaned)

        lower_text = cleaned.lower()
        stopwords = {
            "a",
            "an",
            "and",
            "api",
            "at",
            "based",
            "endpoint",
            "exposes",
            "for",
            "handling",
            "http",
            "https",
            "login",
            "the",
            "uses",
            "with",
        }
        excluded_params = stopwords | {item.lower() for item in role_candidates}
        roles = [item for item in role_candidates if cls._contains_term(lower_text, item)]
        objects = [item for item in object_candidates if cls._contains_term(lower_text, item)]
        key_parameters = sorted(
            {
                item
                for item in params
                if item.lower() not in excluded_params
                and not cls._contains_term(lower_text, item.lower() + " endpoint")
            }
        )

        return cls(
            name=name or "feature",
            description=cleaned,
            entry_points=urls if urls else sorted(set(paths)),
            roles=roles,
            objects=objects,
            flow_steps=sentences[:3],
            key_parameters=key_parameters[:10],
        )

    @staticmethod
    def _extract_urls(text: str) -> list[str]:
        """提取输入中的完整 URL，并去掉常见中文标点尾巴。"""
        raw_urls = re.findall(r"https?://[^\s,;，；。！？]+", text)
        urls: list[str] = []
        for value in raw_urls:
            url = value.rstrip("，。！？；,:;)")
            if url and url not in urls:
                urls.append(url)
        return urls

    @staticmethod
    def _contains_term(text: str, term: str) -> bool:
        """英文词使用词边界，中文直接使用子串匹配。"""
        if re.search(r"[A-Za-z0-9_]", term):
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(term.lower())}(?![A-Za-z0-9_])"
            return re.search(pattern, text) is not None
        return term in text


class TestFamily(StrictModel):
    """可复用的测试家族。"""

    id: str
    name: str
    description: str
    tactics: list[str] = Field(default_factory=list)


class TestFamilyRule(StrictModel):
    """功能点到测试家族映射用的配置规则。"""

    id: str
    when_keywords: list[str] = Field(default_factory=list)
    when_roles: list[str] = Field(default_factory=list)
    when_objects: list[str] = Field(default_factory=list)
    when_flows: list[str] = Field(default_factory=list)
    when_parameters: list[str] = Field(default_factory=list)
    test_family_ids: list[str]


class TestFamilyMappingConfig(StrictModel):
    """整份测试家族映射配置。"""

    families: list[TestFamily]
    rules: list[TestFamilyRule]


class TestFamilyRecommendation(StrictModel):
    """单个功能点的排序推荐结果。"""

    family: TestFamily
    score: int
    matched_terms: list[str] = Field(default_factory=list)
    matched_rule_ids: list[str] = Field(default_factory=list)


class TaskNode(StrictModel):
    """任务树节点，字段尽量扁平，方便 agent 读写。"""

    id: str = Field(default_factory=new_id)
    title: str
    node_type: NodeType
    status: NodeStatus = NodeStatus.TODO
    parent_id: str | None = None
    source: str = "manual"
    related_feature_id: str | None = None
    related_test_family: str | None = None
    notes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    child_ids: list[str] = Field(default_factory=list)
    description: str = ""
    conclusion_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_fields(cls, data: Any) -> Any:
        """兼容旧构造字段名，减少连带修改。"""
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        if "node_type" not in normalized and "kind" in normalized:
            normalized["node_type"] = normalized.pop("kind")
        if "related_feature_id" not in normalized and "feature_point_id" in normalized:
            normalized["related_feature_id"] = normalized.pop("feature_point_id")
        if "related_test_family" not in normalized and "test_family_id" in normalized:
            normalized["related_test_family"] = normalized.pop("test_family_id")
        if "evidence_refs" not in normalized and "evidence_ids" in normalized:
            normalized["evidence_refs"] = normalized.pop("evidence_ids")
        return normalized

    @property
    def kind(self) -> NodeType:
        return self.node_type

    @kind.setter
    def kind(self, value: NodeType) -> None:
        self.node_type = value

    @property
    def feature_point_id(self) -> str | None:
        return self.related_feature_id

    @feature_point_id.setter
    def feature_point_id(self, value: str | None) -> None:
        self.related_feature_id = value

    @property
    def test_family_id(self) -> str | None:
        return self.related_test_family

    @test_family_id.setter
    def test_family_id(self, value: str | None) -> None:
        self.related_test_family = value

    @property
    def evidence_ids(self) -> list[str]:
        return self.evidence_refs

    @evidence_ids.setter
    def evidence_ids(self, value: list[str]) -> None:
        self.evidence_refs = value


class TaskTreeModel(StrictModel):
    """可序列化的任务树状态。"""

    root_ids: list[str] = Field(default_factory=list)
    nodes: dict[str, TaskNode] = Field(default_factory=dict)


class AgentRuntimeRequest(StrictModel):
    """agent 运行时的统一请求。"""

    agent_name: str
    system_prompt: str
    user_prompt: str
    context: dict[str, Any] = Field(default_factory=dict)


class AgentRuntimeResponse(StrictModel):
    """agent 运行时的统一响应。"""

    agent_name: str
    content: str
    raw: dict[str, Any] = Field(default_factory=dict)


class ActCommand(StrictModel):
    """act agent 产出的单次工具调用请求。"""

    tool_name: str
    command: str


class ActResult(StrictModel):
    """act agent 的原始结果，reasoning agent 不应直接读取。"""

    node_id: str
    tool_name: str
    command: str
    exit_code: int
    raw_output: str
    agent_output: str | None = None
    started_at: str
    finished_at: str


class ParsedActResult(StrictModel):
    """parsing agent 产出的压缩结果。"""

    node_id: str
    summary: str
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    conclusions: list[ConclusionRecord] = Field(default_factory=list)
    state_delta: StateTableDelta = Field(default_factory=StateTableDelta)
    next_status: NodeStatus = NodeStatus.DONE


class ReasoningPlan(StrictModel):
    """把功能点转换成任务树工作项后的结果。"""

    feature_point: FeaturePoint
    info_node: TaskNode
    recommended_families: list[TestFamilyRecommendation]
    test_nodes: list[TaskNode]
    trace: str | None = None


class DemoRunResult(StrictModel):
    """命令行演示返回的聚合结果。"""

    feature_point: FeaturePoint
    plan: ReasoningPlan
    executed_node_id: str | None = None
    act_result: ActResult | None = None
    parsed_result: ParsedActResult | None = None
    reasoning_ingest_trace: str | None = None
    state_table: StateTable
    task_tree: TaskTreeModel
