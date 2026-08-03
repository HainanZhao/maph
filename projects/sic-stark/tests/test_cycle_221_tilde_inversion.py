"""Regression checks for Cycle 221's forced tilde inversion correction."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_221_tilde_inversion import run  # noqa: E402


class TildeInversionTests(unittest.TestCase):
    def test_forced_factor_and_first_shift_sign(self) -> None:
        result = run()
        self.assertEqual(result["survivor_coordinate_audit"]["survivor_count"], 2)
        self.assertEqual(
            result["forced_pochhammer_audit"]["inversion_identity"],
            "C(z;qtilde)*C(z^(-1);qtilde)=1",
        )
        shift = result["first_shift_normalization_audit"]
        self.assertEqual(shift["positive_phase_exponent"], 1311)
        self.assertEqual(shift["raw_phase_exponent"], 1450)
        self.assertFalse(shift["all_match"])
        self.assertTrue(
            all(not row["matches"] for row in shift["rows"])
        )
        self.assertTrue(result["downstream_identity_audit"]["unnormalized_product_sector_match"])


if __name__ == "__main__":
    unittest.main()
