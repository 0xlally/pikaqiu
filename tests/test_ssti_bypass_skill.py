from __future__ import annotations

from pathlib import Path

from pikaqiu_agent.skill_loader import SkillLoader


def test_ssti_bypass_skill_is_searchable_and_reference_backed() -> None:
    root = Path(__file__).resolve().parents[1]
    loader = SkillLoader(root, "skills")
    stats = loader.refresh()

    assert stats["status"] == "ready"
    assert not stats["errors"]

    results = loader.search(
        "SSTI Jinja2 Twig FreeMarker SpEL OGNL Thymeleaf sandbox template injection RCE bypass",
        limit=5,
    )

    assert results
    assert results[0]["id"] == "ssti-bypass-skill"

    skill_text = (
        root / "skills" / "builtin" / "ssti-bypass-skill" / "SKILL.md"
    ).read_text(encoding="utf-8")
    bypass_ref = loader.read_reference(
        "ssti-bypass-skill",
        "references/bypass-playbook.md",
        max_chars=50000,
    )

    for expected in (
        "最小思路",
        "references/bypass-playbook.md",
        "不限制具体打法",
    ):
        assert expected in skill_text

    for expected in (
        "上下文与入口",
        "过滤绕过",
        "引擎载荷",
        "禁 `{{` / `}}`",
        "禁 `.`",
        "禁 `_`",
        "禁引号",
        "禁空格",
        "禁关键字",
        "Jinja2 / Flask",
        "Twig",
        "FreeMarker",
        "SpEL / Java EL / Thymeleaf / OGNL",
        "Velocity / Pebble / Jinjava / Groovy",
        "JavaScript / Node",
        "Ruby / .NET / Go / Elixir / Perl",
        "TInjA",
        "SSTImap",
        "tplmap",
        "Fenjing",
    ):
        assert expected in bypass_ref


def test_ssti_bypass_skill_keeps_references_focused() -> None:
    root = Path(__file__).resolve().parents[1]
    skill_dir = root / "skills" / "builtin" / "ssti-bypass-skill"

    reference_paths = sorted(
        path.relative_to(skill_dir).as_posix()
        for path in (skill_dir / "references").glob("*.md")
    )

    assert reference_paths == [
        "references/bypass-playbook.md",
    ]

    all_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in skill_dir.rglob("*")
        if path.is_file()
    )

    forbidden_terms = (
        "payloads" + "-all" + "-the" + "-things",
        "Payloads" + "All" + "The" + "Things",
        "agent" + "-browser",
        "playwright",
        "verification.md",
        "固定流程",
    )

    for term in forbidden_terms:
        assert term not in all_text
