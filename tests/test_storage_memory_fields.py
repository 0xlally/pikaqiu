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

    def test_new_mission_returns_single_layer_memory(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)

        memory = store.get_memory(mission_id)

        self.assertEqual(memory["summary"], "")
        self.assertEqual(memory["findings"], [])
        self.assertEqual(memory["leads"], [])
        self.assertEqual(memory["dead_ends"], [])
        self.assertEqual(memory["credentials"], [])
        self.assertEqual(memory["next_focus"], [])
        self.assertEqual(memory["nodes"], {})
        self.assertEqual(memory["topology"], [])
        self.assertEqual(
            set(memory),
            {
                "summary",
                "findings",
                "leads",
                "dead_ends",
                "credentials",
                "next_focus",
                "nex_focus",
                "nodes",
                "topology",
                "highest_value_lead",
                "blocked_reason",
                "next_one_command",
                "updated_at",
            },
        )

    def test_single_layer_memory_round_trip(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)
        memory = store.get_memory(mission_id)
        memory.update(
            {
                "summary": "admin route exists; auth needed",
                "findings": ["admin page leaks version"],
                "leads": ["test version-specific exploit"],
                "dead_ends": ["full port scan was blocked"],
                "credentials": ["admin:admin"],
                "next_focus": ["curl -i http://x/admin"],
                "highest_value_lead": "test admin route",
                "blocked_reason": "need raw response",
                "next_one_command": "curl -i -u admin:admin http://x/admin",
                "nodes": {
                    "http://x": {
                        "role": "web",
                        "access_level": "recon",
                        "findings": ["admin route exists"],
                        "credentials": ["admin:admin"],
                        "flags_found": [],
                        "next_steps": ["request /admin with auth"],
                    }
                },
                "topology": ["browser -> web"],
            }
        )

        store.set_memory(mission_id, memory)
        got = store.get_memory(mission_id)

        self.assertEqual(got["summary"], "admin route exists; auth needed")
        self.assertEqual(got["findings"], ["admin page leaks version"])
        self.assertEqual(got["leads"], ["test version-specific exploit"])
        self.assertEqual(got["dead_ends"], ["full port scan was blocked"])
        self.assertEqual(got["credentials"], ["admin:admin"])
        self.assertEqual(got["next_focus"], ["curl -i http://x/admin"])
        self.assertEqual(got["highest_value_lead"], "test admin route")
        self.assertEqual(got["blocked_reason"], "need raw response")
        self.assertEqual(got["next_one_command"], "curl -i -u admin:admin http://x/admin")
        self.assertEqual(got["nodes"]["http://x"]["role"], "web")
        self.assertEqual(got["topology"], ["browser -> web"])
        self.assertEqual(
            set(got),
            {
                "summary",
                "findings",
                "leads",
                "dead_ends",
                "credentials",
                "next_focus",
                "nex_focus",
                "nodes",
                "topology",
                "highest_value_lead",
                "blocked_reason",
                "next_one_command",
                "updated_at",
            },
        )


if __name__ == "__main__":
    unittest.main()
