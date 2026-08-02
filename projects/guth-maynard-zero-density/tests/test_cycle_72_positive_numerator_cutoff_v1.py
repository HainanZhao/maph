from fractions import Fraction as Q
import unittest

from conventions.positive_numerator_cutoff_v1 import cutoff_ledger, verify_all


class Cycle72PositiveNumeratorCutoffTests(unittest.TestCase):
    def test_maximum_denominator(self) -> None:
        row = cutoff_ledger(Q(11, 25))
        self.assertEqual(row["ell_cutoff_exponent"], Q(4, 25))
        self.assertEqual(row["sharp_hessian_loss_exponent"], Q(11, 25))

    def test_shallow_denominator(self) -> None:
        row = cutoff_ledger(Q(3, 25))
        self.assertEqual(row["ell_cutoff_exponent"], Q(12, 25))

    def test_zero_denominator_scale(self) -> None:
        self.assertEqual(cutoff_ledger(Q(0))["ell_cutoff_exponent"], Q(3, 5))

    def test_invalid_scale(self) -> None:
        with self.assertRaises(ValueError):
            cutoff_ledger(Q(1, 2))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("q=1", rows["q1_exception"])
        self.assertIn("X^theta", rows["supersession"])


if __name__ == "__main__":
    unittest.main()
