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
        "Focused SQL/NoSQL/ORM injection skill",
        "Minimal Approach",
        "stable primitive",
        "references/sql-playbook.md",
        "references/nosql-graphql.md",
        "references/orm-query-dsl.md",
        "references/sqlmap-verification.md",
        "not a fixed playbook",
    ):
        assert expected in skill_text

    for removed in (
        "Shortest Loop",
        "Notes",
        "one variable at a time",
        "closed-loop verification",
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
        "DBMS",
        "UNION",
        "SELECT",
        "information_schema",
    ):
        assert expected in playbook

    for removed in (
        "method/url:",
    ):
        assert removed not in playbook
