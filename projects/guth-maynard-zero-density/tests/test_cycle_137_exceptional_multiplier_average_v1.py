import unittest
from fractions import Fraction

from conventions.exceptional_multiplier_average_v1 import average_ledger, theorem_record


class ExceptionalMultiplierAverageTests(unittest.TestCase):
    def test_registered_nonempty_cell(self) -> None:
        row = average_ledger(
            Fraction(16, 25), Fraction(0), Fraction(7, 45), Fraction(184, 225), Fraction(0)
        )
        self.assertEqual(row["edge_ceiling_discretization"], Fraction(1, 45))
        self.assertEqual(row["edge_ceiling_volume"], Fraction(173, 450))
        self.assertEqual(row["edge_ceiling"], Fraction(1, 45))
        self.assertGreater(row["discretization_margin"], 0)

    def test_edge_boundary_ties(self) -> None:
        row = average_ledger(
            Fraction(16, 25), Fraction(0), Fraction(7, 45), Fraction(184, 225), Fraction(1, 45)
        )
        self.assertEqual(row["discretization_margin"], 0)

    def test_strict_exact_region_required(self) -> None:
        with self.assertRaises(ValueError):
            average_ledger(Fraction(7, 10), Fraction(0), Fraction(1, 5), Fraction(3, 5), Fraction(0))

    def test_record_preserves_weighted_target(self) -> None:
        row = theorem_record()
        self.assertIn("B_exc J^2", row["weighted_target"])
        self.assertIn("N^4", row["residual_deficit"])
        self.assertIn("no high-edge", row["boundary"])


if __name__ == "__main__":
    unittest.main()
