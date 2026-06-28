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


MEMORY_COLUMNS = (
    "mission_id",
    "summary",
    "findings_json",
    "leads_json",
    "dead_ends_json",
    "credentials_json",
    "topology_json",
    "updated_at",
)


def _parse_iso_datetime(value: str | None) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    text = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", text)
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _duration_seconds(started_at: str | None, ended_at: str | None) -> int | None:
    start = _parse_iso_datetime(started_at)
    end = _parse_iso_datetime(ended_at)
    if not start or not end:
        return None
    return max(0, int(round((end - start).total_seconds())))


def _knowledge_relevance_score(row: dict[str, Any], tokens: list[str], body_limit: int) -> float:
    title_lower = (row.get("title") or "").lower()
    body_lower = (row.get("body") or row.get("snippet") or "").lower()[:body_limit]
    combined = title_lower + " " + body_lower
    hit_count = sum(1 for token in tokens if token.lower() in combined)
    title_hits = sum(1 for token in tokens if token.lower() in title_lower)
    source = (row.get("source") or "").lower()
    source_boost = 2.0 if "pentest-wiki" in source else 0.0
    return hit_count + title_hits * 0.5 + source_boost


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
                  skills_json TEXT NOT NULL DEFAULT '[]',
                  activated_skills_json TEXT NOT NULL DEFAULT '[]',
                  human_collab_enabled INTEGER NOT NULL DEFAULT 0,
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

                CREATE TABLE IF NOT EXISTS experiment_records (
                  mission_id TEXT PRIMARY KEY,
                  challenge_code TEXT NOT NULL DEFAULT '',
                  difficulty TEXT NOT NULL DEFAULT '',
                  outcome TEXT NOT NULL DEFAULT '',
                  failure_reason TEXT NOT NULL DEFAULT '',
                  key_parameters TEXT NOT NULL DEFAULT '',
                  notes TEXT NOT NULL DEFAULT '',
                  started_at TEXT NOT NULL DEFAULT '',
                  ended_at TEXT NOT NULL DEFAULT '',
                  updated_at TEXT NOT NULL,
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS human_guidance (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  mission_id TEXT NOT NULL,
                  content TEXT NOT NULL,
                  status TEXT NOT NULL DEFAULT 'pending',
                  created_at TEXT NOT NULL,
                  consumed_at TEXT NOT NULL DEFAULT '',
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS observer_agents (
                  id TEXT PRIMARY KEY,
                  mission_id TEXT NOT NULL UNIQUE,
                  parent_id TEXT NOT NULL DEFAULT 'root',
                  task TEXT NOT NULL,
                  status TEXT NOT NULL,
                  metadata_json TEXT NOT NULL DEFAULT '{}',
                  created_at TEXT NOT NULL,
                  updated_at TEXT NOT NULL,
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS observer_messages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  observer_id TEXT NOT NULL,
                  mission_id TEXT NOT NULL,
                  round_no INTEGER NOT NULL,
                  type TEXT NOT NULL,
                  direction TEXT NOT NULL,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  metadata_json TEXT NOT NULL DEFAULT '{}',
                  created_at TEXT NOT NULL,
                  FOREIGN KEY(observer_id) REFERENCES observer_agents(id),
                  FOREIGN KEY(mission_id) REFERENCES missions(id)
                );

                CREATE TABLE IF NOT EXISTS memories (
                  mission_id TEXT PRIMARY KEY,
                  summary TEXT NOT NULL,
                  findings_json TEXT NOT NULL,
                  leads_json TEXT NOT NULL,
                  dead_ends_json TEXT NOT NULL,
                  credentials_json TEXT NOT NULL,
                  topology_json TEXT NOT NULL,
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

                CREATE INDEX IF NOT EXISTS idx_events_mission ON events(mission_id);
                CREATE INDEX IF NOT EXISTS idx_experiment_records_updated ON experiment_records(updated_at);
                CREATE INDEX IF NOT EXISTS idx_human_guidance_mission ON human_guidance(mission_id, id);
                CREATE INDEX IF NOT EXISTS idx_observer_agents_mission ON observer_agents(mission_id);
                CREATE INDEX IF NOT EXISTS idx_observer_messages_mission ON observer_messages(mission_id, id);


                """
            )
            # Migration: add expected_flags column for existing databases
            try:
                self._conn.execute("ALTER TABLE missions ADD COLUMN expected_flags INTEGER NOT NULL DEFAULT 1")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Migration: add per-mission skill selection
            try:
                self._conn.execute("ALTER TABLE missions ADD COLUMN skills_json TEXT NOT NULL DEFAULT '[]'")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Migration: add AI-activated skill tracking
            try:
                self._conn.execute("ALTER TABLE missions ADD COLUMN activated_skills_json TEXT NOT NULL DEFAULT '[]'")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Migration: add per-mission human collaboration toggle
            try:
                self._conn.execute("ALTER TABLE missions ADD COLUMN human_collab_enabled INTEGER NOT NULL DEFAULT 0")
            except sqlite3.OperationalError:
                pass  # Column already exists
            self._rebuild_memories_table_if_needed()

    def _rebuild_memories_table_if_needed(self) -> None:
        rows = self._conn.execute("PRAGMA table_info(memories)").fetchall()
        current_columns = tuple(row["name"] for row in rows)
        if current_columns == MEMORY_COLUMNS:
            return
        select_columns = set(current_columns)
        tmp_table = "memories_new"
        self._conn.execute("DROP TABLE IF EXISTS memories_new")
        self._conn.execute(
            """
            CREATE TABLE memories_new (
              mission_id TEXT PRIMARY KEY,
              summary TEXT NOT NULL,
              findings_json TEXT NOT NULL,
              leads_json TEXT NOT NULL,
              dead_ends_json TEXT NOT NULL,
              credentials_json TEXT NOT NULL,
              topology_json TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              FOREIGN KEY(mission_id) REFERENCES missions(id)
            )
            """
        )
        topology_expr = "topology_json" if "topology_json" in select_columns else "'[]'"
        self._conn.execute(
            f"""
            INSERT INTO {tmp_table}(
              mission_id, summary, findings_json, leads_json,
              dead_ends_json, credentials_json, topology_json, updated_at
            )
            SELECT
              mission_id, summary, findings_json, leads_json,
              dead_ends_json, credentials_json, {topology_expr}, updated_at
            FROM memories
            """
        )
        self._conn.execute("DROP TABLE memories")
        self._conn.execute(f"ALTER TABLE {tmp_table} RENAME TO memories")

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
        skills: list[str] | None = None,
    ) -> str:
        mission_id = str(uuid.uuid4())
        now = _now()
        with self._lock, self._conn:
            self._conn.execute(
                """
                INSERT INTO missions(
                  id, name, target, goal, scope, domains_json, status,
                  max_rounds, max_commands, command_timeout_sec, model,
                  expected_flags, skills_json, created_at, updated_at
                ) VALUES(?, ?, ?, ?, ?, ?, 'queued', ?, ?, ?, ?, ?, ?, ?, ?)
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
                    _json_dumps(skills or []),
                    now,
                    now,
                ),
            )
            self._conn.execute(
                """
                INSERT INTO memories(
                  mission_id, summary, findings_json, leads_json,
                  dead_ends_json, credentials_json, topology_json, updated_at
                ) VALUES(?, '', '[]', '[]', '[]', '[]', '[]', ?)
                """,
                (mission_id, now),
            )
        return mission_id

    def list_missions(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT m.*, flags.captured_flags_blob AS captured_flags_blob
                FROM missions m
                LEFT JOIN (
                  SELECT mission_id, GROUP_CONCAT(content, char(31)) AS captured_flags_blob
                  FROM (
                    SELECT mission_id, content
                    FROM events
                    WHERE type = 'flag'
                    ORDER BY id ASC
                  )
                  GROUP BY mission_id
                ) flags ON flags.mission_id = m.id
                ORDER BY m.created_at DESC, m.rowid DESC
                """
            ).fetchall()
        return [self._mission_row(row) for row in rows]

    def get_mission(self, mission_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                """
                SELECT m.*, flags.captured_flags_blob AS captured_flags_blob
                FROM missions m
                LEFT JOIN (
                  SELECT mission_id, GROUP_CONCAT(content, char(31)) AS captured_flags_blob
                  FROM (
                    SELECT mission_id, content
                    FROM events
                    WHERE type = 'flag'
                    ORDER BY id ASC
                  )
                  GROUP BY mission_id
                ) flags ON flags.mission_id = m.id
                WHERE m.id = ?
                """,
                (mission_id,),
            ).fetchone()
        return self._mission_row(row) if row else None

    def get_captured_flags(self, mission_id: str) -> list[str]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT content
                FROM events
                WHERE mission_id = ? AND type = 'flag'
                ORDER BY id ASC
                """,
                (mission_id,),
            ).fetchall()
        return self._captured_flags_from_contents(row["content"] for row in rows)

    def list_experiment_records(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(self._experiment_records_query()).fetchall()
        return [self._experiment_row(row) for row in rows]

    def get_experiment_record(self, mission_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                self._experiment_records_query("WHERE m.id = ?"),
                (mission_id,),
            ).fetchone()
        return self._experiment_row(row) if row else None

    def upsert_experiment_record(self, mission_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        now = _now()
        with self._lock, self._conn:
            mission = self._conn.execute(
                "SELECT id, status, created_at, updated_at FROM missions WHERE id = ?",
                (mission_id,),
            ).fetchone()
            if not mission:
                return None
            existing = self._conn.execute(
                "SELECT * FROM experiment_records WHERE mission_id = ?",
                (mission_id,),
            ).fetchone()

            def field(name: str, default: str = "") -> str:
                if name not in data:
                    return default
                return str(data.get(name) or "").strip()

            terminal_statuses = {"done", "error", "stopped", "timeout"}
            default_ended = mission["updated_at"] if mission["status"] in terminal_statuses else ""
            challenge_code = field("challenge_code", existing["challenge_code"] if existing else "")
            difficulty = field("difficulty", existing["difficulty"] if existing else "")
            outcome = field(
                "outcome",
                (existing["outcome"] if existing and existing["outcome"] else self._default_experiment_outcome(mission["status"])),
            )
            failure_reason = field("failure_reason", existing["failure_reason"] if existing else "")
            key_parameters = field("key_parameters", existing["key_parameters"] if existing else "")
            notes = field("notes", existing["notes"] if existing else "")
            started_at = field("started_at", existing["started_at"] if existing and existing["started_at"] else mission["created_at"])
            ended_at = field("ended_at", existing["ended_at"] if existing and existing["ended_at"] else default_ended)

            self._conn.execute(
                """
                INSERT INTO experiment_records(
                  mission_id, challenge_code, difficulty, outcome, failure_reason,
                  key_parameters, notes, started_at, ended_at, updated_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(mission_id) DO UPDATE SET
                  challenge_code = excluded.challenge_code,
                  difficulty = excluded.difficulty,
                  outcome = excluded.outcome,
                  failure_reason = excluded.failure_reason,
                  key_parameters = excluded.key_parameters,
                  notes = excluded.notes,
                  started_at = excluded.started_at,
                  ended_at = excluded.ended_at,
                  updated_at = excluded.updated_at
                """,
                (
                    mission_id,
                    challenge_code,
                    difficulty,
                    outcome,
                    failure_reason,
                    key_parameters,
                    notes,
                    started_at,
                    ended_at,
                    now,
                ),
            )
        return self.get_experiment_record(mission_id)

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

    def prepare_mission_resume(self, mission_id: str, extra_rounds: int) -> dict[str, Any] | None:
        """Requeue an ended mission while preserving memory, events, and guidance history."""
        now = _now()
        extra_rounds = max(1, int(extra_rounds))
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT * FROM missions WHERE id = ?",
                (mission_id,),
            ).fetchone()
            if not row:
                return None

            last_round = self._max_round_no_locked(mission_id)
            current_max = int(row["max_rounds"])
            new_max = max(current_max, last_round + extra_rounds)
            self._conn.execute(
                """
                UPDATE missions
                SET status = 'queued',
                    stop_requested = 0,
                    error_message = '',
                    max_rounds = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (new_max, now, mission_id),
            )
            updated = self._conn.execute(
                "SELECT * FROM missions WHERE id = ?",
                (mission_id,),
            ).fetchone()
        return self._mission_row(updated) if updated else None

    def get_max_round_no(self, mission_id: str) -> int:
        with self._lock:
            return self._max_round_no_locked(mission_id)

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

    def request_stop(self, mission_id: str) -> bool:
        with self._lock, self._conn:
            cur = self._conn.execute(
                """
                UPDATE missions
                SET stop_requested = 1,
                    status = CASE
                        WHEN status IN ('queued', 'running') THEN 'stopped'
                        ELSE status
                    END,
                    error_message = CASE
                        WHEN status IN ('queued', 'running') THEN 'Stop requested by operator.'
                        ELSE error_message
                    END,
                    updated_at = ?
                WHERE id = ?
                """,
                (_now(), mission_id),
            )
            return cur.rowcount > 0

    def set_human_collab_enabled(self, mission_id: str, enabled: bool) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                "UPDATE missions SET human_collab_enabled = ?, updated_at = ? WHERE id = ?",
                (1 if enabled else 0, _now(), mission_id),
            )

    def add_activated_skill(self, mission_id: str, skill_id: str) -> list[str]:
        skill_id = str(skill_id).strip()
        if not skill_id:
            return []
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT activated_skills_json FROM missions WHERE id = ?",
                (mission_id,),
            ).fetchone()
            if not row:
                return []
            skills = _json_loads(row["activated_skills_json"], [])
            if skill_id not in skills:
                skills.append(skill_id)
                self._conn.execute(
                    """
                    UPDATE missions
                    SET activated_skills_json = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (_json_dumps(skills), _now(), mission_id),
                )
            return skills

    def ensure_observer_agent(
        self,
        mission_id: str,
        *,
        task: str = "Autonomously supervise the main agent route, skill usage, memory, and progress.",
    ) -> dict[str, Any]:
        now = _now()
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT * FROM observer_agents WHERE mission_id = ?",
                (mission_id,),
            ).fetchone()
            if row:
                return self._observer_agent_row(row)
            observer_id = f"observer-{mission_id}"
            self._conn.execute(
                """
                INSERT INTO observer_agents(
                  id, mission_id, parent_id, task, status, metadata_json, created_at, updated_at
                ) VALUES(?, ?, 'root', ?, 'idle', '{}', ?, ?)
                """,
                (observer_id, mission_id, task, now, now),
            )
            row = self._conn.execute(
                "SELECT * FROM observer_agents WHERE id = ?",
                (observer_id,),
            ).fetchone()
        return self._observer_agent_row(row)

    def update_observer_status(
        self,
        mission_id: str,
        status: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        now = _now()
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT * FROM observer_agents WHERE mission_id = ?",
                (mission_id,),
            ).fetchone()
            if not row:
                return None
            current_meta = _json_loads(row["metadata_json"], {})
            if metadata:
                current_meta.update(metadata)
            self._conn.execute(
                """
                UPDATE observer_agents
                SET status = ?, metadata_json = ?, updated_at = ?
                WHERE mission_id = ?
                """,
                (status, _json_dumps(current_meta), now, mission_id),
            )
            updated = self._conn.execute(
                "SELECT * FROM observer_agents WHERE mission_id = ?",
                (mission_id,),
            ).fetchone()
        return self._observer_agent_row(updated) if updated else None

    def add_observer_message(
        self,
        *,
        mission_id: str,
        round_no: int,
        message_type: str,
        direction: str,
        title: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        observer = self.ensure_observer_agent(mission_id)
        now = _now()
        with self._lock, self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO observer_messages(
                  observer_id, mission_id, round_no, type, direction,
                  title, content, metadata_json, created_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    observer["id"],
                    mission_id,
                    round_no,
                    message_type,
                    direction,
                    title,
                    content,
                    _json_dumps(metadata or {}),
                    now,
                ),
            )
            self._conn.execute(
                "UPDATE observer_agents SET updated_at = ? WHERE id = ?",
                (now, observer["id"]),
            )
            row = self._conn.execute(
                "SELECT * FROM observer_messages WHERE id = ?",
                (int(cur.lastrowid),),
            ).fetchone()
        return self._observer_message_row(row)

    def get_observer_agent(self, mission_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM observer_agents WHERE mission_id = ?",
                (mission_id,),
            ).fetchone()
        return self._observer_agent_row(row) if row else None

    def get_observer_messages(self, mission_id: str, limit: int = 80) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit or 80), 500))
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT *
                FROM observer_messages
                WHERE mission_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (mission_id, limit),
            ).fetchall()
        return list(reversed([self._observer_message_row(row) for row in rows]))

    def get_observer_summary(self, mission_id: str) -> dict[str, Any]:
        agent = self.get_observer_agent(mission_id)
        messages = self.get_observer_messages(mission_id, limit=80)
        decisions = [msg for msg in messages if msg["type"] == "decision"]
        latest_decision = decisions[-1] if decisions else None

        def decision_payload(message: dict[str, Any] | None) -> dict[str, Any]:
            payload = (message or {}).get("metadata", {}).get("decision", {})
            return payload if isinstance(payload, dict) else {}

        latest_payload = decision_payload(latest_decision)
        stats = {
            "messages": len(messages),
            "decisions": len(decisions),
            "ok": sum(
                1 for msg in decisions
                if decision_payload(msg).get("verdict") == "OK"
            ),
            "watch": sum(
                1 for msg in decisions
                if decision_payload(msg).get("verdict") == "WATCH"
            ),
            "interrupts": sum(
                1 for msg in decisions
                if decision_payload(msg).get("verdict") in {"L1", "L2", "L3", "L4", "ENV"}
            ),
            "memory_patches": sum(
                1 for msg in decisions
                if bool(decision_payload(msg).get("memory_patch"))
            ),
            "skill_signals": sum(
                1 for msg in decisions
                if str(decision_payload(msg).get("skill_signal") or "").strip()
            ),
        }
        return {
            "agent": agent,
            "status": (agent or {}).get("status", "idle"),
            "latest_decision": latest_payload,
            "latest_message": latest_decision,
            "messages": messages,
            "stats": stats,
        }

    def add_human_guidance(self, mission_id: str, content: str) -> dict[str, Any]:
        now = _now()
        with self._lock, self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO human_guidance(mission_id, content, status, created_at, consumed_at)
                VALUES(?, ?, 'pending', ?, '')
                """,
                (mission_id, content, now),
            )
            self._conn.execute(
                "UPDATE missions SET updated_at = ? WHERE id = ?",
                (now, mission_id),
            )
            guidance_id = int(cur.lastrowid)
        return {
            "id": guidance_id,
            "mission_id": mission_id,
            "content": content,
            "status": "pending",
            "created_at": now,
            "consumed_at": "",
        }

    def get_human_guidance(self, mission_id: str, limit: int = 30) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT id, mission_id, content, status, created_at, consumed_at
                FROM human_guidance
                WHERE mission_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (mission_id, limit),
            ).fetchall()
        return list(reversed([self._guidance_row(row) for row in rows]))

    def consume_pending_human_guidance(self, mission_id: str, limit: int = 5) -> list[dict[str, Any]]:
        now = _now()
        with self._lock, self._conn:
            mission = self._conn.execute(
                "SELECT human_collab_enabled FROM missions WHERE id = ?",
                (mission_id,),
            ).fetchone()
            if not mission or not bool(mission["human_collab_enabled"]):
                return []
            rows = self._conn.execute(
                """
                SELECT id, mission_id, content, status, created_at, consumed_at
                FROM human_guidance
                WHERE mission_id = ? AND status = 'pending'
                ORDER BY id ASC
                LIMIT ?
                """,
                (mission_id, limit),
            ).fetchall()
            if not rows:
                return []
            ids = [int(row["id"]) for row in rows]
            placeholders = ",".join("?" for _ in ids)
            self._conn.execute(
                f"UPDATE human_guidance SET status = 'consumed', consumed_at = ? WHERE id IN ({placeholders})",
                [now, *ids],
            )
        return [{**self._guidance_row(row), "status": "consumed", "consumed_at": now} for row in rows]

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
            self._conn.execute("DELETE FROM observer_messages WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM observer_agents WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM human_guidance WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM experiment_records WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM events WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM rounds WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM memories WHERE mission_id = ?", (mission_id,))
            self._conn.execute("DELETE FROM missions WHERE id = ?", (mission_id,))
        return True

    def delete_all_missions(self) -> int:
        """Delete ALL missions and associated data."""
        with self._lock, self._conn:
            count = self._conn.execute("SELECT COUNT(*) FROM missions").fetchone()[0]
            self._conn.execute("DELETE FROM observer_messages")
            self._conn.execute("DELETE FROM observer_agents")
            self._conn.execute("DELETE FROM human_guidance")
            self._conn.execute("DELETE FROM experiment_records")
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
                       dead_ends_json, credentials_json, topology_json
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
                "topology": [],
            }
        return {
            "summary": row["summary"],
            "findings": _json_loads(row["findings_json"], []),
            "leads": _json_loads(row["leads_json"], []),
            "dead_ends": _json_loads(row["dead_ends_json"], []),
            "credentials": _json_loads(row["credentials_json"], []),
            "topology": _json_loads(row["topology_json"], []),
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
                score = _knowledge_relevance_score(row, tokens, body_limit=3000)
                scored_and.append((score, row))
            scored_and.sort(key=lambda x: x[0], reverse=True)
            return [row for _, row in scored_and[:limit]]

        # Phase 2: Relaxed OR query with BM25 ranking
        or_query = " OR ".join(f'"{token}"' for token in tokens)
        or_results = self._fts_search(or_query, domains, limit * 2)

        # Phase 3: Re-rank by token hit count + source weight
        scored: list[tuple[float, dict[str, Any]]] = []
        for row in or_results:
            score = _knowledge_relevance_score(row, tokens, body_limit=2000)
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
        return {
            "total_docs": total,
            "domains": {row["domain"]: row["n"] for row in rows},
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

    def find_knowledge_doc_id(self, *, source: str, path: str) -> int | None:
        with self._lock:
            row = self._conn.execute(
                """
                SELECT id
                FROM knowledge_docs
                WHERE source = ? AND path = ?
                LIMIT 1
                """,
                (source, path),
            ).fetchone()
        return int(row["id"]) if row else None

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
        lowered = [token.lower() for token in tokens]
        short_protocol_terms = {"cl", "te", "h2", "h1", "0"}
        for first, second in zip(lowered, lowered[1:]):
            if first in short_protocol_terms and second in short_protocol_terms:
                tokens.extend(
                    [
                        f"{first}.{second}",
                        f"{first}-{second}",
                        f"{first}_{second}",
                        f"{first}{second}",
                    ]
                )
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

    def _experiment_records_query(self, where_clause: str = "") -> str:
        where_sql = f" {where_clause}" if where_clause else ""
        return f"""
            SELECT
              m.id AS mission_id,
              m.name AS mission_name,
              m.target AS target,
              m.goal AS goal,
              m.status AS mission_status,
              m.skills_json AS skills_json,
              m.activated_skills_json AS activated_skills_json,
              m.created_at AS mission_created_at,
              m.updated_at AS mission_updated_at,
              er.challenge_code AS challenge_code,
              er.difficulty AS difficulty,
              er.outcome AS outcome,
              er.failure_reason AS failure_reason,
              er.key_parameters AS key_parameters,
              er.notes AS notes,
              er.started_at AS record_started_at,
              er.ended_at AS record_ended_at,
              er.updated_at AS record_updated_at,
              COALESCE(ev.event_count, 0) AS event_count,
              COALESCE(ev.command_count, 0) AS command_count,
              COALESCE(ev.error_count, 0) AS error_count,
              COALESCE(ev.flag_count, 0) AS flag_count,
              flags.captured_flags_blob AS captured_flags_blob,
              ev.first_started_at AS first_started_at,
              ev.last_ended_at AS last_ended_at
            FROM missions m
            LEFT JOIN experiment_records er ON er.mission_id = m.id
            LEFT JOIN (
              SELECT
                mission_id,
                COUNT(*) AS event_count,
                SUM(CASE WHEN type = 'command' THEN 1 ELSE 0 END) AS command_count,
                SUM(CASE WHEN type = 'flag' THEN 1 ELSE 0 END) AS flag_count,
                SUM(CASE WHEN type = 'error' OR exit_code != 0 THEN 1 ELSE 0 END) AS error_count,
                MIN(NULLIF(started_at, '')) AS first_started_at,
                MAX(NULLIF(ended_at, '')) AS last_ended_at
              FROM events
              GROUP BY mission_id
            ) ev ON ev.mission_id = m.id
            LEFT JOIN (
              SELECT mission_id, GROUP_CONCAT(content, char(31)) AS captured_flags_blob
              FROM (
                SELECT mission_id, content
                FROM events
                WHERE type = 'flag'
                ORDER BY id ASC
              )
              GROUP BY mission_id
            ) flags ON flags.mission_id = m.id
            {where_sql}
            ORDER BY COALESCE(er.updated_at, m.updated_at) DESC, m.created_at DESC
        """

    def _default_experiment_outcome(self, mission_status: str) -> str:
        if mission_status == "done":
            return "success"
        if mission_status == "timeout":
            return "timeout"
        if mission_status == "error":
            return "failed"
        if mission_status == "stopped":
            return "blocked"
        return "unknown"

    def _experiment_row(self, row: sqlite3.Row) -> dict[str, Any]:
        mission_status = row["mission_status"]
        flag_count = int(row["flag_count"] or 0)
        captured_flags = self._captured_flags_from_blob(row["captured_flags_blob"])
        if captured_flags:
            flag_count = len(captured_flags)
        outcome = str(row["outcome"] or "").strip()
        if not outcome:
            outcome = "success" if flag_count > 0 else self._default_experiment_outcome(mission_status)

        terminal_statuses = {"done", "error", "stopped", "timeout"}
        started_at = row["record_started_at"] or row["first_started_at"] or row["mission_created_at"]
        ended_at = row["record_ended_at"] or ""
        if not ended_at and mission_status in terminal_statuses:
            ended_at = row["last_ended_at"] or row["mission_updated_at"]

        return {
            "mission_id": row["mission_id"],
            "mission_name": row["mission_name"],
            "mission_status": mission_status,
            "challenge_code": row["challenge_code"] or "",
            "target": row["target"] or "",
            "goal": row["goal"] or "",
            "difficulty": row["difficulty"] or "",
            "outcome": outcome,
            "failure_reason": row["failure_reason"] or "",
            "key_parameters": row["key_parameters"] or "",
            "notes": row["notes"] or "",
            "started_at": started_at or "",
            "ended_at": ended_at or "",
            "duration_sec": _duration_seconds(started_at, ended_at),
            "selected_skills": _json_loads(row["skills_json"], []),
            "activated_skills": _json_loads(row["activated_skills_json"], []),
            "event_count": int(row["event_count"] or 0),
            "command_count": int(row["command_count"] or 0),
            "error_count": int(row["error_count"] or 0),
            "flag_count": flag_count,
            "captured_flags": captured_flags,
            "captured_flag_count": flag_count,
            "updated_at": row["record_updated_at"] or row["mission_updated_at"],
        }

    def _mission_row(self, row: sqlite3.Row) -> dict[str, Any]:
        if "captured_flags_blob" in row.keys():
            captured_flags = self._captured_flags_from_blob(row["captured_flags_blob"])
        else:
            captured_flags = self.get_captured_flags(row["id"])
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
            "skills": _json_loads(row["skills_json"], []) if "skills_json" in row.keys() else [],
            "activated_skills": _json_loads(row["activated_skills_json"], []) if "activated_skills_json" in row.keys() else [],
            "human_collab_enabled": bool(row["human_collab_enabled"]) if "human_collab_enabled" in row.keys() else False,
            "error_message": row["error_message"],
            "stop_requested": bool(row["stop_requested"]),
            "captured_flags": captured_flags,
            "captured_flag_count": len(captured_flags),
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

    def _flag_from_event_content(self, content: str) -> str:
        text = str(content or "").strip()
        if not text:
            return ""
        return text.splitlines()[0].rsplit(" (", 1)[0].strip()

    def _captured_flags_from_blob(self, blob: Any) -> list[str]:
        if not blob:
            return []
        return self._captured_flags_from_contents(str(blob).split("\x1f"))

    def _captured_flags_from_contents(self, contents: Iterable[Any]) -> list[str]:
        flags: list[str] = []
        seen: set[str] = set()
        for content in contents:
            flag = self._flag_from_event_content(str(content or ""))
            if not flag:
                continue
            key = flag.lower()
            if key in seen:
                continue
            seen.add(key)
            flags.append(flag)
        return flags

    def _observer_agent_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "mission_id": row["mission_id"],
            "parent_id": row["parent_id"],
            "task": row["task"],
            "status": row["status"],
            "metadata": _json_loads(row["metadata_json"], {}),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def _observer_message_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "observer_id": row["observer_id"],
            "mission_id": row["mission_id"],
            "round_no": row["round_no"],
            "type": row["type"],
            "direction": row["direction"],
            "title": row["title"],
            "content": row["content"],
            "metadata": _json_loads(row["metadata_json"], {}),
            "created_at": row["created_at"],
        }

    def _max_round_no_locked(self, mission_id: str) -> int:
        event_row = self._conn.execute(
            "SELECT COALESCE(MAX(round_no), 0) AS n FROM events WHERE mission_id = ?",
            (mission_id,),
        ).fetchone()
        round_row = self._conn.execute(
            "SELECT COALESCE(MAX(round_no), 0) AS n FROM rounds WHERE mission_id = ?",
            (mission_id,),
        ).fetchone()
        return max(int(event_row["n"] or 0), int(round_row["n"] or 0))

    def _guidance_row(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "mission_id": row["mission_id"],
            "content": row["content"],
            "status": row["status"],
            "created_at": row["created_at"],
            "consumed_at": row["consumed_at"],
        }
