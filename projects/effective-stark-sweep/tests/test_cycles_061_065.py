import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


class GenericEngineCW3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.characters = load(
            "artifacts/engine-c-character-selection-v1.json"
        )
        cls.theta = load("artifacts/engine-c-theta-targets-v1.json")
        cls.orbits = load("artifacts/engine-c-unit-orbits-v1.json")
        cls.bridge = load("artifacts/engine-c-packet-bridge-v1.json")
        cls.seal = load(
            "artifacts/engine-c-w3-tranche-01-verified-v1.json"
        )

    def test_exact_character_selection_replays_anchor(self):
        self.assertEqual(self.characters["anchor_replay_count"], 1)
        self.assertEqual(self.characters["new_case_route_count"], 2)
        new = [
            row
            for row in self.characters["records"]
            if row["case_id"] == "RQ-001280"
        ]
        self.assertEqual(len(new), 2)
        self.assertTrue(all(row["stark_s_size"] == 3 for row in new))
        self.assertTrue(
            all(row["exact_separator_index"] == 5 for row in new)
        )

    def test_theta_targets_are_two_route_enclosures(self):
        self.assertEqual(
            self.theta["claim_tag"],
            "ENCLOSED_PRIMITIVE_LPRIME_TARGETS",
        )
        self.assertTrue(self.theta["new_case_two_route_target_overlap"])
        self.assertEqual(len(self.theta["records"]), 3)

    def test_anchor_and_new_orbits(self):
        by_key = {
            (row["case_id"], row["route_id"]): {
                tuple(item) for item in row["isolated_integral_orbit"]
            }
            for row in self.orbits["records"]
        }
        self.assertEqual(
            by_key[("PAPER-II-C-PACKET-0", "Qsqrt(-6)")],
            {(-2, 0), (0, -2), (0, 2), (2, 0)},
        )
        expected = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
        self.assertEqual(
            by_key[("RQ-001280", "Qsqrt(-10)")], expected
        )
        self.assertEqual(
            by_key[("RQ-001280", "Qsqrt(-14)")], expected
        )

    def test_exact_artin_bridge_agrees(self):
        common = self.bridge[
            "identical_two_route_packet_polynomials"
        ]
        self.assertEqual(len(common), 1)
        new = [
            row
            for row in self.bridge["records"]
            if row["case_id"] == "RQ-001280"
        ]
        self.assertEqual(len(new), 2)
        self.assertTrue(
            all(
                row["artin_labeled_packet_polynomial"] == common[0]
                for row in new
            )
        )
        self.assertTrue(
            all(len(row["artin_labeled_positive_norms"]) == 4 for row in new)
        )

    def test_seal_promotes_both_members(self):
        self.assertEqual(self.seal["claim_tag"], "VERIFIED")
        self.assertEqual(
            [row["case_id"] for row in self.seal["members"]],
            ["RQ-001280", "RQ-001297"],
        )
        self.assertTrue(all(self.seal["gates"].values()))

    def test_all_component_source_hashes_replay(self):
        for artifact in (
            self.characters,
            self.theta,
            self.orbits,
            self.bridge,
            self.seal,
        ):
            for relative, expected in artifact["source_hashes"].items():
                actual = hashlib.sha256(
                    (ROOT / relative).read_bytes()
                ).hexdigest()
                self.assertEqual(actual, expected, relative)


if __name__ == "__main__":
    unittest.main()
