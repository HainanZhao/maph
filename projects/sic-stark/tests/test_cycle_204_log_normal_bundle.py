from __future__ import annotations

import unittest

from proof.verify_cycle_204_log_normal_bundle import run


class LogNormalBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_b_generators_are_coordinate_and_a6_invariant(self) -> None:
        b = self.result["b_generator_ledger"]
        self.assertEqual(b["abel_rate_weight"], 0)
        self.assertEqual(b["A6_contraction"]["V_b"], "invariant")
        self.assertEqual(b["positive_coordinate_rescaling"]["eta_b"], "ds_c/s_c=ds/s")

    def test_b_tensor_candidates_retain_rate_weight(self) -> None:
        tensors = self.result["tensor_weight_ledger"]
        self.assertEqual(tensors["row_count"], 36)
        self.assertEqual(tensors["all_candidate_abel_rate_weight"], 1)
        self.assertIn("absent", tensors["missing_operation"])

    def test_direct_fixed_target_map_remains_impossible(self) -> None:
        target = self.result["fixed_target_consequence"]
        self.assertTrue(target["direct_linear_fixed_target_map_impossible"])
        self.assertEqual([row["q"] for row in target["contradictions"]], [2, 3, 5])

    def test_scope_keeps_new_pairing_open(self) -> None:
        self.assertIn("does not exclude", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
