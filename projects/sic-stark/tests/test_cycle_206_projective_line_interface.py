from __future__ import annotations

import unittest

from proof.verify_cycle_206_projective_line_interface import run


class ProjectiveLineInterfaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_full_packet_is_retained_without_an_affine_chart(self) -> None:
        packet = self.result["source_projective_packet"]
        self.assertEqual(packet["coordinate_count_per_h"], 36)
        self.assertEqual(packet["h_channel_count"], 6)
        self.assertEqual(packet["total_labelled_packet_count"], 216)
        self.assertIn("t>0", packet["declared_real_source_locus"])
        self.assertIn("1+t^6+t^12=0", packet["common_factor_base_locus"])
        self.assertIn("no affine coordinate", packet["projective_object"])

    def test_all_denominator_free_source_binomials_vanish(self) -> None:
        ledger = self.result["elementary_binomial_ledger"]
        self.assertEqual(ledger["relation_count"], 150)
        self.assertTrue(ledger["denominator_free"])
        self.assertTrue(ledger["all_relations_identically_zero"])

    def test_common_rate_and_a6_actions_are_projective(self) -> None:
        covariance = self.result["common_line_covariance"]
        self.assertEqual([row["q"] for row in covariance["dilation_records"]], [2, 3, 5])
        self.assertEqual(covariance["source_projective_covariance"], "PROVED")
        self.assertEqual(len(covariance["all_36_label_records"]), 36)

    def test_target_equality_remains_an_open_multiplicative_interface(self) -> None:
        comparison = self.result["c198_projective_comparison"]
        self.assertTrue(comparison["all_36_targets_finite_nonzero"])
        self.assertEqual(comparison["target_elementary_binomial_count"], 25)
        self.assertFalse(comparison["provided_multiplicative_binomial_law"])
        self.assertEqual(
            comparison["comparison_status"],
            "OPEN_REQUIRES_NEW_SOURCE_MULTIPLICATIVE_THEOREM",
        )


if __name__ == "__main__":
    unittest.main()
