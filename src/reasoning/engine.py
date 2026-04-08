from __future__ import annotations

import json
from pathlib import Path
import re

from core.models import NodeType
from reasoning.models import (
    FeatureFamilyMapping,
    FeatureWorkItem,
    IdentifiedFeature,
    ObservationItem,
    ParsingObservation,
    ProposedTestNode,
    ReasoningFeatureDecision,
    ReasoningRuleConfig,
)


PRIMARY_FIELDS = [
    "discovered_actions",
    "discovered_flows",
    "discovered_upload_points",
    "discovered_render_points",
    "discovered_callback_points",
    "discovered_endpoints",
    "discovered_pages",
]

SECONDARY_FIELDS = [
    "discovered_endpoints",
    "discovered_pages",
    "discovered_fields",
    "discovered_objects",
    "discovered_roles",
    "discovered_upload_points",
    "discovered_render_points",
    "discovered_callback_points",
]

FALLBACK_FIELDS = [
    "discovered_objects",
    "discovered_fields",
]

TOKEN_STOPWORDS = {
    "a",
    "all",
    "and",
    "api",
    "at",
    "by",
    "for",
    "from",
    "http",
    "https",
    "in",
    "of",
    "on",
    "page",
    "the",
    "to",
    "v1",
    "v2",
    "www",
}

EXAMPLE_MATCH_WEIGHT = 3


