from fractions import Fraction as Q
import unittest

from conventions.intercept_cleared_ray_box_v1 import (
    frozen_ray_box_cap,
    primitive_ray_rectangle,
    ray_box_key,
    select_populated_ray_box,
    verify_all,
)


PACKET_STATE = {"intercept_packet": "rho=-1/2", "product_shell": "stable", "residuals_retained": True}


def sample_rectangle() -> dict[str, object]:
    return primitive_ray_rectangle(
        [(21, 10), (23, 11), (25, 12)], [(22, 5), (26, 6), (30, 7)],
        left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
        x=100000, height=20, strip_constant=1, packet_state=PACKET_STATE,
        left_start=0, right_start=0, left_multiplier=1, right_multiplier=1,
        scale_delta=10, stable_cutoff=Q(8, 100), lower_coefficient=Q(2), upper_coefficient=Q(3),
    )


class Cycle183InterceptClearedRayBoxTest(unittest.TestCase):
    def test_replay(self) -> None:
        self.assertIn("D=k*q*v*F", verify_all()["primitive_determinant"])

    def test_nonzero_beta_ray_factorization(self) -> None:
        rectangle = sample_rectangle()
        self.assertEqual(rectangle["determinants"]["D"], 2)
        self.assertEqual(rectangle["determinants"]["F"], 1)
        self.assertEqual(rectangle["left_ray"]["clearing"]["u"], 1)
        self.assertEqual(rectangle["right_ray"]["clearing"]["u"], 2)
        self.assertEqual(rectangle["right_ray"]["ray_rows"][0]["t"], 11)

    def test_frozen_seven_field_box(self) -> None:
        rectangle = sample_rectangle()
        self.assertEqual(ray_box_key(rectangle), (2, 2, 2, 4, 1, 1, 1))
        cap = frozen_ray_box_cap(light_threshold=2, height=20, scale_delta=10)
        self.assertEqual(cap, 8100)
        selected = select_populated_ray_box([rectangle, rectangle], box_cap=cap)
        self.assertEqual(selected["stable_rectangle_count"], 2)
        self.assertEqual(selected["frozen_box_cap"], cap)

    def test_stable_cutoff_is_retained(self) -> None:
        with self.assertRaisesRegex(ValueError, "below stable ray product cutoff"):
            primitive_ray_rectangle(
                [(21, 10), (23, 11), (25, 12)], [(22, 5), (26, 6), (30, 7)],
                left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
                x=100000, height=20, strip_constant=1, packet_state=PACKET_STATE,
                left_start=0, right_start=0, left_multiplier=1, right_multiplier=1,
                scale_delta=10, stable_cutoff=9, lower_coefficient=Q(2), upper_coefficient=Q(3),
            )


if __name__ == "__main__":
    unittest.main()
