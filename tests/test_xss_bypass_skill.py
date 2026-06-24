from __future__ import annotations

from pathlib import Path

from pikaqiu_agent.skill_loader import SkillLoader


def test_xss_bypass_skill_is_searchable_and_reference_backed() -> None:
    root = Path(__file__).resolve().parents[1]
    loader = SkillLoader(root, "skills")
    stats = loader.refresh()

    assert stats["status"] == "ready"
    assert not stats["errors"]

    results = loader.search(
        "XSS reflected DOM CSP Trusted Types DOMPurify mXSS admin bot browser runtime bypass",
        limit=5,
    )

    assert results
    assert results[0]["id"] == "xss-bypass-skill"

    bypass_ref = loader.read_reference(
        "xss-bypass-skill",
        "references/bypass-playbook.md",
        max_chars=30000,
    )
    playwright_ref = loader.read_reference(
        "xss-bypass-skill",
        "references/playwright-verification.md",
        max_chars=30000,
    )
    skill_text = (
        root / "skills" / "builtin" / "xss-bypass-skill" / "SKILL.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "最短闭环",
        "绕过过滤和环境限制",
        "小批量代表性探针快速分层",
        "单变量复测归因",
        "定位上下文",
        "确认限制",
        "生成最小 payload",
        "用浏览器验真",
        "强证据后收束",
        "references/bypass-playbook.md",
        "references/playwright-verification.md",
        "失败时写链条位置",
    ):
        assert expected in skill_text

    for expected in (
        "HTML 与 Parser",
        "边界标签",
        "<z autofocus onfocus",
        "少数标签白名单",
        "image/img",
        "src=x onerror",
        "body",
        "style",
        "tag/attr=value/event",
        "check.js",
        "JavaScript 上下文",
        "URL、协议与导航",
        "CSS 与 Scriptless",
        "CSP、Sandbox、Trusted Types",
        "DOM、Framework 与 Sanitizer",
        "DOM clobbering",
        "DOMPurify/mXSS",
        "Framework/CSTI",
        "文件上传与 Admin Bot",
        "最小工具集",
        "jscrewit",
        "jsesc",
        "he",
        "cssesc",
        "terser",
    ):
        assert expected in bypass_ref

    for expected in (
        "Playwright Verification",
        "chromium.launch",
        "console",
        "dialog",
        "pageerror",
        "request failure",
        "postMessage",
        "Trusted Types",
        "Admin Bot",
    ):
        assert expected in playwright_ref


def test_xss_bypass_skill_keeps_references_small_and_current() -> None:
    root = Path(__file__).resolve().parents[1]
    skill_dir = root / "skills" / "builtin" / "xss-bypass-skill"

    reference_paths = sorted(
        path.relative_to(skill_dir).as_posix()
        for path in (skill_dir / "references").glob("*.md")
    )

    assert reference_paths == [
        "references/bypass-playbook.md",
        "references/playwright-verification.md",
    ]

    removed_reference_names = {
        "context-" + "playbook.md",
        "restriction-" + "bypasses.md",
        "minimal-" + "probes.md",
        "payload-" + "catalog.md",
        "escalation-and-" + "evidence.md",
    }
    assert not any((skill_dir / "references" / name).exists() for name in removed_reference_names)

    all_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in skill_dir.rglob("*")
        if path.is_file()
    )

    forbidden_terms = (
        "payloads" + "-all" + "-the" + "-things",
        "Payloads" + "All" + "The" + "Things",
        "payload" + "-all" + "-the" + "-things",
        "agent" + "-browser",
        "tch" + "-headless",
        "js" + "fuck",
        "hiero" + "glyphy",
        "aa" + "encode-cli",
        "jj" + "encode",
    )

    for term in forbidden_terms:
        assert term not in all_text

    assert "Playwright Verification" in all_text
