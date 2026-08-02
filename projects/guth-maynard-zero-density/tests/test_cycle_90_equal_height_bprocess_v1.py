import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from equal_height_bprocess_v1 import (  # noqa: E402
    DENOM_EXP,
    XI_MAX,
    XI_MIN,
    collision_ledger,
    formulas,
    moment_ledger,
    support,
    verify_all,
)

Q = Fraction


class EqualHeightBProcessTests(unittest.TestCase):
    def test_dual_length_and_surplus(self) -> None:
        self.assertEqual(support(XI_MIN)["dual_n"], DENOM_EXP)
        self.assertEqual(support(XI_MIN)["sample_surplus"], Q(1, 25))
        self.assertEqual(support(XI_MAX)["sample_surplus"], Q(13, 75))

    def test_diagonal_and_remainder(self) -> None:
        row = moment_ledger(Q(7, 10))
        self.assertEqual(row["diagonal"], Q(7, 10) + Q(14, 15))
        self.assertEqual(row["remainder_margin"], Q(1, 3))

    def test_collision_margin(self) -> None:
        self.assertEqual(
            collision_ledger(XI_MIN)["target_over_volume_margin"], Q(1, 25)
        )
        self.assertEqual(
            collision_ledger(XI_MAX)["target_over_volume_margin"], Q(13, 75)
        )

    def test_stationary_signs(self) -> None:
        row = formulas()
        self.assertEqual(row["poisson_phase"], "-t*log(r)+n*r")
        self.assertEqual(row["stationary_hessian"], "n^2/t")
        self.assertIn("exp(2*beta*a/D)", row["surface_determinant"])

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["minimum_sample_surplus"], "1/25")
        self.assertIn("two-dimensional saddle discrepancy", row["gate"])


if __name__ == "__main__":
    unittest.main()

