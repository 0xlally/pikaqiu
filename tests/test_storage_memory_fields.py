import unittest

from pikaqiu_agent.storage import MissionStore


class StorageMemoryFieldsTests(unittest.TestCase):
    def _create_mission(self, store: MissionStore) -> str:
        return store.create_mission(
            name="t",
            target="http://x",
            goal="flag",
            scope="http://x",
            domains=["web"],
            max_rounds=1,
            max_commands=1,
            command_timeout_sec=1,
            model="mock",
        )

    def test_new_mission_returns_empty_boards(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)

        memory = store.get_memory(mission_id)

        self.assertEqual(memory["idea_board"], {})
        self.assertEqual(memory["memory_board"], {})

    def test_two_board_memory_round_trip_and_legacy_projection(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)
        memory = store.get_memory(mission_id)
        memory["idea_board"] = {
            "active_direction": "probe upload parser",
            "primary_hypothesis": "avatar upload reaches image parser",
            "next_verification": "curl -i -F file=@polyglot.jpg http://x/upload",
            "next_actions": ["send polyglot upload"],
            "candidate_directions": ["upload parser", "admin cookie"],
            "risk_or_blocker": "need raw upload error",
            "failure_boundary": "parser rejects every content type",
            "blocked_prerequisite": "valid login",
            "required_next_evidence": "status, body, saved path",
            "abandoned": ["wide directory brute force"],
        }
        memory["memory_board"] = {
            "facts": ["upload endpoint exists"],
            "evidence": ["GET /upload returned 200"],
            "constraints": ["no outbound callbacks"],
            "credentials": ["user:pass"],
            "failed_attempts": ["ffuf common paths timed out"],
            "nodes": {"http://x": {"role": "web", "access_level": "http"}},
            "topology": ["browser -> web"],
        }

        store.set_memory(mission_id, memory)
        got = store.get_memory(mission_id)

        self.assertEqual(got["idea_board"]["active_direction"], "probe upload parser")
        self.assertEqual(got["idea_board"]["next_verification"], "curl -i -F file=@polyglot.jpg http://x/upload")
        self.assertEqual(got["memory_board"]["facts"], ["upload endpoint exists"])
        self.assertEqual(got["memory_board"]["evidence"], ["GET /upload returned 200"])
        self.assertEqual(got["memory_board"]["credentials"], ["user:pass"])
        self.assertEqual(got["highest_value_lead"], "probe upload parser")
        self.assertEqual(got["findings"], ["upload endpoint exists"])
        self.assertEqual(got["leads"], ["upload parser", "admin cookie"])
        self.assertEqual(got["dead_ends"], ["ffuf common paths timed out"])
        self.assertEqual(got["next_focus"], ["send polyglot upload"])

    def test_legacy_fields_derive_two_board_memory(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)
        memory = store.get_memory(mission_id)
        memory.update(
            {
                "findings": ["admin page leaks version"],
                "leads": ["test version-specific exploit"],
                "dead_ends": ["full port scan was blocked"],
                "credentials": ["admin:admin"],
                "next_focus": ["curl -i http://x/admin"],
                "highest_value_lead": "test admin route",
                "blocked_reason": "need raw response",
                "primary_hypothesis": "admin route exposes flag after auth",
                "next_verification": "curl -i -u admin:admin http://x/admin",
                "failure_boundary": "admin route returns no useful body",
                "blocked_prerequisite": "valid basic auth",
                "required_next_evidence": "status and response body",
            }
        )

        store.set_memory(mission_id, memory)
        got = store.get_memory(mission_id)

        self.assertEqual(got["idea_board"]["active_direction"], "test admin route")
        self.assertEqual(got["idea_board"]["primary_hypothesis"], "admin route exposes flag after auth")
        self.assertEqual(got["idea_board"]["next_verification"], "curl -i -u admin:admin http://x/admin")
        self.assertEqual(got["idea_board"]["candidate_directions"], ["test version-specific exploit"])
        self.assertEqual(got["memory_board"]["facts"], ["admin page leaks version"])
        self.assertEqual(got["memory_board"]["credentials"], ["admin:admin"])
        self.assertEqual(got["memory_board"]["failed_attempts"], ["full port scan was blocked"])

    def test_explicit_idea_board_next_verification_overrides_stale_legacy_projection(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)
        memory = store.get_memory(mission_id)
        memory["next_verification"] = "curl -i http://x/old"
        memory["next_one_command"] = "curl -i http://x/older"
        memory["idea_board"] = {
            "active_direction": "verify current admin route",
            "next_verification": "curl -i http://x/current-admin",
        }

        store.set_memory(mission_id, memory)
        got = store.get_memory(mission_id)

        self.assertEqual(got["idea_board"]["next_verification"], "curl -i http://x/current-admin")
        self.assertEqual(got["next_verification"], "curl -i http://x/current-admin")
        self.assertEqual(got["next_one_command"], "curl -i http://x/current-admin")

    def test_route_convergence_memory_fields_round_trip(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)
        memory = store.get_memory(mission_id)
        memory["highest_value_lead"] = "verify /cgi-bin alias differential"
        memory["blocked_reason"] = "two scan-like timeouts"
        memory["next_one_command"] = "curl -i http://x/cgi-bin/test"
        memory["primary_hypothesis"] = "current route can reach admin-only content"
        memory["next_verification"] = "curl -i http://x/admin"
        memory["failure_boundary"] = "unanswered_hypothesis"
        memory["blocked_prerequisite"] = "raw admin response"
        memory["required_next_evidence"] = "status, headers, body"
        memory["observer_enforcement_state"] = "pending"
        memory["agent_override_reason"] = "manual test"

        store.set_memory(mission_id, memory)
        got = store.get_memory(mission_id)

        self.assertEqual(got["highest_value_lead"], "verify /cgi-bin alias differential")
        self.assertEqual(got["blocked_reason"], "two scan-like timeouts")
        self.assertEqual(got["next_one_command"], "curl -i http://x/cgi-bin/test")
        self.assertEqual(got["primary_hypothesis"], "current route can reach admin-only content")
        self.assertEqual(got["next_verification"], "curl -i http://x/admin")
        self.assertEqual(got["failure_boundary"], "unanswered_hypothesis")
        self.assertEqual(got["blocked_prerequisite"], "raw admin response")
        self.assertEqual(got["required_next_evidence"], "status, headers, body")
        self.assertEqual(got["observer_enforcement_state"], "pending")
        self.assertEqual(got["agent_override_reason"], "manual test")


if __name__ == "__main__":
    unittest.main()
