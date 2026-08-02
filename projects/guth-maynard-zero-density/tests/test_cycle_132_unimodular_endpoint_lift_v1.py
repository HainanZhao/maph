import unittest
from fractions import Fraction

from conventions.unimodular_endpoint_lift_v1 import (
    endpoint_ledger,
    extremal_ledger,
    theorem_record,
)


class UnimodularEndpointLiftTests(unittest.TestCase):
    def test_full_endpoint_worst_volume(self) -> None:
        row = extremal_ledger(Fraction(16, 25), Fraction(0))
        self.assertEqual(row["rho"], Fraction(1, 3))
        self.assertEqual(row["tau"], Fraction(16, 25))
        self.assertEqual(row["restored_volume"], Fraction(22, 75))
        self.assertEqual(row["volume_margin"], Fraction(1, 25))
        self.assertEqual(row["cluster_allowance"], 0)

    def test_bandwidth_and_tolerance_margins(self) -> None:
        xi = Fraction(16, 25)
        mu = (1 - xi) / 4
        row = extremal_ledger(xi, mu)
        self.assertEqual(row["fourier_bandwidth"], xi - Fraction(4, 15))
        self.assertEqual(row["ray_tolerance"], -(xi + Fraction(1, 3)))
        self.assertGreaterEqual(row["fourier_bandwidth"], Fraction(28, 75))

    def test_left_endpoint_is_accepted(self) -> None:
        xi = Fraction(7, 10)
        mu = Fraction(1, 20)
        rho = Fraction(7, 45) - 2 * mu / 3
        tau = xi + Fraction(1, 3) - rho
        row = endpoint_ledger(xi, mu, rho, tau)
        self.assertGreater(row["volume_margin"], 0)

    def test_record_keeps_open_norm_visible(self) -> None:
        row = theorem_record()
        self.assertIn("H^{-1}", row["fourier_norm"])
        self.assertIn("determinant s", row["inverse_graph"])
        self.assertIn("Fourier norm is not proved", row["boundary"])


if __name__ == "__main__":
    unittest.main()
