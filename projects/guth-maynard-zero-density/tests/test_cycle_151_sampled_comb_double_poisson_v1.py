import unittest
from fractions import Fraction

from conventions.sampled_comb_double_poisson_v1 import (
    exponent_ledger,
    relative_mode_capacity,
    resonance_modulus,
    theorem_record,
)


class SampledCombDoublePoissonTests(unittest.TestCase):
    def test_lcm_resonance(self) -> None:
        row = resonance_modulus(12, 18)
        self.assertEqual(row, {"gcd": 6, "lcm": 36, "coefficient_congruence": 3})

    def test_relative_capacity(self) -> None:
        self.assertEqual(relative_mode_capacity(12, 18), Fraction(1, 3))

    def test_exponent_ledger(self) -> None:
        row = exponent_ledger(
            xi=Fraction(7, 10),
            rho=Fraction(1, 5),
            rho_b=Fraction(1, 4),
            gamma=Fraction(1, 10),
        )
        self.assertEqual(row["lcm"], Fraction(7, 20))
        self.assertEqual(row["resonance_exists_margin"], Fraction(7, 20))
        self.assertEqual(row["relative_to_witness"], Fraction(-3, 20))

    def test_record_keeps_all_three_locks(self) -> None:
        row = theorem_record()
        self.assertIn("lcm", row["structural_implication"])
        self.assertIn("gcd", row["gcd_capacity"])
        self.assertIn("negative", row["negative_lobe"])
        self.assertIn("not bounded", row["boundary"])


if __name__ == "__main__":
    unittest.main()
