from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from pikaqiu_agent.config import AgentSettings
from pikaqiu_agent.llm_client import LLMClient
from pikaqiu_agent.observer import (
    MEMORY_PATCH_KEYS,
    ObserverAgent,
    ObserverDecision,
    SEVERITIES,
    STATES,
)
from pikaqiu_agent.skill_loader import SkillLoader
from pikaqiu_agent.storage import MissionStore

logger = logging.getLogger(__name__)

OBSERVER_STATUSES = {
    "idle",
    "observing",
    "thinking",
    "advising",
    "waiting_next_round",
    "crashed",
}
OBSERVER_RUNTIME_TOOLS = {
    "observer_think",
    "experience_search",
    "load_experience",
    "observer_skill_search",
    "observer_load_skill",
    "observer_finish",
}
MAX_OBSERVER_STEPS = 4
PREFERRED_EXPERIENCE_REFS = [
    "experience/okk/pentest_methodology.md",
    "experience/okk/agent_execution_protocols.md",
    "experience/okk/observability_and_runtime.md",
    "experience/rules/mistakes.md",
    "experience/rules/hunting.md",
    "experience/rules/techniques.md",
    "experience/rules/waf-bypass-protocol.md",
]


def _compact_json(value: Any, limit: int = 4000) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, default=str, separators=(",", ":"))
    except Exception:
        text = str(value)
    return text if len(text) <= limit else text[: limit - 20] + "\n... [truncated]"


def _clean_text(value: Any, limit: int = 1200) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _safe_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(parsed, maximum))


