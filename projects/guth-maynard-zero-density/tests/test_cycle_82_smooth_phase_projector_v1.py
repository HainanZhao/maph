import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from smooth_phase_projector_v1 import (  # noqa: E402
    OCCUPANCY_EXP,
    OLD_CUTOFF,
    Q_EXP,
    RAW_L1_TARGET,
    projector_ledger,
    verify_all,
)

Q = Fraction


class SmoothPhaseProjectorTests(unittest.TestCase):
    def test_per_k_exponent(self) -> None:
        self.assertEqual(Q_EXP + OCCUPANCY_EXP, Q(37, 45))

    def test_new_cutoff(self) -> None:
        self.assertEqual(RAW_L1_TARGET - Q(37, 45), Q(94, 225))

    def test_band_width(self) -> None:
        self.assertEqual(Q(94, 225) - OLD_CUTOFF, Q(1, 18))

    def test_strictness_and_tie(self) -> None:
        self.assertTrue(projector_ledger(OLD_CUTOFF)["strictly_closed"])
        endpoint = projector_ledger(Q(94, 225))
        self.assertFalse(endpoint["strictly_closed"])
        self.assertEqual(endpoint["margin"], 0)

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["per_k_exponent"], "37/45")
        self.assertEqual(row["band_width"], "1/18")
        self.assertIn("fixed-center", row["gate"])


if __name__ == "__main__":
    unittest.main()

