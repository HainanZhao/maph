"""Regression tests for the deterministic Route-A Stream-B continuation."""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_cycle2_stream_b_route_a_v3.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-b-route-a-v3.json"


def module():
    spec = importlib.util.spec_from_file_location("stream_b_a_v3", SCRIPT)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class StreamBRouteAV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = module()

    def test_artifact_is_byte_stable(self):
        subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], check=True, cwd=PROJECT)

    def test_all_three_gm_terms_and_residual_are_explicit(self):
        audit = self.m.exact_exponent_audit()
        terms = audit["theorem_1_1_structural_terms"]
        self.assertEqual(terms["source_terms"], ["L^(2-2sigma)", "L^(18/5-4sigma)", "T L^(12/5-4sigma)"])
        self.assertIn("250(sigma-3/4)^2+3/8", audit["mvt_branch"]["second_term_residual"])
        self.assertIn("2(1-sigma) <= A(sigma)", audit["type_ii"]["conclusion"])

    def test_scope_and_beta_wording_are_contained(self):
        data = json.loads(ARTIFACT.read_text())
        self.assertTrue(data["pass_state"].startswith("NARROW PASS:"))
        self.assertIn("G0", data["claim_boundary"])
        correction = {row["id"]: row for row in data["rows"]}["SB-A21-beta-cutoff-wording-correction"]
        self.assertIn("counting restriction", correction["statement"])

    def test_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text())
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
