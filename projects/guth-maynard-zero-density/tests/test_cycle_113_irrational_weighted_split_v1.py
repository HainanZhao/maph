import unittest
from fractions import Fraction

from conventions.irrational_weighted_split_v1 import floating_split_sum, split_record, theorem_record


class IrrationalWeightedSplitTests(unittest.TestCase):
    def test_exact_general_product(self) -> None:
        row = split_record(d=5, u=2, N=3, R=2)
        self.assertEqual((row["x"], row["y"]), (2, 3))
        self.assertEqual(row["B0"], 1)
        self.assertEqual(row["C0"], 1)
        self.assertEqual(row["K_power"], Fraction(5**5 * 2**3 * 3**2, 6**5))

    def test_compact_examples(self) -> None:
        self.assertLess(floating_split_sum(d=7, N=4, R=3), 1.0)
        self.assertLess(floating_split_sum(d=80, N=79, R=80), 2.0)

    def test_theorem_scope(self) -> None:
        row = theorem_record()
        self.assertIn("(d*N*R)^o(1)", row["split_sum"])
        self.assertIn("lambda_BC^(3/2)", row["scale_sum"])
        self.assertIn("Cycle 112", row["correction"])
        self.assertIn("weak localization", row["boundary"])


if __name__ == "__main__":
    unittest.main()
