from __future__ import annotations

from pikaqiu_agent.prompts import build_tool_system_prompt


def _mission() -> dict[str, object]:
    return {
        "target": "127.0.0.1:8000",
        "goal": "trigger XSS",
        "scope": "local CTF",
        "expected_flags": 1,
    }


def test_skill_catalog_is_not_injected_into_main_system_prompt() -> None:
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

    assert "skill_search" in prompt
    assert "activate_skill" in prompt
    assert "xss-bypass-skill" not in prompt
    assert "browser/runtime verification" not in prompt
    assert "Playwright verification" not in prompt
    assert "XSS bypass planning" not in prompt


def test_enabled_skill_prompt_is_not_injected_into_main_system_prompt() -> None:
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

    assert "skill_read_reference" in prompt
    assert "xss-bypass-skill" not in prompt
    assert "需要浏览器、挑战 harness 或运行时证据" not in prompt
    assert "Browser / Runtime Verification" not in prompt
    assert "references/browser-runtime-verification.md" not in prompt
    assert "必须用 Playwright 收集浏览器证据" not in prompt
    assert "Playwright Verification" not in prompt
    assert "Playwright" not in prompt
