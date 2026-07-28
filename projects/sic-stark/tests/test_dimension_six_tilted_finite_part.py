from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_tilted_finite_part.py"


class DimensionSixTiltedFinitePartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.data = json.loads(completed.stdout)

    def test_component_census(self) -> None:
        components = self.data["components"]
        self.assertEqual(components["purely_oscillatory_count"], 6)
        self.assertEqual(components["one_sided_growing_count"], 30)
        self.assertEqual(len(components["records"]), 36)

    def test_exact_displacement_and_small_divisor_are_recorded(self) -> None:
        arithmetic = self.data["fusion_arithmetic"]
        self.assertEqual(
            arithmetic["exact_base_displacement"],
            "A6*tau-tau=-24*tau*Delta(tau)/(24*tau-5)",
        )
        self.assertEqual(
            arithmetic["continued_fraction"], "[4;overline{1,3}]"
        )
        self.assertIn("sqrt(21)*n+1/2", arithmetic["small_divisor_bound"])

    def test_tilt_independence_is_an_interior_theorem(self) -> None:
        tilted = self.data["tilted_integral"]
        self.assertEqual(
            tilted["status"], "PROVED_IN_INTERIOR_CONVERGENCE_CHAMBER"
        )
        self.assertIn("if the limit exists", tilted["boundary_definition"])


if __name__ == "__main__":
    unittest.main()
