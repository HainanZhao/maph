import unittest
from fractions import Fraction

from conventions.simple_root_volume_v1 import exponent_ledger, theorem_record


class SimpleRootVolumeTests(unittest.TestCase):
    def test_left_endpoint(self) -> None:
        row = exponent_ledger(Fraction(16, 25))
        self.assertEqual(row["raw_volume"], Fraction(92, 75))
        self.assertEqual(row["weighted_volume"], Fraction(109, 150))
        self.assertEqual(row["required_saving"], Fraction(22, 75))

    def test_upper_edge_limit(self) -> None:
        epsilon = Fraction(1, 7500)
        row = exponent_ledger(Fraction(58, 75) - epsilon)
        self.assertEqual(row["required_saving"], Fraction(4, 25) + epsilon)

    def test_factorization_and_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("T_sigma(h) T_tau(h)", row["fourier_factorization"])
        self.assertIn("termwise in absolute value", row["limitation"])
        self.assertIn("does not exclude", row["boundary"])

    def test_rejects_outside_band(self) -> None:
        with self.assertRaises(ValueError):
            exponent_ledger(Fraction(58, 75))


if __name__ == "__main__":
    unittest.main()
