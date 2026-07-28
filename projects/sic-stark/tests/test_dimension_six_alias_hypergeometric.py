#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixAliasHypergeometricTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts/dimension_six_alias_hypergeometric.py"
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_orientation_root_is_universal(self) -> None:
        self.assertTrue(
            self.result[
                "orientation_root_is_universally_minus_one"
            ]
        )
        self.assertEqual(
            self.result["orientation_records_checked"],
            24 * 30,
        )

    def test_alternating_weight_reaches_bailey_locus(self) -> None:
        self.assertTrue(self.result["Bailey_parameter_match_exact"])
        self.assertIn(
            ";q,q)",
            self.result["weighted_bilateral_series"],
        )

    def test_wrap_gate_is_not_overclaimed(self) -> None:
        self.assertFalse(
            self.result[
                "AFK_wrap_supplies_alternating_weight_proved"
            ]
        )
        self.assertTrue(
            self.result[
                "unit_circle_value_requires_boundary_continuation"
            ]
        )


if __name__ == "__main__":
    unittest.main()
