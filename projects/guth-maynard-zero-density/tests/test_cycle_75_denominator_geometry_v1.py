from fractions import Fraction as Q
import unittest

from conventions.denominator_geometry_v1 import (
    det2,
    exponent_cell,
    hessian_aq,
    hessian_nq,
    normalized_hessian,
    primitive_ray_unique,
    transform_aq_to_nq,
    verify_all,
)


class Cycle75DenominatorGeometryTests(unittest.TestCase):
    def test_coordinate_hessians(self) -> None:
        c, a, q = Q(5, 7), Q(2, 3), Q(7, 4)
        original = hessian_aq(c, a, q)
        shifted = hessian_nq(c, a + q, q)
        self.assertEqual(transform_aq_to_nq(original), shifted)
        self.assertEqual(det2(original), -c**2 / (q**2 * (a + q) ** 2))

    def test_affine_normalized_determinant(self) -> None:
        c, a_scale, q_scale = Q(4, 5), Q(1, 9), Q(3, 2)
        x, y = Q(5, 4), Q(7, 5)
        epsilon = a_scale / q_scale
        matrix = normalized_hessian(c, a_scale, q_scale, x, y)
        self.assertEqual(det2(matrix), -Q(1) / (y**2 * (y + epsilon * x) ** 2))

    def test_exact_rays_are_unique_when_primitive(self) -> None:
        self.assertTrue(primitive_ray_unique(2, 5, 3, 7))
        self.assertTrue(primitive_ray_unique(2, 5, 2, 5))
        with self.assertRaises(ValueError):
            primitive_ray_unique(2, 4, 1, 2)

    def test_combined_atlas_removes_old_ell_region(self) -> None:
        row = exponent_cell(Q(11, 25), Q(0), Q(0))
        self.assertFalse(row["live_residual"])
        self.assertEqual(row["ell_injectivity_bound"], Q(4, 25))

    def test_unique_worst_point(self) -> None:
        row = exponent_cell(Q(1, 3), Q(8, 75), Q(1, 3))
        self.assertTrue(row["live_residual"])
        self.assertEqual(row["banked_count_bound"], Q(3, 5))
        self.assertEqual(row["additional_saving_required_strictly_more_than"], Q(7, 15))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("7/15", rows["worst_required_saving"])
        self.assertIn("E14", rows["gate"])


if __name__ == "__main__":
    unittest.main()
