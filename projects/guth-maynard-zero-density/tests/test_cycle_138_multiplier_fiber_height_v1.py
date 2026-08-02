import unittest
from fractions import Fraction

from conventions.multiplier_fiber_height_v1 import (
    cancellation_divisor,
    closure_ledger,
    split_cancellation_divisor,
    theorem_record,
)


class MultiplierFiberHeightTests(unittest.TestCase):
    def test_cross_gcd_identity(self) -> None:
        rows = ((5, 7, 14, 9), (12, 5, 25, 7), (7, 11, 33, 20), (1, 13, 26, 9))
        for a, b, p, q in rows:
            self.assertEqual(cancellation_divisor(a, b, p, q), split_cancellation_divisor(a, b, p, q))

    def test_uniform_extension(self) -> None:
        row = closure_ledger(
            Fraction(16, 25), Fraction(0), Fraction(29, 180), Fraction(4, 5)
        )
        self.assertEqual(row["rho_ceiling"], Fraction(1, 6))
        self.assertEqual(row["extension_beyond_hs"], Fraction(1, 90))
        self.assertGreater(row["discretization_margin"], 0)
        self.assertGreater(row["volume_margin"], 0)

    def test_maximal_mu_extension_is_larger(self) -> None:
        xi = Fraction(16, 25)
        mu = (1 - xi) / 4
        rho = Fraction(1, 6) - mu / 2 - Fraction(1, 1000)
        tau = xi + Fraction(1, 3) - rho
        row = closure_ledger(xi, mu, rho, tau)
        self.assertEqual(row["extension_beyond_hs"], Fraction(1, 90) + mu / 6)
        self.assertGreater(row["volume_gap_condition"], 0)

    def test_record_keeps_regional_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("N^2 H^{-1}", row["fiber_bound"])
        self.assertIn("cancels exactly", row["weighted_count"])
        self.assertIn("no full paired norm", row["boundary"])


if __name__ == "__main__":
    unittest.main()
