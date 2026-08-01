"""Regression tests for the direct official-SWORD Stream-C source closure."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE_CHECK = PROJECT / "proof" / "check_cycle_2_stream_c_explicit_formula_sources_v4.py"
AUDIT = PROJECT / "proof" / "audit_cycle2_stream_c_explicit_formula_v2_v3.py"
SOURCE_ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-explicit-formula-source-closure-v4.json"
AUDIT_ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v3.json"


class ExplicitFormulaV4OfficialTests(unittest.TestCase):
    def test_official_archive_closure(self) -> None:
        result = subprocess.run([sys.executable, str(SOURCE_CHECK)], check=True, capture_output=True, text=True)
        self.assertIn("PASS:", result.stdout)
        self.assertIn("7292f134-d4a7-4063-bd7e-2084259b8fa9", result.stdout)
        data = json.loads(SOURCE_ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["official_source"]["license"], "CC BY-NC-SA 3.0")
        self.assertEqual(data["official_sword_bitstream"]["bytes"], 5334292)
        self.assertEqual(data["official_pdf_members"][0]["member_bytes"], 92250)
        self.assertEqual(data["official_pdf_members"][1]["member_bytes"], 118273)

    def test_adversarial_correction(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(AUDIT_ARTIFACT)], check=True, capture_output=True, text=True)
        data = json.loads(AUDIT_ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["official_access"]["status"], "PROVED")
        self.assertEqual(data["withdrawn_distribution_caveat"]["status"], "PROVED")
        self.assertIn("does not establish G0 PASS", data["preregistration_effect"]["result"])


if __name__ == "__main__":
    unittest.main()
