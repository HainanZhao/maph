from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_cycle_4_p1r_crr_u_formalization_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-crr-u-formalization-v1-hostile-audit-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("crr_u_hostile_audit_v1_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load hostile audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRUFormalizationV1HostileAuditV1Tests(unittest.TestCase):
    def test_failed_decision_and_exact_slack_rows(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["decision"], "FAIL")
        self.assertEqual(data["gate_consequence"]["discovery_search"], "REMAINS_PROHIBITED")
        self.assertEqual([row["id"] for row in data["findings"]], [
            "F1_SLACKED_POINTWISE_SOURCE_HYPOTHESIS",
            "F2_OMITTED_SLACK_IN_RATIONAL_AND_AFFINE_TIES",
            "F3_PHASE_LABEL_DERIVATION_INCOMPLETE",
        ])
        rows = data["exact_slack_recomputation"]
        self.assertEqual(rows["large_value_upper_rows"], ["6+2*delta", "8+4*delta", "8+4*delta"])
        self.assertEqual(rows["energy_upper_rows_at_cardinality_upper"], ["20+5*delta", "20+37/8*delta", "20+5*delta"])
        self.assertEqual(rows["rational_mass_lower_moments"], ["8-3*delta", "20-5*delta"])
        self.assertEqual(rows["affine_lower_rows"], ["28-6*delta", "28-5*delta"])

    def test_replay_runtime_and_input_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["auditor"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_module()
        original = module.INPUTS["v1_artifact"]
        module.INPUTS["v1_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "audited input hash mismatch: v1_artifact"):
            module.audit()
        module.INPUTS["v1_artifact"] = original


if __name__ == "__main__":
    unittest.main()
