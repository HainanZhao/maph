from fractions import Fraction as Q
import unittest

from conventions.fraction_budget_wedge_v1 import fraction_cell, verify_all


class Cycle71FractionBudgetWedgeTests(unittest.TestCase):
    def test_interior(self) -> None:
        row = fraction_cell(Q(1, 10), Q(0))
        self.assertTrue(row["strictly_closed"])
        self.assertEqual(row["strict_count_margin"], Q(1, 25))
        self.assertEqual(row["weighted_pair_bound_exponent"], Q(16, 25))

    def test_boundary_tie(self) -> None:
        row = fraction_cell(Q(3, 25), Q(0))
        self.assertFalse(row["strictly_closed"])
        self.assertEqual(row["strict_count_margin"], Q(0))

    def test_depth_axis(self) -> None:
        self.assertTrue(fraction_cell(Q(0), Q(1, 5))["strictly_closed"])

    def test_outside_admissible(self) -> None:
        with self.assertRaises(ValueError):
            fraction_cell(Q(1, 2), Q(0))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("2theta+kappa", rows["closed_wedge"])
        self.assertIn("unfurled", rows["gate"])


if __name__ == "__main__":
    unittest.main()