class ObserverRuntime:
    """Autonomous supervisory Observer agent runtime.

    This runtime is deliberately narrow: it owns one Observer session per mission,
    can read /experience and skill text for its own judgement, and emits a final
    ObserverDecision. It never creates other agents or runs offensive tools.
    """

    def __init__(
        self,
        settings: AgentSettings,
        store: MissionStore,
        llm_client: LLMClient,
        observer: ObserverAgent,
        *,
        skills: SkillLoader | None = None,
    ) -> None:
        self.settings = settings
        self.store = store
        self.llm = llm_client
        self.observer = observer
        self.skills = skills
        self.experience_root = (settings.workspace_root / "experience").resolve()

    def ensure_session(self, mission_id: str) -> dict[str, Any]:
        return self.store.ensure_observer_agent(mission_id)

    def summary(self, mission_id: str) -> dict[str, Any]:
        return self.store.get_observer_summary(mission_id)

    def observe_tool_result(
        self,
        *,
        mission_id: str,
        round_no: int,
        mission: dict[str, Any],
        memory: dict[str, Any],
        captured_flags: list[str],
        tool_call_log: list[dict[str, Any]],
        round_tool_call_log: list[dict[str, Any]],
        rule_decision: ObserverDecision,
    ) -> ObserverDecision:
        latest = (tool_call_log or [{}])[-1]
        observation = {
            "phase": "tool_result",
            "mission": self._mission_view(mission),
            "memory": self._memory_view(memory),
            "captured_flags": captured_flags,
            "latest_tool_call": self._tool_call_view(latest, include_observer_result=True),
            "recent_tool_calls": self._tool_call_views((tool_call_log or [])[-12:]),
            "round_tool_calls": self._tool_call_views((round_tool_call_log or [])[-12:]),
            "rule_observation": rule_decision.to_dict(),
        }
        return self._run_observer_loop(
            mission_id=mission_id,
            round_no=round_no,
            phase="tool",
            observation=observation,
            rule_decision=rule_decision,
            memory_after=memory,
        )

    def review_round(
        self,
        *,
        mission_id: str,
        round_no: int,
        mission: dict[str, Any],
        memory_before: dict[str, Any],
        memory_after: dict[str, Any],
        tool_call_log: list[dict[str, Any]],
        round_tool_call_log: list[dict[str, Any]],
        llm_call_count: int,
        stall_rounds: int,
        captured_flags: list[str],
    ) -> ObserverDecision:
        rule_decision = self.observer.review_round(
            mission=mission,
            memory_before=memory_before,
            memory_after=memory_after,
            tool_call_log=round_tool_call_log,
            llm_call_count=llm_call_count,
            stall_rounds=stall_rounds,
            captured_flags=captured_flags,
        ).normalised()
        observation = {
            "phase": "round_review",
            "mission": self._mission_view(mission),
            "memory_before": self._memory_view(memory_before),
            "memory_after": self._memory_view(memory_after),
            "captured_flags": captured_flags,
            "llm_call_count": llm_call_count,
            "stall_rounds": stall_rounds,
            "recent_tool_calls": self._tool_call_views((tool_call_log or [])[-16:]),
            "round_tool_calls": self._tool_call_views((round_tool_call_log or [])[-16:], include_observer_result=True),
            "rule_observation": rule_decision.to_dict(),
        }
        return self._run_observer_loop(
            mission_id=mission_id,
            round_no=round_no,
            phase="round",
            observation=observation,
            rule_decision=rule_decision,
            memory_after=memory_after,
        )

    def _run_observer_loop(
        self,
        *,
        mission_id: str,
        round_no: int,
        phase: str,
        observation: dict[str, Any],
        rule_decision: ObserverDecision,
        memory_after: dict[str, Any],
    ) -> ObserverDecision:
        self.ensure_session(mission_id)
        rule_decision = rule_decision.normalised()
        if (
            rule_decision.severity == "critical"
            and any("possible flag" in problem.lower() for problem in rule_decision.problems)
        ):
            self._record_decision(
                mission_id=mission_id,
                round_no=round_no,
                phase=phase,
                decision=rule_decision,
                step=0,
                used_experience=[],
                used_skills=[],
            )
            self._set_status(
                mission_id,
                "waiting_next_round",
                phase=phase,
                last_decision=rule_decision.to_dict(),
            )
            return rule_decision
        transcript: list[dict[str, Any]] = []
        used_experience: list[str] = []
        used_skills: list[str] = []
        self._set_status(mission_id, "observing", phase=phase, round_no=round_no)
        self._add_message(
            mission_id=mission_id,
            round_no=round_no,
            message_type="observation",
            direction="in",
            title=f"Observation: {phase}",
            content=_compact_json(observation, limit=7000),
            metadata={"phase": phase, "rule_decision": rule_decision.to_dict()},
        )

        try:
            for step in range(1, MAX_OBSERVER_STEPS + 1):
                self._set_status(mission_id, "thinking", phase=phase, step=step)
                result = self.llm.invoke_observer_runtime(
                    self._build_prompt(
                        observation=observation,
                        transcript=transcript,
                        step=step,
                        used_experience=used_experience,
                        used_skills=used_skills,
                    ),
                    system=self._system_prompt(),
                )
                tool_name, args = self._parse_tool_call(result.payload, result.raw_text)
                if tool_name == "observer_finish":
                    decision = self._normalise_runtime_decision(
                        args,
                        fallback=rule_decision,
                        used_experience=used_experience,
                        used_skills=used_skills,
                    )
                    decision = self.observer.combine_decisions(rule_decision, decision)
                    self._record_decision(
                        mission_id=mission_id,
                        round_no=round_no,
                        phase=phase,
                        decision=decision,
                        step=step,
                        used_experience=used_experience,
                        used_skills=used_skills,
                    )
                    self._set_status(
                        mission_id,
                        "waiting_next_round",
                        phase=phase,
                        last_decision=decision.to_dict(),
                        experience_refs=used_experience,
                        skill_refs=used_skills,
                    )
                    return decision

                if tool_name not in OBSERVER_RUNTIME_TOOLS:
                    tool_name = "observer_think"
                    args = {
                        "note": f"invalid observer runtime tool requested; raw={_clean_text(result.raw_text, 800)}",
                    }

                self._set_status(mission_id, "advising", phase=phase, step=step, tool=tool_name)
                tool_result = self._dispatch_tool(
                    tool_name,
                    args,
                    used_experience=used_experience,
                    used_skills=used_skills,
                )
                transcript.append({
                    "step": step,
                    "tool": tool_name,
                    "args": args,
                    "result": tool_result,
                })
                self._add_message(
                    mission_id=mission_id,
                    round_no=round_no,
                    message_type="tool" if tool_name != "observer_think" else "think",
                    direction="internal",
                    title=f"{tool_name} step {step}",
                    content=_compact_json({"args": args, "result": tool_result}, limit=6000),
                    metadata={"tool": tool_name, "args": args, "result": tool_result, "step": step},
                )

            decision = self._fallback_decision(
                rule_decision=rule_decision,
                used_experience=used_experience,
                reason="observer runtime reached max internal steps without observer_finish",
            )
            self._record_decision(
                mission_id=mission_id,
                round_no=round_no,
                phase=phase,
                decision=decision,
                step=MAX_OBSERVER_STEPS,
                used_experience=used_experience,
                used_skills=used_skills,
            )
            self._set_status(mission_id, "waiting_next_round", phase=phase, last_decision=decision.to_dict())
            return decision
        except Exception as exc:
            logger.warning("[observer-runtime] failed: %s", exc)
            self._set_status(mission_id, "crashed", phase=phase, error=str(exc)[:1000])
            decision = self._fallback_decision(
                rule_decision=rule_decision,
                used_experience=used_experience,
                reason=f"observer runtime crashed: {exc}",
            )
            self._record_decision(
                mission_id=mission_id,
                round_no=round_no,
                phase=phase,
                decision=decision,
                step=0,
                used_experience=used_experience,
                used_skills=used_skills,
            )
            return decision

    def _system_prompt(self) -> str:
        return (
            "You are the autonomous Observer agent for a CTF/pentest mission. "
            "You are the main agent's cooperative route supervisor: the main agent executes, "
            "you audit the route, evidence quality, repetition, missed leads, and skill opportunities. "
            "Default to not blindly trusting the main agent's execution claims. Accept only observable "
            "evidence from tool output, memory, transcript, and loaded experience. Keep the tone practical "
            "and collaborative; your goal is to help the main agent reach the objective, not to compete with it.\n\n"
            "Sandbox note: tool banners such as 'Kali sandbox local execution result' describe where the "
            "command ran, not whether HTTP/TCP output is target evidence. Judge the actual URL, status code, "
            "headers, response body, cookies, and command stdout/stderr instead of rejecting the output solely "
            "because the command executed from the sandbox.\n\n"
            "You are a supervisory LLM agent, not a general multi-agent framework. "
            "The term sub-agent here means only you, Observer. Do not create agents, spawn agents, "
            "run commands, submit flags, pause the main agent, or modify mission activated skills.\n\n"
            "Your hard-coded capabilities are only these internal tools: observer_think, "
            "experience_search, load_experience, observer_skill_search, observer_load_skill, observer_finish. "
            "You decide when to use load_experience, which experience file matters, whether to search/load skills "
            "for your own judgement, and what route advice to give.\n\n"
            "/experience is the human best-practice route library, not a generic payload dump. "
            "Use experience/okk for agent execution protocols, supervision, context management, and pentest "
            "methodology. Use experience/rules for common mistakes, hunting route choices, proven techniques, "
            "WAF bypass process, never-submit checks, and chain-building judgement. Do not hard-code a scene-to-file "
            "mapping; search or load the files that match the current evidence.\n\n"
            "Low-noise policy: output no_action when the route is evidence-backed and progressing. "
            "Intervene only for a real evidence gap, route deviation, repeated weak action, stall, risk, missed "
            "memory update, or a clearly relevant skill opportunity. A steer must be short, specific, and tell "
            "the main agent exactly what to verify next and what raw output to preserve.\n\n"
            "Steer is stop-the-line only: use action=steer for critical risk, clear repetition, or a blocked route. "
            "For ordinary evidence gaps, prefer action=no_action with a short visible_summary, or action=memory_patch "
            "when memory is missing concrete facts. Never write a tutorial, broad checklist, or user-facing report.\n\n"
            "Every response must be one JSON object: "
            "{\"tool\":\"tool_name\",\"args\":{...}}. "
            "Use observer_finish when done. You have at most 4 internal steps total, including finish.\n\n"
            "Decision schema for observer_finish args: severity none|info|warn|critical; "
            "state progressing|slow|stalled|repeated|off_track|risky; "
            "action no_action|steer|memory_patch|skill_signal; route_assessment string; "
            "problems array; steer_message string; memory_patch object with only findings/leads/dead_ends/next_focus; "
            "skill_signal string; experience_refs array; visible_summary string.\n\n"
            "Length limits: route_assessment <= 240 chars, steer_message <= 320 chars, visible_summary <= 180 chars, "
            "problems <= 3 short bullets. Do not address the main agent as 'you'; use imperative task notes.\n\n"
            "When judging whether the main agent route is correct, combine the current evidence with /experience "
            "best practices. You may search or load experience as needed. If you think the main agent should use "
            "a skill, search/load skills only for your own judgement, then output action=skill_signal and a concise "
            "skill_signal; do not activate it yourself. If you loaded a skill, name the exact skill id and put the "
            "main agent handoff in skill_instruction as an activate_skill(skill_id=\"...\", reason=\"...\") call."
        )

    def _build_prompt(
        self,
        *,
        observation: dict[str, Any],
        transcript: list[dict[str, Any]],
        step: int,
        used_experience: list[str],
        used_skills: list[str],
    ) -> str:
        return (
            f"Internal step {step}/{MAX_OBSERVER_STEPS}.\n"
            "Preferred experience files to consider when relevant, but do not use a fixed scene mapping:\n"
            + "\n".join(f"- {path}" for path in PREFERRED_EXPERIENCE_REFS)
            + "\n\nAvailable tool arguments:\n"
            "- observer_think: {\"note\":\"...\",\"route_assessment\":\"optional\"}\n"
            "- experience_search: {\"query\":\"...\",\"limit\":5}\n"
            "- load_experience: {\"path\":\"experience/...md\",\"max_chars\":8000}\n"
            "- observer_skill_search: {\"query\":\"...\",\"limit\":5}\n"
            "- observer_load_skill: {\"skill_id\":\"...\",\"max_chars\":12000}\n"
            "- observer_finish: final decision schema args\n\n"
            "Current observation:\n"
            f"{_compact_json(observation, limit=9000)}\n\n"
            "Internal transcript so far:\n"
            f"{_compact_json(transcript, limit=9000)}\n\n"
            f"Used experience refs: {_compact_json(used_experience, 1200)}\n"
            f"Loaded observer-only skills: {_compact_json(used_skills, 1200)}\n\n"
            "Route audit checklist before finishing:\n"
            "1. What hypothesis is the main agent testing right now?\n"
            "2. Does the latest tool output contain observable evidence, not just a claim or thin success marker?\n"
            "3. Did the output confirm, deny, or fail to answer the hypothesis?\n"
            "4. Is the current route consistent with /experience best practices for methodology, mistakes, hunting, "
            "techniques, or WAF bypass?\n"
            "5. Is the main agent repeating weak actions, skipping a stronger lead, or failing to write key findings/leads?\n"
            "6. Would a project skill help, based on the evidence? If yes, use observer_skill_search/load_skill for "
            "your own judgement and finish with skill_signal only.\n"
            "7. If you steer, name the exact next verification action and the raw evidence the main agent must capture.\n\n"
            "Do not over-interrupt. If the checklist shows evidence-backed progress, call observer_finish with "
            "action=no_action. If evidence is insufficient but not blocking, do not steer; use a short visible_summary "
            "or memory_patch. Use steer only when the next main-agent action should change immediately.\n\n"
            "Choose exactly one tool now. If enough evidence exists, call observer_finish."
        )

    def _parse_tool_call(self, payload: dict[str, Any], raw_text: str) -> tuple[str, dict[str, Any]]:
        data = payload if isinstance(payload, dict) else {}
        if "tool" not in data and any(key in data for key in ("severity", "state", "action", "route_assessment")):
            return "observer_finish", data
        tool_name = str(data.get("tool") or "").strip()
        args = data.get("args") if isinstance(data.get("args"), dict) else {}
        if not tool_name:
            return "observer_think", {"note": _clean_text(raw_text or data, 1000)}
        return tool_name, args

    def _dispatch_tool(
        self,
        tool_name: str,
        args: dict[str, Any],
        *,
        used_experience: list[str],
        used_skills: list[str],
    ) -> dict[str, Any]:
        if tool_name == "observer_think":
            return {
                "ok": True,
                "note": _clean_text(args.get("note"), 2000),
                "route_assessment": _clean_text(args.get("route_assessment"), 1200),
            }
        if tool_name == "experience_search":
            return self._experience_search(
                str(args.get("query") or ""),
                limit=_safe_int(args.get("limit"), 5, 1, 12),
            )
        if tool_name == "load_experience":
            result = self._load_experience(
                str(args.get("path") or ""),
                max_chars=_safe_int(args.get("max_chars"), 8000, 1000, 20000),
            )
            path = result.get("path")
            if result.get("ok") and path and path not in used_experience:
                used_experience.append(str(path))
            return result
        if tool_name == "observer_skill_search":
            return self._skill_search(
                str(args.get("query") or ""),
                limit=_safe_int(args.get("limit"), 5, 1, 12),
            )
        if tool_name == "observer_load_skill":
            result = self._load_skill(
                str(args.get("skill_id") or ""),
                max_chars=_safe_int(args.get("max_chars"), 12000, 1000, 30000),
            )
            skill_id = result.get("skill_id")
            if result.get("ok") and skill_id and skill_id not in used_skills:
                used_skills.append(str(skill_id))
            return result
        return {"ok": False, "error": f"unknown observer runtime tool: {tool_name}"}

    def _experience_search(self, query: str, *, limit: int) -> dict[str, Any]:
        query = query.strip()
        if not self.experience_root.is_dir():
            return {"ok": False, "query": query, "error": "experience directory not found", "results": []}
        tokens = self._query_tokens(query)
        files = list(self.experience_root.rglob("*.md"))
        scored: list[tuple[float, Path, str]] = []
        for path in files:
            rel = self._experience_rel(path)
            if not rel:
                continue
            text = self._read_text(path)
            haystack = f"{rel}\n{text[:12000]}".lower()
            score = 0.0
            for token in tokens:
                if token in rel.lower():
                    score += 4.0
                if token in haystack:
                    score += 1.0
            if rel in PREFERRED_EXPERIENCE_REFS:
                score += 0.25
            if score > 0 or not tokens:
                snippet = self._snippet(text, tokens)
                scored.append((score, path, snippet))
        scored.sort(key=lambda item: (item[0], -len(str(item[1]))), reverse=True)
        results = [
            {
                "path": self._experience_rel(path),
                "score": round(score, 3),
                "snippet": snippet,
            }
            for score, path, snippet in scored[:limit]
        ]
        return {"ok": True, "query": query, "results": results}

    def _load_experience(self, rel_path: str, *, max_chars: int) -> dict[str, Any]:
        target = self._resolve_experience_path(rel_path)
        if not target:
            return {"ok": False, "path": rel_path, "error": "path must stay inside experience/ and point to a markdown file"}
        text = self._read_text(target)
        truncated = len(text) > max_chars
        if truncated:
            text = text[:max_chars] + "\n... [truncated]"
        return {
            "ok": True,
            "path": self._experience_rel(target),
            "truncated": truncated,
            "content": text,
        }

    def _skill_search(self, query: str, *, limit: int) -> dict[str, Any]:
        if not self.skills:
            return {"ok": False, "query": query, "error": "skill loader unavailable", "results": []}
        stats = self.skills.refresh()
        return {
            "ok": True,
            "query": query,
            "stats": stats,
            "results": self.skills.search(query, limit=limit),
            "note": "Observer-only search; mission activated skills were not modified.",
        }

    def _load_skill(self, skill_id: str, *, max_chars: int) -> dict[str, Any]:
        if not self.skills:
            return {"ok": False, "skill_id": skill_id, "error": "skill loader unavailable"}
        self.skills.refresh()
        skill = self.skills.get_skill(skill_id)
        if not skill:
            return {"ok": False, "skill_id": skill_id, "error": "unknown or disabled skill"}
        prompt = skill.prompt
        truncated = len(prompt) > max_chars
        if truncated:
            prompt = prompt[:max_chars] + "\n... [truncated]"
        return {
            "ok": True,
            "skill_id": skill.id,
            "skill": skill.to_dict(include_prompt=False, include_references=True),
            "prompt": prompt,
            "truncated": truncated,
            "note": "Loaded for Observer judgement only; mission activated skills were not modified.",
        }

    def _normalise_runtime_decision(
        self,
        payload: dict[str, Any],
        *,
        fallback: ObserverDecision,
        used_experience: list[str],
        used_skills: list[str] | None = None,
    ) -> ObserverDecision:
        if not isinstance(payload, dict):
            payload = {}
        used_skills = used_skills or []
        refs = _as_list(payload.get("experience_refs"))
        for ref in used_experience:
            if ref not in refs:
                refs.append(ref)
        skill_signal = str(payload.get("skill_signal") or fallback.skill_signal)
        skill_instruction = str(payload.get("skill_instruction") or "")
        if used_skills and not skill_signal:
            skill_signal = (
                f"activate_skill: {used_skills[-1]} because Observer loaded it as relevant to the current evidence"
            )
        if used_skills and "activate_skill" not in skill_instruction:
            skill_instruction = (
                f"Call activate_skill(skill_id=\"{used_skills[-1]}\", reason=\"Observer identified this skill "
                "as relevant to the current evidence\"), then follow the returned SKILL.md guidance. "
                + skill_instruction
            ).strip()
        action = str(payload.get("action") or "")
        intervention = str(payload.get("intervention") or "")
        if not intervention:
            intervention = {
                "memory_patch": "memory_sync",
                "skill_signal": "skill_card",
                "steer": "steer",
                "no_action": "none",
            }.get(action, fallback.intervention)
        decision = ObserverDecision(
            severity=str(payload.get("severity") or fallback.severity),
            state=str(payload.get("state") or fallback.state),
            intervention=intervention,
            action=str(payload.get("action") or fallback.action),
            route_assessment=str(payload.get("route_assessment") or fallback.route_assessment),
            problems=_as_list(payload.get("problems") or fallback.problems),
            steer_message=str(payload.get("steer_message") or fallback.steer_message),
            memory_patch=payload.get("memory_patch") if isinstance(payload.get("memory_patch"), dict) else fallback.memory_patch,
            skill_card=str(skill_signal or payload.get("skill_card") or fallback.skill_card),
            skill_instruction=skill_instruction,
            skill_signal=skill_signal,
            experience_refs=refs,
            visible_summary=str(payload.get("visible_summary") or payload.get("summary") or ""),
        ).normalised()
        if decision.severity not in SEVERITIES:
            decision.severity = fallback.severity
        if decision.state not in STATES:
            decision.state = fallback.state
        decision.memory_patch = self._safe_memory_patch(decision.memory_patch)
        return decision.normalised()

    def _fallback_decision(
        self,
        *,
        rule_decision: ObserverDecision,
        used_experience: list[str],
        reason: str,
    ) -> ObserverDecision:
        if rule_decision.actionable:
            decision = rule_decision.normalised()
            decision.visible_summary = decision.visible_summary or reason
        else:
            decision = ObserverDecision(
                severity="info",
                state="progressing",
                intervention="none",
                action="no_action",
                route_assessment="Observer runtime did not produce an actionable correction.",
                problems=[],
                visible_summary=reason,
            ).normalised()
        decision.experience_refs = list(dict.fromkeys(decision.experience_refs + used_experience))
        return decision.normalised()

    def _safe_memory_patch(self, patch: dict[str, Any]) -> dict[str, list[str]]:
        safe: dict[str, list[str]] = {}
        if not isinstance(patch, dict):
            return safe
        for key in MEMORY_PATCH_KEYS:
            values = _as_list(patch.get(key))
            if values:
                safe[key] = values[:8]
        return safe

    def _record_decision(
        self,
        *,
        mission_id: str,
        round_no: int,
        phase: str,
        decision: ObserverDecision,
        step: int,
        used_experience: list[str],
        used_skills: list[str],
    ) -> None:
        decision = decision.normalised()
        self._add_message(
            mission_id=mission_id,
            round_no=round_no,
            message_type="decision",
            direction="out",
            title=f"Observer decision: {decision.state}/{decision.action}",
            content=decision.visible_summary or decision.route_assessment or decision.steer_message or "observer_finish",
            metadata={
                "phase": phase,
                "step": step,
                "decision": decision.to_dict(),
                "experience_refs": used_experience,
                "skill_refs": used_skills,
            },
        )

    def _set_status(self, mission_id: str, status: str, **metadata: Any) -> None:
        if status not in OBSERVER_STATUSES:
            status = "idle"
        self.store.update_observer_status(mission_id, status, metadata=metadata)

    def _add_message(self, **kwargs: Any) -> None:
        self.store.add_observer_message(**kwargs)

    def _resolve_experience_path(self, rel_path: str) -> Path | None:
        raw = str(rel_path or "").strip().replace("\\", "/")
        if not raw:
            return None
        if raw.startswith("experience/"):
            raw = raw[len("experience/") :]
        target = (self.experience_root / raw).resolve()
        try:
            target.relative_to(self.experience_root)
        except ValueError:
            return None
        if not target.is_file() or target.suffix.lower() != ".md":
            return None
        return target

    def _experience_rel(self, path: Path) -> str:
        try:
            rel = path.resolve().relative_to(self.settings.workspace_root.resolve())
        except ValueError:
            return ""
        return rel.as_posix()

    def _read_text(self, path: Path) -> str:
        for encoding in ("utf-8", "utf-8-sig", "gb18030"):
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        return path.read_text(encoding="utf-8", errors="replace")

    def _snippet(self, text: str, tokens: list[str], limit: int = 500) -> str:
        if not text:
            return ""
        lower = text.lower()
        pos = -1
        for token in tokens:
            pos = lower.find(token.lower())
            if pos >= 0:
                break
        if pos < 0:
            return _clean_text(text[:limit], limit)
        start = max(0, pos - 160)
        return _clean_text(text[start : start + limit], limit)

    def _query_tokens(self, query: str) -> list[str]:
        seen: set[str] = set()
        tokens: list[str] = []
        for token in re.findall(r"[A-Za-z0-9_.:+/-]+|[\u4e00-\u9fff]{2,}", query.lower()):
            token = token.strip()
            if len(token) < 2 or token in seen:
                continue
            seen.add(token)
            tokens.append(token)
            if len(tokens) >= 16:
                break
        return tokens

    def _mission_view(self, mission: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": mission.get("id"),
            "target": mission.get("target"),
            "goal": mission.get("goal"),
            "scope": mission.get("scope"),
            "domains": mission.get("domains", []),
            "skills": mission.get("skills", []),
            "activated_skills": mission.get("activated_skills", []),
            "status": mission.get("status"),
        }

    def _memory_view(self, memory: dict[str, Any]) -> dict[str, Any]:
        return {
            "summary": memory.get("summary", ""),
            "findings": memory.get("findings", [])[-12:],
            "leads": memory.get("leads", [])[-12:],
            "dead_ends": memory.get("dead_ends", [])[-8:],
            "next_focus": memory.get("next_focus", [])[-8:],
            "credentials": memory.get("credentials", [])[-4:],
            "highest_value_lead": memory.get("highest_value_lead", ""),
            "blocked_reason": memory.get("blocked_reason", ""),
            "next_one_command": memory.get("next_one_command", ""),
        }

    def _tool_call_views(
        self,
        rows: list[dict[str, Any]],
        *,
        include_observer_result: bool = False,
    ) -> list[dict[str, Any]]:
        return [
            self._tool_call_view(row, include_observer_result=include_observer_result)
            for row in rows
        ]

    def _tool_call_view(
        self,
        row: dict[str, Any],
        *,
        include_observer_result: bool = False,
    ) -> dict[str, Any]:
        result = str(row.get("result_observer") or row.get("result_summary") or "")
        data = {
            "tool": row.get("tool"),
            "args_summary": row.get("args_summary"),
            "result_summary": row.get("result_summary"),
            "result_len": row.get("result_len"),
            "exit_code": row.get("exit_code"),
        }
        if include_observer_result:
            data["args_full"] = str(row.get("args_full") or row.get("args_summary") or "")[:1200]
            data["result_observer"] = result
        return data
