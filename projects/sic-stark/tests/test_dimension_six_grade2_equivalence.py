from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dimension_six_grade2_equivalence.py"


class DimensionSixGrade2EquivalenceTests(unittest.TestCase):
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

    def test_grade_two_endpoint_equivalence(self) -> None:
        grade = self.data["grade_2"]
        self.assertEqual(
            grade["pointwise_boundary_packet_identification"],
            "EQUIVALENT",
        )

    def test_regular_continuity_is_not_smuggled_into_the_basis(self) -> None:
        grade = self.data["grade_2"]
        self.assertEqual(
            grade["full_flow_invariant_continuity_statement"],
            "NOT_DERIVED_FROM_EQUATION_33_BY_THE_STANDARD_BASIS",
        )

    def test_tcc_is_not_used_in_the_reduction(self) -> None:
        self.assertIn("TCC6", self.data["prohibited_inputs_not_used"])
        self.assertTrue(self.data["fourier_inverse_checked_on_basis"])

    def test_grade_three_surface_is_material(self) -> None:
        self.assertGreaterEqual(len(self.data["grade_3_attack_surface"]), 8)
        self.assertEqual(
            self.data["standalone_bridge"]["algebraic_half_status"],
            "VERIFIED",
        )


if __name__ == "__main__":
    unittest.main()
