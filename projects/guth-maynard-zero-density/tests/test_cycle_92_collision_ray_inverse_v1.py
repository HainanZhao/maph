import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from collision_ray_inverse_v1 import (  # noqa: E402
    DENOM_EXP,
    XI_MIN,
    separation_margins,
    verify_all,
    web_exponents,
)

Q = Fraction


class CollisionRayInverseTests(unittest.TestCase):
    def test_minimum_margins(self) -> None:
        row = separation_margins(XI_MIN)
        self.assertEqual(row["same_a_farey"], Q(23, 75))
        self.assertEqual(row["cross_a_injectivity"], Q(28, 75))

    def test_web_tradeoff(self) -> None:
        row = web_exponents(Q(1, 10))
        self.assertEqual(row["primitive_denominator_ceiling"], Q(7, 30))
        self.assertEqual(row["distinct_a_floor"], Q(7, 30))

    def test_epsilon_is_retained(self) -> None:
        row = web_exponents(Q(1, 10), Q(1, 100))
        self.assertEqual(row["distinct_a_floor"], Q(7, 30) + Q(1, 100))

    def test_denominator_endpoint(self) -> None:
        self.assertEqual(
            web_exponents(DENOM_EXP)["primitive_denominator_ceiling"], 0
        )

    def test_verification(self) -> None:
        row = verify_all()
        self.assertIn("not yet a transport seed", row["analytic_or_web"])
        self.assertIn("injective labels", row["dyadic_extraction"])


if __name__ == "__main__":
    unittest.main()

