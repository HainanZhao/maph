from fractions import Fraction as Q
import unittest

from conventions.cross_label_pair_determinant_v1 import (
    cross_pair_determinant,
    light_rectangle_population,
    low_product_rectangle_bound,
    stable_determinant_comparison,
    verify_all,
)


class Cycle180CrossLabelPairDeterminantTest(unittest.TestCase):
    def test_replay(self) -> None:
        self.assertIn("nonzero integer D", verify_all()["determinant"])

    def test_nonzero_beta_rectangle(self) -> None:
        row = cross_pair_determinant(
            ((21, 10), (23, 11)), ((22, 5), (26, 6)),
            left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2),
            x=1000, height=20, strip_constant=1, label_spacing=Q(1, 4),
        )
        self.assertEqual(row["determinant_integer"], 2)
        self.assertEqual(row["determinant_error"], 0)

    def test_light_rectangle_population(self) -> None:
        rows = light_rectangle_population([3, 3, 3], threshold=2, label_capacity=3)
        self.assertEqual(rows["ordered_cross_label_rectangles"], 54)
        with self.assertRaisesRegex(ValueError, "not in light branch"):
            light_rectangle_population([5, 1], threshold=2, label_capacity=2)

    def test_low_and_stable_product_branches(self) -> None:
        low = low_product_rectangle_bound(threshold=2, label_capacity=3, product_limit=6)
        self.assertEqual(low["ordered_gap_triples"], 25)
        stable = stable_determinant_comparison(
            label_gap=1, left_gap=10, right_gap=10, determinant=20,
            alpha_gap=Q(1, 5), delta=Q(0), height=20, scale_delta=10, x=1000,
            strip_constant=1, lower_coefficient=Q(2), upper_coefficient=Q(2),
        )
        self.assertEqual(stable["determinant_lower_bound"], 10)


if __name__ == "__main__":
    unittest.main()
