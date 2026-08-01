from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ROUTE_A = ROOT / "proof/run_p7_norm_aggregation_route_a_v1.py"
ROUTE_B = ROOT / "proof/run_p7_norm_aggregation_route_b_v1.py"
ROUTE_B_CORRECTION = ROOT / "proof/correct_p7_norm_aggregation_route_b_v2.py"
RECONCILE = ROOT / "proof/reconcile_p7_norm_aggregation_v1.py"
ARTIFACT = ROOT / "artifacts/p7-norm-aggregation-v1.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class P7NormAggregationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.a = load("p7_route_a_test", ROUTE_A)
        cls.b = load("p7_route_b_test", ROUTE_B)
        cls.r = load("p7_reconcile_test", RECONCILE)
        cls.artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_all_three_replays_are_deterministic(self) -> None:
        for script in (ROUTE_A, ROUTE_B, ROUTE_B_CORRECTION, RECONCILE):
            result = subprocess.run([sys.executable, str(script), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_exact_witness_and_conductor_quotients(self) -> None:
        result = self.artifact["reconciliation"]
        self.assertEqual(result["ray_quotients"]["mod_3"], 2)
        self.assertEqual(result["ray_quotients"]["pi_power_e_1_through_4"], [1, 1, 1, 2])
        self.assertEqual(result["exact_conductors"], ["(3)", "(1+i)^4"])
        self.assertEqual(result["witness"], {"A_chi_3_17": -2, "A_chi_pi4_17": 2})
        self.assertIn("explicit bijection", result["label_reconciliation"])

    def test_norm_identity_and_precise_normalization_scope(self) -> None:
        result = self.artifact["reconciliation"]
        self.assertEqual(result["norm_identity"], "a_Q(i)(n)=sum_{d|n} chi_-4(d)")
        self.assertEqual(result["normalization"]["outcome"], "EXPONENT_HARMLESS_IN_THE_POLYNOMIAL_LENGTH_HEIGHT_REGIME")
        self.assertIn("N<=T^C", result["normalization"]["covered_regime"])
        self.assertTrue(result["normalization"]["uncovered_regime"].startswith("NOT_ESTABLISHED"))

    def test_type_mismatch_is_not_no_go(self) -> None:
        self.assertEqual(self.artifact["gate_outcome"], "PASS_SCOPED_TYPE_MISMATCH_AND_NORMALIZATION")
        self.assertIn("cannot be invoked verbatim", self.artifact["reconciliation"]["direct_import_boundary"])
        self.assertIn("does not exclude", self.artifact["reconciliation"]["non_no_go"])
        self.assertIn("no hostile audit", self.artifact["review_policy"])

    def test_hashed_inputs_and_independence_boundary(self) -> None:
        for row in self.artifact["artifact_identity"].values():
            path = ROOT / row["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"])
        self.assertFalse(self.artifact["route_independence"]["shared_implementation"])
        route_b_text = ROUTE_B.read_text(encoding="utf-8")
        self.assertNotIn("run_p7_norm_aggregation_route_a_v1", route_b_text)
        for script in (ROUTE_A, ROUTE_B, ROUTE_B_CORRECTION, RECONCILE):
            tree = ast.parse(script.read_text(encoding="utf-8"))
            self.assertEqual([node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)], [])


if __name__ == "__main__":
    unittest.main()
