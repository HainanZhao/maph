import unittest
from fractions import Fraction

from conventions.broad_cf_cylinder_v1 import cylinder_ledger, theorem_record


class BroadCFCylinderTests(unittest.TestCase):
    def test_lower_endpoint(self) -> None:
        row = cylinder_ledger(Fraction(16, 25), Fraction(0))
        self.assertEqual(row["broad_denominator_ceiling"], Fraction(11, 75))
        self.assertEqual(row["narrow_range_width"], Fraction(14, 75))
        self.assertEqual(row["weighted_broad_count"], Fraction(22, 75))
        self.assertEqual(row["target_margin"], Fraction(1, 25))

    def test_worst_broad_floor(self) -> None:
        xi = Fraction(58, 75) - Fraction(1, 7500)
        mu = (1 - xi) / 4
        row = cylinder_ledger(xi, mu)
        self.assertGreater(row["broad_denominator_ceiling"], Fraction(7, 300))
        self.assertGreaterEqual(row["narrow_range_width"], Fraction(14, 75))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("O(1+D|J|)", row["grid_spacing"])
        self.assertIn("D/A0", row["broad_count"])
        self.assertIn(">=1/25", row["weighted_count"])
        self.assertIn("narrow cylinders", row["remaining_range"])


if __name__ == "__main__":
    unittest.main()
