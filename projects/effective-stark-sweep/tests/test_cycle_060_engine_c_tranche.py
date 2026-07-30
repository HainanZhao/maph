import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EngineCTrancheBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(
            (
                ROOT
                / "artifacts/engine-c-w3-tranche-01-boundary-v1.json"
            ).read_text()
        )

    def test_no_w3_promotion(self):
        self.assertEqual(
            self.record["promotion_state"],
            "BLOCKED_MISSING_GENERIC_W3",
        )
        self.assertEqual(
            self.record["claim_tag"], "VERIFIED_STAGING_ONLY"
        )

    def test_exact_e_replay_matches_inventory(self):
        tranche = self.record["tranche"]
        self.assertEqual(tranche["route_e_expected"], [2, 2])
        self.assertEqual(tranche["route_e_replayed"], [2, 2])
        self.assertTrue(tranche["inventory_e_assertion"])

    def test_closure_members_are_separate_occurrences(self):
        members = self.record["tranche"]["members"]
        self.assertEqual(
            [member["case_id"] for member in members],
            ["RQ-001280", "RQ-001297"],
        )
        self.assertEqual(
            [member["finite_norm"] for member in members], [32, 64]
        )
        self.assertTrue(all(member["geometry_pass"] for member in members))
        self.assertTrue(
            all(
                member["w3_state"] == "BLOCKED_MISSING_GENERIC_W3"
                for member in members
            )
        )

    def test_all_promotion_components_are_named(self):
        self.assertEqual(
            {
                item["component"]
                for item in self.record["missing_promotion_components"]
            },
            {
                "exact_character_table",
                "arb_orbit_isolation",
                "exact_packet_bridge",
            },
        )


if __name__ == "__main__":
    unittest.main()
