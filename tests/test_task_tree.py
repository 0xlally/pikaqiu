from pathlib import Path

from core.models import ConclusionRecord, EvidenceRecord, NodeStatus, NodeType, ParsedActResult, TaskNode
from core.task_tree import TaskTree


def test_task_tree_core_ops_and_json_persistence(tmp_path: Path) -> None:
    tree = TaskTree()
    feature = tree.create_node(
        title="Login feature",
        node_type=NodeType.INFO,
        source="reasoning",
        related_feature_id="feat-login",
        notes=["entry: /api/login"],
    )
    child = tree.add_child_node(
        parent_id=feature.id,
        title="Collect login parameters",
        node_type=NodeType.INFO,
        source="reasoning",
        related_feature_id="feat-login",
    )
    test_nodes = tree.create_test_nodes_from_feature(
        related_feature_id="feat-login",
        test_families=["auth_bypass", "session_management"],
        parent_id=feature.id,
        source="reasoning",
    )

    tree.update_status(test_nodes[0].id, NodeStatus.DOING)
    pending_test_nodes = tree.get_pending_nodes(NodeType.TEST)
    saved_path = tree.save_json(tmp_path / "task_tree.json")
    loaded_tree = TaskTree.load_json(saved_path)
    markdown = loaded_tree.to_markdown()

    assert child.id in feature.child_ids
    assert len(test_nodes) == 2
    assert pending_test_nodes[0].status == NodeStatus.DOING
    assert saved_path.exists()
    assert "测试 auth_bypass" in markdown
    assert loaded_tree.get_node(test_nodes[1].id).related_test_family == "session_management"


def test_task_tree_keeps_legacy_tasknode_and_parsed_result_compatible() -> None:
    tree = TaskTree()
    parent = tree.add_node(TaskNode(kind=NodeType.INFO, title="Feature", description="Feature root"))
    child = tree.add_node(
        TaskNode(
            kind=NodeType.TEST,
            title="Test Access Control",
            description="Check access control.",
            parent_id=parent.id,
            test_family_id="access_control",
        )
    )

    evidence = EvidenceRecord(source="act", content="simulated")
    conclusion = ConclusionRecord(title="done", summary="done", evidence_ids=[evidence.id], source_node_id=child.id)
    parsed = ParsedActResult(
        node_id=child.id,
        summary="done",
        evidence=[evidence],
        conclusions=[conclusion],
        next_status=NodeStatus.DONE,
    )
    tree.apply_parsed_result(parsed)

    assert child.id in parent.child_ids
    assert evidence.id in tree.get_node(child.id).evidence_refs
    assert tree.get_node(child.id).status == NodeStatus.DONE
    assert "done" in tree.get_node(child.id).notes
