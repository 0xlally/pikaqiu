import unittest

from pikaqiu_agent.storage import MissionStore


class StorageMemoryFieldsTests(unittest.TestCase):
    def test_route_convergence_memory_fields_round_trip(self):
        store = MissionStore(":memory:")
        mission_id = store.create_mission(
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
        memory = store.get_memory(mission_id)
        memory["highest_value_lead"] = "verify /cgi-bin alias differential"
        memory["blocked_reason"] = "two scan-like timeouts"
        memory["next_one_command"] = "curl -i http://x/cgi-bin/test"

        store.set_memory(mission_id, memory)
        got = store.get_memory(mission_id)

        self.assertEqual(got["highest_value_lead"], "verify /cgi-bin alias differential")
        self.assertEqual(got["blocked_reason"], "two scan-like timeouts")
        self.assertEqual(got["next_one_command"], "curl -i http://x/cgi-bin/test")


if __name__ == "__main__":
    unittest.main()
