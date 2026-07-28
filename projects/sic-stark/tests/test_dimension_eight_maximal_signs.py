"""Regression test for the exact maximal-order d=8 phase certificate."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DimensionEightMaximalSignTest(unittest.TestCase):
    def test_all_cocycle_signs_are_exact(self) -> None:
        process = subprocess.run(
            [
                sys.executable,
                "scripts/dimension_eight_maximal_sign_audit.py",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("CHARACTERISTICS_AUDITED=63", process.stdout)
        self.assertIn("BETA_PHASE_COEFFICIENTS_ZERO=1", process.stdout)
        self.assertIn("INTEGRAL_PI_PHASES=1", process.stdout)
        self.assertIn("SIGN_TABLE_MATCH=1", process.stdout)


if __name__ == "__main__":
    unittest.main()
