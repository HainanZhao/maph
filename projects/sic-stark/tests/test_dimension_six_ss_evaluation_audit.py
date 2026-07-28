from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_ss_evaluation_audit.py"


class DimensionSixSSEvaluationAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.data = json.loads(completed.stdout)

    def test_exact_parameter_map_and_source_equations(self) -> None:
        self.assertEqual(cls := self.data["parameter_map"]["pr_plus_ks"], 1)
        self.assertEqual(
            self.data["source"]["degenerate_two_gamma_evaluation"],
            66,
        )
        self.assertEqual(cls, 1)

    def test_meromorphic_identity_hypotheses_are_audited(self) -> None:
        self.assertTrue(
            self.data["all_meromorphic_identity_hypotheses_verified"]
        )
        self.assertTrue(
            self.data["direct_boundary_contour_hypothesis_open"]
        )

    def test_transform_does_not_fake_a_finite_relation(self) -> None:
        verdict = self.data["verdict"]
        self.assertTrue(
            verdict["SS_equation_66_is_a_new_integral_transform_identity"]
        )
        self.assertFalse(
            verdict["SS_supplies_new_finite_multiplicative_relation"]
        )
        self.assertTrue(verdict["conservation_of_obstruction"])


if __name__ == "__main__":
    unittest.main()
