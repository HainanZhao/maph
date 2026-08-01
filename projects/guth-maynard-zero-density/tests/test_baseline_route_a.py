"""Independent regression tests for the exact Cycle 1 Route A replay."""

import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "proof" / "replay_baseline_route_a.py"
ARTIFACT = PROJECT_ROOT / "artifacts" / "baseline-route-a-v3.json"


def load_route_a():
    spec = importlib.util.spec_from_file_location("route_a", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BaselineRouteATest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.route_a = load_route_a()

    def test_crossover_is_exact_and_has_the_stated_sign_change(self):
        sigma = Fraction(7, 10)
        self.assertEqual(self.route_a.ingham_coefficient(sigma), Fraction(30, 13))
        self.assertEqual(self.route_a.guth_maynard_coefficient(sigma), Fraction(30, 13))
        self.assertEqual(self.route_a.coefficient_difference(sigma), 0)
        self.assertLess(self.route_a.coefficient_difference(Fraction(2, 3)), 0)
        self.assertGreater(self.route_a.coefficient_difference(Fraction(3, 4)), 0)

    def test_short_interval_endpoint_formulae_are_exact(self):
        certificate = self.route_a.compute_certificate()
        self.assertEqual(certificate["crossover"]["global_density_coefficient_b"], "30/13")
        self.assertEqual(certificate["uniform_short_interval"]["one_over_b"], "13/30")
        self.assertEqual(certificate["uniform_short_interval"]["theta"], "17/30")
        self.assertEqual(certificate["almost_all_short_interval"]["two_over_b"], "13/15")
        self.assertEqual(certificate["almost_all_short_interval"]["delta_exponent"], "-13/15")
        self.assertEqual(certificate["almost_all_short_interval"]["theta"], "2/15")

    def test_critical_large_values_cell_is_exact(self):
        cell = self.route_a.critical_large_values_cell()
        self.assertEqual(cell["cell"]["V_in_terms_of_T"], "V = T^(3/5)")
        self.assertEqual(
            cell["guth_maynard_theorem_1_1"]["terms"],
            {
                "N^2*V^-2": "2/5",
                "N^(18/5)*V^-4": "12/25",
                "T*N^(12/5)*V^-4": "13/25",
            },
        )
        self.assertEqual(
            cell["guth_maynard_theorem_1_1"]["maximum_T_exponent"], "13/25"
        )
        self.assertEqual(
            cell["classical_equation_1_1"]["terms"],
            {
                "N^2*V^-2": "2/5",
                "T*N*V^-2": "3/5",
                "T*N^4*V^-6": "3/5",
            },
        )
        self.assertEqual(
            cell["classical_equation_1_1"]["minimum_inside_T_times_min"], "3/5"
        )
        self.assertEqual(cell["classical_equation_1_1"]["maximum_T_exponent"], "3/5")
        self.assertEqual(cell["strict_gain_in_T_exponent"], "2/25")

    def test_zero_density_bottleneck_cell_has_the_exact_tie_pattern(self):
        cell = self.route_a.zero_density_bottleneck_cell()
        self.assertEqual(cell["parameters"]["L_in_U"], "L = U^(5/6)")
        self.assertEqual(cell["parameters"]["threshold"], "V = L^sigma = U^(7/12)")
        self.assertEqual(
            cell["theorem_1_1_at_U"]["terms"],
            {
                "L^2*V^-2": "1/2",
                "L^(18/5)*V^-4": "2/3",
                "U*L^(12/5)*V^-4": "2/3",
            },
        )
        self.assertEqual(cell["theorem_1_1_at_U"]["maximum_U_exponent"], "2/3")
        self.assertEqual(
            cell["proposition_11_1_energy_bound_at_U"]["terms"],
            {
                "|W|*L^(4-4*sigma)": "5/3",
                "|W|^(21/8)*U^(1/4)*L^(1-2*sigma)": "5/3",
                "|W|^3*L^(1-2*sigma)": "5/3",
            },
        )
        aggregation = cell["subinterval_aggregation"]
        self.assertEqual(aggregation["number_of_subintervals"], "T/U = T^(1/13)")
        self.assertEqual(aggregation["local_bound"], "U^(2/3) = T^(8/13)")
        self.assertEqual(aggregation["total_T_exponent"], "9/13")

    def test_proof_script_contains_no_float_literals(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        float_literals = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, float)
        ]
        self.assertEqual(float_literals, [])

    def test_replay_writes_an_artifact_consistent_with_the_certificate(self):
        subprocess.run([sys.executable, str(SCRIPT)], check=True, cwd=PROJECT_ROOT)
        artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        certificate = self.route_a.compute_certificate()
        self.assertEqual(artifact["artifact_version"], 3)
        self.assertEqual(artifact["route"], "A")
        self.assertEqual(artifact["arithmetic"], "exact fractions.Fraction only")
        self.assertEqual(artifact["crossover"], certificate["crossover"])
        self.assertEqual(artifact["uniform_short_interval"], certificate["uniform_short_interval"])
        self.assertEqual(artifact["almost_all_short_interval"], certificate["almost_all_short_interval"])
        self.assertEqual(artifact["critical_large_values_cell"], certificate["critical_large_values_cell"])
        self.assertEqual(artifact["zero_density_bottleneck_cell"], certificate["zero_density_bottleneck_cell"])
        self.assertEqual(artifact["replay"]["script_sha256"], self.route_a.source_sha256(SCRIPT))
        mathematical_part = {
            key: value
            for key, value in artifact.items()
            if key not in {"mathematical_certificate_sha256", "replay"}
        }
        self.assertEqual(
            artifact["mathematical_certificate_sha256"],
            self.route_a.canonical_sha256(mathematical_part),
        )
        self.assertEqual(artifact["frozen_source"]["arxiv_identifier"], "2405.20552v2")


if __name__ == "__main__":
    unittest.main()
