from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_four_two_base_calibration.py"


@unittest.skipUnless(
    os.environ.get("SIC_STARK_RUN_ARB") == "1",
    "set SIC_STARK_RUN_ARB=1 in the pinned python-flint environment",
)
class DimensionFourTwoBaseCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--digits",
                "30",
                "--tolerance",
                "1e-12",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.output = completed.stdout

    def test_two_base_control_is_enclosed(self) -> None:
        self.assertIn("D4_FACTORIZATION_ENCLOSURES=3/3", self.output)
        self.assertIn(
            "D4_TWO_BASE_ALIAS_CLASS_ENCLOSURES=3/3",
            self.output,
        )
        self.assertIn("D4_TWO_BASE_CALIBRATION_ENCLOSED=1", self.output)

    def test_even_wrap_uses_level_sixteen(self) -> None:
        self.assertIn("D4_ANALYTIC_LENS_LEVEL=8", self.output)
        self.assertIn("D4_EVEN_WRAP_PHASE_LEVEL=16", self.output)
        self.assertIn("D4_LEVEL_24_REJECTED=1", self.output)
        self.assertIn("D4_FUSED_BILATERAL_ARGUMENT=-q", self.output)


if __name__ == "__main__":
    unittest.main()
