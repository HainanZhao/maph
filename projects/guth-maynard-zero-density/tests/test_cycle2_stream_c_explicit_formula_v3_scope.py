"""Regression tests for the primary-source scope correction."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE_CHECK = PROJECT / "proof" / "check_cycle_2_stream_c_explicit_formula_sources_v3.py"
AUDIT = PROJECT / "proof" / "audit_cycle2_stream_c_explicit_formula_v2_v2.py"
AUDIT_ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v2.json"


class ExplicitFormulaV3ScopeTests(unittest.TestCase):
    def test_primary_source_scope_and_renderer_pin(self) -> None:
        source = subprocess.run([sys.executable, str(SOURCE_CHECK)], check=True, capture_output=True, text=True)
        self.assertIn("mutool 1.23.10", source.stdout)
        subprocess.run([sys.executable, str(AUDIT), "--check", str(AUDIT_ARTIFACT)], check=True, capture_output=True, text=True)
        data = json.loads(AUDIT_ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["mathematical_source_authority"]["status"], "PROVED")
        self.assertEqual(data["distribution_caveat"]["status"], "OBSERVED")
        self.assertIn("not establish G0 PASS", data["preregistration_effect"]["result"])


if __name__ == "__main__":
    unittest.main()
