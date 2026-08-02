import unittest
from fractions import Fraction

from conventions.divisor_comb_sign_test_v1 import (
    divisor_comb_norm,
    escape_norm_floor,
    one_ray_escape_ledger,
    theorem_record,
)


class DivisorCombSignTestTests(unittest.TestCase):
    def test_test_vector_norm(self) -> None:
        self.assertEqual(
            divisor_comb_norm(q_length=10.0, frequency_length=100.0, modulus=4.0),
            50.0,
        )

    def test_escape_norm_floor(self) -> None:
        self.assertEqual(
            escape_norm_floor(
                negative_witness=80.0,
                strict_error=5.0,
                test_vector_norm=25.0,
            ),
            3.0,
        )

    def test_one_ray_scale(self) -> None:
        row = one_ray_escape_ledger(
            xi=Fraction(7, 10),
            rho=Fraction(1, 5),
        )
        self.assertEqual(row["escape_norm_squared"], Fraction(7, 6))
        self.assertEqual(row["excess"], Fraction(2, 15))

    def test_record_is_scoped(self) -> None:
        row = theorem_record()
        self.assertIn("reinforce", row["no_strict_antialignment"])
        self.assertIn("endpoint error", row["escape_split"])
        self.assertIn("not bounded", row["boundary"])


if __name__ == "__main__":
    unittest.main()
