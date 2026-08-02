import unittest
from fractions import Fraction

from conventions.projective_tolerance_v1 import theorem_record, tolerance_exponents


class ProjectiveToleranceTests(unittest.TestCase):
    def test_endpoint(self) -> None:
        row = tolerance_exponents(xi=Fraction(16, 25))
        self.assertEqual(row["laurent_tolerance"], Fraction(-16, 25))
        self.assertEqual(row["mode_ceiling"], Fraction(7, 25))

    def test_height_gain(self) -> None:
        row = tolerance_exponents(xi=Fraction(58, 75), coefficient_height=Fraction(2, 15))
        self.assertEqual(row["mode_ceiling"], Fraction(11, 75))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("1/K", row["laurent_tolerance"])
        self.assertIn("7/25", row["worst_exponent"])
        self.assertIn("not yet been summed", row["boundary"])


if __name__ == "__main__":
    unittest.main()
