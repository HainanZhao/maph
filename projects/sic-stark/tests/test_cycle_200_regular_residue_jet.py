from __future__ import annotations

import unittest

from proof.verify_cycle_200_regular_residue_jet import run


class RegularResidueJetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_paired_pole_sector_has_only_even_jets(self) -> None:
        jets = self.result["paired_pole_jet_parity"]
        self.assertEqual(jets["retained_orders_through_five"], [0, 2, 4])
        self.assertTrue(jets["odd_delta_jets_source_forbidden_by_pair_symmetry"])
        self.assertEqual(jets["all_a_b_rank_upper_bound_through_order_five"], 30)
        self.assertIn("binom(5,b)", jets["fixed_a_collision_witness"])

    def test_off_support_coefficient_is_source_derived_but_rate_dependent(self) -> None:
        regular = self.result["first_off_support_coefficient"]
        self.assertEqual(
            regular["first_s_coefficient"],
            "lambda/(1-cosh(c_beta*Lambda))",
        )
        self.assertIn("not a lambda-independent endpoint limit", regular["rate_dependence"])

    def test_full_packets_have_all_36_analytic_rank(self) -> None:
        packets = self.result["full_packet_independence"]
        self.assertEqual(packets["row_count"], 36)
        self.assertEqual(packets["analytic_function_rank"], 36)
        self.assertIn("does not construct J", packets["scope"])

    def test_scope_preserves_interface_boundary(self) -> None:
        boundary = self.result["claim_boundary"]
        self.assertIn("not an endpoint distribution", boundary)
        self.assertIn("neither a", boundary)


if __name__ == "__main__":
    unittest.main()
