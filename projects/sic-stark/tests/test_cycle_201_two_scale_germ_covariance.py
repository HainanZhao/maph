from __future__ import annotations

import unittest

from proof.verify_cycle_201_two_scale_germ_covariance import run


class TwoScaleGermCovarianceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_source_regular_component_has_weight_one(self) -> None:
        action = self.result["source_regulator_action"]
        self.assertEqual(action["dilations"], [2, 3, 5])
        self.assertEqual(action["regular_weight"], 1)

    def test_regulator_invariance_kills_regular_component(self) -> None:
        no_go = self.result["invariant_linear_functional_no_go"]
        self.assertEqual(no_go["restriction_on_E_reg"], "zero")
        self.assertIn("q=2", no_go["proof"])

    def test_remaining_boundary_rank_cannot_hit_all_targets(self) -> None:
        rank = self.result["all_row_rank_consequence"]
        self.assertEqual(rank["surviving_boundary_rank_upper_bound"], 30)
        self.assertEqual(rank["C198_distinct_target_basis_dimension"], 36)
        self.assertTrue(rank["linear_all36_target_map_impossible"])

    def test_scope_does_not_claim_general_no_go(self) -> None:
        self.assertIn("does not exclude", self.result["claim_boundary"])
        self.assertIn("does not prove", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
