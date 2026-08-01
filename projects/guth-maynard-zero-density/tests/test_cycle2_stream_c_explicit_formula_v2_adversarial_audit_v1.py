"""Regression tests for the hostile v2 formula-source audit."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_cycle2_stream_c_explicit_formula_v2_v1.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v1.json"


class ExplicitFormulaV2AdversarialAuditTests(unittest.TestCase):
    def test_audit_replays_and_keeps_provenance_gap_visible(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], check=True, capture_output=True, text=True)
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertIn("multiplicity", data["mathematical_hypotheses"]["multiplicity"])
        self.assertEqual(data["licensing_and_provenance"]["status"], "OBSERVED")
        self.assertEqual(len(data["route_b_v4_adjudication"]["blockers"]), 3)
        self.assertIn("not PASS", data["preregistration_effect"]["result"])


if __name__ == "__main__":
    unittest.main()
