import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from signed_regime_split_v1 import (  # noqa: E402
    ATOM_EXP,
    FOURIER_CEILING,
    MOMENT_CUTOFF,
    RAW_L1_TARGET,
    SQRT_ATOM_EXP,
    UNSIGNED_CUTOFF,
    signed_contract,
    verify_all,
)

Q = Fraction


class SignedRegimeSplitTests(unittest.TestCase):
    def test_atom_and_square_root(self) -> None:
        self.assertEqual(ATOM_EXP, Q(14, 15))
        self.assertEqual(SQRT_ATOM_EXP, Q(7, 15))
        self.assertEqual(Q(3, 5) - SQRT_ATOM_EXP, Q(2, 15))

    def test_moment_boundary(self) -> None:
        self.assertEqual(MOMENT_CUTOFF, Q(58, 75))
        self.assertEqual(
            signed_contract(MOMENT_CUTOFF)["cauchy_l1"], RAW_L1_TARGET
        )

    def test_required_saving(self) -> None:
        self.assertEqual(
            signed_contract(UNSIGNED_CUTOFF)["required_saving_from_unsigned"], 0
        )
        self.assertEqual(
            signed_contract(MOMENT_CUTOFF)["required_saving_from_unsigned"],
            Q(2, 15),
        )

    def test_ceiling_allowance(self) -> None:
        self.assertEqual(
            signed_contract(FOURIER_CEILING)["average_allowance"], Q(2, 15)
        )

    def test_verification(self) -> None:
        row = verify_all()
        self.assertIn("V(0)=0", row["projector_zero_mode"])
        self.assertEqual(row["moment_regime"], "16/25<=xi<58/75")
        self.assertIn("sparse large values", row["gate"])


if __name__ == "__main__":
    unittest.main()

