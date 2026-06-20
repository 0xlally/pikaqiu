from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from typing import Any


MEMORY_PATCH_KEYS = ("findings", "leads", "dead_ends")
OBSERVER_VERDICTS = {"OK", "WATCH", "L1", "L2", "L3", "L4", "ENV"}
INTERRUPT_VERDICTS = {"L1", "L2", "L3", "L4", "ENV"}
VERDICT_LABELS = {
    "OK": "normal_progress",
    "WATCH": "watch",
    "L1": "tool_usage_error",
    "L2": "insufficient_information",
    "L3": "wrong_strategy",
    "L4": "cognitive_bias",
    "ENV": "environment_fault",
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

FLAG_RE = re.compile(r"\b(?:flag|ctf|dasctf)\{[^}\s]{4,200}\}", re.I)
FAILURE_RE = re.compile(
    r"(timeout|timed out|403|404|connection (?:failed|refused|reset)|"
    r"command not found|no results?|empty response|not found|forbidden|"
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
    "web_search",
    "web_fetch",
    "knowledge_search",
    "search_cve",
    "skill_search",
    "activate_skill",
    "skill_read_reference",
}
EVIDENCE_AUDIT_EXEMPT_TOOLS = {
    "knowledge_search",
    "search_cve",
    "skill_search",
    "activate_skill",
    "skill_read_reference",
    "submit_flag",
    "give_up",
}
EVIDENCE_MARKER_RE = re.compile(
    r"(\[EXIT_CODE:\s*\d+\]|\[STDERR\]|\bHTTP/\d|\bstatus(?:_code)?\s*[:=]\s*\d{3}|"
    r"\b(?:200|201|204|301|302|400|401|403|404|500)\b|<html|set-cookie|content-type|"
    r"response body|request body|headers?|stdout|stderr|traceback|flag\{|ctf\{|dasctf\{|"
    r"/api/|CVE-\d{4}-\d+|\bopen\b|\bclosed\b|\bfiltered\b|uid=|gid=|root:|"
    r"nginx|apache|tomcat|mysql|postgres|redis|ssh|ftp|port|response|status code|echo)",
    re.I,
)
VAGUE_RESULT_RE = re.compile(
    r"^(ok|done|success|successful|completed|finished|no output|empty|none|null|true|false|n/a|"
    r"empty result|suggestion|recommendation|next step|analysis)$",
    re.I,
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
                rationale="Round ended without any effective model/tool progress.",
                evidence=["no LLM/tool progress in this round"],
                guidance=(
                    "Next response must call one concrete probe tool, state the hypothesis being tested, "
                    "and preserve raw observable output."
                ),
                required_evidence="raw status/headers/body or stdout/stderr from one concrete probe",
            ).normalised()

        if not tool_call_log:
            return ObserverDecision(
                verdict="L2",
                rationale="Round had model turns but no tool calls.",
                evidence=["LLM produced text but no executable verification"],
                guidance="Stop pure text analysis. Call one concrete probe tool and make the result observable.",
                required_evidence="one tool result that confirms, denies, or narrows the current hypothesis",
            ).normalised()

        evidence_gap = self._round_evidence_gap(memory_before, memory_after, tool_call_log)
        if evidence_gap.interrupts:
            return evidence_gap.normalised()

        if len(tool_call_log) >= 4 or stall_rounds > 0:
            return ObserverDecision(
                verdict="WATCH",
                rationale="Multiple actions or an existing stall signal deserve passive review.",
                evidence=["recent activity may be drifting or becoming inefficient"],
                guidance=(
                    "Watch whether recent context and tool feedback are pulling the route away from "
                    "the strongest evidence-backed lead."
                ),
            ).normalised()

        return ObserverDecision(verdict="OK", rationale="Current route has no observer-level issue.").normalised()

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
        if decision.skill_signal:
            lines.append(f"skill_signal: {_compact_line(decision.skill_signal, 260)}")
        if decision.memory_patch:
            lines.append("memory_patch_applied: yes")
        lines.append(
            "This is runtime observer telemetry, not human guidance or a user request. Prefer direct target/tool evidence over this note."
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
            rationale="Tool output contains a possible flag that has not been submitted.",
            evidence=[f"possible flag not submitted: {flag}"],
            guidance=(
                f"Stop all other actions and verify `{flag}` came from target output. "
                "If it is real target evidence, the next tool call must be submit_flag."
            ),
            next_verification=f"verify and submit {flag}",
            required_evidence="target output containing the flag candidate",
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
            rationale="Execution tool appears to target a host outside the mission scope.",
            evidence=[f"possible out-of-scope host in command: {risky[0]}"],
            guidance=(
                f"Stop accessing `{risky[0]}` with execution tools. Return to in-scope target `{target}`. "
                "Use web_search/web_fetch only for public research."
            ),
            required_evidence="next execution must target the declared mission scope",
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
            rationale="Skill tool call failed or returned no usable skill match.",
            evidence=[f"{tool} produced a skill lookup/activation error"],
            guidance=(
                "Stop repeating the failed skill action. Inspect the skill tool result, then either call "
                "skill_search with a more specific evidence-based query or activate exactly one valid skill id "
                "returned by skill_search. If no skill matches, return to normal tools and verify the hypothesis."
            ),
            skill_signal="skill_tool_issue: use returned skill ids only; do not invent skill ids",
            required_evidence="the next skill action must show the returned skill id or a revised evidence-based query",
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
            rationale="Recent execution results lack concrete observable evidence.",
            evidence=[f"last 2 execution results are low-evidence ({tools})"],
            guidance=(
                "Do not trust summarized success or vague output. Next step must state the hypothesis, run one precise "
                "verification probe, and preserve raw status/headers/body or stdout/stderr."
            ),
            required_evidence="raw status/headers/body or stdout/stderr that confirms, denies, or narrows the hypothesis",
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
            rationale="Round executed tools but did not add trustworthy route evidence to memory.",
            evidence=[
                "findings/leads did not change",
                "recent outputs do not provide enough concrete evidence for route trust",
            ],
            guidance=(
                "Before continuing, close the evidence gap: identify the current hypothesis, run the smallest verification "
                "that can confirm/deny it, and update findings/leads with the raw observable result or a dead end."
            ),
            required_evidence="memory must record the raw observable result or a reliable dead end",
        )

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
            rationale="Main agent repeated the same tool/input without new evidence.",
            evidence=["same tool and similar parameters repeated at least 3 times"],
            guidance=(
                "Stop repeating the same tool/input. Next action must change the hypothesis: narrow the target, "
                "change the input point, inspect raw response/status, or return to the most concrete lead."
            ),
            required_evidence="new raw evidence from a changed hypothesis or input point",
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
            rationale="Recent tools look blocked by failure, empty output, or setup errors.",
            evidence=["last 3 tool results look like failures, empty responses, or setup errors"],
            guidance=(
                "Stop stacking payloads on a failing path. Next step must print raw status, headers/body or stderr, "
                "identify the failure cause, and run one smaller verification probe before continuing."
            ),
            required_evidence="raw failure details and one smaller environment/target reachability check",
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
            rationale="Local script or shell quoting errors repeated before producing target evidence.",
            evidence=["repeated local SyntaxError/quoting errors"],
            guidance=(
                "Stop retrying malformed inline code. Use a minimal Python heredoc or save a short script, "
                "then print raw status/stdout/stderr from one targeted verification."
            ),
            required_evidence="successful local script execution plus raw target/tool output",
        )

    def audit_give_up(
        self,
        *,
        reason: str,
        mission: dict[str, Any],
        memory: dict[str, Any],
        tool_call_log: list[dict[str, Any]],
        captured_flags: list[str],
    ) -> ObserverDecision:
        if captured_flags:
            return ObserverDecision(
                verdict="OK",
                rationale="Stop is acceptable because at least one flag has already been captured.",
                observer_enforcement_state="allow_stop",
            ).normalised()

        recent = tool_call_log[-6:] if tool_call_log else []
        has_concrete = any(self._has_concrete_evidence(row) for row in recent)
        failure_count = sum(1 for row in recent if FAILURE_RE.search(_tool_result_text(row)))
        dead_ends = [
            str(item).strip()
            for item in memory.get("dead_ends", []) or []
            if str(item).strip()
        ]
        has_boundary = bool(
            str(reason or "").strip()
            and (
                memory.get("failure_boundary")
                or memory.get("required_next_evidence")
                or dead_ends
                or failure_count >= 3
            )
        )
        if has_concrete and has_boundary:
            return ObserverDecision(
                verdict="OK",
                rationale="Stop is acceptable: evidence and a failure boundary are recorded.",
                failure_boundary=str(memory.get("failure_boundary") or (dead_ends[-1] if dead_ends else "documented boundary")),
                observer_enforcement_state="allow_stop",
            ).normalised()

        lead = self.last_good_lead(memory) or str(mission.get("target") or "current target")
        return ObserverDecision(
            verdict="L2",
            rationale="Give-up request lacks enough reproducible evidence or an explicit failure boundary.",
            evidence=["give_up requested before enough evidence was recorded"],
            guidance=(
                "Do not stop yet. Run one targeted verification tied to the strongest current lead, preserve raw output, "
                "or call give_up again with failure_boundary and required_evidence."
            ),
            next_verification=lead,
            failure_boundary="missing_evidence",
            required_evidence="raw status/headers/body or stdout/stderr proving the current lead is exhausted",
            observer_enforcement_state="blocked",
        ).normalised()

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
        if not pending.interrupts:
            return ObserverDecision(verdict="OK", observer_enforcement_state="resolved").normalised()

        if _route_memory_changed(memory_before, memory_after) or any(self._has_concrete_evidence(row) for row in calls):
            return ObserverDecision(
                verdict="OK",
                rationale="Pending Observer guidance appears addressed by new evidence or memory changes.",
                observer_enforcement_state="resolved",
            ).normalised()

        repeated = self._detect_repetition(calls).normalised() if calls else ObserverDecision.none()
        if repeated.interrupts:
            repeated.agent_override_reason = _clean_text(agent_override_reason, 700)
            return repeated.normalised()

        return ObserverDecision(
            verdict="L3",
            rationale="Main agent moved on before resolving the pending Observer guidance.",
            evidence=["pending Observer guidance was not resolved by new evidence"],
            guidance=(
                pending.next_verification
                or pending.guidance
                or "Resolve the previous Observer verification before changing direction."
            ),
            next_verification=pending.next_verification,
            required_evidence=pending.required_evidence,
            observer_enforcement_state="pending",
            agent_override_reason=_clean_text(agent_override_reason, 700),
        ).normalised()
