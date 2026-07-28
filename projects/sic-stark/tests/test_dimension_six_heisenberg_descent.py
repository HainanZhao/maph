from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixHeisenbergDescentTests(unittest.TestCase):
    def test_two_exact_six_dimensional_blocks(self) -> None:
        output = subprocess.check_output(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "dimension_six_heisenberg_descent.py"
                ),
            ],
            text=True,
        )
        result = json.loads(output)
        self.assertTrue(result["finite_weyl_bridge_exists"])
        self.assertFalse(result["analytic_operator_restriction_identified"])
        self.assertEqual(result["common_block_dimension"], 6)
        self.assertEqual(
            result["level_24_trivial_block"]["basis_supports"],
            [
                [0, 12],
                [2, 14],
                [4, 16],
                [6, 18],
                [8, 20],
                [10, 22],
            ],
        )
        self.assertEqual(
            [record["ambient_heisenberg_level"] for record in result["records"]],
            [24, 504],
        )
        self.assertEqual(
            [record["lattice_index"] for record in result["records"]],
            [4, 84],
        )
        for record in result["records"]:
            self.assertEqual(record["weyl_commutator_order"], 6)
            self.assertEqual(
                record["trivial_central_character_block_dimension"],
                6,
            )
            self.assertTrue(record["lattice_preserved_by_L"])
            self.assertTrue(record["lattice_preserved_by_A"])


if __name__ == "__main__":
    unittest.main()
