from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_five_two_base_calibration.py"


@unittest.skipUnless(
    os.environ.get("SIC_STARK_RUN_ARB") == "1",
    "set SIC_STARK_RUN_ARB=1 in the pinned python-flint environment",
)
class DimensionFiveTwoBaseCalibrationTests(unittest.TestCase):
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

    def test_two_base_pipeline_is_enclosed(self) -> None:
        self.assertIn("D5_FACTORIZATION_ENCLOSURES=3/3", self.output)
        self.assertIn(
            "D5_TWO_BASE_ALIAS_CLASS_ENCLOSURES=6/6",
            self.output,
        )
        self.assertIn("D5_TWO_BASE_CALIBRATION_ENCLOSED=1", self.output)

    def test_proved_packet_is_recovered(self) -> None:
        self.assertIn("D5_PROVED_PACKET_ENCLOSED=1", self.output)

    def test_calibration_selects_closed_locus_branch(self) -> None:
        self.assertIn("D5_CLOSED_LOCUS_ARGUMENT=+q", self.output)
        self.assertIn("D5_ANALYTIC_LENS_LEVEL=15", self.output)
        self.assertIn("D5_FUSION_SIGN_BIT=0", self.output)
        self.assertIn("D6_NEIGHBOR_ARGUMENT=-q", self.output)
        self.assertIn("D5_CALIBRATION_BRANCH=A", self.output)


if __name__ == "__main__":
    unittest.main()
