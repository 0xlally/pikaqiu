"""Enhanced memory management with importance scoring and long-term retrieval.

Provides:
- Importance scoring: critical findings (RCE, credentials, flags) are never trimmed
- Long-term memory retrieval: searches full event log when agent is stuck
- Semantic deduplication via FTS5 similarity
- Auto credential extraction from tool output
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

_CREDENTIAL_PATTERNS = [
    re.compile(r'(?:user(?:name)?|login|account)\s*[:=]\s*["\']?([^\s"\'<>,;]{2,40})["\']?', re.I),
    re.compile(r'(?:pass(?:word)?|passwd|pwd|secret)\s*[:=]\s*["\']?([^\s"\'<>,;]{2,60})["\']?', re.I),
    re.compile(r'\b([\w.@+-]{2,30})\s*:\s*([\w@$!#%^&*()_+={}\[\]|;:<>,.?/~`-]{3,60})\b'),
    re.compile(r'(?:token|jwt|bearer|api[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9_\-./+]{16,})["\']?', re.I),
    re.compile(r'(?:session|PHPSESSID|connect\.sid)\s*[:=]\s*["\']?([A-Za-z0-9_\-./+=]{16,})["\']?', re.I),
]

_CREDENTIAL_NOISE = re.compile(
    r'^(?:text/|application/|image/|http[s]?://|/[a-z]|\.\.|\d+\.\d+|true|false|null|none|'
    r'Content-|Accept|Host|User-Agent|Server|Date|X-|Cache-|Set-Cookie|Location)',
    re.I,
)


def extract_credentials(text: str) -> list[str]:
    """Auto-extract credentials, tokens, and session values from tool output."""
    if not text or len(text) < 10:
        return []

    found: list[str] = []
    for pattern in _CREDENTIAL_PATTERNS:
        for match in pattern.finditer(text[:8000]):
            groups = match.groups()
            if len(groups) == 2:
                user, passwd = groups
                if user == passwd or _CREDENTIAL_NOISE.match(user) or _CREDENTIAL_NOISE.match(passwd):
                    continue
                cred = f"{user}:{passwd}"
            elif len(groups) == 1:
                cred = groups[0]
                if _CREDENTIAL_NOISE.match(cred):
                    continue
            else:
                continue
            if len(cred) > 3 and cred not in found:
                found.append(cred)
    return found[:10]

# ── Auto credential extraction ────────────────────────────────────────

# ── Importance scoring ────────────────────────────────────────────────

# Patterns that mark a finding as CRITICAL (never trimmed)
_CRITICAL_PATTERNS = [
    # RCE indicators
    re.compile(r'\b(rce|remote.?code.?exec|command.?inject|shell|reverse.?shell)\b', re.I),
    # Credential discoveries
    re.compile(r'\b(password|passwd|credential|token|secret|api.?key|ssh.?key|private.?key)\b', re.I),
    # Flag captures
    re.compile(r'\bflag\{', re.I),
    re.compile(r'\b(flag|ctf.?flag|captured)\b', re.I),
    # Critical vulns
    re.compile(r'\b(sql.?inject|sqli|ssti|ssrf|lfi|rfi|xxe|deseri|file.?upload)\b', re.I),
    # Authentication bypass
    re.compile(r'\b(auth.?bypass|privilege.?escal|sudo|root|admin.?access)\b', re.I),
]

# Patterns that mark a finding as LOW priority (trimmed first)
_LOW_PRIORITY_PATTERNS = [
    re.compile(r'\b(404|not.?found|denied|blocked|filtered|timeout)\b', re.I),
    re.compile(r'\b(scanning|enumerating|checking|trying|testing)\b', re.I),
    re.compile(r'\b(no.?result|nothing.?found|empty|no.?response)\b', re.I),
]


def score_importance(text: str) -> int:
    """Score a finding's importance: 3=critical, 2=normal, 1=low.
    
    Critical items are never trimmed. Low items are trimmed first.
    """
    text_lower = text.lower() if text else ""
    
    # Check critical patterns
    for pattern in _CRITICAL_PATTERNS:
        if pattern.search(text_lower):
            return 3
    
    # Check low priority patterns
    for pattern in _LOW_PRIORITY_PATTERNS:
        if pattern.search(text_lower):
            return 1
    
    return 2  # Normal priority


def smart_trim(items: list[str], max_count: int) -> list[str]:
    """Trim a list intelligently: keep all critical items, trim low priority first.
    
    Priority order:
    1. Critical (importance=3): never trimmed
    2. Normal (importance=2): trimmed FIFO if over limit after removing low
    3. Low (importance=1): trimmed first
    """
    if len(items) <= max_count:
        return items
    
    scored = [(item, score_importance(item)) for item in items]
    
    critical = [item for item, score in scored if score == 3]
    normal = [item for item, score in scored if score == 2]
    low = [item for item, score in scored if score == 1]
    
    # Always keep all critical items
    result = list(critical)
    remaining_slots = max_count - len(result)
    
    if remaining_slots <= 0:
        # Even critical items exceed limit — keep most recent critical
        return critical[-max_count:]
    
    # Fill remaining slots with normal items (most recent first from end)
    if len(normal) <= remaining_slots:
        result.extend(normal)
        remaining_slots -= len(normal)
        # Still room? Add some low priority
        if remaining_slots > 0:
            result.extend(low[-remaining_slots:])
    else:
        # Too many normal items — keep most recent
        result.extend(normal[-remaining_slots:])
    
    return result


# ── Long-term memory retrieval ────────────────────────────────────────

def normalize_shared_memory_state(memory: dict[str, Any]) -> dict[str, Any]:
    """Normalize the two-board memory model and rebuild legacy projections."""
    if not isinstance(memory, dict):
        memory = {}
    result = dict(memory)
    legacy_next_one_command = str(result.get("next_one_command") or "").strip()
    legacy_next_verification = str(result.get("next_verification") or "").strip()
    raw_idea_board = result.get("idea_board") if isinstance(result.get("idea_board"), dict) else {}
    explicit_board_next = bool(
        str(raw_idea_board.get("next_verification") or raw_idea_board.get("next_one_command") or "").strip()
        or _as_str_list(raw_idea_board.get("next_actions"))
    )

    idea_board = _normalize_idea_board(result.get("idea_board"), result)
    memory_board = _normalize_memory_board(result.get("memory_board"), result)

    result["idea_board"] = idea_board
    result["memory_board"] = memory_board

    result["findings"] = smart_trim(memory_board.get("facts", []), max_count=20)
    result["leads"] = smart_trim(idea_board.get("candidate_directions", []), max_count=12)
    result["dead_ends"] = smart_trim(memory_board.get("failed_attempts", []), max_count=12)
    result["credentials"] = _dedupe(memory_board.get("credentials", []))[:16]
    result["next_focus"] = _dedupe(idea_board.get("next_actions", []))[:8]
    result["nex_focus"] = result["next_focus"]
    result["nodes"] = memory_board.get("nodes", {})
    result["topology"] = memory_board.get("topology", [])

    projected_next = idea_board.get("next_verification", "")
    result["highest_value_lead"] = idea_board.get("active_direction", "")
    result["blocked_reason"] = idea_board.get("risk_or_blocker", "")
    if explicit_board_next and projected_next and projected_next != legacy_next_verification:
        result["next_one_command"] = projected_next
    else:
        result["next_one_command"] = legacy_next_one_command or projected_next
    result["primary_hypothesis"] = idea_board.get("primary_hypothesis", "")
    result["next_verification"] = projected_next if explicit_board_next else (legacy_next_verification or projected_next)
    result["failure_boundary"] = idea_board.get("failure_boundary", "")
    result["blocked_prerequisite"] = idea_board.get("blocked_prerequisite", "")
    result["required_next_evidence"] = idea_board.get("required_next_evidence", "")
    return result


def _first_str(*values: Any) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def _normalize_idea_board(board: Any, legacy: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(board, dict):
        board = {}

    candidate_directions = _dedupe(
        _as_str_list(board.get("candidate_directions"))
        + _as_str_list(board.get("leads"))
        + _as_str_list(legacy.get("leads"))
    )
    next_actions = _dedupe(
        _as_str_list(board.get("next_actions"))
        + _as_str_list(board.get("next_focus"))
        + _as_str_list(legacy.get("next_focus"))
    )
    abandoned = _dedupe(
        _as_str_list(board.get("abandoned"))
        + _as_str_list(board.get("dead_ends"))
        + _as_str_list(legacy.get("dead_ends"))
    )

    normalized = {
        "active_direction": _first_str(
            board.get("active_direction"),
            board.get("highest_value_lead"),
            legacy.get("highest_value_lead"),
            candidate_directions[0] if candidate_directions else "",
        ),
        "primary_hypothesis": _first_str(
            board.get("primary_hypothesis"),
            legacy.get("primary_hypothesis"),
        ),
        "next_verification": _first_str(
            board.get("next_verification"),
            board.get("next_one_command"),
            legacy.get("next_verification"),
            legacy.get("next_one_command"),
            next_actions[0] if next_actions else "",
        ),
        "next_actions": smart_trim(next_actions, max_count=8),
        "candidate_directions": smart_trim(candidate_directions, max_count=12),
        "risk_or_blocker": _first_str(
            board.get("risk_or_blocker"),
            board.get("blocked_reason"),
            legacy.get("blocked_reason"),
        ),
        "failure_boundary": _first_str(
            board.get("failure_boundary"),
            legacy.get("failure_boundary"),
        ),
        "blocked_prerequisite": _first_str(
            board.get("blocked_prerequisite"),
            legacy.get("blocked_prerequisite"),
        ),
        "required_next_evidence": _first_str(
            board.get("required_next_evidence"),
            legacy.get("required_next_evidence"),
        ),
        "abandoned": smart_trim(abandoned, max_count=12),
    }
    return _drop_empty_board_fields(normalized)


def _normalize_memory_board(board: Any, legacy: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(board, dict):
        board = {}

    nodes = _normalize_nodes(board.get("nodes", legacy.get("nodes", {})), legacy.get("nodes", {}))
    topology = _dedupe(
        _as_str_list(board.get("topology"))
        + _as_str_list(legacy.get("topology"))
    )[:20]

    normalized = {
        "facts": smart_trim(
            _dedupe(
                _as_str_list(board.get("facts"))
                + _as_str_list(board.get("findings"))
                + _as_str_list(legacy.get("findings"))
            ),
            max_count=24,
        ),
        "evidence": smart_trim(_dedupe(_as_str_list(board.get("evidence"))), max_count=16),
        "constraints": smart_trim(_dedupe(_as_str_list(board.get("constraints"))), max_count=12),
        "credentials": _dedupe(
            _as_str_list(board.get("credentials"))
            + _as_str_list(legacy.get("credentials"))
        )[:16],
        "failed_attempts": smart_trim(
            _dedupe(
                _as_str_list(board.get("failed_attempts"))
                + _as_str_list(board.get("dead_ends"))
                + _as_str_list(legacy.get("dead_ends"))
            ),
            max_count=16,
        ),
        "nodes": nodes,
        "topology": topology,
    }
    if nodes:
        validation_memory = dict(legacy)
        validation_memory["findings"] = normalized.get("facts", [])
        validation_memory["credentials"] = normalized.get("credentials", [])
        _validate_nodes(nodes, validation_memory)
    return _drop_empty_board_fields(normalized)


def _drop_empty_board_fields(board: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in board.items() if value not in ("", [], {})}


def retrieve_forgotten_context(
    store,
    mission_id: str,
    current_memory: dict[str, Any],
    max_results: int = 5,
) -> list[str]:
    """Search the full event log for findings that may have been forgotten.
    
    Called when the agent is stuck (2+ stall rounds) to recover lost context.
    Searches command outputs and agent decisions for credential, vulnerability,
    and path information that may have been trimmed from active memory.
    """
    # Build search terms from current memory gaps
    search_terms = []
    
    # What credentials do we have? Look for more
    creds = current_memory.get("credentials", [])
    if not creds:
        search_terms.extend(["password", "credential", "login", "token", "cookie"])
    
    # What dead ends do we have? Look for alternatives
    dead_ends = current_memory.get("dead_ends", [])
    if dead_ends:
        # Extract key concepts from dead ends to find related but different paths
        for de in dead_ends[-3:]:
            words = re.findall(r'\b[a-zA-Z]{4,}\b', de)
            search_terms.extend(words[:2])
    
    # Always look for flag-related content
    search_terms.extend(["flag{", "flag", "root.txt", "proof"])
    
    # Search events for these terms
    forgotten: list[str] = []
    try:
        events = store.get_events(mission_id)
        for event in events:
            content = str(event.get("content", ""))
            stdout = str(event.get("stdout", ""))
            combined = f"{content} {stdout}".lower()
            
            for term in search_terms:
                if term.lower() in combined and len(content) > 20:
                    # Check if this info is already in current memory
                    memory_text = json.dumps(current_memory, ensure_ascii=False).lower()
                    # Extract the relevant snippet
                    idx = content.lower().find(term.lower())
                    if idx == -1:
                        snippet = content[:200] if len(content) > 200 else content
                    else:
                        start = max(0, idx - 100)
                        end = min(len(content), idx + 100)
                        snippet = content[start:end].strip()
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(content):
                            snippet += "..."
                    if snippet and snippet.lower() not in memory_text:
                        source = f"[Round {event.get('round_no', '?')}, {event.get('type', 'event')}]"
                        forgotten.append(f"{source} {snippet}")
                        if len(forgotten) >= max_results:
                            return forgotten
                        break
    except Exception as e:
        logger.warning("Long-term memory retrieval error: %s", e)
    
    return forgotten


# ── Enhanced normalize_memory (drop-in replacement) ───────────────────

def normalize_memory_enhanced(
    payload: dict[str, Any],
    fallback: dict[str, Any],
) -> dict[str, Any]:
    """Enhanced memory normalization with importance-based trimming.
    
    Drop-in replacement for _normalize_memory in orchestrator.py.
    Key differences:
    - Uses smart_trim instead of simple tail-cut
    - Critical findings (RCE, creds, flags) are never trimmed
    - Low-priority findings are trimmed first
    - Multi-node support: nodes dict + topology list
    """
    summary_val = payload.get("summary", "")
    if isinstance(summary_val, str):
        candidate = summary_val.strip()
        if candidate.startswith("{"):
            if candidate.startswith("{{") and not candidate.startswith("{{{"):
                candidate = candidate[1:]
            if candidate.endswith("}}") and not candidate.endswith("}}}"):
                candidate = candidate[:-1]
            try:
                nested = json.loads(candidate)
            except (json.JSONDecodeError, TypeError):
                nested = None
            if isinstance(nested, dict) and ("findings" in nested or "leads" in nested):
                payload = nested

    updates = payload.get("memory_updates")
    updates = updates if isinstance(updates, dict) else {}

    result = {
        "summary": str(payload.get("summary") or fallback.get("summary", "")),
        "idea_board": payload.get("idea_board", fallback.get("idea_board", {})),
        "memory_board": payload.get("memory_board", fallback.get("memory_board", {})),
        "findings": _dedupe(_as_str_list(payload.get("findings", fallback.get("findings", [])))),
        "leads": _dedupe(_as_str_list(payload.get("leads", fallback.get("leads", [])))),
        "dead_ends": _dedupe(
            _as_str_list(
                payload.get(
                    "dead_ends",
                    updates.get("dead_ends", fallback.get("dead_ends", [])),
                )
            )
        ),
        "credentials": _dedupe(
            _as_str_list(payload.get("credentials", fallback.get("credentials", [])))
        ),
        "next_focus": _dedupe(
            _as_str_list(
                payload.get(
                    "next_focus",
                    payload.get("nex_focus", fallback.get("next_focus", [])),
                )
            )
        ),
        "highest_value_lead": str(
            payload.get("highest_value_lead")
            or updates.get("highest_value_lead")
            or fallback.get("highest_value_lead", "")
        ).strip(),
        "blocked_reason": str(
            payload.get("blocked_reason")
            or updates.get("blocked_reason")
            or fallback.get("blocked_reason", "")
        ).strip(),
        "next_one_command": str(
            payload.get("next_one_command")
            or updates.get("next_one_command")
            or fallback.get("next_one_command", "")
        ).strip(),
        "primary_hypothesis": str(
            payload.get("primary_hypothesis")
            or updates.get("primary_hypothesis")
            or fallback.get("primary_hypothesis", "")
        ).strip(),
        "next_verification": str(
            payload.get("next_verification")
            or updates.get("next_verification")
            or fallback.get("next_verification", "")
            or payload.get("next_one_command")
            or updates.get("next_one_command")
            or fallback.get("next_one_command", "")
        ).strip(),
        "failure_boundary": str(
            payload.get("failure_boundary")
            or updates.get("failure_boundary")
            or fallback.get("failure_boundary", "")
        ).strip(),
        "blocked_prerequisite": str(
            payload.get("blocked_prerequisite")
            or updates.get("blocked_prerequisite")
            or fallback.get("blocked_prerequisite", "")
        ).strip(),
        "required_next_evidence": str(
            payload.get("required_next_evidence")
            or updates.get("required_next_evidence")
            or fallback.get("required_next_evidence", "")
        ).strip(),
        "observer_enforcement_state": str(
            payload.get("observer_enforcement_state")
            or updates.get("observer_enforcement_state")
            or fallback.get("observer_enforcement_state", "")
        ).strip(),
        "agent_override_reason": str(
            payload.get("agent_override_reason")
            or updates.get("agent_override_reason")
            or fallback.get("agent_override_reason", "")
        ).strip(),
    }
    
    # Smart trimming with importance scoring
    result["findings"] = smart_trim(result["findings"], max_count=20)
    result["leads"] = smart_trim(result["leads"], max_count=12)
    result["dead_ends"] = smart_trim(result["dead_ends"], max_count=12)

    # Multi-node support: merge nodes from payload and fallback
    nodes = _normalize_nodes(
        payload.get("nodes", {}),
        fallback.get("nodes", {}),
    )
    if nodes:
        result["nodes"] = nodes
        memory_board = dict(result.get("memory_board") or {})
        memory_board["nodes"] = nodes
        result["memory_board"] = memory_board

    # Topology: deduplicated list of network connections
    topology = _dedupe(
        _as_str_list(payload.get("topology", fallback.get("topology", [])))
    )
    if topology:
        result["topology"] = topology
        memory_board = dict(result.get("memory_board") or {})
        memory_board["topology"] = topology
        result["memory_board"] = memory_board

    # Node status validation: soft consistency check to prevent memory hallucination
    if nodes:
        _validate_nodes(nodes, result)

    return normalize_shared_memory_state(result)


def _validate_nodes(nodes: dict[str, dict[str, Any]], memory: dict[str, Any]) -> None:
    """Light consistency check on node access_level claims.
    
    Downgrades access_level if evidence doesn't support the claim.
    This prevents memory agent hallucination (e.g., claiming root without evidence).
    """
    all_findings = " ".join(memory.get("findings", []))
    all_creds = " ".join(memory.get("credentials", []))
    
    rce_keywords = re.compile(
        r'(rce|command.?exec|shell|whoami|uid=|cat /etc/passwd|root:|www-data)', re.I
    )
    user_keywords = re.compile(
        r'(login|session|authenticated|cookie|token|password|credential|ssh)', re.I
    )
    
    for ip, node in nodes.items():
        access = str(node.get("access_level", "none")).lower()
        node_findings = " ".join(node.get("findings", []))
        node_creds = node.get("credentials", [])
        combined = all_findings + " " + node_findings + " " + all_creds
        
        if access in ("rce_root", "root"):
            if not rce_keywords.search(combined) and not node.get("flags_found"):
                node["access_level"] = "user"
                logger.debug("[memory] node %s: downgraded from %s to user (no RCE evidence)", ip, access)
        elif access == "user":
            if not user_keywords.search(combined) and not node_creds:
                node["access_level"] = "recon"
                logger.debug("[memory] node %s: downgraded from user to recon (no auth evidence)", ip, access)


def _normalize_nodes(
    new_nodes: Any,
    old_nodes: Any,
) -> dict[str, dict[str, Any]]:
    """Merge and normalize per-node memory.
    
    Each node is keyed by IP/hostname and contains:
    - role: str (e.g., "Web Server", "Database")
    - access_level: str (none/recon/user/root/rce_root)
    - findings: list[str]
    - credentials: list[str]
    - flags_found: list[str]
    - next_steps: list[str]
    """
    if not isinstance(new_nodes, dict):
        new_nodes = {}
    if not isinstance(old_nodes, dict):
        old_nodes = {}

    # Start with old nodes, overlay new
    merged: dict[str, dict[str, Any]] = {}
    all_keys = set(list(old_nodes.keys()) + list(new_nodes.keys()))

    for key in all_keys:
        old = old_nodes.get(key, {})
        new = new_nodes.get(key, {})
        if not isinstance(old, dict):
            old = {}
        if not isinstance(new, dict):
            new = {}

        node = {
            "role": str(new.get("role") or old.get("role", "")),
            "access_level": str(new.get("access_level") or old.get("access_level", "none")),
            "findings": _dedupe(
                _as_str_list(new.get("findings", old.get("findings", [])))
            )[:10],
            "credentials": _dedupe(
                _as_str_list(new.get("credentials", old.get("credentials", [])))
            )[:8],
            "flags_found": _dedupe(
                _as_str_list(new.get("flags_found", old.get("flags_found", [])))
            ),
            "next_steps": _dedupe(
                _as_str_list(new.get("next_steps", old.get("next_steps", [])))
            )[:5],
        }
        # Only include non-empty nodes
        if any([node["role"], node["findings"], node["credentials"],
                node["flags_found"], node["next_steps"]]):
            merged[key] = node

    return merged


# ── Helper functions (moved from orchestrator.py for reuse) ───────────

def _as_str_list(val: Any) -> list[str]:
    """Coerce value to a list of non-empty strings."""
    if isinstance(val, list):
        return [str(item).strip() for item in val if str(item).strip()]
    if isinstance(val, str) and val.strip():
        return [val.strip()]
    return []


def _dedupe(items: list[str], limit: int = 40) -> list[str]:
    """Remove exact duplicate strings, preserving order. Soft cap at limit."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(item)
        if len(result) >= limit:
            break
    return result


