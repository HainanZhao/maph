import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Cycle060Test(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(
            (ROOT / "data/q6-second-base-scope-v1.json").read_text()
        )

    def test_second_base_is_exactly_reconstructed(self):
        route = self.record["second_route"]
        self.assertEqual(route["base"], "Q(sqrt(-3))")
        self.assertEqual(route["base_roots_of_unity_w_k"], 6)
        self.assertEqual(route["character_field_roots_of_unity_e"], 12)
        self.assertEqual(route["selected_character"], [1, 1])
        self.assertEqual(route["selection"]["separating_index"], 3)
        self.assertTrue(
            route["selection"]["source_first_30_coefficients_match"]
        )

    def test_normalized_bridge_is_algebraic_only(self):
        bridge = self.record["normalized_algebraic_bridge"]
        self.assertEqual(bridge["root_free_identity"], "q_8^3=q_12^2")
        self.assertEqual(bridge["exact_identity_count"], 256)
        self.assertEqual(
            bridge["claim_tag"],
            "VERIFIED_ALGEBRAIC_ALIGNMENT_NOT_STARK_IDENTIFICATION",
        )
        self.assertFalse(self.record["scope_failure"]["case_promoted"])

    def test_scope_failure_halts_before_arb(self):
        failure = self.record["scope_failure"]
        self.assertEqual(failure["actual_stark_s_size"], 2)
        self.assertFalse(failure["global_unit_clause_applies"])
        self.assertEqual(
            failure["code"], "STARK_S_SIZE_2_NO_GLOBAL_UNIT_CLAUSE"
        )
        self.assertEqual(failure["disposition"], "HALT_BEFORE_ARB")

    def test_source_hashes_replay(self):
        for relative, expected in self.record["source_hashes"].items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, relative)


if __name__ == "__main__":
    unittest.main()
