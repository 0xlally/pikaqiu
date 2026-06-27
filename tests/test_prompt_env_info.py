from __future__ import annotations

import json

from pikaqiu_agent.prompts import _build_env_info_section, _compact_env_info_for_prompt


def test_env_info_compacts_instead_of_truncating_raw_json() -> None:
    env_info = json.dumps(
        {
            "flag_path_dictionary": {
                "sandbox_path": "/opt/pikaqiu-tools/flag-paths.txt",
                "count": 119,
                "sample": ["flag", "FLAG", "flag.txt", "FLAG.txt"],
            },
            "tool_guidance": {
                "rule": "Pick the smallest tool.",
                "categories": [
                    {
                        "id": "local_artifact_analysis",
                        "tools": ["rg:rg"],
                        "examples": ['rg -n "flag|password|secret|token" .'],
                    },
                    {
                        "id": "web_discovery",
                        "tools": ["ffuf:ffuf", "sqlmap:sqlmap"],
                        "examples": ["ffuf -u http://TARGET/FUZZ -w common.txt"],
                    },
                ],
            },
            "pentest_tools": {"misc": ["git", "rg", "jq"], "sqli": ["sqlmap"]},
            "wordlists": {
                "rockyou": "/usr/share/wordlists/rockyou.txt",
                "common.txt": "/usr/share/seclists/Discovery/Web-Content/common.txt",
            },
            "offline_databases": {"searchsploit": {"path": "/usr/share/exploitdb"}},
            "python_packages": {f"pkg{i}": "available" for i in range(80)},
            "padding": "x" * 8000,
        },
        ensure_ascii=False,
    )

    compact = _compact_env_info_for_prompt(env_info)
    section = _build_env_info_section(env_info)

    assert len(compact) < 3200
    assert "... (truncated)" not in compact
    assert "/opt/pikaqiu-tools/flag-paths.txt" in compact
    assert "rg:rg" in compact
    assert "rockyou" in compact
    assert "searchsploit" in compact
    assert "padding" not in compact
    assert compact in section
