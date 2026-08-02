import unittest
from fractions import Fraction

from conventions.common_multiplier_scalar_v1 import (
    common_multiplier,
    scalar_ledger,
    theorem_record,
)


class CommonMultiplierScalarTests(unittest.TestCase):
    def test_exact_rectangle_multiplier(self) -> None:
        xa, xb = Fraction(2, 3), Fraction(10, 21)
        xc, xd = Fraction(7, 5), Fraction(1, 1)
        self.assertEqual(xb * xc, xd * xa)
        self.assertEqual(common_multiplier(xa, xb, xc, xd), Fraction(5, 7))

    def test_strict_region_ledger(self) -> None:
        row = scalar_ledger(Fraction(7, 10), Fraction(0), Fraction(1, 5), Fraction(13, 20))
        self.assertEqual(row["tail_frequency"], Fraction(9, 20))
        self.assertEqual(row["legendre_margin"], Fraction(1, 10))
        self.assertEqual(row["next_partial_quotient_floor"], Fraction(1, 10))
        self.assertEqual(row["next_denominator_floor"], Fraction(1, 2))

    def test_boundary_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            scalar_ledger(Fraction(7, 10), Fraction(0), Fraction(1, 5), Fraction(3, 5))

    def test_record_keeps_exception_average_open(self) -> None:
        row = theorem_record()
        self.assertIn("one reduced rational r_d", row["common_multiplier"])
        self.assertIn("N^3/S", row["scalar_dichotomy"])
        self.assertIn("no averaged exclusion", row["boundary"])


if __name__ == "__main__":
    unittest.main()
