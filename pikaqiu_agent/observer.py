from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from typing import Any


SEVERITIES = {"none", "info", "warn", "critical"}
STATES = {"progressing", "slow", "stalled", "repeated", "off_track", "risky"}
OBSERVER_ACTIONS = {"no_action", "steer", "memory_patch", "skill_signal"}
INTERVENTIONS = {
    "none",
    "steer",
    "follow_up",
    "rollback_steer",
    "memory_sync",
    "skill_card",
}
MEMORY_PATCH_KEYS = ("findings", "leads", "dead_ends", "next_focus")

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
    r"completed|success|no output|empty result|suggestion|recommendation|next step|analysis)$",
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


def _json_excerpt(value: Any, limit: int = 3000) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)[:limit]


def _route_memory_changed(before: dict[str, Any], after: dict[str, Any]) -> bool:
    for key in ("findings", "leads", "next_focus"):
        if _str_list((before or {}).get(key, [])) != _str_list((after or {}).get(key, [])):
            return True
    return False


def _tool_args_text(row: dict[str, Any], *, limit: int | None = None) -> str:
    text = str(row.get("args_full") or row.get("args_summary") or "")
    return text if limit is None else text[:limit]


def _tool_result_text(row: dict[str, Any], *, limit: int | None = None) -> str:
    text = str(row.get("result_full") or row.get("result_observer") or row.get("result_summary") or "")
    return text if limit is None else text[:limit]


def _tool_call_prompt_view(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool": row.get("tool"),
        "args_summary": _tool_args_text(row, limit=300),
        "result_summary": _tool_result_text(row, limit=800),
        "result_len": row.get("result_len"),
        "exit_code": row.get("exit_code"),
    }


@dataclass
class ObserverDecision:
    severity: str = "none"
    state: str = "progressing"
    intervention: str = "none"
    action: str = "no_action"
    route_assessment: str = ""
    problems: list[str] = field(default_factory=list)
    steer_message: str = ""
    memory_patch: dict[str, list[str]] = field(default_factory=dict)
    # Kept for API/UI compatibility. This is now a freeform skill signal/query,
    # not a hard-coded skill chosen by Python rules.
    skill_card: str = "none"
    skill_instruction: str = ""
    skill_signal: str = ""
    experience_refs: list[str] = field(default_factory=list)
    visible_summary: str = ""

    @classmethod
    def none(cls) -> "ObserverDecision":
        return cls()

    def normalised(self) -> "ObserverDecision":
        severity = self.severity if self.severity in SEVERITIES else "warn"
        state = self.state if self.state in STATES else "slow"
        intervention = self.intervention if self.intervention in INTERVENTIONS else "steer"
        action = self.action if self.action in OBSERVER_ACTIONS else "steer"
        if action == "no_action" and intervention != "none":
            if intervention == "memory_sync":
                action = "memory_patch"
            elif intervention == "skill_card":
                action = "skill_signal"
            else:
                action = "steer"
        if intervention == "none" and action != "no_action":
            intervention = {
                "memory_patch": "memory_sync",
                "skill_signal": "skill_card",
            }.get(action, "steer")
        skill_card = _clean_text(self.skill_card, 180) or "none"
        if skill_card.lower() in {"", "none", "null", "false"}:
            skill_card = "none"
        skill_signal = _clean_text(self.skill_signal or ("" if skill_card == "none" else skill_card), 600)
        patch: dict[str, list[str]] = {}
        raw_patch = self.memory_patch if isinstance(self.memory_patch, dict) else {}
        for key in MEMORY_PATCH_KEYS:
            vals = _str_list(raw_patch.get(key, []))
            if vals:
                patch[key] = vals[:8]
        if action == "no_action":
            if patch:
                action = "memory_patch"
            elif skill_signal:
                action = "skill_signal"
            elif self.steer_message:
                action = "steer"
        if intervention == "none" and action != "no_action":
            intervention = {
                "memory_patch": "memory_sync",
                "skill_signal": "skill_card",
            }.get(action, "steer")
        return ObserverDecision(
            severity=severity,
            state=state,
            intervention=intervention,
            action=action,
            route_assessment=_clean_text(self.route_assessment, 500),
            problems=_str_list(self.problems)[:4],
            steer_message=_clean_text(self.steer_message, 700),
            memory_patch=patch,
            skill_card=skill_card if not skill_signal else skill_signal,
            skill_instruction=_clean_text(self.skill_instruction, 700),
            skill_signal=skill_signal,
            experience_refs=_str_list(self.experience_refs)[:10],
            visible_summary=_clean_text(self.visible_summary, 360),
        )

    @property
    def actionable(self) -> bool:
        return self.action != "no_action" or self.intervention != "none" or bool(
            self.steer_message or self.memory_patch or self.skill_card != "none" or self.skill_signal
        )

    @property
    def needs_llm(self) -> bool:
        return self.severity in {"warn", "critical"} and self.intervention in {
            "steer",
            "follow_up",
            "rollback_steer",
            "memory_sync",
            "skill_card",
        }

    def signature(self) -> str:
        core = "|".join(
            [self.severity, self.state, self.intervention, self.action, self.skill_card, ";".join(self.problems[:2])]
        )
        return core[:300]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self.normalised())


