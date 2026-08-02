import unittest
from fractions import Fraction

from conventions.weighted_weak_sector_v1 import exponent_ledger, theorem_record


class WeightedWeakSectorTests(unittest.TestCase):
    def test_worst_endpoint(self) -> None:
        row = exponent_ledger(Fraction(16, 25))
        self.assertEqual(row["weak_total"], Fraction(59, 150))
        self.assertEqual(row["margin"], Fraction(1, 25))

    def test_upper_band_edge(self) -> None:
        row = exponent_ledger(Fraction(3, 4))
        self.assertEqual(row["energy_term"], Fraction(17, 60))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("at most one integer A", row["A_uniqueness"])
        self.assertIn("1/25", row["exponent"])
        self.assertIn("simple-root", row["boundary"])


if __name__ == "__main__":
    unittest.main()
