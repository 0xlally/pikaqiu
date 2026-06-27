from __future__ import annotations

import json

from pikaqiu_agent.prompts import (
    _build_env_info_section,
    _compact_env_info_for_prompt,
    build_tool_memory_prompt,
)


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


def test_memory_prompt_stall_rebase_is_memory_agent_mode() -> None:
    prompt = build_tool_memory_prompt(
        mission={"target": "http://target", "goal": "capture flag"},
        previous_memory={
            "summary": "疑似 SQLi，但未构造真假 oracle",
            "findings": ["GET /search.php returned 200"],
            "leads": ["继续试登录绕过"],
            "dead_ends": [],
            "credentials": [],
            "topology": [],
        },
        round_no=3,
        tool_call_log=None,
        mode="stall_rebase",
        stall_rounds=2,
        reason="stall_rounds=2",
    )

    assert "你是 MemoryAgent" in prompt
    assert "当前模式：stall_rebase" in prompt
    assert "不要删除已经被原始响应、命令输出、源码执行路径或可复现实验证明的漏洞事实" in prompt
    assert "优先给出能判真假的最小验证" in prompt
    assert "记忆清洗 agent" not in prompt