def should_inject_decision(decision: ObserverDecision, *, phase: str) -> bool:
    """Decide whether an Observer decision should enter the main-agent context."""
    decision = decision.normalised()
    if not decision.actionable:
        return False
    if phase == "tool":
        return decision.action == "steer" and decision.severity in {"warn", "critical"}
    if decision.severity == "critical":
        return True
    if phase == "round" and decision.state in {"stalled", "repeated", "risky"}:
        return True
    if phase == "round" and decision.intervention in {"follow_up", "rollback_steer"}:
        return True
    return False


class ObserverAgent:
    """Rule-triggered observer with LLM-owned progress, memory, and skill judgement."""

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
            if decision.actionable:
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
        """Return a lightweight trigger; the LLM decides progress and memory value."""
        if llm_call_count == 0:
            return ObserverDecision(
                severity="warn",
                state="stalled",
                intervention="follow_up",
                problems=["round ended without any model/tool progress"],
                steer_message=(
                    "This round produced no effective action. Next response must call a concrete tool, "
                    "state the hypothesis being tested, and print raw observable output."
                ),
            ).normalised()

        if not tool_call_log:
            return ObserverDecision(
                severity="warn",
                state="stalled",
                intervention="follow_up",
                problems=["round had LLM turns but no tool calls"],
                steer_message=(
                    "Stop pure text analysis. Call one concrete probe tool and make the result observable."
                ),
            ).normalised()

        evidence_gap = self._round_evidence_gap(memory_before, memory_after, tool_call_log)
        if evidence_gap.actionable:
            return evidence_gap.normalised()

        if len(tool_call_log) >= 4 or stall_rounds > 0:
            return ObserverDecision(
                severity="warn",
                state="slow",
                intervention="steer",
                problems=[
                    "round needs observer LLM review: multiple actions or existing stall signal",
                    "AI must decide whether the results are progress, repetition, off-track, memory-worthy, or skill-worthy",
                ],
                steer_message=(
                    "Observer review required. Classify the last actions using the behavior taxonomy and /experience route rules, "
                    "then tell the main agent exactly what to stop doing and what concrete evidence-backed step to do next."
                ),
            ).normalised()

        return ObserverDecision(
            severity="info",
            state="progressing",
            intervention="none",
            problems=[],
        ).normalised()

    def normalize_llm_decision(
        self,
        payload: dict[str, Any],
        *,
        fallback: ObserverDecision,
        raw_text: str = "",
    ) -> ObserverDecision:
        if not isinstance(payload, dict) or not payload:
            patched = fallback.normalised()
            if raw_text.strip():
                patched.steer_message = raw_text.strip()[:1600]
            return patched.normalised()

        decision = ObserverDecision(
            severity=str(payload.get("severity") or fallback.severity),
            state=str(payload.get("state") or payload.get("progress_state") or fallback.state),
            intervention=str(payload.get("intervention") or fallback.intervention),
            action=str(payload.get("action") or fallback.action),
            route_assessment=str(payload.get("route_assessment") or fallback.route_assessment),
            problems=_str_list(payload.get("problems") or fallback.problems),
            steer_message=str(payload.get("steer_message") or payload.get("recommendation") or fallback.steer_message),
            memory_patch=payload.get("memory_patch") if isinstance(payload.get("memory_patch"), dict) else fallback.memory_patch,
            skill_card=str(
                payload.get("skill_card")
                or payload.get("skill_hint")
                or payload.get("skill_query")
                or payload.get("skill_signal")
                or fallback.skill_card
            ),
            skill_instruction=str(
                payload.get("skill_instruction")
                or payload.get("skill_guidance")
                or fallback.skill_instruction
            ),
            skill_signal=str(payload.get("skill_signal") or fallback.skill_signal),
            experience_refs=_str_list(payload.get("experience_refs") or fallback.experience_refs),
            visible_summary=str(payload.get("visible_summary") or fallback.visible_summary),
        ).normalised()

        if fallback.problems and not decision.problems:
            decision.problems = fallback.problems
        return decision.normalised()

    def combine_decisions(self, base: ObserverDecision, refined: ObserverDecision) -> ObserverDecision:
        base = base.normalised()
        refined = refined.normalised()
        if not refined.actionable:
            if base.severity == "critical" and base.actionable:
                return base
            return refined
        if base.severity == "critical" and refined.severity != "critical":
            refined.severity = "critical"
        if base.problems and not refined.problems:
            refined.problems = base.problems
        return refined.normalised()

    def merge_rule_and_llm_decisions(self, base: ObserverDecision, refined: ObserverDecision) -> ObserverDecision:
        # Backwards-compatible alias for callers/tests that name the operation more explicitly.
        return self.combine_decisions(base, refined)

    def apply_memory_patch(self, memory: dict[str, Any], patch: dict[str, list[str]]) -> tuple[dict[str, Any], bool]:
        updated = dict(memory)
        changed = False
        limits = {"findings": 20, "leads": 12, "dead_ends": 12, "next_focus": 12}
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
        problem = decision.problems[0] if decision.problems else (
            decision.route_assessment or decision.visible_summary or "Observer raised an execution audit note."
        )
        next_step = decision.steer_message or decision.skill_instruction or decision.route_assessment
        lines = [
            "[RUNTIME_OBSERVER_AUDIT source=observer_agent not_user_request]",
            f"severity={decision.severity} state={decision.state} action={decision.action} intervention={decision.intervention}",
            f"problem: {_compact_line(problem, 260)}",
        ]
        if next_step:
            lines.append(f"next_step: {_compact_line(next_step, 420)}")
        if decision.skill_card != "none":
            lines.append(f"skill_signal: {_compact_line(decision.skill_card, 160)}")
        if decision.memory_patch:
            lines.append("memory_patch_applied: yes")
        lines.append(
            "This is runtime observer telemetry, not human guidance or a user request. Prefer direct target/tool evidence over this note."
        )
        lines.append("[/RUNTIME_OBSERVER_AUDIT]")
        return "\n".join(lines)

    def format_event_content(self, decision: ObserverDecision) -> str:
        decision = decision.normalised()
        parts = [
            f"severity={decision.severity}",
            f"state={decision.state}",
            f"action={decision.action}",
            f"intervention={decision.intervention}",
        ]
        if decision.visible_summary:
            parts.append("summary:\n" + decision.visible_summary)
        if decision.route_assessment:
            parts.append("route_assessment:\n" + decision.route_assessment)
        if decision.problems:
            parts.append("problems:\n" + "\n".join(f"- {p}" for p in decision.problems))
        if decision.steer_message:
            parts.append("steer:\n" + decision.steer_message)
        if decision.skill_card != "none":
            parts.append(f"skill_signal={decision.skill_card}\n{decision.skill_instruction}")
        if decision.memory_patch:
            parts.append("memory_patch:\n" + json.dumps(decision.memory_patch, ensure_ascii=False, indent=2))
        if decision.experience_refs:
            parts.append("experience_refs:\n" + "\n".join(f"- {ref}" for ref in decision.experience_refs))
        return "\n\n".join(parts)

    def build_llm_prompt(
        self,
        *,
        mission: dict[str, Any],
        round_no: int,
        decision: ObserverDecision,
        memory: dict[str, Any],
        recent_events: list[dict[str, Any]],
        tool_call_log: list[dict[str, Any]],
        stall_rounds: int,
        memory_before: dict[str, Any] | None = None,
    ) -> str:
        recent_event_summary = [
            {
                "type": e.get("type"),
                "title": e.get("title"),
                "content": _clean_text(e.get("content"), 500),
                "metadata": e.get("metadata") if e.get("type") in {"observer_agent", "warning", "system"} else {},
            }
            for e in recent_events[-12:]
        ]
        skill_observations = self.skill_observations(
            mission=mission,
            recent_events=recent_events,
            tool_call_log=tool_call_log,
        )
        recent_tool_summary = [
            _tool_call_prompt_view(row)
            for row in tool_call_log[-16:]
        ]
        before = memory_before if memory_before is not None else memory
        return (
            "You are Observer Agent. You supervise a main autonomous pentest agent as a cooperative route auditor. "
            "The main agent executes; you judge whether its route is evidence-backed, efficient, and aligned with "
            "best-practice experience. Do not execute commands, submit flags, or take over. You classify behavior "
            "and send a concrete steer only when it will improve the next action.\n\n"
            "Output JSON only with fields: severity, state, intervention, problems, steer_message, "
            "memory_patch, skill_card, skill_instruction.\n"
            f"Allowed severity={sorted(SEVERITIES)}; state={sorted(STATES)}; "
            f"intervention={sorted(INTERVENTIONS)}.\n"
            "skill_card is NOT a fixed enum. Use 'none', an exact skill id already returned/activated, "
            "or a concise skill_search query based on evidence. Do not invent skill ids.\n\n"
            "Behavior taxonomy:\n"
            "- repeated: same or very similar tool, command, URL, payload, wordlist, exploit, or skill query is tried repeatedly "
            "without a changed hypothesis or new observable evidence; repeated activation of the same invalid skill also counts.\n"
            "- stalled/idle: no tool calls, pure text loops, three consecutive timeouts/empty/403/404/connection failures/"
            "command-not-found results, or many probes whose outputs do not answer the stated hypothesis.\n"
            "- off_track: the agent leaves scope, ignores a concrete finding/lead, keeps broad scanning after a specific "
            "attack surface appears, uses a skill that does not match the evidence, or continues after a skill error "
            "without correcting the query/id.\n"
            "- risky: possible flag not submitted, out-of-scope target, destructive/irreversible action, or behavior that "
            "can corrupt the run state.\n"
            "- memory_sync: only if tool output contains concrete useful evidence missing from memory_after. "
            "Useful evidence can be a credential, route, parameter, product/version, confirmed vulnerability, exploit output, "
            "flag candidate, reliable dead end, or precise next focus. You decide this semantically; Python rules do not filter it.\n"
            "- skill judgement: inspect skill_search, activate_skill, skill_read_reference, enabled skills, and skill errors. "
            "If a skill seems needed but was not called, tell the main agent to call skill_search with an exact evidence-based query. "
            "If activation failed/no match, tell it to use returned IDs or rewrite the query. If a skill is active but ignored, "
            "tell it to follow that active skill or read required references.\n\n"
            "steer_message requirements: explicitly say what to stop, why it is a problem, what exact next action to take, "
            "and what output/evidence the main agent must print or verify. Keep it short but operational.\n\n"
            f"mission={_json_excerpt(mission, 1600)}\n"
            f"round_no={round_no} stall_rounds={stall_rounds}\n"
            f"rule_trigger={_json_excerpt(decision.to_dict(), 1600)}\n"
            f"memory_before={_json_excerpt(before, 3000)}\n"
            f"memory_after={_json_excerpt(memory, 3000)}\n"
            f"recent_tool_calls={_json_excerpt(recent_tool_summary, 6500)}\n"
            f"skill_observations={_json_excerpt(skill_observations, 2200)}\n"
            f"recent_events={_json_excerpt(recent_event_summary, 4500)}\n"
        )

    def skill_observations(
        self,
        *,
        mission: dict[str, Any],
        recent_events: list[dict[str, Any]] | None = None,
        tool_call_log: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        calls = tool_call_log or []
        events = recent_events or []
        skill_calls = [
            {
                "tool": row.get("tool"),
                "args_summary": _tool_args_text(row, limit=300),
                "result_summary": _tool_result_text(row, limit=500),
                "result_len": row.get("result_len"),
                "exit_code": row.get("exit_code"),
            }
            for row in calls
            if row.get("tool") in SKILL_TOOL_NAMES
        ]
        failed_skill_calls = [
            row for row in skill_calls
            if SKILL_ERROR_RE.search(_tool_result_text(row))
        ]
        skill_events = [
            {
                "type": event.get("type"),
                "title": event.get("title"),
                "content": _clean_text(event.get("content"), 500),
            }
            for event in events[-20:]
            if "skill" in str(event.get("title", "")).lower()
            or "skill" in str(event.get("content", "")).lower()
        ]
        return {
            "selected_skills": _str_list(mission.get("skills", [])),
            "activated_skills": _str_list(mission.get("activated_skills", [])),
            "skill_tool_call_count": len(skill_calls),
            "skill_calls": skill_calls[-8:],
            "failed_skill_calls": failed_skill_calls[-5:],
            "skill_events": skill_events[-6:],
            "skill_search_called": any(row.get("tool") == "skill_search" for row in skill_calls),
            "activate_skill_called": any(row.get("tool") == "activate_skill" for row in skill_calls),
        }

    def last_good_lead(self, memory: dict[str, Any]) -> str:
        for key in ("next_focus", "leads", "findings"):
            items = _str_list(memory.get(key, []))
            if items:
                return items[-1]
        return ""

    def _detect_unsubmitted_flag(self, text: str, captured_flags: list[str]) -> ObserverDecision:
        flags = [flag for flag in FLAG_RE.findall(text) if flag not in captured_flags]
        if not flags:
            return ObserverDecision.none()
        flag = flags[0]
        return ObserverDecision(
            severity="critical",
            state="risky",
            intervention="steer",
            problems=[f"tool output contains possible flag that has not been submitted: {flag}"],
            steer_message=(
                f"Stop all other actions and verify `{flag}` came from target output. "
                "If it is real target evidence, the next tool call must be submit_flag."
            ),
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
            severity="critical",
            state="risky",
            intervention="steer",
            problems=[f"possible out-of-scope host in command: {risky[0]}"],
            steer_message=(
                f"Stop accessing `{risky[0]}` with execution tools. Return to in-scope target `{target}`. "
                "Use web_search/web_fetch only for public research."
            ),
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
            severity="warn",
            state="off_track",
            intervention="skill_card",
            problems=[f"{tool} appears to have failed or returned no usable skill match"],
            steer_message=(
                "Stop repeating the failed skill action. Inspect the skill tool result, then either "
                "call skill_search with a more specific evidence-based query or activate exactly one valid "
                "skill id returned by skill_search. If no skill matches, return to normal tools and verify the hypothesis."
            ),
            skill_card="skill_tool_issue",
            skill_instruction="Observe skill_search/activate_skill results; do not invent or hard-code skill ids.",
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
            severity="warn",
            state="slow",
            intervention="steer",
            problems=[f"last 2 execution results lack concrete observable evidence ({tools})"],
            steer_message=(
                "Do not trust summarized success or vague output. Next step must state the hypothesis, run one precise "
                "verification probe, and preserve raw status/headers/body or stdout/stderr so Observer can judge progress."
            ),
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
            severity="warn",
            state="slow",
            intervention="steer",
            problems=[
                "round executed tools but did not add findings/leads/next_focus",
                "recent outputs do not provide enough concrete evidence for route trust",
            ],
            steer_message=(
                "Before continuing, close the evidence gap: identify the current hypothesis, run the smallest verification "
                "that can confirm/deny it, and update findings/leads/next_focus with the raw observable result or a dead end."
            ),
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
            severity="warn",
            state="repeated",
            intervention="steer",
            problems=["same tool and similar parameters repeated at least 3 times"],
            steer_message=(
                "Stop repeating the same tool/input. Next action must change the hypothesis: narrow the target, "
                "change the input point, inspect raw response/status, or return to the most concrete lead."
            ),
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
            severity="warn",
            state="stalled",
            intervention="follow_up",
            problems=["last 3 tool results look like failures, empty responses, or setup errors"],
            steer_message=(
                "Stop stacking payloads on a failing path. Next step must print raw status, headers/body or stderr, "
                "identify the failure cause, and run one smaller verification probe before continuing."
            ),
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
            severity="warn",
            state="stalled",
            intervention="steer",
            problems=["local script or shell quoting errors repeated before producing target evidence"],
            steer_message=(
                "Stop retrying malformed inline code. Use a minimal Python heredoc or save a short script, "
                "then print raw status/stdout/stderr from one targeted verification."
            ),
        )
