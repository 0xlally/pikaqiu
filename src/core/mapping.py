from __future__ import annotations

import json
from pathlib import Path
import re

from core.models import FeaturePoint, TestFamilyMappingConfig, TestFamilyRecommendation


class TestFamilyMapper:
    """基于配置的功能点到测试家族映射器。"""

    __test__ = False

    def __init__(self, config: TestFamilyMappingConfig) -> None:
        self.config = config
        self.family_by_id = {family.id: family for family in config.families}
        self.family_order = {family.id: index for index, family in enumerate(config.families)}

    @classmethod
    def from_file(cls, path: str | Path) -> "TestFamilyMapper":
        """从 JSON 文件加载映射配置。"""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(TestFamilyMappingConfig.model_validate(data))

    def recommend(self, feature: FeaturePoint) -> list[TestFamilyRecommendation]:
        """用轻量规则给功能点排序推荐测试家族。"""
        text_blob = " ".join(
            [
                feature.name,
                feature.description,
                " ".join(feature.entry_points),
                " ".join(feature.roles),
                " ".join(feature.objects),
                " ".join(feature.flow_steps),
                " ".join(feature.key_parameters),
            ]
        ).lower()

        scored: dict[str, dict[str, object]] = {}
        for rule in self.config.rules:
            matched_terms = sorted(
                {
                    *self._match_terms(rule.when_keywords, text_blob),
                    *self._match_terms(rule.when_roles, text_blob),
                    *self._match_terms(rule.when_objects, text_blob),
                    *self._match_terms(rule.when_flows, text_blob),
                    *self._match_terms(rule.when_parameters, text_blob),
                }
            )
            if not matched_terms:
                continue

            for family_id in rule.test_family_ids:
                entry = scored.setdefault(
                    family_id,
                    {
                        "score": 0,
                        "matched_terms": set(),
                        "matched_rule_ids": set(),
                    },
                )
                entry["score"] = int(entry["score"]) + len(matched_terms)
                entry["matched_terms"].update(matched_terms)
                entry["matched_rule_ids"].add(rule.id)

        recommendations: list[TestFamilyRecommendation] = []
        for family_id, entry in scored.items():
            family = self.family_by_id[family_id]
            recommendations.append(
                TestFamilyRecommendation(
                    family=family,
                    score=int(entry["score"]),
                    matched_terms=sorted(entry["matched_terms"]),
                    matched_rule_ids=sorted(entry["matched_rule_ids"]),
                )
            )

        recommendations.sort(
            key=lambda item: (-item.score, self.family_order[item.family.id], item.family.name.lower())
        )
        return recommendations

    def _match_terms(self, terms: list[str], text_blob: str) -> list[str]:
        return [term for term in terms if self._contains_term(text_blob, term)]

    def _contains_term(self, text: str, term: str) -> bool:
        """英文词使用词边界，中文直接使用子串匹配。"""
        if re.search(r"[A-Za-z0-9_]", term):
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(term.lower())}(?![A-Za-z0-9_])"
            return re.search(pattern, text) is not None
        return term.lower() in text
