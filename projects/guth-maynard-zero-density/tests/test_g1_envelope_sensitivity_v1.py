from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proof"
ARTIFACTS = ROOT / "artifacts"


class G1EnvelopeSensitivityV1Tests(unittest.TestCase):
    def run_checked(self, script: str) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROOF / script), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_all_exact_routes_replay(self) -> None:
        self.run_checked("derive_g1_envelope_sensitivity_route_a_v1.py")
        self.run_checked("derive_g1_envelope_sensitivity_route_b_v1.py")
        self.run_checked("reconcile_g1_envelope_sensitivity_v1.py")

    def test_optimized_mode_fails_closed(self) -> None:
        for script in (
            "derive_g1_envelope_sensitivity_route_a_v1.py",
            "derive_g1_envelope_sensitivity_route_b_v1.py",
            "reconcile_g1_envelope_sensitivity_v1.py",
        ):
            completed = subprocess.run(
                [sys.executable, "-O", str(PROOF / script), "--check"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)

    def test_reconciled_critical_and_no_effect_records(self) -> None:
        value = json.loads((ARTIFACTS / "g1-envelope-sensitivity-reconciliation-v1.json").read_text())
        self.assertEqual(value["epistemic_status"], "PROVED")
        mapped = value["reconciled_map"]
        self.assertEqual(mapped["zero_B_residual_rows"], 11)
        self.assertEqual(mapped["zero_residual_term"], "LV3 only")
        self.assertEqual(
            mapped["critical_cell"]["residuals"],
            {"LV1": "3/13", "LV2": "1/13", "LV3": "0/1"},
        )
        self.assertIn("third Theorem 1.1 term", mapped["required_improvement_target"])
        self.assertEqual(value["contained_no_effect"]["epistemic_status"], "PROVED")
        self.assertEqual(value["formal_conditional_margin"]["premise_tag"], "CONJECTURED")
        self.assertEqual(
            value["formal_conditional_margin"]["left_extension_crossing"],
            "300h^2+(90-50mu)h-65mu=0",
        )

    def test_observed_replay_performance_record_is_scoped(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PROOF / "run_g1_envelope_sensitivity_v1.py"), "--check-performance"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        value = json.loads((ARTIFACTS / "g1-envelope-sensitivity-replay-v1-performance.json").read_text())
        self.assertEqual(value["epistemic_status"], "OBSERVED")
        self.assertEqual(value["reconciliation"]["path"], "artifacts/g1-envelope-sensitivity-reconciliation-v1.json")
        self.assertEqual(len(value["replays"]), 3)


if __name__ == "__main__":
    unittest.main()
