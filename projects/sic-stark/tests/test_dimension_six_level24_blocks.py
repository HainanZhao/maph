#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixLevel24BlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_level24_blocks.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_characteristics_land_in_four_six_dimensional_blocks(self) -> None:
        self.assertEqual(
            self.result["coefficient_block_counts"],
            {"0": 12, "1": 6, "2": 6, "3": 12},
        )
        self.assertEqual(
            len(self.result["characteristic_records"]),
            36,
        )

    def test_stabilizer_pairs_inverse_central_characters(self) -> None:
        self.assertTrue(
            self.result[
                "stabilizer_is_identity_on_local_level_six_labels"
            ]
        )
        self.assertEqual(
            [
                self.result["coefficient_blocks"][str(block)][
                    "stabilizer_target_block"
                ]
                for block in range(4)
            ],
            [0, 3, 2, 1],
        )

    def test_ideal_and_coefficient_polarizations_are_distinct(self) -> None:
        comparison = self.result["polarization_comparison"]
        self.assertEqual(
            comparison["coefficient_smith_invariants"],
            [1, 4],
        )
        self.assertEqual(
            comparison["ideal_smith_invariants"],
            [2, 2],
        )
        self.assertFalse(comparison["integral_unimodular_equivalence"])

    def test_ideal_blocks_are_glued_three_plus_three(self) -> None:
        for block in self.result["ideal_blocks"].values():
            self.assertTrue(
                block[
                    "three_dimensions_from_each_coefficient_block"
                ]
            )
            self.assertEqual(len(block["basis_supports"]), 6)

    def test_even_inversion_gaussian_records_remaining_gate(self) -> None:
        phase = self.result["inversion_phase_match"]
        self.assertTrue(phase["block_pairing_r_to_minus_r"])
        self.assertFalse(
            phase["level24_gaussian_restricts_to_level6_gaussian"]
        )
        self.assertTrue(
            phase["restriction_is_fourth_power_with_linear_gauge"]
        )
        self.assertTrue(
            phase["P12_sign_exchange_occurs_exactly_on_odd_blocks"]
        )


if __name__ == "__main__":
    unittest.main()
