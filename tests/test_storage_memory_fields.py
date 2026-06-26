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
        self.assertEqual(memory["topology"], [])
        self.assertEqual(
            set(memory),
            {
                "summary",
                "findings",
                "leads",
                "dead_ends",
                "credentials",
                "topology",
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
        self.assertEqual(got["topology"], ["browser -> web"])
        self.assertEqual(
            set(got),
            {
                "summary",
                "findings",
                "leads",
                "dead_ends",
                "credentials",
                "topology",
            },
        )

    def test_memory_table_schema_contains_only_current_fields(self):
        store = MissionStore(":memory:")

        columns = [
            row["name"]
            for row in store._conn.execute("PRAGMA table_info(memories)").fetchall()
        ]

        self.assertEqual(
            columns,
            [
                "mission_id",
                "summary",
                "findings_json",
                "leads_json",
                "dead_ends_json",
                "credentials_json",
                "topology_json",
                "updated_at",
            ],
        )

    def test_request_stop_immediately_marks_running_mission_stopped(self):
        store = MissionStore(":memory:")
        mission_id = self._create_mission(store)
        store.update_mission_status(mission_id, "running")

        updated = store.request_stop(mission_id)
        mission = store.get_mission(mission_id)

        self.assertTrue(updated)
        self.assertTrue(mission["stop_requested"])
        self.assertEqual(mission["status"], "stopped")
        self.assertEqual(mission["error_message"], "Stop requested by operator.")


if __name__ == "__main__":
    unittest.main()
