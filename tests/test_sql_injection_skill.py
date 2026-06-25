from __future__ import annotations

from pathlib import Path

from pikaqiu_agent.skill_loader import SkillLoader


def test_sql_injection_skill_main_file_stays_minimal_and_reference_backed() -> None:
    root = Path(__file__).resolve().parents[1]
    loader = SkillLoader(root, "skills")
    stats = loader.refresh()

    assert stats["status"] == "ready"
    assert not stats["errors"]

    results = loader.search(
        "SQL NoSQL ORM GraphQL injection UNION blind oracle sqlmap",
        limit=5,
    )

    assert results
    assert results[0]["id"] == "sql-injection-skill"

    skill_text = (
        root / "skills" / "builtin" / "sql-injection-skill" / "SKILL.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "最小思路",
        "稳定原语",
        "references/sql-playbook.md",
        "references/nosql-graphql.md",
        "references/orm-query-dsl.md",
        "references/sqlmap-verification.md",
        "不限制具体打法",
    ):
        assert expected in skill_text

    for removed in (
        "最短闭环",
        "记录卡点",
        "每次只改变一个变量",
        "闭环验证",
    ):
        assert removed not in skill_text

    assert len(skill_text) < 1800

    for ref in (
        "references/sql-playbook.md",
        "references/nosql-graphql.md",
        "references/orm-query-dsl.md",
        "references/sqlmap-verification.md",
    ):
        text = loader.read_reference("sql-injection-skill", ref, max_chars=1000)
        assert not text.startswith("[skill_read_reference]")
        assert text.strip()


def test_sql_playbook_is_bypass_oriented() -> None:
    root = Path(__file__).resolve().parents[1]
    playbook = (
        root
        / "skills"
        / "builtin"
        / "sql-injection-skill"
        / "references"
        / "sql-playbook.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "上下文与入口",
        "DBMS 差异",
        "UNION 回显",
        "布尔 / 错误 / 时间盲注",
        "登录与返回行控制",
        "非 SELECT 利用",
        "过滤绕过",
        "空白被禁",
        "引号被禁",
        "逗号被禁",
        "UNION` / `SELECT` 被禁",
        "information_schema` 被禁",
        "常用目标数据",
    ):
        assert expected in playbook

    for removed in (
        "基线与上下文",
        "结论格式",
        "按“已证明的信号”",
        "不要喷 payload 字典",
        "每次只改变一个变量",
        "method/url:",
    ):
        assert removed not in playbook
