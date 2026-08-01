"""Regression tests for the independent exact Route A v4 case-split audit."""

import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_theorem_1_2_case_split_route_a_v4.py"
ARTIFACT = PROJECT / "artifacts" / "theorem-1-2-case-split-route-a-v4.json"


def load_module():
    spec = importlib.util.spec_from_file_location("route_a_v4", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TheoremOneTwoRouteAV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.route = load_module()

    def test_all_branches_are_covered_and_o_one_is_not_erased(self):
        certificate = self.route.theorem_1_2_case_split()
        self.assertTrue(certificate["coverage"]["all_branch_labels_exercised"])
        self.assertTrue(certificate["coverage"]["o_one_containment_retained"])
        self.assertIn("Type", certificate["type_ii"]["source_bound_exponent"].replace("2(1-s)", "Type II"))
        self.assertIn("q <= alpha(s)", certificate["coverage"]["q_branches"])
        self.assertIn("q > alpha(s)", certificate["coverage"]["q_branches"])
        large = certificate["integer_choice"]["large_n"]
        self.assertIn("o(1)", large["source_upper"])
        self.assertIn("no finite-T exact", large["contained_conclusion"])

    def test_exact_boundary_values_and_strict_margin(self):
        certificate = self.route.theorem_1_2_case_split()
        endpoints = certificate["monotonicity_and_endpoints"]["endpoint_values"]
        self.assertEqual(endpoints["u(7/10), u(4/5)"], ["15/13", "15/14"])
        self.assertEqual(endpoints["uniform_gap_u_minus_1"], "1/14")
        gm = certificate["guth_maynard_branch_q_le_alpha"]
        self.assertEqual(gm["exact_endpoint_substitutions"]["first"], ["9/13", "3/7"])
        self.assertEqual(gm["exact_endpoint_substitutions"]["second"], ["9/13", "3/7"])
        self.assertEqual(gm["exact_endpoint_substitutions"]["third"], ["9/13", "3/7"])
        margin = certificate["mean_value_branch_q_gt_alpha"]["second_term"]
        self.assertEqual(margin["exact_margin_at_7_10_3_4_4_5"], ["1/26", "1/54", "1/14"])
        self.assertIn(">0", margin["margin_identity"])

    def test_no_float_literals_in_proof_script(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        floats = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, float)
        ]
        self.assertEqual(floats, [])

    def test_one_command_replay_and_hashed_artifact(self):
        subprocess.run([sys.executable, str(SCRIPT)], check=True, cwd=PROJECT)
        artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        body = {
            key: value
            for key, value in artifact.items()
            if key not in {"mathematical_certificate_sha256", "replay"}
        }
        self.assertEqual(artifact["artifact_version"], 4)
        self.assertEqual(artifact["route"], "A")
        self.assertEqual(artifact["arithmetic"], "exact fractions.Fraction only")
        self.assertEqual(
            artifact["mathematical_certificate_sha256"], self.route.canonical_sha256(body)
        )
        self.assertEqual(artifact["replay"]["script_sha256"], self.route.file_sha256(SCRIPT))


if __name__ == "__main__":
    unittest.main()
