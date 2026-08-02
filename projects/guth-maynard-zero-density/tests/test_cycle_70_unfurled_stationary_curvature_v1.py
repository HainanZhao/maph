from fractions import Fraction as Q
import unittest

from conventions.unfurled_stationary_curvature_v1 import endpoint_ledger, verify_all


class Cycle70UnfurledStationaryCurvatureTests(unittest.TestCase):
    def test_shallow_loss(self) -> None:
        row = endpoint_ledger(Q(0))
        self.assertEqual(row["automatic_small_ell_cutoff_exponent"], Q(6, 25))
        self.assertEqual(row["weakest_hessian_exponent"], -Q(9, 25))

    def test_critical_loss(self) -> None:
        row = endpoint_ledger(Q(6, 25))
        self.assertEqual(row["automatic_small_ell_cutoff_exponent"], Q(0))
        self.assertEqual(row["weakest_hessian_exponent"], -Q(3, 5))

    def test_factored_hessian(self) -> None:
        self.assertIn("exp(4*pi*x)-1", endpoint_ledger(Q(0))["factored_hessian"])

    def test_invalid_depth(self) -> None:
        with self.assertRaises(ValueError):
            endpoint_ledger(Q(1, 2))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("positive", rows["nondegeneracy"])
        self.assertIn("two-variable", rows["gate"])


if __name__ == "__main__":
    unittest.main()
