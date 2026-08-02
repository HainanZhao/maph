from fractions import Fraction as Q
import unittest

from conventions.double_b_process_v1 import (
    K_MAX,
    LOW_K_CUTOFF,
    det2,
    dual_hessian,
    exponent_ledger,
    primal_hessian,
    verify_all,
)


class Cycle79DoubleBProcessTests(unittest.TestCase):
    def test_primal_determinant(self) -> None:
        beta, r, q, d_scale = Q(2), Q(3), Q(5), Q(7)
        matrix = primal_hessian(beta, r, q, d_scale)
        self.assertEqual(det2(matrix), -(beta * r / d_scale) ** 2)

    def test_dual_determinant(self) -> None:
        scale, k, r = Q(4), Q(5), Q(6)
        matrix = dual_hessian(scale, k, r)
        self.assertEqual(det2(matrix), -scale**2 / (k**2 * r**2))

    def test_support_ceiling(self) -> None:
        row = exponent_ledger(K_MAX)
        self.assertEqual(row["h_exponent"], Q(21, 25))
        self.assertTrue(row["positive_h_stationary"])

    def test_low_boundary(self) -> None:
        row = exponent_ledger(LOW_K_CUTOFF)
        self.assertEqual(row["h_exponent"], Q(0))
        self.assertTrue(row["positive_h_stationary"])

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("31/25", rows["fourier_contract"])
        self.assertIn("margin 1/25", rows["low_frequency"])


if __name__ == "__main__":
    unittest.main()
