from __future__ import annotations

from pydantic import Field

from core.models import NodeType, StrictModel, new_id


class ObservationItem(StrictModel):
    """parsing 侧的一条结构化事实。"""

    text: str
    evidence_refs: list[str] = Field(default_factory=list)
    source: str | None = None


class ParsingObservation(StrictModel):
    """parsing agent 输出给 reasoning agent 的结构化事实集合。"""

    discovered_pages: list[ObservationItem] = Field(default_factory=list)
    discovered_endpoints: list[ObservationItem] = Field(default_factory=list)
    discovered_fields: list[ObservationItem] = Field(default_factory=list)
    discovered_objects: list[ObservationItem] = Field(default_factory=list)
    discovered_actions: list[ObservationItem] = Field(default_factory=list)
    discovered_flows: list[ObservationItem] = Field(default_factory=list)
    discovered_roles: list[ObservationItem] = Field(default_factory=list)
    discovered_render_points: list[ObservationItem] = Field(default_factory=list)
    discovered_upload_points: list[ObservationItem] = Field(default_factory=list)
    discovered_callback_points: list[ObservationItem] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    def sections(self) -> dict[str, list[ObservationItem]]:
        """以扁平字典形式返回所有结构化分区。"""
        return {
            "discovered_pages": self.discovered_pages,
            "discovered_endpoints": self.discovered_endpoints,
            "discovered_fields": self.discovered_fields,
            "discovered_objects": self.discovered_objects,
            "discovered_actions": self.discovered_actions,
            "discovered_flows": self.discovered_flows,
            "discovered_roles": self.discovered_roles,
            "discovered_render_points": self.discovered_render_points,
            "discovered_upload_points": self.discovered_upload_points,
            "discovered_callback_points": self.discovered_callback_points,
        }


class IdentifiedFeature(StrictModel):
    """从结构化事实中识别出的可测试业务能力单元。"""

    feature_id: str = Field(default_factory=new_id)
    title: str
    summary: str
    evidence_refs: list[str] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)


class FeatureFamilyMapping(StrictModel):
    """单个功能点命中的测试家族映射结果。"""

    feature_id: str
    family_ids: list[str]
    primary_family_id: str
    confidence: float
    reasons: list[str] = Field(default_factory=list)
    family_names: list[str] = Field(default_factory=list)
    family_scores: dict[str, int] = Field(default_factory=dict)


class ProposedTestNode(StrictModel):
    """reasoning 侧提出的 test node 草案。"""

    title: str
    node_type: NodeType = NodeType.TEST
    source_feature_id: str
    family_ids: list[str]
    primary_family_id: str
    rationale: str
    priority: int


class ReasoningFeatureDecision(StrictModel):
    """reasoning 阶段的最终结构化决策结果。"""

    identified_features: list[IdentifiedFeature] = Field(default_factory=list)
    family_mapping: list[FeatureFamilyMapping] = Field(default_factory=list)
    proposed_test_nodes: list[ProposedTestNode] = Field(default_factory=list)


class ReasoningFamily(StrictModel):
    """固定测试家族配置。"""

    family_id: str
    family_name: str


class ReasoningFamilyRule(StrictModel):
    """单条命中规则。"""

    rule_id: str
    family_id: str
    weight: int
    keywords: list[str] = Field(default_factory=list)
    synonyms: list[str] = Field(default_factory=list)
    source_fields: list[str] = Field(default_factory=list)
    reason: str


class ReasoningRuleConfig(StrictModel):
    """整份功能点到测试家族映射规则文档。"""

    families: list[ReasoningFamily]
    rules: list[ReasoningFamilyRule]


class FeatureWorkItem(StrictModel):
    """推理引擎内部使用的功能点工作单元。"""

    title: str
    source_field: str
    facts: list[tuple[str, ObservationItem]] = Field(default_factory=list)
    tokens: list[str] = Field(default_factory=list)

    def add_fact(self, source_field: str, item: ObservationItem, tokens: list[str]) -> None:
        self.facts.append((source_field, item))
        self.tokens = sorted(set(self.tokens) | set(tokens))

    def all_texts(self) -> list[str]:
        return [item.text for _, item in self.facts]

    def all_evidence_refs(self) -> list[str]:
        refs: list[str] = []
        for _, item in self.facts:
            for ref in item.evidence_refs:
                if ref not in refs:
                    refs.append(ref)
        return refs


def make_observation_item(text: str, *evidence_refs: str, source: str | None = None) -> ObservationItem:
    """供测试和示例使用的轻量辅助函数。"""
    return ObservationItem(text=text, evidence_refs=list(evidence_refs), source=source)
