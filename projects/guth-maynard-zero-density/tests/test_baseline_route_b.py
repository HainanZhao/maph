"""Regression tests for the independent exact Route-B baseline audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "replay_baseline_route_b.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-1-route-b-baseline.json"


class BaselineRouteBTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_artifact_replays_byte_for_byte(self) -> None:
        self.run_script("--check", str(ARTIFACT))

    def test_certificate_has_frozen_baselines(self) -> None:
        data = json.loads(self.run_script().stdout)
        analysis = data["exact_case_analysis"]
        self.assertEqual(data["frozen_hypotheses"]["sigma_domain_for_case_split"], "1/2 <= sigma <= 1")
        self.assertEqual(analysis["crossover"]["unique_root_in_domain"], "7/10")
        self.assertEqual(analysis["crossover"]["value_at_root"], "30/13")
        self.assertEqual(analysis["global_envelope"]["b"], "30/13")
        thresholds = data["short_interval_thresholds"]
        self.assertEqual(thresholds["uniform"]["theta"], "17/30")
        self.assertEqual(thresholds["almost_all"]["theta"], "2/15")

    def test_sign_polynomials_cover_the_declared_cases(self) -> None:
        # This independently checks the endpoint signs named in the artifact.
        b = Fraction(30, 13)
        ingham = lambda s: Fraction(3, 1) / (2 - s)
        gm = lambda s: Fraction(15, 1) / (3 + 5 * s)
        huxley = lambda s: Fraction(3, 1) / (3 * s - 1)
        self.assertLessEqual(ingham(Fraction(1, 2)), b)
        self.assertLessEqual(ingham(Fraction(7, 10)), b)
        self.assertLessEqual(gm(Fraction(7, 10)), b)
        self.assertLessEqual(gm(Fraction(4, 5)), b)
        self.assertLessEqual(huxley(Fraction(4, 5)), b)
        self.assertLessEqual(huxley(Fraction(1, 1)), b)
        self.assertEqual(ingham(Fraction(7, 10)), gm(Fraction(7, 10)))

    def test_critical_large_values_cell_has_the_published_strict_gain(self) -> None:
        data = json.loads(self.run_script().stdout)
        cell = data["critical_large_values_cell"]
        self.assertEqual(cell["parameterization"]["N"], "T^(4/5)")
        self.assertEqual(cell["parameterization"]["V"], "N^(3/4) = T^(3/5)")
        self.assertEqual(cell["guth_maynard_theorem_1_1"]["max_T_exponent"], "13/25")
        self.assertEqual(cell["classical_equation_1_1"]["max_T_exponent"], "3/5")
        self.assertEqual(cell["strict_gain"]["classical_minus_guth_maynard"], "2/25")
        self.assertEqual(
            cell["classical_equation_1_1"]["min_branch_equality"],
            "15/25 = 15/25",
        )

    def test_almost_all_is_not_mislabeled_as_an_independent_analytic_derivation(self) -> None:
        data = json.loads(self.run_script().stdout)
        statement = data["short_interval_thresholds"]["almost_all"]["classification"]
        self.assertIn("REPLAYED", statement)
        self.assertIn("not independently", statement)


if __name__ == "__main__":
    unittest.main()
