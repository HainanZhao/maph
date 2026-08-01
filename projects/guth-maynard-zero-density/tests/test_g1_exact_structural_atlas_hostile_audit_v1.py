"""Regression coverage for the bounded hostile G1 exact-atlas audit."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g1_exact_structural_atlas_hostile_v1.py"
ARTIFACT = PROJECT / "artifacts/g1-exact-structural-atlas-hostile-audit-v1.json"
PERFORMANCE = PROJECT / "artifacts/g1-exact-structural-atlas-hostile-audit-v1-performance.json"


class G1ExactStructuralAtlasHostileAuditV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text())

    def test_exact_rows_and_known_containment_are_both_preserved(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "OBSERVED")
        exact = self.data["exact_rational_recomputation"]
        self.assertEqual(exact["status"], "PASS")
        self.assertEqual(exact["epistemic_status"], "PROVED")
        self.assertEqual((exact["local_rows"], exact["transfer_rows"], exact["energy_diagonal_rows"]), (7744, 560, 704))
        execution = self.data["execution_mode_checks"]
        self.assertEqual(execution["optimized_exact_atlas"]["status"], "PASS_FAIL_CLOSED")
        self.assertEqual(execution["optimized_preregistration"]["status"], "CONTAINED_OPTIMIZATION_BYPASS_OBSERVED")
        self.assertEqual(execution["optimized_preregistration"]["exit_status"], 0)
        self.assertEqual(self.data["convention_provenance"]["status"], "CONTAINED_DUPLICATED_CONVENTION_OBSERVED")
        self.assertEqual(self.data["decision"]["status"], "REMEDIATION_REQUIRED")

    def test_historical_replay_halts_on_the_versioned_convention_correction(self) -> None:
        completed = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("frozen hash mismatch", completed.stderr)
        performance = json.loads(PERFORMANCE.read_text())
        self.assertEqual(performance["epistemic_status"], "OBSERVED")
        self.assertEqual(performance["audit_artifact"]["sha256"], __import__("hashlib").sha256(ARTIFACT.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
