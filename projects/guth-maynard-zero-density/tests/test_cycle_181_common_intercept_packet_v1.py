from fractions import Fraction as Q
import unittest

from conventions.common_intercept_packet_v1 import (
    common_intercept_rectangle,
    eligible_intercept_count,
    stable_packet_pigeonhole,
    verify_all,
)


class Cycle181CommonInterceptPacketTest(unittest.TestCase):
    def test_replay(self) -> None:
        self.assertIn("I=e*q-d*q'", verify_all()["intercept_exactification"])

    def test_nonzero_beta_common_intercept(self) -> None:
        row = common_intercept_rectangle(
            ((21, 10), (23, 11)), ((22, 5), (26, 6)),
            left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2),
            x=100000, height=20, strip_constant=1, stable_product_cutoff=8,
        )
        self.assertEqual(row["intercept_determinant"], 0)
        self.assertEqual(row["common_intercept"]["value"], Q(-1, 2))
        self.assertEqual(row["slope_determinant"], 2)
        self.assertEqual(row["phase_state"]["beta"], Q(1, 2))
        self.assertEqual(row["left_pair"]["residuals"]["first"], 0)

    def test_cutoff_is_not_weakened_for_fixture(self) -> None:
        with self.assertRaisesRegex(ValueError, "intercept exactification cutoff"):
            common_intercept_rectangle(
                ((21, 10), (23, 11)), ((22, 5), (26, 6)),
                left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2),
                x=1000, height=20, strip_constant=1, stable_product_cutoff=8,
            )

    def test_denominator_packets_and_population(self) -> None:
        self.assertEqual(
            eligible_intercept_count([Q(-1, 2), Q(-3, 6)], beta=Q(1, 2), x=100000, height=20, strip_constant=1),
            1,
        )
        with self.assertRaisesRegex(ValueError, "outside beta tube"):
            eligible_intercept_count([Q(-1, 2), Q(-2, 3)], beta=Q(1, 2), x=100000, height=20, strip_constant=1)
        self.assertEqual(stable_packet_pigeonhole(stable_rectangles=641, height=20), 33)


if __name__ == "__main__":
    unittest.main()