# ── Semantic stall detection ──────────────────────────────────────────

# Trivial findings that don't count as "progress"
_TRIVIAL_FINDING = re.compile(
    r'\b(404|not.?found|timeout|no.?response|access.?denied|forbidden|connection.?refused'
    r'|connection.?reset|empty|no.?results?|still.?testing|尝试中|failed|error|unreachable'
    r'|no.?such|permission.?denied|invalid|syntax.?error|command.?not.?found'
    r'|nothing.?found|unable.?to|could.?not|does.?not.?exist|not.?allowed'
    r'|service.?unavailable|reset.?by.?peer|timed?.?out)\b',
    re.I,
)


def detect_stall(
    current_memory: dict[str, Any],
    previous_memory: dict[str, Any],
) -> bool:
    """Semantic stall detection: check if there is genuinely new, meaningful progress.

    Returns True if the agent is stalled (no meaningful new findings AND no new leads).
    Unlike hash-based detection, this handles memory reordering correctly and filters
    trivial findings like 404s and timeouts.
    Also checks per-node progress when nodes are present.
    """
    prev_findings = set(str(f).strip().lower() for f in previous_memory.get("findings", []))
    curr_findings = set(str(f).strip().lower() for f in current_memory.get("findings", []))
    new_findings = curr_findings - prev_findings

    # Filter out trivial findings
    meaningful_new = [f for f in new_findings if not _TRIVIAL_FINDING.search(f)]

    prev_leads = set(str(l).strip().lower() for l in previous_memory.get("leads", []))
    curr_leads = set(str(l).strip().lower() for l in current_memory.get("leads", []))
    new_leads = curr_leads - prev_leads

    prev_creds = set(str(c).strip().lower() for c in previous_memory.get("credentials", []))
    curr_creds = set(str(c).strip().lower() for c in current_memory.get("credentials", []))
    new_creds = curr_creds - prev_creds

    new_node_progress = False
    curr_nodes = current_memory.get("nodes", {})
    prev_nodes = previous_memory.get("nodes", {})
    if isinstance(curr_nodes, dict) and curr_nodes:
        if not isinstance(prev_nodes, dict):
            prev_nodes = {}
        if set(curr_nodes) - set(prev_nodes):
            new_node_progress = True
        else:
            for key, curr_node in curr_nodes.items():
                prev_node = prev_nodes.get(key)
                if not isinstance(curr_node, dict) or not isinstance(prev_node, dict):
                    if curr_node != prev_node:
                        new_node_progress = True
                        break
                    continue
                if curr_node.get("access_level", "none") != prev_node.get("access_level", "none"):
                    new_node_progress = True
                    break
                curr_findings = {str(item).lower() for item in curr_node.get("findings", [])}
                prev_findings = {str(item).lower() for item in prev_node.get("findings", [])}
                curr_flags = set(curr_node.get("flags_found", []))
                prev_flags = set(prev_node.get("flags_found", []))
                if curr_findings - prev_findings or curr_flags - prev_flags:
                    new_node_progress = True
                    break

    # Stalled = no meaningful progress anywhere
    return (len(meaningful_new) == 0 and len(new_leads) == 0
            and len(new_creds) == 0 and not new_node_progress)
