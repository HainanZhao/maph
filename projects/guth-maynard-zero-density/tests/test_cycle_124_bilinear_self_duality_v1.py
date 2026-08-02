import unittest
from fractions import Fraction

from conventions.bilinear_self_duality_v1 import exponent_ledger, theorem_record


class BilinearSelfDualityTests(unittest.TestCase):
    def test_target_identity(self) -> None:
        row = exponent_ledger(Fraction(16, 25))
        self.assertEqual(row["diagonal_second_moment"], Fraction(118, 75))
        self.assertEqual(row["alias_target"], row["diagonal_second_moment"])
        self.assertEqual(row["required_trivial_saving"], Fraction(14, 15))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("e(-ell n'g^a)", row["mode_change"])
        self.assertIn("rank O(X^epsilon)", row["tensor_separation"])
        self.assertIn("exactly the Cycle-87 target", row["cauchy_target"])
        self.assertIn("norm-neutral", row["self_duality"])
        self.assertIn("does not exclude", row["boundary"])

    def test_rejects_outside_band(self) -> None:
        with self.assertRaises(ValueError):
            exponent_ledger(Fraction(3, 5))


if __name__ == "__main__":
    unittest.main()
