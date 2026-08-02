import unittest
from fractions import Fraction

from conventions.fiber_saturation_inverse_v1 import (
    reduced_labels,
    saturation_ledger,
    theorem_record,
)


class FiberSaturationInverseTests(unittest.TestCase):
    def test_slack_closure_threshold(self) -> None:
        xi, mu = Fraction(16, 25), Fraction(0)
        rho, tau, edge = Fraction(1, 5), Fraction(4, 5), Fraction(1, 20)
        tied = saturation_ledger(xi, mu, rho, tau, edge, Fraction(1, 15))
        self.assertEqual(tied["slack_threshold"], Fraction(1, 15))
        self.assertEqual(tied["discretization_margin"], 0)
        closed = saturation_ledger(xi, mu, rho, tau, edge, Fraction(7, 100))
        self.assertGreater(closed["discretization_margin"], 0)
        self.assertGreater(closed["volume_margin"], 0)

    def test_jump_is_amplified_by_edge_and_slack(self) -> None:
        row = saturation_ledger(
            Fraction(7, 10), Fraction(0), Fraction(1, 5), Fraction(7, 10), Fraction(1, 20), Fraction(1, 20)
        )
        self.assertEqual(row["legendre_margin"], Fraction(2, 5))
        self.assertEqual(row["next_partial_quotient_floor"], Fraction(2, 5))

    def test_reduced_divisor_labels(self) -> None:
        left, right = reduced_labels(15, 14, 5, 3, 3, 7)
        self.assertEqual(left, (35, 9))
        self.assertEqual(right, (25, 6))
        self.assertEqual(Fraction(*right) / Fraction(*left), Fraction(15, 14))

    def test_record_retains_scope(self) -> None:
        row = theorem_record()
        self.assertIn("J X^{-epsilon}", row["divisor_seed"])
        self.assertIn("zeta=o(1)", row["near_saturation"])
        self.assertIn("no theorem forces", row["boundary"])


if __name__ == "__main__":
    unittest.main()
