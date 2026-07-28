from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dimension_six_boundary_integral_audit.py"


class DimensionSixBoundaryIntegralAuditTests(unittest.TestCase):
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

    def test_vertical_contour_is_excluded(self) -> None:
        self.assertEqual(
            self.data["original_vertical_contour_absolute_convergence"],
            "EXCLUDED",
        )
        self.assertEqual(
            self.data["single_vertical_contour_for_all_36_frequencies"],
            "EXCLUDED",
        )

    def test_meromorphic_value_remains_verified(self) -> None:
        self.assertEqual(
            self.data["meromorphic_boundary_evaluation"]["status"],
            "VERIFIED_BY_SS_EQUATION_66",
        )

    def test_only_fusion_continuity_remains(self) -> None:
        self.assertEqual(self.data["residual_sublemma_count"], 1)
        self.assertEqual(
            self.data["residual_sublemmas"][0]["status"],
            "OPEN",
        )

    def test_tilted_value_and_component_census(self) -> None:
        self.assertEqual(
            self.data["tilted_finite_part"]["tilt_independence"],
            "PROVED_BY_CAUCHY_AND_VANISHING_CAPS",
        )
        self.assertEqual(
            self.data["component_census"],
            {
                "one_sided_growing_strip_required": 30,
                "purely_oscillatory_Fresnel": 6,
            },
        )


if __name__ == "__main__":
    unittest.main()
