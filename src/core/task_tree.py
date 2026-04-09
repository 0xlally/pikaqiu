from __future__ import annotations

from pathlib import Path

from core.models import NodeStatus, NodeType, ParsedActResult, TaskNode, TaskTreeModel


class TaskTree:
    """可变任务树，支持 JSON 持久化和 markdown 导出。"""

    def __init__(self, model: TaskTreeModel | None = None) -> None:
        self.model = model or TaskTreeModel()

    def create_node(
        self,
        title: str,
        node_type: NodeType,
        source: str,
        parent_id: str | None = None,
        related_feature_id: str | None = None,
        related_test_family: str | None = None,
        notes: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        description: str = "",
        metadata: dict[str, object] | None = None,
    ) -> TaskNode:
        """按扁平参数创建并插入一个节点。"""
        node = TaskNode(
            title=title,
            node_type=node_type,
            source=source,
            parent_id=parent_id,
            related_feature_id=related_feature_id,
            related_test_family=related_test_family,
            notes=notes or [],
            evidence_refs=evidence_refs or [],
            description=description,
            metadata=metadata or {},
        )
        return self.add_node(node)

    def add_node(self, node: TaskNode) -> TaskNode:
        """插入节点并维护父子关系。"""
        if node.id in self.model.nodes:
            raise ValueError(f"重复的节点 id：{node.id}")
        self.model.nodes[node.id] = node

        if node.parent_id:
            parent = self.get_node(node.parent_id)
            if node.id not in parent.child_ids:
                parent.child_ids.append(node.id)
        elif node.id not in self.model.root_ids:
            self.model.root_ids.append(node.id)

        return node

    def add_child_node(
        self,
        parent_id: str,
        title: str,
        node_type: NodeType,
        source: str,
        related_feature_id: str | None = None,
        related_test_family: str | None = None,
        notes: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        description: str = "",
    ) -> TaskNode:
        """为指定父节点追加子节点。"""
        return self.create_node(
            title=title,
            node_type=node_type,
            source=source,
            parent_id=parent_id,
            related_feature_id=related_feature_id,
            related_test_family=related_test_family,
            notes=notes,
            evidence_refs=evidence_refs,
            description=description,
        )

    def get_node(self, node_id: str) -> TaskNode:
        """获取指定节点，不存在就抛出清晰错误。"""
        try:
            return self.model.nodes[node_id]
        except KeyError as exc:
            raise KeyError(f"未知节点 id：{node_id}") from exc

    def update_status(self, node_id: str, status: NodeStatus) -> TaskNode:
        """原地更新节点状态。"""
        node = self.get_node(node_id)
        node.status = status
        return node

    def get_pending_nodes(self, node_type: NodeType | None = None) -> list[TaskNode]:
        """返回所有未完成节点，可按类型过滤。"""
        result: list[TaskNode] = []
        for node in self.model.nodes.values():
            if node.status == NodeStatus.DONE:
                continue
            if node_type is not None and node.node_type != node_type:
                continue
            result.append(node)
        return result

    def next_todo(self, kind: NodeType | None = None) -> TaskNode | None:
        """返回优先级最高的 TODO 节点，兼容旧调用方式。"""
        candidates: list[TaskNode] = []
        for node in self.model.nodes.values():
            if node.status != NodeStatus.TODO:
                continue
            if kind is not None and node.node_type != kind:
                continue
            candidates.append(node)

        if not candidates:
            return None

        candidates.sort(key=self._node_sort_key)
        return candidates[0]

    def _node_sort_key(self, node: TaskNode) -> tuple[int, str]:
        # 越小越优先
        score = -self._priority_score(node)
        return (score, node.id)

    def _priority_score(self, node: TaskNode) -> int:
        metadata = node.metadata or {}
        explicit_score = metadata.get("priority_score")
        if isinstance(explicit_score, int):
            return explicit_score

        stage = str(metadata.get("stage") or "").strip().lower()
        stage_scores = {
            "exploit_retry": 100,
            "authenticated_object_access": 90,
            "object_access": 90,
            "object_enum": 80,
            "login_restore": 70,
            "generic_family_test": 50,
            "info_recon": 30,
        }
        if stage in stage_scores:
            return stage_scores[stage]

        source = (node.source or "").lower()
        title = (node.title or "").lower()
        if "retry" in source or "retry" in title:
            return 100
        if "登录后" in title or "post_login" in source:
            return 90
        if node.node_type == NodeType.TEST:
            return 50
        return 30

    def create_test_nodes_from_feature(
        self,
        related_feature_id: str,
        test_families: list[str],
        parent_id: str | None = None,
        source: str = "reasoning",
    ) -> list[TaskNode]:
        """根据功能点批量创建 test 子节点。"""
        created: list[TaskNode] = []
        for family in test_families:
            created.append(
                self.create_node(
                    title=f"测试 {family}",
                    node_type=NodeType.TEST,
                    source=source,
                    parent_id=parent_id,
                    related_feature_id=related_feature_id,
                    related_test_family=family,
                    notes=[f"由功能点 {related_feature_id} 自动生成"],
                )
            )
        return created

    def apply_parsed_result(self, parsed_result: ParsedActResult) -> TaskNode:
        """把 parsing 压缩结果回填到源节点。"""
        node = self.get_node(parsed_result.node_id)
        for item in parsed_result.evidence:
            if item.id not in node.evidence_refs:
                node.evidence_refs.append(item.id)
        for item in parsed_result.conclusions:
            if item.id not in node.conclusion_ids:
                node.conclusion_ids.append(item.id)
        node.status = parsed_result.next_status
        if parsed_result.summary and parsed_result.summary not in node.notes:
            node.notes.append(parsed_result.summary)
        return node

    def list_nodes(self, kind: NodeType | None = None, status: NodeStatus | None = None) -> list[TaskNode]:
        """兼容旧调用方式的查询接口。"""
        result: list[TaskNode] = []
        for node in self.model.nodes.values():
            if kind is not None and node.node_type != kind:
                continue
            if status is not None and node.status != status:
                continue
            result.append(node)
        return result

    def save_json(self, path: str | Path) -> Path:
        """把任务树序列化到 JSON 文件。"""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.model.model_dump_json(indent=2), encoding="utf-8")
        return target

    @classmethod
    def load_json(cls, path: str | Path) -> "TaskTree":
        """从 JSON 文件加载任务树。"""
        data = Path(path).read_text(encoding="utf-8")
        return cls(TaskTreeModel.model_validate_json(data))

    def to_markdown(self) -> str:
        """导出为适合其他 agent 直接读取的 markdown。"""
        lines = [
            "# 任务树",
            "",
            f"- 节点总数: {len(self.model.nodes)}",
            f"- 未完成节点数: {len(self.get_pending_nodes())}",
            "",
        ]
        for node in self.model.nodes.values():
            lines.append(f"## {node.title}")
            lines.append(f"- id: {node.id}")
            lines.append(f"- node_type: {node.node_type.value}")
            lines.append(f"- status: {node.status.value}")
            lines.append(f"- parent_id: {node.parent_id or '-'}")
            lines.append(f"- source: {node.source}")
            lines.append(f"- related_feature_id: {node.related_feature_id or '-'}")
            lines.append(f"- related_test_family: {node.related_test_family or '-'}")
            lines.append(f"- child_ids: {', '.join(node.child_ids) or '-'}")
            lines.append(f"- evidence_refs: {', '.join(node.evidence_refs) or '-'}")
            lines.append(f"- notes: {' | '.join(node.notes) or '-'}")
            if node.description:
                lines.append(f"- description: {node.description}")
            lines.append("")
        return "\n".join(lines).strip() + "\n"
