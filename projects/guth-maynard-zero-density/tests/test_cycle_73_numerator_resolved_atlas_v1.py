from fractions import Fraction as Q
import unittest

from conventions.numerator_resolved_atlas_v1 import numerator_cell, verify_all


class Cycle73NumeratorResolvedAtlasTests(unittest.TestCase):
    def test_bounded_numerator_closure(self) -> None:
        row = numerator_cell(Q(1, 5), Q(0), Q(0))
        self.assertTrue(row["strictly_closed"])
        self.assertEqual(row["strict_margin"], Q(1, 25))
        self.assertEqual(row["ell_exponent"], Q(2, 5))

    def test_bulk_curvature(self) -> None:
        row = numerator_cell(Q(1, 5), Q(0), Q(1, 5))
        self.assertFalse(row["strictly_closed"])
        self.assertEqual(row["hessian_loss_exponent"], Q(0))

    def test_boundary(self) -> None:
        row = numerator_cell(Q(1, 5), Q(1, 25), Q(0))
        self.assertFalse(row["strictly_closed"])
        self.assertEqual(row["strict_margin"], Q(0))

    def test_invalid_numerator(self) -> None:
        with self.assertRaises(ValueError):
            numerator_cell(Q(1, 10), Q(0), Q(1, 5))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("theta+alpha+kappa", rows["closed_region"])
        self.assertEqual(rows["hessian_loss"], "theta-alpha")


if __name__ == "__main__":
    unittest.main()
