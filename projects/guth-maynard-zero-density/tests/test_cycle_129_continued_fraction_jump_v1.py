import unittest
from fractions import Fraction

from conventions.continued_fraction_jump_v1 import jump_ledger, theorem_record


class ContinuedFractionJumpTests(unittest.TestCase):
    def test_minimum_margin(self) -> None:
        row = jump_ledger(Fraction(16, 25), Fraction(0))
        self.assertEqual(row["legendre_margin"], Fraction(23, 75))
        self.assertEqual(row["next_denominator_floor"], Fraction(16, 25))
        self.assertEqual(row["occupied_mode_target"], Fraction(1, 3))

    def test_low_branch_threshold(self) -> None:
        xi = Fraction(7, 10)
        mu = (1 - xi) / 4
        row = jump_ledger(xi, mu)
        self.assertEqual(row["next_partial_quotient_floor"], xi / 2 + Fraction(1, 6))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("Legendre's criterion", row["legendre"])
        self.assertIn("q_next", row["convergent_error"])
        self.assertIn(">>KM", row["next_denominator"])
        self.assertIn(">>KM^2/Q", row["partial_quotient"])
        self.assertIn("O((Q/M)X^epsilon)", row["averaged_target"])


if __name__ == "__main__":
    unittest.main()
