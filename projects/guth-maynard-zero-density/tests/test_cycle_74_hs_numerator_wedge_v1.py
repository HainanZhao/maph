from fractions import Fraction as Q
import unittest

from conventions.hs_numerator_wedge_v1 import hs_numerator_cell, verify_all


class Cycle74HSNumeratorWedgeTests(unittest.TestCase):
    def test_new_cell(self) -> None:
        row = hs_numerator_cell(Q(11, 50), Q(0), Q(1, 50))
        self.assertTrue(row["new_beyond_fraction_budget"])
        self.assertEqual(row["summed_count_exponent"], Q(23, 100))
        self.assertEqual(row["strict_margin"], Q(1, 100))

    def test_theta_endpoint_ties(self) -> None:
        row = hs_numerator_cell(Q(6, 25), Q(0), Q(1, 100))
        self.assertFalse(row["strictly_closed"])
        self.assertEqual(row["summed_count_exponent"], Q(6, 25))

    def test_transition(self) -> None:
        row = hs_numerator_cell(Q(1, 5), Q(0), Q(1, 100))
        self.assertEqual(row["fixed_q_after_trivial_min"], Q(1, 100))

    def test_derivative_dominates(self) -> None:
        row = hs_numerator_cell(Q(11, 50), Q(0), Q(1, 50))
        self.assertGreater(row["derivative_term"], row["tube_term"])
        self.assertGreater(row["derivative_term"], row["ratio_term"])

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("theta+w", rows["summed_bound"])
        self.assertIn("average in q", rows["gate"])


if __name__ == "__main__":
    unittest.main()
