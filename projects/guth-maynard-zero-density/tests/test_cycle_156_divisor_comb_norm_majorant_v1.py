import unittest
from fractions import Fraction

from conventions.divisor_comb_norm_majorant_v1 import divisor_comb_norm_majorant, theorem_record


class DivisorCombNormMajorantTests(unittest.TestCase):
    def test_exact_count_and_h_at_most_k_constant(self) -> None:
        row = divisor_comb_norm_majorant(
            frequency_length=10, modulus=4, anchor_ratio=Fraction(1)
        )
        self.assertEqual(row["multiple_count"], 3)
        self.assertEqual(row["norm_squared_majorant_constant"], 2)

    def test_fixed_anchor_ratio(self) -> None:
        row = divisor_comb_norm_majorant(
            frequency_length=10, modulus=15, anchor_ratio=Fraction(3, 2)
        )
        self.assertEqual(row["multiple_count"], 1)
        self.assertEqual(row["norm_squared_majorant_constant"], Fraction(5, 2))

    def test_rejects_unfrozen_ratio_failure(self) -> None:
        with self.assertRaises(ValueError):
            divisor_comb_norm_majorant(
                frequency_length=10, modulus=16, anchor_ratio=Fraction(3, 2)
            )

    def test_boundary(self) -> None:
        self.assertIn("does not", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
