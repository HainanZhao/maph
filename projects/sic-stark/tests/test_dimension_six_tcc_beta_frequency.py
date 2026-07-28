#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixTccBetaFrequencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/dimension_six_tcc_beta_frequency.py"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_shift_one_frequency_map(self) -> None:
        self.assertEqual(
            self.result["shift_one_closed_map"],
            "(u,v)->(N,ell)=(2-u,-u-v) mod 6",
        )
        self.assertTrue(self.result["shift_one_map_is_bijective"])

    def test_shift_zero_frequency_map(self) -> None:
        self.assertEqual(
            self.result["shift_zero_closed_map"],
            "(u,v)->(N,ell)=(2-u-v,-v) mod 6",
        )
        self.assertTrue(self.result["shift_zero_map_is_bijective"])

    def test_every_output_has_one_residue_class(self) -> None:
        self.assertEqual(len(self.result["records"]["0"]), 36)
        self.assertEqual(len(self.result["records"]["1"]), 36)


if __name__ == "__main__":
    unittest.main()
