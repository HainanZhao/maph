from __future__ import annotations

import unittest

from proof.verify_cycle_202_normal_derivative_target_weight import run


class NormalDerivativeTargetWeightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_normal_data_has_weight_one_on_all_rows(self) -> None:
        normal = self.result["normal_data"]
        self.assertEqual(normal["row_count"], 36)
        self.assertEqual(normal["rate_weight"], 1)
        self.assertEqual(normal["dilations"], [2, 3, 5])

    def test_c198_targets_are_nonzero_and_rate_zero(self) -> None:
        targets = self.result["fixed_targets"]
        self.assertEqual(targets["row_count"], 36)
        self.assertTrue(targets["all_endpoint_values_finite_nonzero"])
        self.assertEqual(targets["abel_rate_weight"], 0)

    def test_direct_fixed_target_bridge_is_impossible(self) -> None:
        result = self.result["direct_bridge_weight_contradiction"]
        self.assertTrue(result["all_36_direct_equalities_impossible"])
        self.assertEqual([row["q"] for row in result["contradictions"]], [2, 3, 5])

    def test_scope_excludes_broader_constructions(self) -> None:
        self.assertIn("does not exclude", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
