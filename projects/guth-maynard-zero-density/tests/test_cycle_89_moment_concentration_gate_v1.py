import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from moment_concentration_gate_v1 import (  # noqa: E402
    FOURIER_CEILING,
    MOMENT_SPLIT,
    random_fourth_moment,
    required_excess,
    required_fourth_moment,
    verify_all,
)

Q = Fraction


class MomentConcentrationGateTests(unittest.TestCase):
    def test_forced_exponent(self) -> None:
        self.assertEqual(required_fourth_moment(Q(9, 10)), 3 * Q(9, 10) + Q(8, 25))

    def test_random_scale(self) -> None:
        self.assertEqual(random_fourth_moment(Q(9, 10)), Q(9, 10) + Q(28, 15))

    def test_split_and_ceiling(self) -> None:
        self.assertEqual(required_excess(MOMENT_SPLIT), 0)
        self.assertEqual(required_excess(FOURIER_CEILING), Q(2, 3))

    def test_strict_l1_saving_costs_twice(self) -> None:
        xi = Q(1)
        delta = Q(1, 100)
        self.assertEqual(required_excess(xi, delta) - required_excess(xi), 2 * delta)

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["forced_excess"], "2xi-116/75+2delta")
        self.assertIn("necessary, not sufficient", row["interpretation"])


if __name__ == "__main__":
    unittest.main()

