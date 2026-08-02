import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from nonstationary_mellin_branch_v1 import (  # noqa: E402
    D_EXP,
    XI_MAX,
    XI_MIN,
    integration_by_parts_exponent,
    required_order,
    support_exponents,
    verify_all,
)

Q = Fraction


class NonstationaryMellinBranchTests(unittest.TestCase):
    def test_frequency_floor(self) -> None:
        self.assertEqual(support_exponents(XI_MIN)["minimum_t"], D_EXP)

    def test_strict_ceiling(self) -> None:
        self.assertEqual(
            support_exponents(XI_MAX)["strict_delta_h_ceiling"], Q(13, 75)
        )

    def test_integration_decay(self) -> None:
        self.assertEqual(integration_by_parts_exponent(Q(7, 10), 3), Q(-11, 10))

    def test_arbitrary_support_absorption(self) -> None:
        for xi in (XI_MIN, XI_MAX):
            order = required_order(xi, Q(20))
            total = support_exponents(xi)["ordered_pair_cells"] + integration_by_parts_exponent(xi, order)
            self.assertLessEqual(total, Q(-20))

    def test_verification(self) -> None:
        row = verify_all()
        self.assertIn("O_B(X^-B)", row["full_branch"])
        self.assertIn("remain open", row["open_transition"])


if __name__ == "__main__":
    unittest.main()

