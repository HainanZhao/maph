import unittest
from fractions import Fraction

from conventions.transition_entropy_v1 import (
    entropy_ledger,
    normalized_tail,
    recovered_error,
    shear_lift,
    theorem_record,
)


class TransitionEntropyTests(unittest.TestCase):
    def test_shear_preserves_determinant(self) -> None:
        p, q, p0, r0 = 3, 2, 5, 3
        for t in (-5, 0, 9):
            p1, r1 = shear_lift(p, q, p0, r0, t)
            self.assertEqual(p1 * q - p * r1, 1)

    def test_tail_recovers_error(self) -> None:
        alpha = Fraction(7, 5)
        p, q, r = 4, 3, 4
        theta = normalized_tail(alpha, p, q, r)
        self.assertTrue(0 < theta < 1)
        self.assertEqual(recovered_error(q, r, theta), abs(alpha - Fraction(p, q)))

    def test_full_endpoint_entropy_floor(self) -> None:
        xi = Fraction(16, 25)
        mu = Fraction(0)
        rho = Fraction(1, 3)
        tau = xi
        row = entropy_ledger(xi, mu, rho, tau)
        self.assertEqual(row["shear_entropy"], Fraction(23, 75))
        self.assertEqual(row["full_endpoint_minimum"], Fraction(23, 75))

    def test_record_is_scoped(self) -> None:
        row = theorem_record()
        self.assertIn("S/N", row["dyadic_entropy"])
        self.assertIn("theta", row["scoped_no_go"])
        self.assertIn("not a no-go theorem", row["boundary"])


if __name__ == "__main__":
    unittest.main()
