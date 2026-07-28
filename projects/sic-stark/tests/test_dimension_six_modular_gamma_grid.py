#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixModularGammaGridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_modular_gamma_grid.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_all_characteristics_embed_in_affine_grid(self) -> None:
        self.assertEqual(self.result["sample_count"], 36)
        self.assertEqual(len(self.result["sample_records"]), 36)

    def test_grid_closes_by_general_gamma_functional_shifts(self) -> None:
        closure = self.result["closure_relations"]
        self.assertTrue(
            closure[
                "six_b_steps_equal_functional_shift_difference"
            ]
        )
        self.assertEqual(
            closure["six_a_steps"]["discrete_coordinate"],
            -24,
        )

    def test_reflection_closes_on_affine_characteristics(self) -> None:
        self.assertEqual(
            self.result["reflection_on_characteristics"],
            "(a,b)->(1-a,-b) mod 6",
        )
        self.assertTrue(
            self.result[
                "primitive_two_gamma_kernel_lives_on_same_affine_grid"
            ]
        )
        self.assertEqual(len(self.result["reflection_records"]), 36)


if __name__ == "__main__":
    unittest.main()
