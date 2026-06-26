from __future__ import annotations

from pathlib import Path

from pikaqiu_agent.skill_loader import SkillLoader


def test_ssti_bypass_skill_is_searchable_and_reference_backed() -> None:
    root = Path(__file__).resolve().parents[1]
    loader = SkillLoader(root, "skills")
    stats = loader.refresh()

    assert stats["status"] == "ready"
    assert not stats["errors"]

    queries = (
        "SSTI Jinja2 Twig FreeMarker SpEL OGNL Thymeleaf sandbox template injection RCE bypass",
        "template injection from_string session workflow Django delayed render",
        "render_template_string output constraint statement tag blacklist bypass",
    )
    for query in queries:
        results = loader.search(query, limit=5)
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
        "使用原则",
        "响应驱动流程",
        "基础探针",
        "参考资料",
        "references/bypass-playbook.md",
        "按响应分类推进",
        "覆盖完整性",
        "不要用单个 payload 排除 SSTI",
    ):
        assert expected in skill_text

    for expected in (
        "响应分类决策树",
        "黑盒识别提示",
        "响应信号速查",
        "完整探测清单",
        "确认与升级门槛",
        "什么时候确认 SSTI",
        "什么时候升级利用",
        "什么时候收敛或换入口",
        "forbidden characters",
        "not a number",
        "不只看当前响应",
        "引擎指纹矩阵",
        "Django 特别注意",
        "过滤与后置校验分离",
        "入口覆盖",
        "延迟消费",
        "上下文与入口",
        "过滤绕过",
        "引擎载荷",
        "禁 `{{` / `}}`",
        "{% if 7*7 == 49 %}49{% endif %}",
        "禁 `.`",
        "禁 `_`",
        "禁引号",
        "禁空格",
        "禁关键字",
        "Jinja2 / Flask",
        "Twig",
        "Django 黑盒优先级",
        "settings.SECRET_KEY",
        "自动转义 / HTML 转义",
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
