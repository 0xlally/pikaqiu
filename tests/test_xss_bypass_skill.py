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
        "Focused XSS bypass skill",
        "minimal-difference probes",
        "browser/runtime verification",
        "Shortest Loop",
        "Locate the context",
        "Identify constraints",
        "Generate the smallest payload",
        "Verify in a browser",
        "references/bypass-playbook.md",
        "references/playwright-verification.md",
        "record the exact blocker",
    ):
        assert expected in skill_text

    for expected in (
        "HTML",
        "<z autofocus onfocus",
        "image/img",
        "src=x onerror",
        "body",
        "style",
        "tag/attr=value/event",
        "check.js",
        "JavaScript",
        "URL",
        "CSS",
        "CSP",
        "DOM clobbering",
        "DOMPurify/mXSS",
        "Framework/CSTI",
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
