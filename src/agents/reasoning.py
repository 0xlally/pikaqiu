from __future__ import annotations

from core.mapping import TestFamilyMapper
from core.models import (
    AgentRuntimeRequest,
    FeaturePoint,
    NodeType,
    ParsedActResult,
    ReasoningPlan,
    StateTable,
    TaskNode,
)
from core.state_table import StateTableStore
from core.task_tree import TaskTree
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
你是SRC测试系统中的全局 reasoning agent。

你的职责：
1. 维护长会话上下文、任务树和全局决策。
2. 只从 parsing agent 的结构化结果中识别功能点。
3. 将功能点映射到测试家族。
4. 决定是否创建 info node 和 test node。
5. 任何新节点都必须符合任务树字段规范。

节点定义：
1. info node 是信息收集任务，只负责发现页面、接口、字段、参数、对象、流程、角色、上传点、回显点、回调点等事实。
2. info node 不负责漏洞结论，不负责测试家族判断，不直接承载攻击步骤。
3. test node 是围绕一个功能点或测试家族展开的测试任务，用于后续覆盖验证。
4. test node 必须明确关联 related_feature_id；已经命中测试家族时，必须写入 related_test_family。

任务树字段规范：
- id
- title
- node_type，值只能是 info 或 test
- status，值只能是 todo、doing、done
- parent_id
- source
- related_feature_id
- related_test_family
- notes
- evidence_refs

输出要求：
1. 你生成或修改的节点必须遵守上面的字段规范。
2. 创建 info node 时，node_type 必须是 info，status 必须是 todo，related_test_family 为空。
3. 创建 test node 时，node_type 必须是 test，status 必须是 todo，related_feature_id 必填，related_test_family 按命中的家族填写。
4. notes 只写简洁的决策理由、命中原因、待验证要点，不写冗长原文。
5. evidence_refs 只保存证据引用 id，不内嵌原始证据全文。
6. 信息不足时先补 info node，不要强行创建 test node。

你不能做的事：
1. 不能直接读取 act agent 的原始输出。
2. 不能把证据全文写进结论。
3. 不能混淆事实提取和漏洞判断。
4. 不能把测试家族判断写到 info node 的职责说明里。

决策顺序：
1. 先读 parsing agent 的结构化结果。
2. 再识别功能点。
3. 再映射测试家族。
4. 最后扩展任务树。
""".strip()


class ReasoningAgent:
    """负责全局规划、任务树扩展和结构化事实吸收的 reasoning agent。"""

    def __init__(
        self,
        runtime: AgentRuntime,
        mapper: TestFamilyMapper,
        feature_engine: FeatureReasoningEngine | None = None,
    ) -> None:
        self.runtime = runtime
        self.mapper = mapper
        self.feature_engine = feature_engine

    def plan_feature(self, feature: FeaturePoint, task_tree: TaskTree) -> ReasoningPlan:
        """根据功能点创建一个 info node 和一组 test node。"""
        trace = self.runtime.run(
            AgentRuntimeRequest(
                agent_name="reasoning",
                system_prompt=REASONING_SYSTEM_PROMPT,
                user_prompt=f"请围绕功能点规划测试覆盖：{feature.description}",
                context={
                    "feature_point_id": feature.id,
                    "task_tree_node_fields": TASK_TREE_NODE_FIELDS,
                    "info_node_definition": "只做信息收集，不做漏洞结论和测试家族判断。",
                    "test_node_definition": "围绕功能点和测试家族展开验证，必须写 related_feature_id 和 related_test_family。",
                },
            )
        )

        info_node = task_tree.add_node(
            TaskNode(
                kind=NodeType.INFO,
                title=f"功能点：{feature.name}",
                description=feature.description,
                feature_point_id=feature.id,
                source="reasoning",
                notes=[trace.content] if trace.content else [],
            )
        )

        recommendations = self.mapper.recommend(feature)
        test_nodes: list[TaskNode] = []
        for item in recommendations:
            matched = ", ".join(item.matched_terms[:6]) or "无直接命中词"
            node = TaskNode(
                kind=NodeType.TEST,
                title=f"测试 {item.family.name}",
                description=f"围绕功能点“{feature.name}”覆盖 {item.family.description}。",
                parent_id=info_node.id,
                feature_point_id=feature.id,
                test_family_id=item.family.id,
                source="reasoning",
                notes=[f"命中词：{matched}"],
                metadata={
                    "matched_terms": matched,
                    "matched_rule_ids": item.matched_rule_ids,
                },
            )
            task_tree.add_node(node)
            test_nodes.append(node)

        return ReasoningPlan(
            feature_point=feature,
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
    ) -> StateTable:
        """reasoning agent 只吸收 parsing agent 压缩后的结果。"""
        self.runtime.run(
            AgentRuntimeRequest(
                agent_name="reasoning",
                system_prompt=REASONING_SYSTEM_PROMPT,
                user_prompt=f"请吸收节点 {parsed_result.node_id} 的 parsing 结果并更新全局计划。",
                context={
                    "node_id": parsed_result.node_id,
                    "summary": parsed_result.summary,
                    "task_tree_node_fields": TASK_TREE_NODE_FIELDS,
                },
            )
        )
        task_tree.apply_parsed_result(parsed_result)
        return state_store.apply_delta(parsed_result.state_delta)

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
