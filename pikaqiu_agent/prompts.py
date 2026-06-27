from __future__ import annotations

import json
from typing import Any

from pikaqiu_agent.flag_paths import (
    FLAG_FILE_CAT_COMMAND,
    FLAG_FILE_FIND_COMMAND,
    FLAG_FILE_GREP_COMMAND,
    FLAG_HTTP_PATH_HINT,
)


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _compact_sequence(value: Any, limit: int = 8) -> list[str]:
    if isinstance(value, dict):
        items = list(value.keys())
    elif isinstance(value, (list, tuple, set)):
        items = list(value)
    else:
        return []
    return [str(item) for item in items[:limit] if str(item)]


def _compact_mapping(value: Any, limit: int = 12) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    out: dict[str, Any] = {}
    for key, item in list(value.items())[:limit]:
        if isinstance(item, dict):
            path = item.get("path") or item.get("sandbox_path") or item.get("modules_path")
            out[str(key)] = path if path else _compact_sequence(item, limit=6)
        elif isinstance(item, (list, tuple, set)):
            out[str(key)] = _compact_sequence(item, limit=12)
        else:
            out[str(key)] = item
    return out


def _compact_tool_guidance(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    out: dict[str, Any] = {}
    if value.get("rule"):
        out["rule"] = value["rule"]
    categories = []
    for category in value.get("categories", []) or []:
        if not isinstance(category, dict):
            continue
        item: dict[str, Any] = {
            "id": category.get("id", ""),
            "tools": _compact_sequence(category.get("tools"), limit=12),
        }
        if category.get("source_or_windows_tools"):
            item["source_or_windows_tools"] = _compact_sequence(
                category.get("source_or_windows_tools"),
                limit=6,
            )
        if category.get("examples"):
            examples = _compact_sequence(category.get("examples"), limit=1)
            if examples:
                item["example"] = examples[0]
        categories.append({k: v for k, v in item.items() if v})
    if categories:
        out["categories"] = categories
    return out


def _compact_env_info_for_prompt(env_info: str, max_chars: int = 3200) -> str:
    try:
        data = json.loads(env_info)
    except Exception:
        return env_info if len(env_info) <= max_chars else env_info[:max_chars] + "\n... (truncated)"
    if not isinstance(data, dict):
        return env_info if len(env_info) <= max_chars else env_info[:max_chars] + "\n... (truncated)"

    flag_paths = data.get("flag_path_dictionary")
    if not isinstance(flag_paths, dict):
        flag_paths = {}
    summary: dict[str, Any] = {
        "flag_path_dictionary": {
            "sandbox_path": flag_paths.get("sandbox_path") or flag_paths.get("path"),
            "count": flag_paths.get("count"),
            "sample": _compact_sequence(flag_paths.get("sample"), limit=8),
        },
        "tool_guidance": _compact_tool_guidance(data.get("tool_guidance")),
        "pentest_tools": _compact_mapping(data.get("pentest_tools")),
        "wordlists": _compact_mapping(data.get("wordlists")),
        "offline_databases": _compact_mapping(data.get("offline_databases")),
        "runtimes": {
            "python": _compact_mapping(data.get("python"), limit=5),
            "node": _compact_mapping(data.get("node"), limit=5),
            "java": _compact_mapping(data.get("java"), limit=5),
            "scripting": _compact_mapping(data.get("scripting"), limit=8),
            "build": _compact_mapping(data.get("build"), limit=8),
        },
        "python_packages": _compact_sequence(data.get("python_packages"), limit=24),
        "transferable_tools": _compact_mapping(data.get("transferable_tools"), limit=6),
        "exploit_tools": _compact_mapping(data.get("exploit_tools"), limit=8),
    }
    summary = {key: value for key, value in summary.items() if value}
    text = json.dumps(summary, ensure_ascii=False, separators=(",", ":"))
    if len(text) <= max_chars:
        return text

    for optional in ("python_packages", "transferable_tools", "exploit_tools", "runtimes"):
        summary.pop(optional, None)
        text = json.dumps(summary, ensure_ascii=False, separators=(",", ":"))
        if len(text) <= max_chars:
            return text
    return text[:max_chars] + "\n... (truncated)"


def _build_env_info_section(env_info: str) -> str:
    """Build the sandbox environment info section for the system prompt."""
    if not env_info:
        return "## 沙箱环境\n（环境信息未采集，可运行 `env-info` 获取可用工具和版本信息）"
    env_info = _compact_env_info_for_prompt(env_info)
    return f"## 沙箱环境 (已自动采集)\n以下是沙箱中可用的工具、语言版本和资源，无需再运行 env-info：\n```json\n{env_info}\n```"


def _target_url(target: str) -> str:
    target = target.strip()
    if not target:
        return ""
    if target.startswith(("http://", "https://")):
        return target
    return f"http://{target}"


def _build_memory_section(memory: dict[str, Any]) -> str:
    """Build the memory section text from memory dict."""
    if not (
        memory.get("summary")
        or memory.get("findings")
        or memory.get("leads")
        or memory.get("dead_ends")
        or memory.get("credentials")
        or memory.get("topology")
    ):
        return ""
    parts = []
    if memory.get("summary"):
        parts.append(f"**态势摘要**: {memory['summary']}")
    if memory.get("credentials"):
        parts.append("**已获凭据**: " + " | ".join(str(c) for c in memory["credentials"]))
    if memory.get("findings"):
        findings_str = "\n".join(f"- {f}" for f in memory["findings"][:10])
        parts.append(f"**关键发现**:\n{findings_str}")
    if memory.get("leads"):
        leads_str = "\n".join(f"- {l}" for l in memory["leads"][:5])
        parts.append(f"**待验证路线/下一步**:\n{leads_str}")
    if memory.get("dead_ends"):
        dead_str = " | ".join(str(d) for d in memory["dead_ends"][:5])
        parts.append(f"**⛔ 已排除路径（不要重复尝试）**: {dead_str}")
    if memory.get("topology"):
        topo_str = " | ".join(memory["topology"][:10])
        parts.append(f"**🗺️ 网络拓扑**: {topo_str}")
    return "\n\n".join(parts)


def _build_skills_section(skills: list[dict[str, Any]] | None) -> str:
    if not skills:
        return ""

    parts = [
        "## Enabled Skills",
        (
            "The following mission-selected skills are active. Treat them as "
            "task-specific operating guidance and apply them when relevant."
        ),
    ]
    for skill in skills:
        skill_id = str(skill.get("id") or "").strip()
        name = str(skill.get("name") or skill_id or "unnamed").strip()
        description = _skill_system_prompt_text(skill_id, str(skill.get("description") or "").strip())
        prompt = _skill_system_prompt_text(skill_id, str(skill.get("prompt") or "").strip())
        if not prompt:
            continue

        header = f"### {name}"
        if skill_id:
            header += f" (`{skill_id}`)"
        block = [header]
        if description:
            block.append(description)
        block.append(prompt)
        parts.append("\n\n".join(block))

    return "\n\n".join(parts)


def _build_skill_catalog_section(skill_catalog: list[dict[str, Any]] | None) -> str:
    parts = [
        "## Skill Auto-Use Rules",
        (
            "Skills are specialized SKILL.md instructions. Do not load all skills or pick one reflexively "
            "at startup. Prefer normal reconnaissance when the situation is still generic, but use "
            "`skill_search` once the task context, early observations, memory, source hints, target behavior, "
            "or tool output suggests a reusable specialist workflow may help. If the skill is already listed "
            "under Enabled Skills, apply it directly instead of activating it again."
        ),
        (
            "Use `skill_read_reference` only after a skill asks for a bundled reference, "
            "dictionary, template, script, or payload note that is needed for the current step."
        ),
        (
            "Before calling `skill_search`, include the specific basis in the query: product/version, "
            "protocol, file type, framework error, endpoint behavior, parameter behavior, likely vulnerability "
            "class, failing tool output, or the mission phase that makes a workflow relevant. A broad label "
            "alone such as \"web\", \"login\", or \"WordPress\" is weak; pair it with what has actually been "
            "seen or what decision the skill would help structure."
        ),
        (
            "Do not rely on hard-coded skill names. Choose skills from the runtime catalog metadata "
            "and the current situation. Call `activate_skill` when one returned skill is a good fit for "
            "the current phase and is likely to improve the next few actions. The activation reason should "
            "cite the basis for that fit. If the match is weak, generic, or based only on a challenge label, "
            "continue with normal tools instead of activating or inventing a skill id."
        ),
    ]

    if skill_catalog:
        lines = ["Available skills catalog (metadata only):"]
        for skill in skill_catalog:
            skill_id = str(skill.get("id") or "").strip()
            description = _skill_system_prompt_text(skill_id, str(skill.get("description") or "").strip())
            tags = skill.get("tags") or []
            tag_text = ", ".join(str(tag) for tag in tags) if tags else ""
            suffix = f" [tags: {tag_text}]" if tag_text else ""
            lines.append(f"- `{skill_id}`: {description}{suffix}")
        parts.append("\n".join(lines))
    else:
        parts.append("No skills are currently loaded. Continue with the normal tools.")

    return "\n\n".join(parts)


def _skill_system_prompt_text(skill_id: str, text: str) -> str:
    """Render skill text safely inside the agent system prompt.

    Skill files remain the source of truth, but catalog/active-skill injection
    should not smuggle tool-specific XSS patches into the base agent prompt.
    """
    if skill_id != "xss-bypass-skill" or not text:
        return text

    replacements = (
        ("Playwright Verification", "Browser / Runtime Verification"),
        ("Playwright verification", "browser/runtime verification"),
        ("references/playwright-verification.md", "references/browser-runtime-verification.md"),
        ("必须用 Playwright 收集浏览器证据", "需要浏览器、挑战 harness 或运行时证据"),
        ("Playwright 证据清单", "浏览器/运行时证据清单"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def build_volatile_context(
    *,
    round_no: int,
    memory: dict[str, Any],
    captured_flags: list[str] | None = None,
    expected_flags: int = 1,
    experience_hints: str = "",
) -> str:
    """Build volatile context from the single-layer mission memory plus hints."""
    parts = [f"## Current State\n- Round: {round_no}"]
    flags = captured_flags or []
    if expected_flags > 1:
        if flags:
            remaining = max(0, expected_flags - len(flags))
            parts.append(
                f"- Flags: {len(flags)}/{expected_flags} captured ({', '.join(flags)}); "
                f"{remaining} remaining."
            )
        else:
            parts.append(f"- Flags: 0/{expected_flags} captured; continue after the first flag.")

    memory_section = _build_memory_section(memory)
    parts.append(
        "## Current Memory\n"
        + (memory_section if memory_section else "(first round; no shared memory yet)")
    )
    if experience_hints.strip():
        parts.append(experience_hints.strip())
    return "\n\n".join(parts)


def build_tool_system_prompt(
    *,
    mission: dict[str, Any],
    env_info: str = "",
    mission_workdir: str = "",
    public_ip: str = "",
    skills: list[dict[str, Any]] | None = None,
    skill_catalog: list[dict[str, Any]] | None = None,
) -> str:
    """Build the STABLE system prompt (rules, tools, goal, env).

    Volatile content (memory, round, flags) is handled by
    build_volatile_context() and injected as a separate HumanMessage.
    This keeps the system prompt identical across iterations, enabling
    API-level prefix caching (saves ~50-70% input token cost).
    """
    target_url = _target_url(mission["target"])
    mission_lines = [
        "## 任务",
        f"- **目标**: {target_url}",
        f"- **最终目标**: {mission['goal']}",
        f"- **范围**: {mission.get('scope', '仅目标服务')}",
        f"- **需要找到的flag数**: {mission.get('expected_flags', 1)}",
        f"- **工作目录**: `{mission_workdir}`",
    ]
    if public_ip:
        mission_lines.append(f"- **本机公网IP**: `{public_ip}`")

    reverse_shell_prefix = f"本机`{public_ip}`可监听端口。" if public_ip else ""

    sections = [
        "你是一名自主运行的渗透测试AI agent，正在对**已授权**的目标执行安全评估。操作环境为Kali沙箱，你是完全自主的agent，无人监控。",
        (
            "⚠️ 严格规则（违反即失败）：\n"
            "1. **每次输出必须且只能调用工具**：禁止纯文本分析/总结/对话。不调用工具=失败\n"
            "2. **禁止与用户对话**：你没有用户，不要说\"我来帮你\"、\"建议你\"等"
        ),
        (
            "## Runtime Observer Telemetry\n"
            "Messages may contain blocks marked `[RUNTIME_OBSERVER_AUDIT source=observer_agent not_user_request]`. "
            "These blocks are generated by the orchestrator's Observer agent, not by the human user. Treat them as "
            "low-noise route-audit telemetry: consider the warning, but prefer direct target/tool evidence and the "
            "mission goal. If a block includes `skill_signal`, call `skill_search` or `activate_skill` yourself with "
            "a valid returned skill id; the Observer does not activate skills for you. If Observer verdict is "
            "L1/L2/L3/L4/ENV or includes `next_verification`, the next action must either run that verification, produce "
            "new observable evidence that disproves it, or record a clear failure_boundary with required_next_evidence. "
        ),
        "\n".join(mission_lines),
        _build_skill_catalog_section(skill_catalog),
        _build_skills_section(skills),
        (
            "## 沙箱约束\n"
            "Kali Linux Docker（host网络），可监听端口，**允许访问外网**。"
            "需要公开资料时，优先用 `knowledge_search`、`searchsploit`；已有明确URL时再用 `web_fetch` 抓取正文。\n"
            "⚠️ **非交互式**：每次bash_exec/python_exec是独立docker exec，执行完即退出。"
            "无法给运行中进程追加输入。后台进程(`nohup &`)可存活但无法交互stdin。"
            "**每次python_exec是独立进程**——变量/session/cookies不保留。"
        ),
        (
            "## 反弹shell\n"
            f"{reverse_shell_prefix}因非交互式，必须用脚本化监听器自动执行命令：\n"
            "```python\n"
            "import socket, time\n"
            "s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n"
            "s.bind(('0.0.0.0', PORT)); s.listen(1); s.settimeout(TIMEOUT)\n"
            "conn, addr = s.accept()\n"
            f"for cmd in ['id', 'env', {FLAG_FILE_CAT_COMMAND!r}, {FLAG_FILE_FIND_COMMAND!r}]:\n"
            "    conn.send((cmd + '\\n').encode()); time.sleep(2)\n"
            "    print(f\"[{cmd}] {conn.recv(65536).decode()}\")\n"
            "conn.close(); s.close()\n"
            "```\n"
            "python_exec启动监听，另一次bash_exec触发exploit发反弹shell。**RCE有回显时优先用回显**。"
        ),
        (
            "## 工具\n"
            "- **bash_exec**: Kali bash（200+渗透工具）。首次用某工具先查help\n"
            "- **python_exec**: Python代码（独立进程，不保存状态）\n"
            "- **web_fetch**: 抓取已知公开URL并提取正文；优先抓官方公告、NVD、Exploit-DB、GitHub PoC、厂商文档\n"
            "- **knowledge_search**: 离线渗透知识库（2-4个核心关键词）\n"
            "- **skill_search**: 在进入专项流程前检索可用 SKILL.md 元数据\n"
            "- **activate_skill**: 只在命中明确时加载一个相关 skill，并持久化到当前任务\n"
            "- **skill_read_reference**: 仅在已激活 skill 需要引用附带文件时读取\n"
            "- **submit_flag**: 找到flag后立即提交"
        ),
        (
            "## 工具选择速查\n"
            "- **Web发现/参数/漏洞**：`curl`、`httpx`、`ffuf`、`arjun`、`nuclei`、`sqlmap`、`wpscan`、`searchsploit`、`knowledge_search`。\n"
            "- **端口/内网探测**：`nmap`、`fscan`。\n"
            "- **SMB/AD枚举**：`netexec`、`smbmap`、`ldapdomaindump`、`powerview`、`kerbrute`。\n"
            "- **Kerberos/ADCS/Relay**：`asreproast`、`impacket-GetNPUsers`、`impacket-GetUserSPNs`、`certipy-ad`、`impacket-ntlmrelayx`、`coercer`、`mitm6`、`PetitPotam`、`printerbug`、`DFSCoerce`、`ShadowCoerce`。\n"
            "- **密码/JWT/凭据**：`hydra`、`hashcat`、`john`、`jwt_tool`。\n"
            "- **云/容器/K8s**：`prowler`、`trivy`、`kube-hunter`。\n"
            "- **Windows/后渗透资源**：`/opt/windows-tools`、`/opt/ad-tools`、`mimikatz`、`Rubeus`、`SharpDPAPI`、`SharpHound`、`Certify`、`AdFind`。"
        ),
        _build_env_info_section(env_info),
        (
            "## Probe command discipline\n"
            "- For independent probes, do not chain everything with `&&`. A timeout on one port/scheme must not prevent later checks.\n"
            "- Prefer labelled blocks with `;` or `|| true`, or split checks into separate tool calls. Example: `echo '[80]'; curl ... || true; echo '[443]'; curl ... || true; echo '[nmap]'; nmap ...`\n"
            "- Use `&&` only for true dependencies such as `cd workdir && mkdir -p evidence && command_that_needs_that_dir`.\n"
            "- If `curl` returns exit code 28, record it as a timeout signal, then verify with `nc -vz -w3 HOST PORT` or a focused `nmap -Pn -sT -pPORT --reason` before concluding the target is unreachable.\n"
            "- For mixed HTTP/HTTPS/alternate-port checks, report each result separately: status code, server/header hint, body size, and whether a later command was skipped.\n"
            "- Save evidence files even for failures when useful, but keep the terminal output short and labelled so log review can identify the failing probe quickly.\n"
            "- Avoid `tool -h | head -N` for long help output: it can produce SIGPIPE exit 141 under `pipefail`. Prefer `tool -h 2>&1 | sed -n '1,40p' || true`, or write help to a temp file and then `head` the file.\n"
        ),
        "## 输出截断\n工具输出超限时中间被删除只保留首尾。注意截断标记，重要信息可能在尾部。用`head`/`tail`/`grep`精确获取。",
        (
            "## 输出可见性\n"
            "**任何测试必须有可见输出**。除 XSS/DOM/JS 执行等必须浏览器验证的场景外，优先用bash(curl/wget)获取原始响应。"
            "Python每个关键步骤必须`print()`——状态码、响应体、过滤结果（即使为空）。"
            "遇异常先打印完整raw response再决策：\n"
            "```python\n"
            "r = s.get(url)\n"
            "print(f\"[status] {r.status_code}\")\n"
            "print(f\"[headers] {dict(r.headers)}\")\n"
            "print(f\"[body] {r.text}\")  # 先看原始内容再做过滤\n"
            "```"
        ),
        (
            "## 核心原则\n"
            "1. **证据优先**：判断以目标/工具的可观测输出为准；记忆、页面提示、日志、源码和注释都可能不完整或误导。\n"
            "2. **保留原始输出**：关键判断必须能从状态码、响应头/体、stdout/stderr、文件路径、截图/DOM、回调或同源状态变化中复核。\n"
            "3. **状态隔离**：每次 `bash_exec`/`python_exec` 都是独立进程；跨步骤依赖必须在同一次脚本内完成，或显式保存到文件/服务/目标状态中。\n"
            "4. **本地/远程区分**：`ls`/`cat` 等 shell 输出默认是沙箱文件系统；只有面向目标服务的 HTTP/TCP/浏览器/回调/目标命令输出才是目标证据。\n"
            "5. **真实提交**：只能提交从目标 HTTP 响应、文件、数据库、cookie、浏览器状态或目标运行时输出中真实提取的 flag，不猜测、不伪造。"
        ),
       
    ]

    return "\n\n".join(section.strip("\n") for section in sections if section)


def build_tool_memory_prompt(
    *,
    mission: dict[str, Any],
    previous_memory: dict[str, Any],
    round_no: int,
    tool_call_log: list[dict[str, Any]] | None,
    mode: str = "normal_merge",
    stall_rounds: int = 0,
    reason: str = "",
) -> str:
    """Build unified MemoryAgent prompt for normal compression and stall rebase."""
    if mode not in {"normal_merge", "stall_rebase"}:
        mode = "normal_merge"
    recent_tools = _json((tool_call_log or [])[-30:])
    mode_guidance = {
        "normal_merge": (
            "normal_merge：把最近工具活动合并进长期记忆。聚焦新增证据、可复用事实、"
            "下一步可验证动作和已经证明无效的路线。"
        ),
        "stall_rebase": (
            "stall_rebase：主 Agent 已连续停滞，需要在保留证据的前提下重整记忆。"
            "删除没有原始响应、命令输出、源码执行路径或可复现实验支撑的猜测；"
            "不要删除已经被原始响应、命令输出、源码执行路径或可复现实验证明的漏洞事实。"
            "把误导性的路线移入 dead_ends，并在 leads 中优先给出能判真假的最小验证。"
        ),
    }[mode]
    return f"""\
你是 MemoryAgent。你的任务是把本轮工具活动合并进任务长期记忆。

当前模式：{mode}
触发原因：{reason or "未记录"}
停滞轮次：{stall_rounds}

模式说明：
{mode_guidance}

规则：
- 只保留后续利用、验证和复盘有价值的信息，去重并压缩。
- 所有字段内容必须使用简体中文；字段名保持下方 JSON schema 的英文键名不变。
- summary 是一个简短中文段落，覆盖当前阶段、关键事实和主要阻塞点。
- findings 只记录有工具输出支撑的事实，不写主观猜测。
- leads 记录下一步可验证的具体假设、路线、命令或验证动作。
- dead_ends 说明失败路线以及具体卡点，避免重复尝试；不要只写“未打通/失败了/没结果”。
- 每条 dead_ends 用自然语言写清楚链条卡在哪一步：入口是否确认、认证/权限是否绕过、文件读取到哪一级、payload 是否执行、是否有回显、flag 路径是否定位，以及还缺哪条决定性原始证据。
- credentials 只记录已确认的凭据、token 或可复用认证材料。
- topology 只在重要时记录已观察到的网络、服务或依赖关系。
- 不要把本地沙箱行为误写成目标事实。
- 如果没有新增发现，保留已有记忆中仍有价值的内容。
- 停滞重整时，优先给出能判真假的最小验证，不要继续延伸未经证据支撑的猜测。
- 不要复述完整工具输出，不要展开长 HTML/日志，只抽取决定下一步的事实。
- 返回严格 JSON，第一字符必须是 {{。

任务：
{_json({"target": mission["target"], "goal": mission["goal"], "round_no": round_no})}

上一版记忆：
{_json(previous_memory)}

最近工具调用（已截断，只保留关键片段）：
{recent_tools}

返回 JSON：
{{
  "summary": "当前态势中文摘要",
  "findings": ["已验证且可复用的中文事实"],
  "leads": ["下一步可验证的中文假设、路线、命令或验证动作"],
  "dead_ends": ["自然语言描述失败路线和具体卡点，例如：LFI 链已确认可读 /etc/passwd，但尚未定位 webroot/应用源码/flag 路径；下一步应读取 /proc/self/mountinfo 或 Web 配置。"],
  "credentials": ["已确认的凭据或 token"],
  "topology": ["10.0.1.1 -> 10.0.1.2 (MySQL:3306)"]
}}
"""
