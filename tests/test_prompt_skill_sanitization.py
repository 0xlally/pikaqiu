from __future__ import annotations

from pikaqiu_agent.prompts import build_tool_system_prompt


def _mission() -> dict[str, object]:
    return {
        "target": "127.0.0.1:8000",
        "goal": "trigger XSS",
        "scope": "local CTF",
        "expected_flags": 1,
    }


def test_xss_skill_catalog_does_not_inject_playwright_special_case() -> None:
    prompt = build_tool_system_prompt(
        mission=_mission(),
        skill_catalog=[
            {
                "id": "xss-bypass-skill",
                "description": (
                    "Use when Codex needs context-aware XSS bypass planning, "
                    "minimal-difference probes, Playwright verification, DOM tracing."
                ),
                "tags": ["xss"],
            }
        ],
    )

    assert "xss-bypass-skill" in prompt
    assert "browser/runtime verification" in prompt
    assert "Playwright verification" not in prompt
    assert "XSS bypass planning" in prompt


def test_enabled_xss_skill_prompt_does_not_force_playwright_in_system_prompt() -> None:
    prompt = build_tool_system_prompt(
        mission=_mission(),
        skills=[
            {
                "id": "xss-bypass-skill",
                "name": "xss-bypass-skill",
                "description": "XSS bypass with Playwright verification.",
                "prompt": (
                    "# xss-bypass-skill\n"
                    "涉及 DOM、事件、CSP、Trusted Types、sandbox、mXSS、上传预览或 admin bot 时，"
                    "必须用 Playwright 收集浏览器证据。\n"
                    "- `references/playwright-verification.md`：Playwright 证据清单和最小 Node 模板。\n"
                    "## Playwright Verification\n"
                ),
            }
        ],
    )

    assert "xss-bypass-skill" in prompt
    assert "需要浏览器、挑战 harness 或运行时证据" in prompt
    assert "Browser / Runtime Verification" in prompt
    assert "references/browser-runtime-verification.md" in prompt
    assert "必须用 Playwright 收集浏览器证据" not in prompt
    assert "Playwright Verification" not in prompt
    assert "Playwright" not in prompt
