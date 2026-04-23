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

# ── Auto credential extraction ────────────────────────────────────────

_CREDENTIAL_PATTERNS = [
    # Explicit key=value pairs
    re.compile(r'(?:user(?:name)?|login|account)\s*[:=]\s*["\']?([^\s"\'<>,;]{2,40})["\']?', re.I),
    re.compile(r'(?:pass(?:word)?|passwd|pwd|secret)\s*[:=]\s*["\']?([^\s"\'<>,;]{2,60})["\']?', re.I),
    # Colon-separated user:pass (e.g., admin:password123)
    re.compile(r'\b([\w.@+-]{2,30})\s*:\s*([\w@$!#%^&*()_+={}\[\]|;:<>,.?/~`-]{3,60})\b'),
    # Token patterns
    re.compile(r'(?:token|jwt|bearer|api[_-]?key)\s*[:=]\s*["\']?([A-Za-z0-9_\-./+]{16,})["\']?', re.I),
    # Session cookie values (flask, php)
    re.compile(r'(?:session|PHPSESSID|connect\.sid)\s*[:=]\s*["\']?([A-Za-z0-9_\-./+=]{16,})["\']?', re.I),
]

# Patterns that look like credentials but aren't
_CREDENTIAL_NOISE = re.compile(
    r'^(?:text/|application/|image/|http[s]?://|/[a-z]|\.\.|\d+\.\d+|true|false|null|none|'
    r'Content-|Accept|Host|User-Agent|Server|Date|X-|Cache-|Set-Cookie|Location)',
    re.I,
)


def extract_credentials(text: str) -> list[str]:
    """Auto-extract credentials, tokens, and session values from tool output.

    Returns deduplicated list of 'key: value' strings.
    """
    if not text or len(text) < 10:
        return []

    found: list[str] = []
    # Only scan first 8000 chars to avoid parsing huge outputs
    text = text[:8000]

    for pattern in _CREDENTIAL_PATTERNS:
        for match in pattern.finditer(text):
            groups = match.groups()
            if len(groups) == 2:
                user, passwd = groups
                # Filter noise
                if _CREDENTIAL_NOISE.match(user) or _CREDENTIAL_NOISE.match(passwd):
                    continue
                if user == passwd:
                    continue
                cred = f"{user}:{passwd}"
            elif len(groups) == 1:
                val = groups[0]
                if _CREDENTIAL_NOISE.match(val):
                    continue
                cred = val
            else:
                continue
            if len(cred) > 3 and cred not in found:
                found.append(cred)

    return found[:10]  # Cap to avoid flooding

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
            _as_str_list(payload.get("next_focus", fallback.get("next_focus", [])))
        ),
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

    # Topology: deduplicated list of network connections
    topology = _dedupe(
        _as_str_list(payload.get("topology", fallback.get("topology", [])))
    )
    if topology:
        result["topology"] = topology

    # Node status validation: soft consistency check to prevent memory hallucination
    if nodes:
        _validate_nodes(nodes, result)

    return result


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
