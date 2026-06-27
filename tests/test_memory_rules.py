from pikaqiu_agent.memory import normalize_memory_enhanced
from pikaqiu_agent.memory_rules import normalize_dead_end


def test_normalize_dead_end_keeps_natural_language_but_adds_detail() -> None:
    item = normalize_dead_end("directory brute force timed out")

    assert "失败路线卡点待补全" in item
    assert "入口是否确认" in item
    assert "payload 是否执行" in item
    assert "flag 路径是否定位" in item
    assert "hypothesis=" not in item


def test_normalize_dead_end_preserves_specific_natural_language() -> None:
    detail = (
        "LFI 链卡在 flag 路径定位：入口 /read?file= 已确认可读 /etc/passwd，"
        "但尚未读到 webroot 或应用源码，payload 有回显，下一步需要读取 mountinfo。"
    )

    assert normalize_dead_end(detail) == detail


def test_memory_normalization_keeps_dead_ends_readable() -> None:
    memory = normalize_memory_enhanced(
        {
            "summary": "x",
            "findings": [],
            "leads": [],
            "dead_ends": ["ffuf common.txt timed out"],
            "credentials": [],
            "topology": [],
        },
        {},
    )

    assert len(memory["dead_ends"]) == 1
    assert "失败路线卡点待补全" in memory["dead_ends"][0]
    assert "hypothesis=" not in memory["dead_ends"][0]
