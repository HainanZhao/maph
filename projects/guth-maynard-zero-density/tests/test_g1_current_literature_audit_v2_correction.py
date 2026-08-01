"""Regression tests for the preserved-v1 G1 literature-audit correction."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_g1_current_literature_v2_correction.py"
V1_REPORT = PROJECT / "docs" / "g1-current-literature-audit-v1.md"
CORRECTION_REPORT = PROJECT / "docs" / "g1-current-literature-audit-v2-correction.md"
ARTIFACT = PROJECT / "artifacts" / "g1-current-literature-audit-v2-correction.json"

spec = importlib.util.spec_from_file_location("g1_current_literature_audit_v2_correction", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load G1 literature-audit v2 correction module")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class G1CurrentLiteratureAuditV2CorrectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_builder_reconstructs_artifact_exactly(self) -> None:
        self.assertEqual(module.encoded(module.build()), ARTIFACT.read_bytes())

    def test_sealed_v1_is_preserved_with_the_recorded_defect(self) -> None:
        report = V1_REPORT.read_bytes()
        self.assertEqual(hashlib.sha256(report).hexdigest(), module.V1_REPORT_SHA256)
        self.assertEqual(report.count(bytes((13,))), 1)
        self.assertEqual(report.find(bytes((13,))), module.DEFECT_OFFSET)
        self.assertEqual(report.count(module.BAD_FRAGMENT), 1)

    def test_successor_report_is_clean_and_names_the_corrected_identifier(self) -> None:
        report = CORRECTION_REPORT.read_bytes()
        self.assertNotIn(bytes((13,)), report)
        self.assertIn(module.CORRECTED_FRAGMENT, report)
        self.assertIn(b"mathematical, provenance, overlap, route-selection, or novelty claim changes.", report)

    def test_claim_scope_and_preservation_are_explicit(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "OBSERVED")
        self.assertIn("changes no source", self.data["claim_boundary"])
        correction = self.data["correction"]
        self.assertIn("None", correction["affected_claims"])
        self.assertIn("not a theorem", correction["non_promotion"])
        preserved = self.data["integrity"]["preserved_v1"]
        self.assertEqual(preserved["v1_report"]["sha256"], module.V1_REPORT_SHA256)
        self.assertEqual(preserved["v1_artifact"]["sha256"], module.V1_ARTIFACT_SHA256)

    def test_optimized_python_is_rejected(self) -> None:
        result = subprocess.run(
            [sys.executable, "-O", str(SCRIPT), "--check"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("optimized Python is not permitted", result.stderr)


if __name__ == "__main__":
    unittest.main()
