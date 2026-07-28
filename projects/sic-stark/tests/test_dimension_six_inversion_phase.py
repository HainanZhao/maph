#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixInversionPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_inversion_phase.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_exact_phase_quotient_is_level_six_chirp(self) -> None:
        self.assertEqual(
            self.result["kappa_formula"],
            "kappa_b=b+4+6*(b mod 2) mod 12",
        )
        for column in self.result["columns"].values():
            self.assertEqual(len(column["phase_records"]), 6)

    def test_wrap_sign_selects_integer_or_half_integer_sector(self) -> None:
        for second in range(6):
            column = self.result["columns"][str(second)]
            expected = "integer" if second % 2 == 0 else "half_integer"
            self.assertEqual(column["required_fourier_sector"], expected)
            self.assertEqual(
                column["wrap_sign"],
                1 if second % 2 == 0 else -1,
            )

    def test_every_parity_corrected_gauss_transform_is_flat(self) -> None:
        self.assertTrue(
            self.result[
                "all_gauss_transforms_have_squared_modulus_six"
            ]
        )
        for column in self.result["columns"].values():
            self.assertEqual(
                {
                    record["squared_modulus"]
                    for record in column["gauss_transform_records"]
                },
                {6},
            )
            self.assertTrue(
                all(
                    record["norm_minus_six_phi12_remainder"]
                    == [0, 0, 0, 0]
                    for record in column["gauss_transform_records"]
                )
            )


if __name__ == "__main__":
    unittest.main()
