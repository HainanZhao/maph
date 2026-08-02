import unittest
from fractions import Fraction

from conventions.freiman_ray_web_v1 import threshold_ledger, theorem_record


class FreimanRayWebTests(unittest.TestCase):
    def test_threshold_endpoints(self) -> None:
        left = threshold_ledger(Fraction(16, 25), Fraction(1, 10))
        self.assertEqual(left["high_multiplicity_threshold"], Fraction(9, 100))
        self.assertTrue(left["high_multiplicity"])
        near_right = threshold_ledger(Fraction(58, 75) - Fraction(1, 7500), Fraction(3, 50))
        self.assertEqual(near_right["high_multiplicity_threshold"], Fraction(17, 300) + Fraction(1, 30000))

    def test_energy_identity_at_threshold(self) -> None:
        xi = Fraction(7, 10)
        mu = (1 - xi) / 4
        row = threshold_ledger(xi, mu)
        self.assertEqual(row["energy_floor_from_excess"], xi - Fraction(4, 15))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("M^4K>>Q^3", row["integer_forcing"])
        self.assertIn("R^4/(2D-1)", row["energy"])
        self.assertIn("Freiman 2-homomorphism", row["valuation_web"])
        self.assertIn("does not give", row["seed_gate"])


if __name__ == "__main__":
    unittest.main()
