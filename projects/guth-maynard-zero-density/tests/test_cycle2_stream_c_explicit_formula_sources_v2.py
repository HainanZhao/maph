"""Regression test for the OA formula-source closure."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "check_cycle_2_stream_c_explicit_formula_sources_v2.py"


class ExplicitFormulaSourcesV2Tests(unittest.TestCase):
    def test_frozen_oa_source_replays(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True)
        self.assertIn("PASS", result.stdout)
        self.assertIn("LICENSE PROVENANCE", result.stdout)


if __name__ == "__main__":
    unittest.main()
