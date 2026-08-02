import unittest
from fractions import Fraction
from math import exp

from conventions.critical_rational_ray_v1 import (
    CriticalRay,
    farey_spacing,
    theorem_record,
)


class CriticalRationalRayTests(unittest.TestCase):
    def test_label_height_and_critical_identity(self) -> None:
        row = CriticalRay(B=2, C=3, a=2, b=-3, Q=5, M=3)
        self.assertEqual(row.label, Fraction(9, 4))
        self.assertLessEqual(row.label.numerator, row.height_budget)
        self.assertLessEqual(row.label.denominator, row.height_budget)
        self.assertAlmostEqual(exp(row.w * row.critical_point), float(row.label))

    def test_strong_compiler_anchor(self) -> None:
        row = CriticalRay(B=2, C=3, a=2, b=-3, Q=5, M=3)
        result = row.compile(row.critical_point + 1e-8)
        self.assertTrue(result["unique_fixed_w"])
        self.assertTrue(result["injective_across_w"])
        self.assertTrue(result["strong_compiler"])

    def test_farey_spacing_exhaustive(self) -> None:
        height = 12
        rationals = {
            Fraction(numerator, denominator)
            for numerator in range(1, height + 1)
            for denominator in range(1, height + 1)
        }
        rationals = sorted(rationals)
        for left, right in zip(rationals, rationals[1:]):
            self.assertGreaterEqual(farey_spacing(left, right), Fraction(1, height * height))

    def test_invalid_orientation(self) -> None:
        with self.assertRaises(ValueError):
            CriticalRay(B=1, C=1, a=2, b=1, Q=2, M=2)

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("1/(2*H^2)", record["fixed_w_uniqueness"])
        self.assertIn("no bound", record["boundary"])


if __name__ == "__main__":
    unittest.main()
