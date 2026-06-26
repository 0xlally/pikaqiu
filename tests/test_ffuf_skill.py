from __future__ import annotations

from pathlib import Path

from pikaqiu_agent.skill_loader import SkillLoader


def test_ffuf_skill_is_found_for_endpoint_discovery_and_form_mapping() -> None:
    root = Path(__file__).resolve().parents[1]
    loader = SkillLoader(root, "skills")
    stats = loader.refresh()

    assert stats["status"] == "ready"
    assert not stats["errors"]

    query = (
        "Flask Werkzeug Blog Raider login/register web app needs endpoint discovery "
        "and form/input mapping before vulnerability testing"
    )
    results = loader.search(query, limit=5)

    assert results
    assert any(result["id"] == "ffuf-skill" for result in results)

    skill_text = (
        root / "skills" / "builtin" / "ffuf-skill" / "SKILL.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "endpoint discovery",
        "login/register form input mapping",
        "SecLists Paths",
        "/usr/share/seclists/Discovery/Web-Content/common.txt",
        "/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt",
        "POST Form Field Name Fuzzing",
        "Raw Request Fuzzing",
    ):
        assert expected in skill_text
