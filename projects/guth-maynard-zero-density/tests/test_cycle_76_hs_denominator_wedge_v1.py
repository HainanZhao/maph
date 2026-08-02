from fractions import Fraction as Q
import unittest

from conventions.hs_denominator_wedge_v1 import hs_denominator_cell, verify_all


class Cycle76HSDenominatorWedgeTests(unittest.TestCase):
    def test_new_witness(self) -> None:
        row = hs_denominator_cell(Q(6, 25), Q(0), Q(0))
        self.assertTrue(row["new_beyond_cycle75"])
        self.assertEqual(row["summed_numerator_count_exponent"], Q(9, 50))
        self.assertEqual(row["denominator_strict_margin"], Q(3, 50))

    def test_endpoint_tie(self) -> None:
        row = hs_denominator_cell(Q(6, 25), Q(0), Q(9, 175))
        self.assertFalse(row["denominator_strictly_closed"])
        self.assertEqual(row["denominator_strict_margin"], Q(0))

    def test_derivative_dominates_other_hs_terms(self) -> None:
        for theta, kappa, alpha in (
            (Q(6, 25), Q(0), Q(0)),
            (Q(1, 3), Q(8, 75), Q(1, 5)),
            (Q(11, 25), Q(0), Q(1, 10)),
        ):
            row = hs_denominator_cell(theta, kappa, alpha)
            self.assertGreater(row["denominator_derivative_term"], row["denominator_tube_term"])
            self.assertGreater(row["denominator_derivative_term"], row["denominator_ratio_term"])

    def test_transition_at_three_twentieths(self) -> None:
        row = hs_denominator_cell(Q(3, 20), Q(0), Q(0))
        self.assertEqual(row["fixed_a_after_trivial_min"], Q(3, 20))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("9/50", rows["new_witness"])
        self.assertIn("E14", rows["gate"])


if __name__ == "__main__":
    unittest.main()
