import unittest
from fractions import Fraction

from conventions.bounded_multiplier_divisor_fan_v1 import (
    bounded_multiplier_inverse,
    divisor_fan_row,
    multiplier_cap,
    theorem_record,
)


class BoundedMultiplierDivisorFanTests(unittest.TestCase):
    def test_cap_and_mass_compiler(self) -> None:
        row = bounded_multiplier_inverse(
            contribution_bound=Fraction(2),
            target_mass=Fraction(1),
            rows=[
                (Fraction(1, 2), 1, Fraction(1)),
                (Fraction(1, 2), 2, Fraction(1, 2)),
            ],
        )
        self.assertEqual(multiplier_cap(contribution_bound=Fraction(2), target_mass=Fraction(1)), 4)
        self.assertLessEqual(row["large_multiplier_mass_upper_bound"], Fraction(1, 2))
        self.assertGreaterEqual(row["bounded_multiplier_mass"], Fraction(1, 2))
        self.assertLessEqual(row["chosen_multiplier"], 4)
        self.assertGreaterEqual(row["chosen_multiplier_mass"], row["chosen_multiplier_lower_bound"])

    def test_exact_divisor_fan_identity(self) -> None:
        row = divisor_fan_row(witness_denominator=60, multiplier=4, divisor=20)
        self.assertEqual(row["mode_denominator"], 80)
        self.assertEqual(row["gcd"], 20)

    def test_rejects_unlicensed_mass(self) -> None:
        with self.assertRaises(ValueError):
            bounded_multiplier_inverse(
                contribution_bound=Fraction(1),
                target_mass=Fraction(1),
                rows=[(Fraction(1), 2, Fraction(1))],
            )

    def test_record_keeps_inverse_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("ceil(2C/kappa)", row["bounded_multiplier"])
        self.assertIn("gcd", row["divisor_fan"])
        self.assertIn("does not", row["boundary"])


if __name__ == "__main__":
    unittest.main()
