from __future__ import annotations

import unittest

from proof.verify_cycle_212_logarithmic_axis_to_packet_orientation import run


class LogarithmicAxisToPacketOrientationTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_both_logarithmic_lifts_reach_distinct_cusps(self):
        lifts = self.result["logarithmic_lifts"]["lifts"]
        self.assertEqual([row["epsilon"] for row in lifts], [1, -1])
        self.assertEqual([row["s_to_zero_cusp"] for row in lifts], ["t->infinity, [e_(0,5)]", "t->0^+, [e_(5,0)]"])

    def test_embedding_and_frobenius_do_not_supply_analytic_selector(self):
        self.assertEqual(self.result["real_embedding_audit"]["epsilon_selector"], "NOT_SUPPLIED")
        self.assertEqual(self.result["frobenius_provenance_audit"]["analytic_coordinate_action"], "NOT_SUPPLIED_BY_FROZEN_ARTIFACT")

    def test_a6_keeps_both_signs(self):
        audit = self.result["two_sign_equivariance_audit"]
        self.assertEqual(audit["frozen_selector_count"], 0)
        self.assertEqual(audit["A6_action_on_epsilon"], "NOT_SUPPLIED; both covariant lifts remain admissible")


if __name__ == "__main__":
    unittest.main()
