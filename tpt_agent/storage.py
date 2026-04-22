from __future__ import annotations

import json
import re
import sqlite3
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _json_loads(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default


def _parse_version_tuple(ver_str: str) -> tuple[int, ...]:
    """Parse a version string like '5.0.23' into (5, 0, 23)."""
    parts = re.findall(r"\d+", ver_str.split("-")[0].strip())
    return tuple(int(p) for p in parts) if parts else ()


def _version_match_score(version_info: str, target: tuple[int, ...], target_raw: str) -> float:
    """Score how well a CVE's version_info matches the target version.

    Returns 0.0-1.0:
      1.0 = definite match (target in range)
      0.5 = possible match (can't determine, or no version info)
      0.0 = definite mismatch (target outside range)
    """
    if not version_info:
        return 0.5  # No version info → might match
    if not target:
        return 0.5

    info = version_info.lower().strip()

    # Exact version mentioned → strong match
    if target_raw in info:
        return 1.0

    best_score = 0.3  # Default: has version info but doesn't match well

    for part in info.split(","):
        part = part.strip()
        if not part:
            continue

        # Range: "5.0.0-5.0.24"
        range_match = re.match(r"(\d+(?:\.\d+)+)\s*-\s*(\d+(?:\.\d+)+)", part)
        if range_match:
            low = _parse_version_tuple(range_match.group(1))
            high = _parse_version_tuple(range_match.group(2))
            if low and high and low <= target <= high:
                return 1.0
            if low and high:
                best_score = max(best_score, 0.1)
            continue

        # Comparison: "<=5.0.5", "<5.0.5", ">=3.0", ">3.0"
        cmp_match = re.match(r"([<>]=?)\s*(\d+(?:\.\d+)+)", part)
        if cmp_match:
            op = cmp_match.group(1)
            ver = _parse_version_tuple(cmp_match.group(2))
            if ver:
                if op == "<=" and target <= ver:
                    return 1.0
                if op == "<" and target < ver:
                    return 1.0
                if op == ">=" and target >= ver:
                    return 0.9
                if op == ">" and target > ver:
                    return 0.9
                best_score = max(best_score, 0.1)
            continue

        # Wildcard: "5.x"
        wild_match = re.match(r"(\d+)\.x", part)
        if wild_match:
            major = int(wild_match.group(1))
            if target and target[0] == major:
                return 0.9
            best_score = max(best_score, 0.1)
            continue

        # Single version: check if target is close
        single_ver = _parse_version_tuple(part)
        if single_ver:
            if single_ver == target:
                return 1.0
            # Same major.minor → likely relevant
            if len(single_ver) >= 2 and len(target) >= 2 and single_ver[:2] == target[:2]:
                best_score = max(best_score, 0.7)
            elif single_ver and target and single_ver[0] == target[0]:
                best_score = max(best_score, 0.5)

    return best_score


class MissionStore:
    def __init__(self, db_path: Path | str) -> None:
        db_path = Path(db_path) if isinstance(db_path, str) and db_path != ":memory:" else db_path
        if isinstance(db_path, Path):
            db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._setup()

    def _setup(self) -> None:
        with self._lock, self._conn:
            self._conn.executescript(
                """
                PRAGMA journal_mode=WAL;

                CREATE TABLE IF NOT EXISTS meta (
                  key TEXT PRIMARY KEY,
                  value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS missions (
                  id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  target TEXT NOT NULL,
                  goal TEXT NOT NULL,
                  scope TEXT NOT NULL,
                  domains_json TEXT NOT NULL,
                  status TEXT NOT NULL,
                  max_rounds INTEGER NOT NULL,
                  max_commands INTEGER NOT NULL,
                  command_timeout_sec INTEGER NOT NULL,
                  model TEXT NOT NULL,
                  expected_flags INTEGER NOT NULL DEFAULT 1,
                  error_message TEXT NOT NULL DEFAULT '',
                  stop_requested INTEGER NOT NULL DEFAULT 0,
                  created_at TEXT NOT NULL,
                  updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS rounds (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mission_id TEXT NOT NULL,
                  round_no INTEGER NOT NULL,
                  worker_role TEXT NOT NULL,
                  prompt_excerpt TEXT NOT NULL,
                  raw_response TEXT NOT NULL,
                  decision_json TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS events (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mission_id TEXT NOT NULL,
                  round_no INTEGER NOT NULL,
                  type TEXT NOT NULL,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  command TEXT NOT NULL DEFAULT '',
                  exit_code INTEGER NOT NULL DEFAULT 0,
                  metadata_json TEXT NOT NULL DEFAULT '{}',
                  started_at TEXT NOT NULL,
                  ended_at TEXT NOT NULL,
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS memories (
                  mission_id TEXT PRIMARY KEY,
                  summary TEXT NOT NULL,
                  findings_json TEXT NOT NULL,
                  leads_json TEXT NOT NULL,
                  dead_ends_json TEXT NOT NULL,
                  credentials_json TEXT NOT NULL,
                  next_focus_json TEXT NOT NULL,
                  updated_at TEXT NOT NULL,
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS knowledge_docs (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  source TEXT NOT NULL,
                  domain TEXT NOT NULL,
                  title TEXT NOT NULL,
                  path TEXT NOT NULL,
                  body TEXT NOT NULL,
                  updated_at TEXT NOT NULL
                );

                CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
                  title,
                  path,
                  body,
                  content='knowledge_docs',
                  content_rowid='id',
                  tokenize='unicode61'
                );

                CREATE TABLE IF NOT EXISTS cve_poc_index (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  cve_id TEXT,
                  product TEXT NOT NULL,
                  version_info TEXT,
                  vuln_type TEXT,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  poc_path TEXT,
                  poc_url TEXT,
                  category TEXT,
                  has_local_poc INTEGER DEFAULT 0,
                  poc_content TEXT DEFAULT ''
                );

                CREATE INDEX IF NOT EXISTS idx_cve_product ON cve_poc_index(product);
                CREATE INDEX IF NOT EXISTS idx_cve_id ON cve_poc_index(cve_id);
                CREATE INDEX IF NOT EXISTS idx_cve_vuln ON cve_poc_index(vuln_type);
                CREATE INDEX IF NOT EXISTS idx_events_mission ON events(mission_id);

                
                """
            )
            # Migration: add expected_flags column for existing databases
            try:
                self._conn.execute("ALTER TABLE missions ADD COLUMN expected_flags INTEGER NOT NULL DEFAULT 1")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Migration: add poc_content column to cve_poc_index
            try:
                self._conn.execute("ALTER TABLE cve_poc_index ADD COLUMN poc_content TEXT DEFAULT ''")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Migration: add nodes_json and topology_json columns for multi-node memory
            for col, default_val in (("nodes_json", "{}"), ("topology_json", "[]")):
                try:
                    self._conn.execute(f"ALTER TABLE memories ADD COLUMN {col} TEXT NOT NULL DEFAULT '{default_val}'")
                except sqlite3.OperationalError:
                    pass  # Column already exists

    def set_meta(self, key: str, value: str) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT INTO meta(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, value),
            )

    def get_meta(self, key: str, default: str = "") -> str:
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default

    def create_mission(
        self,
        *,
        name: str,
        target: str,
        goal: str,
        scope: str,
        domains: list[str],
        max_rounds: int,
        max_commands: int,
        command_timeout_sec: int,
        model: str,
        expected_flags: int = 1,
    ) -> str:
        mission_id = str(uuid.uuid4())
        now = _now()
        with self._lock, self._conn:
            self._conn.execute(
                """
                INSERT INTO missions(
                  id, name, target, goal, scope, domains_json, status,
                  max_rounds, max_commands, command_timeout_sec, model,
                  expected_flags, created_at, updated_at
                ) VALUES(?, ?, ?, ?, ?, ?, 'queued', ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mission_id,
                    name,
                    target,
                    goal,
                    scope,
                    _json_dumps(domains),
                    max_rounds,
                    max_commands,
                    command_timeout_sec,
                    model,
                    expected_flags,
                    now,
                    now,
                ),
            )
            self._conn.execute(
                """
                INSERT INTO memories(
                  mission_id, summary, findings_json, leads_json,
                  dead_ends_json, credentials_json, next_focus_json, updated_at
                ) VALUES(?, '', '[]', '[]', '[]', '[]', '[]', ?)
                """,
                (mission_id, now),
            )
        return mission_id

    def list_missions(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM missions ORDER BY created_at DESC, rowid DESC"
            ).fetchall()
        return [self._mission_row(row) for row in rows]

    def get_mission(self, mission_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM missions WHERE id = ?", (mission_id,)
            ).fetchone()
        return self._mission_row(row) if row else None

    def update_mission_status(
        self, mission_id: str, status: str, error_message: str = ""
    ) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE missions
                SET status = ?, error_message = ?, updated_at = ?
                WHERE id = ?
                """,
                (status, error_message, _now(), mission_id),
            )

    def update_mission_target(
        self, mission_id: str, *, target: str, scope: str | None = None
    ) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE missions
                SET target = ?, scope = ?, updated_at = ?
                WHERE id = ?
                """,
                (target, scope or target, _now(), mission_id),
            )

    def request_stop(self, mission_id: str) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "UPDATE missions SET stop_requested = 1, updated_at = ? WHERE id = ?",
                (_now(), mission_id),
            )

    def reset_stale_missions(self) -> int:
        """On server startup, mark any running/queued missions as stopped (they can't still be running)."""
        with self._lock, self._conn:
            cur = self._conn.execute(
                "UPDATE missions SET status = 'stopped', updated_at = ? WHERE status IN ('running', 'queued')",
                (_now(),),
            )
        return cur.rowcount

    def delete_mission(self, mission_id: str) -> bool:
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT id FROM missions WHERE id = ?",
                (mission_id,),
            ).fetchone()
            if not row:
                return False
            self._conn.execute("DELETE FROM events WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM rounds WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM memories WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM missions WHERE id = ?", (mission_id,))
        return True

    def delete_all_missions(self) -> int:
        """Delete ALL missions and associated data."""
        with self._lock, self._conn:
            count = self._conn.execute("SELECT COUNT(*) FROM missions").fetchone()[0]
            self._conn.execute("DELETE FROM events")
            self._conn.execute("DELETE FROM rounds")
            self._conn.execute("DELETE FROM memories")
            self._conn.execute("DELETE FROM missions")
        return count

    def should_stop(self, mission_id: str) -> bool:
        with self._lock:
            row = self._conn.execute(
                "SELECT stop_requested FROM missions WHERE id = ?", (mission_id,)
            ).fetchone()
        return bool(row and row["stop_requested"])

    def add_round(
        self,
        *,
        mission_id: str,
        round_no: int,
        worker_role: str,
        prompt_excerpt: str,
        raw_response: str,
        decision: dict[str, Any],
    ) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                INSERT INTO rounds(
                  mission_id, round_no, worker_role,
                  prompt_excerpt, raw_response, decision_json, created_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mission_id,
                    round_no,
                    worker_role,
                    prompt_excerpt,
                    raw_response,
                    _json_dumps(decision),
                    _now(),
                ),
            )

    def get_rounds(self, mission_id: str) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT round_no, worker_role, prompt_excerpt, raw_response,
                       decision_json, created_at
                FROM rounds
                WHERE mission_id = ?
                ORDER BY round_no ASC, id ASC
                """,
                (mission_id,),
            ).fetchall()
        return [
            {
                "round_no": row["round_no"],
                "worker_role": row["worker_role"],
                "prompt_excerpt": row["prompt_excerpt"],
                "raw_response": row["raw_response"],
                "decision": _json_loads(row["decision_json"], {}),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def add_event(
        self,
        *,
        mission_id: str,
        round_no: int,
        event_type: str,
        title: str,
        content: str,
        command: str = "",
        exit_code: int = 0,
        metadata: dict[str, Any] | None = None,
        started_at: str | None = None,
        ended_at: str | None = None,
    ) -> int:
        """Insert an event and return its DB row id."""
        ts = _now()
        with self._lock, self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO events(
                  mission_id, round_no, type, title, content, command, exit_code,
                  metadata_json, started_at, ended_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mission_id,
                    round_no,
                    event_type,
                    title,
                    content,
                    command,
                    exit_code,
                    _json_dumps(metadata or {}),
                    started_at or ts,
                    ended_at or ts,
                ),
            )
        return cur.lastrowid

    def update_event_content(self, event_id: int, content: str) -> None:
        """Update the content of an existing event (used for streaming live output)."""
        with self._lock, self._conn:
            self._conn.execute(
                "UPDATE events SET content = ?, ended_at = ? WHERE id = ?",
                (content, _now(), event_id),
            )

    def finalize_event(
        self,
        event_id: int,
        *,
        event_type: str,
        title: str,
        content: str,
        command: str = "",
        exit_code: int = 0,
    ) -> None:
        """Update a running event to its final state (type, title, content, exit_code)."""
        with self._lock, self._conn:
            self._conn.execute(
                "UPDATE events SET type = ?, title = ?, content = ?, command = ?, exit_code = ?, ended_at = ? WHERE id = ?",
                (event_type, title, content, command, exit_code, _now(), event_id),
            )

    def delete_event(self, event_id: int) -> None:
        """Silently remove an event (e.g. a transient thinking indicator)."""
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM events WHERE id = ?", (event_id,))

    def get_events(self, mission_id: str) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT id, round_no, type, title, content, command, exit_code,
                       metadata_json, started_at, ended_at
                FROM events
                WHERE mission_id = ?
                ORDER BY id ASC
                """,
                (mission_id,),
            ).fetchall()
        return [self._event_row(row) for row in rows]

    def get_recent_events(self, mission_id: str, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT id, round_no, type, title, content, command, exit_code,
                       metadata_json, started_at, ended_at
                FROM events
                WHERE mission_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (mission_id, limit),
            ).fetchall()
        return list(reversed([self._event_row(row) for row in rows]))

    def set_memory(self, mission_id: str, memory: dict[str, Any]) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE memories
                SET summary = ?,
                    findings_json = ?,
                    leads_json = ?,
                    dead_ends_json = ?,
                    credentials_json = ?,
                    next_focus_json = ?,
                    nodes_json = ?,
                    topology_json = ?,
                    updated_at = ?
                WHERE mission_id = ?
                """,
                (
                    memory.get("summary", ""),
                    _json_dumps(memory.get("findings", [])),
                    _json_dumps(memory.get("leads", [])),
                    _json_dumps(memory.get("dead_ends", [])),
                    _json_dumps(memory.get("credentials", [])),
                    _json_dumps(memory.get("next_focus", [])),
                    _json_dumps(memory.get("nodes", {})),
                    _json_dumps(memory.get("topology", [])),
                    _now(),
                    mission_id,
                ),
            )

    def get_memory(self, mission_id: str) -> dict[str, Any]:
        with self._lock:
            row = self._conn.execute(
                """
                SELECT summary, findings_json, leads_json,
                       dead_ends_json, credentials_json, next_focus_json,
                       nodes_json, topology_json,
                       updated_at
                FROM memories
                WHERE mission_id = ?
                """,
                (mission_id,),
            ).fetchone()
        if not row:
            return {
                "summary": "",
                "findings": [],
                "leads": [],
                "dead_ends": [],
                "credentials": [],
                "next_focus": [],
                "nodes": {},
                "topology": [],
                "updated_at": "",
            }
        return {
            "summary": row["summary"],
            "findings": _json_loads(row["findings_json"], []),
            "leads": _json_loads(row["leads_json"], []),
            "dead_ends": _json_loads(row["dead_ends_json"], []),
            "credentials": _json_loads(row["credentials_json"], []),
            "next_focus": _json_loads(row["next_focus_json"], []),
            "nodes": _json_loads(row["nodes_json"], {}),
            "topology": _json_loads(row["topology_json"], []),
            "updated_at": row["updated_at"],
        }


    def replace_knowledge_docs(self, docs: Iterable[dict[str, str]]) -> int:
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM knowledge_fts")
            self._conn.execute("DELETE FROM knowledge_docs")
            count = 0
            now = _now()
            for doc in docs:
                cursor = self._conn.execute(
                    """
                    INSERT INTO knowledge_docs(source, domain, title, path, body, updated_at)
                    VALUES(?, ?, ?, ?, ?, ?)
                    """,
                    (
                        doc["source"],
                        doc["domain"],
                        doc["title"],
                        doc["path"],
                        doc["body"],
                        now,
                    ),
                )
                rowid = int(cursor.lastrowid)
                self._conn.execute(
                    """
                    INSERT INTO knowledge_fts(rowid, title, path, body)
                    VALUES(?, ?, ?, ?)
                    """,
                    (rowid, doc["title"], doc["path"], doc["body"]),
                )
                count += 1
        return count

    def search_knowledge(
        self, query: str, domains: list[str] | None = None, limit: int = 6
    ) -> list[dict[str, Any]]:
        tokens = self._query_tokens(query)
        if not tokens:
            return []

        # Phase 1: Try AND query with top tokens (adaptive: more tokens = more precise)
        max_and = min(len(tokens), max(3, len(tokens) // 2))
        and_tokens = tokens[:max_and]
        and_query = " AND ".join(f'"{token}"' for token in and_tokens)
        and_results = self._fts_search(and_query, domains, limit * 2)
        if len(and_results) >= 2:
            # Re-rank AND results by full token hit count + source weight
            scored_and: list[tuple[float, dict[str, Any]]] = []
            for row in and_results:
                title_lower = (row.get("title") or "").lower()
                body_lower = (row.get("body") or row.get("snippet") or "").lower()[:3000]
                combined = title_lower + " " + body_lower
                hit_count = sum(1 for t in tokens if t.lower() in combined)
                title_hits = sum(1 for t in tokens if t.lower() in title_lower)
                # Boost pentest-wiki (curated) over skill/zip docs
                source = (row.get("source") or "").lower()
                source_boost = 2.0 if "pentest-wiki" in source else 0.0
                score = hit_count + title_hits * 0.5 + source_boost
                scored_and.append((score, row))
            scored_and.sort(key=lambda x: x[0], reverse=True)
            return [row for _, row in scored_and[:limit]]

        # Phase 2: Relaxed OR query with BM25 ranking
        or_query = " OR ".join(f'"{token}"' for token in tokens)
        or_results = self._fts_search(or_query, domains, limit * 2)

        # Phase 3: Re-rank by token hit count + source weight
        scored: list[tuple[float, dict[str, Any]]] = []
        for row in or_results:
            title_lower = (row.get("title") or "").lower()
            body_lower = (row.get("body") or row.get("snippet") or "").lower()[:2000]
            combined = title_lower + " " + body_lower
            hit_count = sum(1 for t in tokens if t.lower() in combined)
            title_hits = sum(1 for t in tokens if t.lower() in title_lower)
            source = (row.get("source") or "").lower()
            source_boost = 2.0 if "pentest-wiki" in source else 0.0
            score = hit_count + title_hits * 0.5 + source_boost
            scored.append((score, row))
        scored.sort(key=lambda x: x[0], reverse=True)

        results = [row for _, row in scored[:limit]]
        if len(results) < 2:
            # Re-ranking was too aggressive or OR returned nothing — LIKE fallback
            rows = self._search_knowledge_like(tokens=tokens, domains=domains, limit=limit)
            results = [
                {
                    "id": row["id"],
                    "source": row["source"],
                    "domain": row["domain"],
                    "title": row["title"],
                    "path": row["path"],
                    "body": row["body"],
                }
                for row in rows
            ]
        return results

    def _fts_search(
        self, fts_query: str, domains: list[str] | None, limit: int
    ) -> list[dict[str, Any]]:
        """Execute FTS5 MATCH query with optional domain filter."""
        domain_clause = ""
        params: list[Any] = [fts_query]
        if domains:
            placeholders = ",".join("?" for _ in domains)
            domain_clause = f"AND d.domain IN ({placeholders})"
            params.extend(domains)
        params.append(limit)

        sql = f"""
            SELECT d.id, d.source, d.domain, d.title, d.path, d.body,
                   snippet(knowledge_fts, 2, '[', ']', ' ... ', 32) AS snippet
            FROM knowledge_fts
            JOIN knowledge_docs d ON d.id = knowledge_fts.rowid
            WHERE knowledge_fts MATCH ? {domain_clause}
            ORDER BY bm25(knowledge_fts)
            LIMIT ?
        """
        try:
            with self._lock:
                rows = self._conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError:
            rows = []
        return [
            {
                "id": row["id"],
                "source": row["source"],
                "domain": row["domain"],
                "title": row["title"],
                "path": row["path"],
                "snippet": row["snippet"],
                "body": row["body"],
            }
            for row in rows
        ]

    def get_knowledge_stats(self) -> dict[str, Any]:
        with self._lock:
            total = self._conn.execute("SELECT COUNT(*) AS n FROM knowledge_docs").fetchone()["n"]
            rows = self._conn.execute(
                "SELECT domain, COUNT(*) AS n FROM knowledge_docs GROUP BY domain ORDER BY n DESC"
            ).fetchall()
            cve_total = 0
            try:
                cve_total = self._conn.execute("SELECT COUNT(*) AS n FROM cve_poc_index").fetchone()["n"]
            except sqlite3.OperationalError:
                pass
        return {
            "total_docs": total,
            "domains": {row["domain"]: row["n"] for row in rows},
            "cve_poc_entries": cve_total,
        }

    def get_knowledge_doc(self, doc_id: int) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                """
                SELECT id, source, domain, title, path, body, updated_at
                FROM knowledge_docs
                WHERE id = ?
                """,
                (doc_id,),
            ).fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "source": row["source"],
            "domain": row["domain"],
            "title": row["title"],
            "path": row["path"],
            "body": row["body"],
            "updated_at": row["updated_at"],
        }

    # ── CVE POC Index Methods ────────────────────────────────────────────

    def replace_cve_index(self, entries: Iterable[dict[str, Any]]) -> int:
        """Replace all entries in cve_poc_index table."""
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM cve_poc_index")
            count = 0
            for entry in entries:
                products = entry.get("products", [])
                cve_ids = entry.get("cve_ids", [])
                vuln_types = entry.get("vuln_types", [])
                # Create one row per product (or one with empty product if none)
                product_list = products if products else [""]
                cve_str = ",".join(cve_ids)
                vuln_str = ",".join(vuln_types)
                for product in product_list:
                    self._conn.execute(
                        """
                        INSERT INTO cve_poc_index(
                            cve_id, product, version_info, vuln_type,
                            title, description, poc_path, poc_url,
                            category, has_local_poc, poc_content
                        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            cve_str,
                            product,
                            entry.get("version_info", ""),
                            vuln_str,
                            entry.get("title", ""),
                            entry.get("description", ""),
                            entry.get("poc_path", ""),
                            entry.get("poc_url", ""),
                            entry.get("category", ""),
                            1 if entry.get("has_local_poc") else 0,
                            entry.get("poc_content", ""),
                        ),
                    )
                    count += 1
        return count

    def search_cve_poc(
        self,
        product: str = "",
        version: str = "",
        cve_id: str = "",
        vuln_type: str = "",
        keyword: str = "",
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Two-layer CVE search: product/CVE filter → version ranking.

        Args:
            product: Product name (e.g., "thinkphp", "shiro", "weblogic")
            version: Target version for matching (e.g., "5.0.23")
            cve_id: CVE ID to search (e.g., "CVE-2021-44228")
            vuln_type: Vulnerability type filter (e.g., "rce", "sqli")
            keyword: Free-text keyword search in title/description
            limit: Max results to return
        """
        conditions: list[str] = []
        params: list[Any] = []

        if cve_id:
            cve_id_upper = cve_id.upper().strip()
            conditions.append("cve_id LIKE ?")
            params.append(f"%{cve_id_upper}%")

        if product:
            product_lower = product.lower().strip()
            conditions.append("product LIKE ?")
            params.append(f"%{product_lower}%")

        if vuln_type:
            conditions.append("vuln_type LIKE ?")
            params.append(f"%{vuln_type.lower().strip()}%")

        if keyword:
            kw = keyword.strip()
            conditions.append("(title LIKE ? OR description LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%"])

        if not conditions:
            return []

        where = " AND ".join(conditions)
        fetch_limit = limit * 3  # Fetch extra for version filtering
        params.append(fetch_limit)

        try:
            with self._lock:
                rows = self._conn.execute(
                    f"""
                    SELECT id, cve_id, product, version_info, vuln_type,
                           title, description, poc_path, poc_url,
                           category, has_local_poc, poc_content
                    FROM cve_poc_index
                    WHERE {where}
                    LIMIT ?
                    """,
                    params,
                ).fetchall()
        except sqlite3.OperationalError:
            rows = []

        results = [dict(row) for row in rows]

        if not version or not results:
            # No version to filter — rank by relevance heuristics
            results.sort(key=lambda r: (r.get("has_local_poc", 0), bool(r.get("cve_id"))), reverse=True)
            return results[:limit]

        # Version-aware scoring
        target_ver = _parse_version_tuple(version)
        scored: list[tuple[float, dict[str, Any]]] = []
        for row in results:
            score = _version_match_score(row.get("version_info", ""), target_ver, version)
            scored.append((score, row))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [row for _, row in scored[:limit]]

    def get_cve_index_stats(self) -> dict[str, Any]:
        """Get stats about the CVE POC index."""
        with self._lock:
            try:
                total = self._conn.execute("SELECT COUNT(*) AS n FROM cve_poc_index").fetchone()["n"]
                products = self._conn.execute(
                    "SELECT product, COUNT(*) AS n FROM cve_poc_index WHERE product != '' "
                    "GROUP BY product ORDER BY n DESC LIMIT 20"
                ).fetchall()
                with_cve = self._conn.execute(
                    "SELECT COUNT(*) AS n FROM cve_poc_index WHERE cve_id != ''"
                ).fetchone()["n"]
            except sqlite3.OperationalError:
                return {"total": 0, "products": {}, "with_cve": 0}
        return {
            "total": total,
            "products": {row["product"]: row["n"] for row in products},
            "with_cve": with_cve,
        }

    def _query_tokens(self, query: str) -> list[str]:
        seen: set[str] = set()
        tokens: list[str] = []
        for token in self._expand_query_tokens(query):
            if token in seen:
                continue
            seen.add(token)
            tokens.append(token)
            if len(tokens) >= 20:
                break
        return tokens

    def _expand_query_tokens(self, query: str) -> list[str]:
        tokens: list[str] = []
        for raw in re.findall(r"[A-Za-z0-9][A-Za-z0-9_./:+-]*|[\u4e00-\u9fff]{2,}", query):
            token = raw.strip().strip('"').strip("'").strip()
            if len(token) < 2:
                continue
            tokens.append(token)
            if re.fullmatch(r"[\u4e00-\u9fff]{4,}", token):
                for width in (2, 3):
                    for idx in range(0, len(token) - width + 1):
                        tokens.append(token[idx : idx + width])
        return tokens

    def _search_knowledge_like(
        self,
        *,
        tokens: list[str],
        domains: list[str] | None,
        limit: int,
    ) -> list[sqlite3.Row]:
        like_clauses = " OR ".join(["title LIKE ? OR body LIKE ?"] * len(tokens))
        fallback_params: list[Any] = []
        for token in tokens:
            like = f"%{token}%"
            fallback_params.extend([like, like])
        fallback_clause = ""
        if domains:
            placeholders = ",".join("?" for _ in domains)
            fallback_clause = f"AND domain IN ({placeholders})"
            fallback_params.extend(domains)
        fallback_params.append(limit)
        with self._lock:
            return self._conn.execute(
                f"""
                SELECT id, source, domain, title, path, body
                FROM knowledge_docs
                WHERE ({like_clauses}) {fallback_clause}
                ORDER BY id DESC
                LIMIT ?
                """,
                fallback_params,
            ).fetchall()

    def _mission_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "name": row["name"],
            "target": row["target"],
            "goal": row["goal"],
            "scope": row["scope"],
            "domains": _json_loads(row["domains_json"], []),
            "status": row["status"],
            "max_rounds": row["max_rounds"],
            "max_commands": row["max_commands"],
            "command_timeout_sec": row["command_timeout_sec"],
            "model": row["model"],
            "expected_flags": row["expected_flags"] if "expected_flags" in row.keys() else 1,
            "error_message": row["error_message"],
            "stop_requested": bool(row["stop_requested"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _event_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "round_no": row["round_no"],
            "type": row["type"],
            "title": row["title"],
            "content": row["content"],
            "command": row["command"],
            "exit_code": row["exit_code"],
            "metadata": _json_loads(row["metadata_json"], {}),
            "started_at": row["started_at"],
            "ended_at": row["ended_at"],
        }
