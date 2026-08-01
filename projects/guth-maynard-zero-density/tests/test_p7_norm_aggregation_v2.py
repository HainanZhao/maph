from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "proof/run_p7_norm_aggregation_route_a_v1.py",
    ROOT / "proof/run_p7_norm_aggregation_route_b_v1.py",
    ROOT / "proof/correct_p7_norm_aggregation_route_b_v2.py",
    ROOT / "proof/reconcile_p7_norm_aggregation_v2_correction.py",
]
ARTIFACT = ROOT / "artifacts/p7-norm-aggregation-v2-correction.json"


class P7NormAggregationV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replays_and_hashed_inputs(self) -> None:
        for script in SCRIPTS:
            result = subprocess.run([sys.executable, str(script), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
        for row in self.data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_witness_and_exact_conductors(self) -> None:
        reconciled = self.data["reconciliation"]
        self.assertEqual(reconciled["ray_quotients"], {"mod_3": 2, "pi_power_e_1_through_4": [1, 1, 1, 2]})
        self.assertEqual(reconciled["exact_conductors"], ["(3)", "(1+i)^4"])
        self.assertEqual(reconciled["witness"], {"A_chi_3_17": -2, "A_chi_pi4_17": 2})

    def test_norm_and_normalization_are_scoped(self) -> None:
        reconciled = self.data["reconciliation"]
        self.assertEqual(reconciled["norm_identity"], "a_Q(i)(n)=sum_{d|n} chi_-4(d)")
        self.assertEqual(reconciled["normalization"]["outcome"], "EXPONENT_HARMLESS_IN_THE_POLYNOMIAL_LENGTH_HEIGHT_REGIME")
        self.assertIn("N<=T^C", reconciled["normalization"]["covered_regime"])
        self.assertTrue(reconciled["normalization"]["uncovered_regime"].startswith("NOT_ESTABLISHED"))

    def test_type_mismatch_is_not_a_no_go(self) -> None:
        self.assertEqual(self.data["gate_outcome"], "PASS_SCOPED_TYPE_MISMATCH_AND_NORMALIZATION")
        self.assertIn("cannot be invoked verbatim", self.data["reconciliation"]["direct_import_boundary"])
        self.assertIn("does not exclude", self.data["reconciliation"]["non_no_go"])
        self.assertIn("no hostile audit", self.data["review_policy"])


if __name__ == "__main__":
    unittest.main()
