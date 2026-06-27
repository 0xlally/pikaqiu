from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from typing import Any

from pikaqiu_agent.flag_capture import FLAG_RE
from pikaqiu_agent.flag_paths import FLAG_FILE_CAT_COMMAND, FLAG_FILE_FIND_COMMAND, FLAG_FILE_GREP_COMMAND
from pikaqiu_agent.memory_rules import normalize_dead_ends


MEMORY_PATCH_KEYS = ("findings", "leads", "dead_ends")
OBSERVER_VERDICTS = {"OK", "WATCH", "L1", "L2", "L3", "L4", "ENV"}
INTERRUPT_VERDICTS = {"L1", "L2", "L3", "L4", "ENV"}
VERDICT_LABELS = {
    "OK": "正常推进",
    "WATCH": "观察中",
    "L1": "工具使用错误",
    "L2": "信息不足",
    "L3": "策略方向错误",
    "L4": "认知偏差",
    "ENV": "环境故障",
}
VERDICT_PRIORITY = {
    "OK": 0,
    "WATCH": 1,
    "L1": 2,
    "L2": 2,
    "L3": 3,
    "ENV": 3,
    "L4": 4,
}

FAILURE_RE = re.compile(
    r"(timeout|timed out|403|404|connection (?:failed|refused|reset)|"
    r"no results?|empty response|not found|forbidden|"
    r"permission denied|traceback|exception|error|failed|unavailable|invalid)",
    re.I,
)
SKILL_TOOL_NAMES = {"skill_search", "activate_skill", "skill_read_reference"}
SKILL_ERROR_RE = re.compile(
    r"(unknown skill|no skills?|not found|unavailable|missing|failed|error|"
    r"exception|invalid|call skill_search|no match|disabled)",
    re.I,
)
SCOPE_SAFE_TOOLS = {
    "web_fetch",
    "knowledge_search",
    "skill_search",
    "activate_skill",
    "skill_read_reference",
}
EVIDENCE_AUDIT_EXEMPT_TOOLS = {
    "knowledge_search",
    "skill_search",
    "activate_skill",
    "skill_read_reference",
    "submit_flag",
}
EVIDENCE_MARKER_RE = re.compile(
    r"(\[EXIT_CODE:\s*\d+\]|\[STDERR\]|\bHTTP/\d|\bstatus(?:_code)?\s*[:=]\s*\d{3}|"
    r"\b(?:200|201|204|301|302|400|401|403|404|500)\b|<html|set-cookie|content-type|"
    r"response body|request body|headers?|stdout|stderr|traceback|"
    r"/api/|CVE-\d{4}-\d+|\bopen\b|\bclosed\b|\bfiltered\b|uid=|gid=|root:|"
    r"nginx|apache|tomcat|mysql|postgres|redis|ssh|ftp|port|response|status code|echo)",
    re.I,
)
VAGUE_RESULT_RE = re.compile(
    r"^(ok|done|success|successful|completed|finished|no output|empty|none|null|true|false|n/a|"
    r"empty result|suggestion|recommendation|next step|analysis)$",
    re.I,
)
STRONG_EVIDENCE_RULES = (
    (
        "lfi_passwd",
        re.compile(r"root:x:0:0:|daemon:x:1:1:|/bin/(?:bash|sh)\b", re.I),
        "LFI 已读到系统账户文件特征",
        (
            "围绕已验证 LFI 收束：读取 /proc/self/mountinfo、Web 服务配置和应用源码，"
            "定位 webroot、日志路径或 flag 路径。"
        ),
        "原始响应需包含目标返回的文件内容、请求 URL、HTTP 状态码，以及下一步读取到的配置/源码片段。",
    ),
    (
        "flag_file_read",
        re.compile(r"\b(?:flag|FLAG|ctf|CTF)\{[^}\s]{4,200}\}|(?i:/(?:flag|flag\.txt)\b[^\n]{0,120}(?:200|contents?|read|found))"),
        "响应中已出现 flag 内容或 flag 文件读取线索",
        (
            "围绕已出现的 flag 证据收束：确认该值来自目标原始输出；若已经是完整 flag，立即提交，"
            "不要继续扩展攻击面。"
        ),
        "保留包含 flag 候选值或 flag 文件路径的原始响应，并记录提交结果。",
    ),
    (
        "sensitive_config",
        re.compile(
            r"(?:DB_PASSWORD|DATABASE_URL|MYSQL_PASSWORD|REDIS_PASSWORD|SECRET_KEY|APP_KEY|JWT_SECRET|AWS_ACCESS_KEY_ID|"
            r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|password\s*[:=]\s*['\"][^'\"]{4,})",
            re.I,
        ),
        "敏感配置、密钥或凭据材料已泄露",
        (
            "围绕已泄露配置收束：先验证凭据用途和服务位置，再用最小请求访问后台、数据库、对象存储或签名接口；"
            "保留每次凭据复用的状态码和响应差异。"
        ),
        "保留泄露字段来源、原始响应片段、凭据复用目标和验证前后的状态码/响应差异。",
    ),
    (
        "rce_uid",
        re.compile(r"\buid=\d+\([^)]+\)\s+gid=\d+\([^)]+\)|\buid=\d+\s+gid=\d+", re.I),
        "命令执行已返回 uid/gid",
        (
            f"围绕已验证 RCE 收束：先确认当前目录和环境变量，再执行 `{FLAG_FILE_CAT_COMMAND}`；"
            f"必要时执行 `{FLAG_FILE_FIND_COMMAND}`，并用 `{FLAG_FILE_GREP_COMMAND}` 做小范围内容检索。"
        ),
        "保留命令回显中的 uid/gid、当前目录、flag 文件读取结果或 find 命中路径。",
    ),
    (
        "ssti_eval",
        re.compile(r"(?:\{\{\s*7\s*[*+]\s*7\s*\}\}|\${\s*7\s*[*+]\s*7\s*}|<%=\s*7\s*[*+]\s*7\s*%>)[^\n]{0,120}\b(?:49|14)\b", re.I),
        "模板表达式已产生可计算回显",
        (
            "围绕已验证 SSTI 收束：识别模板引擎和过滤边界，做最小文件读取或命令执行验证；"
            "不要再换无关参数。"
        ),
        "保留输入 payload、渲染回显、模板引擎判断依据，以及下一步文件读取/RCE 的原始结果。",
    ),
    (
        "sqli_error_or_union",
        re.compile(
            r"(?:SQL syntax|mysql_fetch|MariaDB|PostgreSQL|SQLite|ODBC|ORA-\d{5}|"
            r"You have an error in your SQL syntax|UNION SELECT[^\n]{0,160}(?:HTTP/\d|status|200|column|database\(\)))",
            re.I,
        ),
        "SQL 注入错误或 UNION 线索已可观察",
        (
            "围绕已验证 SQLi 收束：固定注入点，先确认列数/回显位/数据库类型，再读取当前库表或 flag 相关表；"
            "保留每一步数据库枚举和读取的原始响应。"
        ),
        "保留注入 URL/参数、错误或 UNION 回显、列数/回显位判断，以及读取到的库表/flag 线索。",
    ),
    (
        "ssrf_internal",
        re.compile(
            r"(?:169\.254\.169\.254|metadata\.google\.internal|latest/meta-data|127\.0\.0\.1|localhost|"
            r"file:///|gopher://|dict://)[\s\S]{0,500}(?:HTTP/\d|200|root:x:|instance-id|ami-id|hostname|uid=)",
            re.I,
        ),
        "SSRF/内网读取已产生内部响应特征",
        (
            "围绕已验证 SSRF 收束：枚举最小内网/metadata 路径或协议能力，优先读取凭据、配置和可访问管理端；"
            "不要大范围端口扫描。"
        ),
        "保留 SSRF 参数、目标内部 URL、状态码、响应体特征和下一步内部资源读取结果。",
    ),
    (
        "webshell_upload",
        re.compile(r"\b(?:webshell|shell\.php|cmd=|system\(|passthru\(|eval\(|assert\()\b", re.I),
        "疑似 WebShell/可执行写入链已出现",
        (
            "优先做最小回显验证：访问写入路径并执行 id/whoami；若可执行，立即进入 flag 搜索，"
            "若 404/403，先验证写入目录和 Web 可达路径映射。"
        ),
        "保留写入响应、访问 URL、HTTP 状态码和 id/whoami 原始回显。",
    ),
    (
        "auth_cookie",
        re.compile(
            r"set-cookie:[^\n]*(?:phpsessid|connect\.sid|session|jwt|token)|"
            r"\b(?:jwt|bearer\s+[A-Za-z0-9_.-]{16,})\b|"
            r"\b(?:user_id|is_admin|role)\s*[:=]",
            re.I,
        ),
        "认证态或会话材料已出现",
        (
            "围绕已拿到的认证材料收束：复用同一 Session 访问登录后页面、管理接口和已发现敏感端点，"
            "先验证身份差异，再尝试 IDOR/权限边界。"
        ),
        "保留 Set-Cookie/token、复用前后的状态码/响应差异，以及目标页面返回的身份或权限证据。",
    ),
    (
        "cve_version",
        re.compile(r"\bCVE-\d{4}-\d{4,7}\b|(?:wordpress|drupal|joomla|next\.js|flask|django|apache|nginx)[^\n]{0,80}\b\d+\.\d+(?:\.\d+)?", re.I),
        "产品/版本或 CVE 线索已足够具体",
        (
            "围绕产品版本/CVE 做定向验证：先查本地 knowledge_search/searchsploit，再用一个最小 PoC 验证决定性响应；"
            "记录版本来源、PoC 来源和验证响应差异。"
        ),
        "保留版本来源、CVE/PoC 来源、最小验证请求和原始响应差异。",
    ),
    (
        "api_object",
        re.compile(
            r"\b(?:s3|bucket|object[_ -]?key|presigned)\b|"
            r"\b(?:\.next/static|_next/static|chunk)\b|"
            r"/api/(?:s3|files|objects|assets|storage|download)\b",
            re.I,
        ),
        "对象 API、静态 chunk 或存储 key 线索已出现",
        (
            "围绕对象/API 线索收束：解析前端 chunk 和接口响应，枚举已知 key 的相邻命名，"
            "优先拿 metadata/列表/错误差异，不要盲目大字典爆破。"
        ),
        "保留接口 URL、对象 key、状态码差异、metadata 或 chunk 中提取的真实字段。",
    ),
    (
        "deserialization_marker",
        re.compile(
            r"(?:ysoserial|__wakeup|__destruct|ObjectInputStream|pickle|java\.io\.Serializable|"
            r"O:\d+:\"[^\"]+\":\d+:\{|rO0AB|aced0005)[^\n]{0,240}(?:error|exception|stack|uid=|HTTP/\d|200)",
            re.I,
        ),
        "反序列化入口或 gadget 反馈已可观察",
        (
            "围绕反序列化证据收束：确认序列化格式、触发点和回显/副作用，再做最小 DNS/文件写入/命令执行验证；"
            "不要盲换 gadget。"
        ),
        "保留序列化样本、触发请求、异常/回显/副作用证据，以及最小 gadget 验证结果。",
    ),
)


def _str_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _clean_text(value: Any, limit: int = 600) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def _compact_line(value: Any, limit: int = 280) -> str:
    text = _clean_text(value, limit * 2)
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def _normalise_arg(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\b\d+\b", "N", value)
    value = re.sub(r"https?://[^/\s]+", "URLHOST", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:220]


def _similar(a: str, b: str) -> bool:
    if not a or not b:
        return False
    return SequenceMatcher(None, a, b).ratio() >= 0.88


def _normalise_verdict(value: Any) -> str:
    verdict = str(value or "").strip().upper()
    return verdict if verdict in OBSERVER_VERDICTS else "OK"


def _verdict_allows_interrupt(verdict: str) -> bool:
    return _normalise_verdict(verdict) in INTERRUPT_VERDICTS


def _route_memory_changed(before: dict[str, Any], after: dict[str, Any]) -> bool:
    for key in ("findings", "leads"):
        if _str_list((before or {}).get(key, [])) != _str_list((after or {}).get(key, [])):
            return True
    return False


def _tool_args_text(row: dict[str, Any], *, limit: int | None = None) -> str:
    text = str(row.get("args_full") or row.get("args_summary") or "")
    return text if limit is None else text[:limit]


def _tool_result_text(row: dict[str, Any], *, limit: int | None = None) -> str:
    text = str(row.get("result_full") or row.get("result_observer") or row.get("result_summary") or "")
    return text if limit is None else text[:limit]


@dataclass
class ObserverDecision:
    verdict: str = "OK"
    rationale: str = ""
    evidence: list[str] = field(default_factory=list)
    guidance: str = ""
    next_verification: str = ""
    required_evidence: str = ""
    memory_patch: dict[str, list[str]] = field(default_factory=dict)
    skill_signal: str = ""
    experience_refs: list[str] = field(default_factory=list)
    primary_hypothesis: str = ""
    failure_boundary: str = ""
    blocked_prerequisite: str = ""
    observer_enforcement_state: str = ""
    agent_override_reason: str = ""

    @classmethod
    def none(cls) -> "ObserverDecision":
        return cls()

    def normalised(self) -> "ObserverDecision":
        patch: dict[str, list[str]] = {}
        raw_patch = self.memory_patch if isinstance(self.memory_patch, dict) else {}
        for key in MEMORY_PATCH_KEYS:
            vals = _str_list(raw_patch.get(key, []))
            if vals:
                patch[key] = vals[:8]
        skill_signal = _clean_text(self.skill_signal, 600)
        if skill_signal.lower() in {"none", "null", "false"}:
            skill_signal = ""
        return ObserverDecision(
            verdict=_normalise_verdict(self.verdict),
            rationale=_clean_text(self.rationale, 600),
            evidence=_str_list(self.evidence)[:4],
            guidance=_clean_text(self.guidance, 900),
            next_verification=_clean_text(self.next_verification, 700),
            required_evidence=_clean_text(self.required_evidence, 600),
            memory_patch=patch,
            skill_signal=skill_signal,
            experience_refs=_str_list(self.experience_refs)[:10],
            primary_hypothesis=_clean_text(self.primary_hypothesis, 500),
            failure_boundary=_clean_text(self.failure_boundary, 260),
            blocked_prerequisite=_clean_text(self.blocked_prerequisite, 500),
            observer_enforcement_state=_clean_text(self.observer_enforcement_state, 120),
            agent_override_reason=_clean_text(self.agent_override_reason, 700),
        )

    @property
    def interrupts(self) -> bool:
        return _verdict_allows_interrupt(self.verdict)

    def signature(self) -> str:
        decision = self.normalised()
        core = "|".join(
            [
                decision.verdict,
                decision.skill_signal,
                decision.rationale,
                ";".join(decision.evidence[:2]),
                decision.guidance,
            ]
        )
        return core[:300]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self.normalised())


def should_inject_decision(decision: ObserverDecision, *, phase: str) -> bool:
    """Only interrupt the main agent for the explicit L/ENV verdict family."""
    decision = decision.normalised()
    if (
        phase == "round"
        and decision.observer_enforcement_state == "strong_evidence"
        and (decision.next_verification or decision.guidance)
    ):
        return True
    if not decision.interrupts:
        return False
    if phase == "tool" and decision.verdict not in {"L1", "L4", "ENV"}:
        return False
    return True


class ObserverAgent:
    """Low-noise Observer built around the OK/WATCH/L1/L2/L3/L4/ENV protocol."""

    def observe_tool_call(
        self,
        *,
        mission: dict[str, Any],
        tool_call_log: list[dict[str, Any]],
        memory: dict[str, Any],
        captured_flags: list[str],
    ) -> ObserverDecision:
        if not tool_call_log:
            return ObserverDecision.none()

        recent = tool_call_log[-12:]
        current = recent[-1]
        tool = str(current.get("tool", ""))
        args = _tool_args_text(current)
        result = _tool_result_text(current)
        combined = f"{tool}\n{args}\n{result}"

        for detector in (
            lambda: self._detect_unsubmitted_flag(combined, captured_flags),
            lambda: self._detect_scope_risk(mission, tool, args),
            lambda: self._detect_skill_tool_issue(recent),
            lambda: self._detect_local_script_error_loop(recent),
            lambda: self._detect_failure_loop(recent),
            lambda: self._detect_low_evidence_execution(recent),
            lambda: self._detect_repetition(recent),
        ):
            decision = detector().normalised()
            if decision.interrupts:
                return decision
        return ObserverDecision.none()

    def review_round(
        self,
        *,
        mission: dict[str, Any],
        memory_before: dict[str, Any],
        memory_after: dict[str, Any],
        tool_call_log: list[dict[str, Any]],
        llm_call_count: int,
        stall_rounds: int,
        captured_flags: list[str],
    ) -> ObserverDecision:
        """Return a rule-level observation; the runtime LLM may refine it."""
        if llm_call_count == 0:
            return ObserverDecision(
                verdict="L2",
                rationale="本轮没有产生有效的模型或工具推进。",
                evidence=["本轮没有 LLM 或工具层面的有效进展"],
                guidance=(
                    "下一步必须调用一个具体探测工具，说明正在验证的假设，并保留原始可观察输出。"
                ),
                required_evidence="一次具体探测得到的原始状态码、响应头、响应体或 stdout/stderr",
            ).normalised()

        if not tool_call_log:
            return ObserverDecision(
                verdict="L2",
                rationale="本轮有模型输出，但没有工具调用。",
                evidence=["LLM 只产生文本，没有可执行验证"],
                guidance="停止纯文本分析。调用一个具体探测工具，并让结果可观察。",
                required_evidence="一个能够确认、否定或收窄当前假设的工具结果",
            ).normalised()

        strong_evidence = self._detect_strong_evidence(tool_call_log, memory_after)
        if strong_evidence.observer_enforcement_state == "strong_evidence":
            return strong_evidence.normalised()

        evidence_gap = self._round_evidence_gap(memory_before, memory_after, tool_call_log)
        if evidence_gap.interrupts:
            return evidence_gap.normalised()

        if len(tool_call_log) >= 4 or stall_rounds > 0:
            return ObserverDecision(
                verdict="WATCH",
                rationale="近期动作较多或已有停滞信号，适合被动观察。",
                evidence=["近期活动可能出现轻微偏移或效率下降"],
                guidance=(
                    "观察后续是否被近期上下文和工具反馈牵引，偏离当前最强证据支撑的线索。"
                ),
            ).normalised()

        return ObserverDecision(verdict="OK", rationale="当前路线没有达到 Observer 级别的问题。").normalised()

    def combine_decisions(self, base: ObserverDecision, refined: ObserverDecision) -> ObserverDecision:
        base = base.normalised()
        refined = refined.normalised()
        if self._hard_interrupt(base) and not refined.interrupts:
            return base
        if base.interrupts and refined.interrupts:
            if VERDICT_PRIORITY[base.verdict] > VERDICT_PRIORITY[refined.verdict]:
                return self._merge_decision(base, refined)
            return self._merge_decision(refined, base)
        return self._merge_decision(refined, base)

    def apply_memory_patch(self, memory: dict[str, Any], patch: dict[str, list[str]]) -> tuple[dict[str, Any], bool]:
        updated = dict(memory)
        changed = False
        limits = {"findings": 20, "leads": 12, "dead_ends": 12}
        for key in MEMORY_PATCH_KEYS:
            incoming = _str_list(patch.get(key, []))
            if not incoming:
                continue
            if key == "dead_ends":
                incoming = normalize_dead_ends(incoming)
            existing = _str_list(updated.get(key, []))
            seen = {item.lower() for item in existing}
            for item in incoming:
                if item.lower() in seen:
                    continue
                existing.append(item)
                seen.add(item.lower())
                changed = True
            updated[key] = existing[-limits[key]:]
        return updated, changed

    def format_injection(self, decision: ObserverDecision) -> str:
        decision = decision.normalised()
        lines = [
            "[RUNTIME_OBSERVER_AUDIT source=observer_agent not_user_request]",
            f"verdict={decision.verdict}({VERDICT_LABELS.get(decision.verdict, decision.verdict)})",
        ]
        if decision.rationale:
            lines.append(f"rationale: {_compact_line(decision.rationale, 320)}")
        if decision.evidence:
            lines.append("evidence: " + " | ".join(_compact_line(item, 220) for item in decision.evidence[:3]))
        next_step = decision.guidance or decision.next_verification
        if next_step:
            lines.append(f"guidance: {_compact_line(next_step, 520)}")
        if decision.next_verification:
            lines.append(f"next_verification: {_compact_line(decision.next_verification, 420)}")
        if decision.required_evidence:
            lines.append(f"required_evidence: {_compact_line(decision.required_evidence, 360)}")
        if decision.observer_enforcement_state:
            lines.append(f"observer_signal: {_compact_line(decision.observer_enforcement_state, 120)}")
        if decision.skill_signal:
            lines.append(f"skill_signal: {_compact_line(decision.skill_signal, 260)}")
        if decision.memory_patch:
            lines.append("memory_patch_applied: yes")
        lines.append(
            "这是 runtime observer 遥测，不是人工指导或用户请求。判断时优先相信直接目标/工具证据。"
        )
        lines.append("[/RUNTIME_OBSERVER_AUDIT]")
        return "\n".join(lines)

    def format_event_content(self, decision: ObserverDecision) -> str:
        decision = decision.normalised()
        parts = [f"verdict={decision.verdict} ({VERDICT_LABELS.get(decision.verdict, decision.verdict)})"]
        if decision.rationale:
            parts.append("rationale:\n" + decision.rationale)
        if decision.evidence:
            parts.append("evidence:\n" + "\n".join(f"- {item}" for item in decision.evidence))
        if decision.guidance:
            parts.append("guidance:\n" + decision.guidance)
        if decision.next_verification:
            parts.append("next_verification:\n" + decision.next_verification)
        if decision.required_evidence:
            parts.append("required_evidence:\n" + decision.required_evidence)
        if decision.failure_boundary:
            parts.append("failure_boundary:\n" + decision.failure_boundary)
        if decision.observer_enforcement_state:
            parts.append("observer_signal:\n" + decision.observer_enforcement_state)
        if decision.skill_signal:
            parts.append("skill_signal:\n" + decision.skill_signal)
        if decision.memory_patch:
            parts.append("memory_patch:\n" + json.dumps(decision.memory_patch, ensure_ascii=False, indent=2))
        if decision.experience_refs:
            parts.append("experience_refs:\n" + "\n".join(f"- {ref}" for ref in decision.experience_refs))
        return "\n\n".join(parts)

    def last_good_lead(self, memory: dict[str, Any]) -> str:
        for key in ("leads", "findings"):
            items = _str_list(memory.get(key, []))
            if items:
                return items[-1]
        return ""

    def _hard_interrupt(self, decision: ObserverDecision) -> bool:
        decision = decision.normalised()
        if decision.verdict in {"L4", "ENV"}:
            return True
        text = " ".join(decision.evidence + [decision.rationale, decision.guidance]).lower()
        return "possible flag" in text or "out-of-scope" in text

    def _merge_decision(self, preferred: ObserverDecision, fallback: ObserverDecision) -> ObserverDecision:
        preferred = preferred.normalised()
        fallback = fallback.normalised()
        return ObserverDecision(
            verdict=preferred.verdict,
            rationale=preferred.rationale or fallback.rationale,
            evidence=preferred.evidence or fallback.evidence,
            guidance=preferred.guidance or fallback.guidance,
            next_verification=preferred.next_verification or fallback.next_verification,
            required_evidence=preferred.required_evidence or fallback.required_evidence,
            memory_patch=preferred.memory_patch or fallback.memory_patch,
            skill_signal=preferred.skill_signal or fallback.skill_signal,
            experience_refs=list(dict.fromkeys(preferred.experience_refs + fallback.experience_refs)),
            primary_hypothesis=preferred.primary_hypothesis or fallback.primary_hypothesis,
            failure_boundary=preferred.failure_boundary or fallback.failure_boundary,
            blocked_prerequisite=preferred.blocked_prerequisite or fallback.blocked_prerequisite,
            observer_enforcement_state=preferred.observer_enforcement_state or fallback.observer_enforcement_state,
            agent_override_reason=preferred.agent_override_reason or fallback.agent_override_reason,
        ).normalised()

    def _detect_unsubmitted_flag(self, text: str, captured_flags: list[str]) -> ObserverDecision:
        flags = [flag for flag in FLAG_RE.findall(text) if flag not in captured_flags]
        if not flags:
            return ObserverDecision.none()
        flag = flags[0]
        return ObserverDecision(
            verdict="L4",
            rationale="工具输出中出现疑似 flag，但尚未提交。",
            evidence=[f"疑似 flag 尚未提交：{flag}"],
            guidance=(
                f"暂停其他动作，验证 `{flag}` 是否来自目标输出。"
                "如果是真实目标证据，下一次工具调用必须 submit_flag。"
            ),
            next_verification=f"验证并提交 {flag}",
            required_evidence="包含该 flag 候选值的目标输出",
        )

    def _detect_scope_risk(self, mission: dict[str, Any], tool: str, args: str) -> ObserverDecision:
        if tool in SCOPE_SAFE_TOOLS:
            return ObserverDecision.none()
        target = str(mission.get("target") or "")
        target_host = re.sub(r"^https?://", "", target).split("/")[0].split(":")[0].strip()
        if not target_host:
            return ObserverDecision.none()
        urls = re.findall(r"https?://([^/\s:]+)", args)
        risky = [host for host in urls if host and target_host not in host and host not in target_host]
        if not risky:
            return ObserverDecision.none()
        return ObserverDecision(
            verdict="L4",
            rationale="执行工具疑似访问了任务范围外的主机。",
            evidence=[f"命令中出现疑似越界主机：{risky[0]}"],
            guidance=(
                f"停止用执行工具访问 `{risky[0]}`。回到范围内目标 `{target}`。"
                "公开资料抓取只能在已有明确 URL 时使用 web_fetch；漏洞资料优先用 knowledge_search/searchsploit。"
            ),
            required_evidence="下一次执行必须指向声明的任务范围",
        )

    def _detect_skill_tool_issue(self, recent: list[dict[str, Any]]) -> ObserverDecision:
        current = recent[-1]
        tool = str(current.get("tool", ""))
        if tool not in SKILL_TOOL_NAMES:
            return ObserverDecision.none()
        result = _tool_result_text(current)
        if not SKILL_ERROR_RE.search(result):
            return ObserverDecision.none()
        return ObserverDecision(
            verdict="L1",
            rationale="Skill 工具调用失败，或没有返回可用 skill 匹配。",
            evidence=[f"{tool} 产生 skill 查找/激活错误"],
            guidance=(
                "停止重复失败的 skill 动作。先检查 skill 工具结果；然后用更具体、基于证据的查询调用 "
                "skill_search，或只激活 skill_search 返回的一个有效 skill id。若无匹配，回到普通工具验证假设。"
            ),
            skill_signal="skill_tool_issue：只能使用返回的 skill id，不要编造 skill id",
            required_evidence="下一次 skill 动作必须展示返回的 skill id，或展示修订后的基于证据的查询",
        )

    def _detect_low_evidence_execution(self, recent: list[dict[str, Any]]) -> ObserverDecision:
        effective = [row for row in recent[-5:] if not self._is_evidence_audit_exempt(row)]
        if len(effective) < 2:
            return ObserverDecision.none()
        weak_recent = [row for row in effective[-2:] if self._is_low_evidence_call(row)]
        if len(weak_recent) < 2:
            return ObserverDecision.none()
        tools = ", ".join(str(row.get("tool", "")) for row in weak_recent)
        return ObserverDecision(
            verdict="L2",
            rationale="近期执行结果缺少具体可观察证据。",
            evidence=[f"最近 2 次执行结果证据强度不足（{tools}）"],
            guidance=(
                "不要相信概括式成功或模糊输出。下一步必须说明假设，执行一次精确验证，并保留原始状态码、响应头、响应体或 stdout/stderr。"
            ),
            required_evidence="能确认、否定或收窄假设的原始状态码、响应头、响应体或 stdout/stderr",
        )

    def _round_evidence_gap(
        self,
        memory_before: dict[str, Any],
        memory_after: dict[str, Any],
        tool_call_log: list[dict[str, Any]],
    ) -> ObserverDecision:
        effective = [row for row in tool_call_log if not self._is_evidence_audit_exempt(row)]
        if len(effective) < 2 or _route_memory_changed(memory_before, memory_after):
            return ObserverDecision.none()
        weak_count = sum(1 for row in effective[-3:] if self._is_low_evidence_call(row))
        has_concrete = any(self._has_concrete_evidence(row) for row in effective[-4:])
        if weak_count < 2 and has_concrete:
            return ObserverDecision.none()
        return ObserverDecision(
            verdict="L2",
            rationale="本轮执行了工具，但没有向记忆增加可信路线证据。",
            evidence=[
                "findings/leads 没有变化",
                "近期输出不足以为当前路线提供具体证据",
            ],
            guidance=(
                "继续前先补齐证据缺口：明确当前假设，运行能确认/否定它的最小验证，并用原始可观察结果更新 findings/leads 或 dead_ends。"
            ),
            required_evidence="记忆必须记录原始可观察结果，或一个可靠 dead end",
        )

    def _detect_strong_evidence(
        self,
        tool_call_log: list[dict[str, Any]],
        memory: dict[str, Any],
    ) -> ObserverDecision:
        recent = [row for row in tool_call_log[-6:] if not self._is_evidence_audit_exempt(row)]
        if not recent:
            return ObserverDecision.none()
        memory_text = " ".join(_str_list(memory.get("leads", [])) + _str_list(memory.get("findings", []))).lower()
        for row in reversed(recent):
            args_text = _tool_args_text(row, limit=1200)
            result_text = _tool_result_text(row, limit=6000)
            for signal, pattern, rationale, guidance, required_evidence in STRONG_EVIDENCE_RULES:
                haystack = result_text
                if signal in {"api_object", "ssrf_internal"}:
                    haystack = f"{args_text}\n{result_text}"
                if not pattern.search(haystack):
                    continue
                if signal in memory_text and any(term in memory_text for term in ("收束", "下一步", "读取", "验证")):
                    return ObserverDecision.none()
                lead = f"[强证据:{signal}] {guidance}"
                return ObserverDecision(
                    verdict="WATCH",
                    rationale=rationale,
                    evidence=[_compact_line(_tool_result_text(row), 260)],
                    guidance=guidance,
                    next_verification=guidance,
                    required_evidence=required_evidence,
                    memory_patch={"leads": [lead]},
                    primary_hypothesis=rationale,
                    observer_enforcement_state="strong_evidence",
                ).normalised()
        return ObserverDecision.none()

    def _is_evidence_audit_exempt(self, row: dict[str, Any]) -> bool:
        return str(row.get("tool", "")) in EVIDENCE_AUDIT_EXEMPT_TOOLS

    def _is_low_evidence_call(self, row: dict[str, Any]) -> bool:
        result = _tool_result_text(row).strip()
        if not result:
            return True
        if FAILURE_RE.search(result):
            return False
        if self._has_concrete_evidence(row):
            return False
        cleaned = _clean_text(result, 260).strip()
        if len(cleaned) < 80:
            return True
        if VAGUE_RESULT_RE.match(cleaned):
            return True
        guidance_words = ("should", "could", "maybe", "recommend", "suggest", "next step", "analysis")
        lowered = cleaned.lower()
        return any(word in lowered for word in guidance_words)

    def _has_concrete_evidence(self, row: dict[str, Any]) -> bool:
        result = _tool_result_text(row)
        if FLAG_RE.search(result):
            return True
        if EVIDENCE_MARKER_RE.search(result):
            return True
        tool = str(row.get("tool", ""))
        if tool in {"bash_exec", "python_exec", "web_fetch"} and len(result.strip()) >= 180:
            return True
        return False

    def _detect_repetition(self, recent: list[dict[str, Any]]) -> ObserverDecision:
        if len(recent) < 3:
            return ObserverDecision.none()
        current = recent[-1]
        current_sig = f"{current.get('tool')}:{_normalise_arg(_tool_args_text(current))}"
        repeats = 0
        for row in recent[-6:]:
            sig = f"{row.get('tool')}:{_normalise_arg(_tool_args_text(row))}"
            if sig == current_sig or _similar(sig, current_sig):
                repeats += 1
        if repeats < 3:
            return ObserverDecision.none()
        return ObserverDecision(
            verdict="L4",
            rationale="主 agent 重复了同类工具/输入，但没有获得新证据。",
            evidence=["同一工具和相似参数至少重复 3 次"],
            guidance=(
                "停止重复同一工具/输入。下一步必须改变假设：收窄目标、改变输入点、检查原始响应/状态，或回到最具体线索。"
            ),
            required_evidence="来自已改变假设或输入点的新原始证据",
        )

    def _detect_failure_loop(self, recent: list[dict[str, Any]]) -> ObserverDecision:
        if len(recent) < 3:
            return ObserverDecision.none()
        failures = [
            row for row in recent[-3:]
            if FAILURE_RE.search(_tool_result_text(row))
        ]
        if len(failures) < 3:
            return ObserverDecision.none()
        return ObserverDecision(
            verdict="ENV",
            rationale="近期工具疑似被失败、空输出或环境配置错误阻塞。",
            evidence=["最近 3 次工具结果表现为失败、空响应或配置错误"],
            guidance=(
                "停止在失败路径上叠 payload。下一步必须打印原始状态、响应头/响应体或 stderr，定位失败原因，再运行一个更小的验证探针。"
            ),
            required_evidence="原始失败细节，以及一个更小的环境/目标可达性检查",
        )

    def _detect_local_script_error_loop(self, recent: list[dict[str, Any]]) -> ObserverDecision:
        if len(recent) < 2:
            return ObserverDecision.none()
        pattern = re.compile(r"SyntaxError|unterminated string|unexpected EOF|shell quoting|unexpected end of file", re.I)
        failures = [
            row for row in recent[-3:]
            if str(row.get("tool", "")) in {"bash_exec", "python_exec"}
            and pattern.search(_tool_result_text(row))
        ]
        if len(failures) < 2:
            return ObserverDecision.none()
        return ObserverDecision(
            verdict="L1",
            rationale="本地脚本或 shell 引号错误反复出现，尚未产生目标证据。",
            evidence=["反复出现本地 SyntaxError/引号错误"],
            guidance=(
                "停止重试畸形内联代码。使用最小 Python heredoc 或保存短脚本，再从一次定向验证中打印原始状态/stdout/stderr。"
            ),
            required_evidence="本地脚本成功执行，以及原始目标/工具输出",
        )

    def audit_override(
        self,
        *,
        pending_decision: ObserverDecision,
        next_tool_calls: list[dict[str, Any]],
        memory_before: dict[str, Any],
        memory_after: dict[str, Any],
        agent_override_reason: str,
    ) -> ObserverDecision:
        pending = pending_decision.normalised()
        calls = next_tool_calls or []
        if not pending.interrupts and pending.observer_enforcement_state != "strong_evidence":
            return ObserverDecision(verdict="OK", observer_enforcement_state="resolved").normalised()

        if _route_memory_changed(memory_before, memory_after) or any(self._has_concrete_evidence(row) for row in calls):
            return ObserverDecision(
                verdict="OK",
                rationale="待处理 Observer 建议已被新证据或记忆变化覆盖。",
                observer_enforcement_state="resolved",
            ).normalised()

        repeated = self._detect_repetition(calls).normalised() if calls else ObserverDecision.none()
        if repeated.interrupts:
            repeated.agent_override_reason = _clean_text(agent_override_reason, 700)
            return repeated.normalised()

        return ObserverDecision(
            verdict="L3",
            rationale="主 agent 在解决待处理 Observer 建议前改变了方向。",
            evidence=["待处理 Observer 建议没有被新证据解决"],
            guidance=(
                pending.next_verification
                or pending.guidance
                or "改变方向前先解决上一条 Observer 验证要求。"
            ),
            next_verification=pending.next_verification,
            required_evidence=pending.required_evidence,
            observer_enforcement_state="pending",
            agent_override_reason=_clean_text(agent_override_reason, 700),
        ).normalised()
