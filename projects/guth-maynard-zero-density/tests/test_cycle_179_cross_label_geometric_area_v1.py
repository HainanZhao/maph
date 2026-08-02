from fractions import Fraction as Q
import unittest

from conventions.cross_label_geometric_area_v1 import (
    bezout_base_recovery,
    geometric_tower,
    light_triangle_population,
    rational_base_exact_tower,
    same_label_area_resonance,
    verify_all,
)


class Cycle179CrossLabelGeometricAreaTest(unittest.TestCase):
    def test_replay(self) -> None:
        self.assertIn("beta cancels exactly", verify_all()["area_identity"])

    def test_varying_base_remains_uniform(self) -> None:
        output = geometric_tower(height=50, base_denominator=17, chart_multiples=40)
        self.assertLessEqual(output["total_rows"], 150)
        self.assertLessEqual(output["ordered_cross_label_mass"], 9 * 50 * 50)

    def test_area_retains_nonzero_beta(self) -> None:
        output = same_label_area_resonance(
            (21, 10), (23, 11), (22, 5),
            alpha_same=Q(1, 2), alpha_other=Q(1, 4), beta=Q(1, 2),
            x=1000, height=20, strip_constant=1,
        )
        self.assertEqual(output["area_integer"], 11)
        self.assertEqual(output["area_error"], 0)

    def test_exact_rational_gcd_compression_branches(self) -> None:
        recovery = bezout_base_recovery([2, 3], [Q(9, 4), Q(27, 8)])
        self.assertEqual(recovery["recovered_base"], Q(3, 2))
        integral = rational_base_exact_tower(20, numerator_base=2, denominator_base=1, chart_multiples=9)
        self.assertLessEqual(integral["ordered_cross_label_mass"], integral["uniform_cross_bound"])

    def test_triangle_light_boundary(self) -> None:
        output = light_triangle_population([3, 3, 3], threshold=2, label_capacity=3)
        self.assertEqual(output["oriented_cross_label_triangles"], 108)
        with self.assertRaisesRegex(ValueError, "not in light branch"):
            light_triangle_population([5, 1], threshold=2, label_capacity=2)


if __name__ == "__main__":
    unittest.main()
