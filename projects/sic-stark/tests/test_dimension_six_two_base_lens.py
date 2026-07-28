from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_two_base_lens.py"


@unittest.skipUnless(
    os.environ.get("SIC_STARK_RUN_ARB") == "1",
    "set SIC_STARK_RUN_ARB=1 in the pinned python-flint environment",
)
class DimensionSixTwoBaseLensTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--digits",
                "30",
                "--tolerance",
                "1e-14",
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.output = completed.stdout

    def test_trace_integrality_fuses_both_base_pairs(self) -> None:
        self.assertIn("TRACE_INTEGRALITY_FUSION_VERIFIED=1", self.output)

    def test_two_base_factorization_and_aliases_are_enclosed(self) -> None:
        self.assertIn(
            "DIRECT_VS_FACTORIZED_CONTINUATION_ENCLOSURES=3/3",
            self.output,
        )
        self.assertIn("TWO_BASE_ALIAS_CLASS_ENCLOSURES=9/9", self.output)
        self.assertIn("TWO_BASE_INTERIOR_PACKET_ENCLOSED=1", self.output)

    def test_equal_base_series_is_boundary_only(self) -> None:
        self.assertIn(
            "RETIRED_EQUAL_BASE_2PSI2_RECOVERED_ONLY_AT_BOUNDARY=1",
            self.output,
        )


if __name__ == "__main__":
    unittest.main()