class FeatureReasoningEngine:
    """从 parsing 事实中识别功能点并映射测试家族。"""

    __test__ = False

    def __init__(self, config: ReasoningRuleConfig) -> None:
        self.config = config
        self.family_by_id = {family.family_id: family for family in config.families}
        self.family_order = {family.family_id: index for index, family in enumerate(config.families)}

    @classmethod
    def from_file(cls, path: str | Path) -> "FeatureReasoningEngine":
        """从 JSON 文件加载规则。"""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(ReasoningRuleConfig.model_validate(data))

    def analyze(self, observation: ParsingObservation) -> ReasoningFeatureDecision:
        """执行完整的功能点识别和测试家族映射流程。"""
        work_items = self.identify_features(observation)
        identified_features: list[IdentifiedFeature] = []
        family_mapping: list[FeatureFamilyMapping] = []
        proposed_test_nodes: list[ProposedTestNode] = []

        for work_item in work_items:
            feature = self._build_feature(work_item)
            mapping = self.map_feature(feature, work_item)
            identified_features.append(feature)
            if mapping is None:
                continue
            family_mapping.append(mapping)
            proposed_test_nodes.append(self._build_test_node(feature, mapping))

        return ReasoningFeatureDecision(
            identified_features=identified_features,
            family_mapping=family_mapping,
            proposed_test_nodes=proposed_test_nodes,
        )

    def identify_features(self, observation: ParsingObservation) -> list[FeatureWorkItem]:
        """基于结构化事实构建功能点工作单元。"""
        sections = observation.sections()
        work_items: list[FeatureWorkItem] = []

        for field_name in PRIMARY_FIELDS:
            for item in sections[field_name]:
                self._merge_or_create_work_item(work_items, field_name, item)

        if not work_items:
            for field_name in FALLBACK_FIELDS:
                for item in sections[field_name]:
                    self._merge_or_create_work_item(work_items, field_name, item)

        for field_name in SECONDARY_FIELDS:
            for item in sections[field_name]:
                self._attach_secondary_fact(work_items, field_name, item)

        for note in observation.notes:
            self._attach_secondary_fact(work_items, "notes", ObservationItem(text=note))

        return work_items

    def map_feature(self, feature: IdentifiedFeature, work_item: FeatureWorkItem) -> FeatureFamilyMapping | None:
        """把单个功能点映射到一个或多个测试家族。"""
        scores: dict[str, int] = {}
        reasons: list[str] = []

        for rule in self.config.rules:
            matched_terms = self._match_rule_terms(work_item, rule.source_fields, rule.keywords, rule.synonyms)
            if not matched_terms:
                continue
            scores[rule.family_id] = scores.get(rule.family_id, 0) + rule.weight * len(matched_terms)
            reasons.append(f"{rule.family_id}: {rule.reason}；命中 {', '.join(matched_terms)}")

        for family in self.config.families:
            matched_examples = self._match_family_examples(work_item, family.typical_feature_examples)
            if not matched_examples:
                continue
            scores[family.family_id] = scores.get(family.family_id, 0) + EXAMPLE_MATCH_WEIGHT * len(matched_examples)
            reasons.append(
                f"{family.family_id}: 命中典型功能点例子；命中 {', '.join(matched_examples[:4])}"
            )

        if not scores:
            return None

        family_ids = sorted(scores, key=lambda family_id: (-scores[family_id], self.family_order[family_id]))
        primary_family_id = family_ids[0]
        confidence = self._confidence(scores[primary_family_id], len(family_ids))

        return FeatureFamilyMapping(
            feature_id=feature.feature_id,
            family_ids=family_ids,
            primary_family_id=primary_family_id,
            confidence=confidence,
            reasons=reasons,
            family_names=[self.family_by_id[family_id].family_name for family_id in family_ids],
            family_scores=scores,
        )

    def _build_feature(self, work_item: FeatureWorkItem) -> IdentifiedFeature:
        """把内部工作单元转换成公共功能点结构。"""
        texts = self._unique_list(work_item.all_texts())
        title = self._feature_title(work_item.title, texts)
        summary = "; ".join(texts[:5])
        return IdentifiedFeature(
            title=title,
            summary=summary,
            evidence_refs=work_item.all_evidence_refs(),
            facts=texts,
        )

    def _build_test_node(self, feature: IdentifiedFeature, mapping: FeatureFamilyMapping) -> ProposedTestNode:
        """把功能点决策转换成 test 节点提议。"""
        return ProposedTestNode(
            title=f"Test {feature.title}",
            node_type=NodeType.TEST,
            source_feature_id=feature.feature_id,
            family_ids=mapping.family_ids,
            primary_family_id=mapping.primary_family_id,
            rationale="; ".join(mapping.reasons[:3]),
            priority=self._priority(mapping.family_scores[mapping.primary_family_id]),
        )

    def _merge_or_create_work_item(
        self,
        work_items: list[FeatureWorkItem],
        source_field: str,
        item: ObservationItem,
    ) -> None:
        """把主事实合并到已有功能点簇，或者新建一个功能点簇。"""
        title = self._clean_title(item.text)
        tokens = self._tokens(item.text)
        same_title = [work_item for work_item in work_items if work_item.title == title]
        if same_title:
            same_title[0].add_fact(source_field, item, tokens)
            return
        if work_items:
            overlaps = [len(set(work_item.tokens) & set(tokens)) for work_item in work_items]
            best_overlap = max(overlaps)
            if best_overlap >= 1:
                best_index = overlaps.index(best_overlap)
                work_items[best_index].add_fact(source_field, item, tokens)
                return
        work_item = FeatureWorkItem(title=title, source_field=source_field)
        work_item.add_fact(source_field, item, tokens)
        work_items.append(work_item)

    def _attach_secondary_fact(
        self,
        work_items: list[FeatureWorkItem],
        source_field: str,
        item: ObservationItem,
    ) -> None:
        """把次级事实附着到最相关的功能点簇。"""
        if not work_items:
            self._merge_or_create_work_item(work_items, source_field, item)
            return

        tokens = self._tokens(item.text)
        overlaps = [len(set(work_item.tokens) & set(tokens)) for work_item in work_items]
        best_overlap = max(overlaps)
        if best_overlap == 0 and len(work_items) > 1:
            return

        best_index = overlaps.index(best_overlap)
        work_items[best_index].add_fact(source_field, item, tokens)

    def _match_rule_terms(
        self,
        work_item: FeatureWorkItem,
        source_fields: list[str],
        keywords: list[str],
        synonyms: list[str],
    ) -> list[str]:
        """返回规则命中的关键词和同义词。"""
        matched: list[str] = []
        for fact_source, fact_item in work_item.facts:
            if source_fields and fact_source not in source_fields:
                continue
            for term in keywords + synonyms:
                if term in matched:
                    continue
                if self._contains_term(fact_item.text.lower(), term):
                    matched.append(term)
        return matched

    def _match_family_examples(self, work_item: FeatureWorkItem, examples: list[str]) -> list[str]:
        """使用家族典型功能点例子做弱监督匹配。"""
        if not examples:
            return []

        matched: list[str] = []
        for _, fact_item in work_item.facts:
            text = fact_item.text.lower()
            for example in examples:
                normalized = " ".join(example.lower().split())
                if not normalized or normalized in matched:
                    continue
                if self._contains_term(text, normalized):
                    matched.append(normalized)
        return matched

    def _feature_title(self, base_title: str, texts: list[str]) -> str:
        """生成简洁的功能点标题。"""
        if texts:
            return texts[0][:80]
        return base_title[:80]

    def _clean_title(self, text: str) -> str:
        """规范化原始事实文本，用作功能点标题。"""
        cleaned = " ".join(text.strip().split())
        return cleaned[:80] or "feature"

    def _tokens(self, text: str) -> list[str]:
        """从文本中提取用于相似度比较的简单 token。"""
        tokens = re.findall(r"[A-Za-z0-9_]+", text.lower())
        result: list[str] = []
        for token in tokens:
            if token in TOKEN_STOPWORDS:
                continue
            if token not in result:
                result.append(token)
        return result

    def _contains_term(self, text: str, term: str) -> bool:
        """英文词使用词边界，中文直接使用子串匹配。"""
        lower_term = term.lower()
        if re.search(r"[A-Za-z0-9_]", lower_term):
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(lower_term)}(?![A-Za-z0-9_])"
            return re.search(pattern, text) is not None
        return lower_term in text

    def _confidence(self, primary_score: int, family_count: int) -> float:
        """把命中分数转换成简单置信度。"""
        confidence = 0.35 + min(primary_score, 8) * 0.07 + min(family_count, 3) * 0.03
        return round(min(confidence, 0.98), 2)

    def _priority(self, primary_score: int) -> int:
        """把主命中分数映射成优先级。"""
        if primary_score >= 8:
            return 1
        if primary_score >= 4:
            return 2
        return 3

    def _unique_list(self, values: list[str]) -> list[str]:
        """在保留原顺序的前提下去重。"""
        unique: list[str] = []
        for value in values:
            if value not in unique:
                unique.append(value)
        return unique


def default_reasoning_rule_path() -> Path:
    """返回默认 reasoning 规则配置路径。"""
    return Path(__file__).resolve().parents[2] / "config" / "reasoning_family_rules.json"
