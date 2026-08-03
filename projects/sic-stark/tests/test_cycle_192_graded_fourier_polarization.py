#!/usr/bin/env python3
"""Independent regression checks for Cycle 192's finite result."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
LEVEL = 24
DIMENSION = 6


class Cycle192GradedFourierPolarizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "proof"
                    / "verify_cycle_192_graded_fourier_polarization.py"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_full_fourier_pairing_independently(self) -> None:
        """Check every ambient character coefficient against the block rule."""

        action = self.result["source_block_action"]["action"]
        for parity in range(2):
            for sign, sign_name in ((1, "+"), (-1, "-")):
                key = f"B_({parity},{sign_name})"
                target = action[key]["target"]
                target_parity = 0 if target[3] == "0" else 1
                target_sign = 1 if target[-2] == "+" else -1
                kernel = action[key]["kernel_exponents_mod_24"]
                for source in range(DIMENSION):
                    for ambient in range(LEVEL):
                        survives = 1 + sign * (-1) ** ambient != 0
                        self.assertEqual(survives, ambient % 2 == target_parity)
                        if not survives:
                            continue
                        output = ((ambient - target_parity) // 2) % DIMENSION
                        expected = (
                            ambient * (parity + 2 * source)
                        ) % LEVEL
                        actual = kernel[output][source]
                        if ambient >= target_parity + 12:
                            actual = (
                                actual + (12 if target_sign == -1 else 0)
                            ) % LEVEL
                        self.assertEqual(expected, actual)

    def test_forced_closure_and_twisted_holonomy(self) -> None:
        closure = self.result["forced_closure"]
        self.assertFalse(closure["two_block_sum_is_F24_invariant"])
        self.assertEqual(closure["closure_dimension"], 18)
        self.assertEqual(
            closure["unique_smallest_F24_invariant_closure"],
            ["B_(0,+)", "B_(0,-)", "B_(1,+)"],
        )
        records = self.result["alias_holonomy_intertwining"]["records"]
        p_one = [record for record in records if record["source_block"] == "B_(1,+)"][0]
        self.assertEqual(
            [entry["root_exponent_mod_24"] for entry in p_one["monomial_three_shift_records"]],
            [6, 6, 6, 18, 18, 18],
        )

    def test_all36_carriers_and_retained_phases(self) -> None:
        carriers = self.result["all36_afk_carriers"]
        self.assertEqual(carriers["rows_checked"], 36)
        self.assertEqual(
            carriers["carrier_counts"],
            {"W_0": 12, "W_1": 6, "W_2": 6, "W_3": 12},
        )
        self.assertTrue(carriers["capital_gamma_normalization_retained_separately"])
        self.assertTrue(carriers["afk_phase_retained_separately"])
        for row in carriers["rows"]:
            first, second = row["characteristic"]
            r = (second - 1) % 4
            offset = (second - 1 - r) // 4
            self.assertEqual(
                row["afk_local_coordinate"],
                (-first + offset) % DIMENSION,
            )

    def test_polarization_exponent_is_a_normalizer_invariant(self) -> None:
        ideal = {(2 * first % LEVEL, 2 * second % LEVEL)
                 for first in range(LEVEL) for second in range(LEVEL)}
        coefficient = {(4 * first % LEVEL, second % LEVEL)
                       for first in range(LEVEL) for second in range(LEVEL)}
        self.assertEqual(len(ideal), 144)
        self.assertEqual(len(coefficient), 144)

        def additive_order(point: tuple[int, int]) -> int:
            for multiple in range(1, LEVEL + 1):
                if all(multiple * coordinate % LEVEL == 0 for coordinate in point):
                    return multiple
            raise AssertionError("finite-module order missing")

        self.assertEqual(max(map(additive_order, ideal)), 12)
        self.assertEqual(max(map(additive_order, coefficient)), 24)
        obstruction = self.result["finite_metaplectic_polarization_obstruction"]
        self.assertEqual(obstruction["ideal_subgroup_exponent"], 12)
        self.assertEqual(obstruction["coefficient_subgroup_exponent"], 24)
        self.assertFalse(obstruction["finite_metaplectic_intertwiner_exists"])


if __name__ == "__main__":
    unittest.main()
