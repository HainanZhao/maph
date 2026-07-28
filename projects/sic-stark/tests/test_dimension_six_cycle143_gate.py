from __future__ import annotations

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_cycle143_gate.py"


@unittest.skipUnless(
    shutil.which("python3")
    and os.environ.get("SIC_STARK_RUN_ARB") == "1",
    "set SIC_STARK_RUN_ARB=1 in the pinned python-flint environment",
)
class DimensionSixCycle143GateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--digits",
                "30",
                "--tolerance",
                "2e-7",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.output = completed.stdout

    def test_upstream_packet_and_endpoint_are_enclosed(self) -> None:
        self.assertIn("UPSTREAM_X_ALG_ENCLOSED=1", self.output)
        self.assertIn(
            "ALL_225_ANALYTIC_MINOR_BALLS_CONTAIN_ZERO=1",
            self.output,
        )
        self.assertIn(
            "AFK_ENDPOINT_MINUS_4_SQRT7_VERIFIED=1",
            self.output,
        )

    def test_equal_base_link_is_excluded_off_boundary(self) -> None:
        self.assertIn("GEODESIC_EQUAL_BASE_EXCLUSIONS=3", self.output)
        self.assertIn(
            "EQUAL_BASE_OPEN_GEODESIC_NEIGHBORHOOD_EXISTS=0",
            self.output,
        )

    def test_hard_gate_halts_downstream_cycles(self) -> None:
        self.assertIn("COMPLETE_CHAIN_ENCLOSED=0", self.output)
        self.assertIn("DOWNSTREAM_CYCLES_AUTHORIZED=0", self.output)


if __name__ == "__main__":
    unittest.main()
