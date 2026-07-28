#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixBetaKernelMatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_beta_kernel_match.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_general_modular_bezout_parameters(self) -> None:
        self.assertEqual(
            self.result["general_modular_parameters"],
            {
                "p": -115,
                "k": 24,
                "r": 5,
                "s": 24,
                "bezout_identity": "p*r+k*s=1",
            },
        )

    def test_primitive_quotient_is_published_beta_kernel(self) -> None:
        self.assertTrue(
            self.result["beta_kernel_specialization"]["exact_match"]
        )
        self.assertIn(
            "tau_6^h",
            self.result["normalized_kernel_identity"],
        )
        self.assertEqual(
            len(self.result["normalization_ratio_records"]),
            36,
        )

    def test_two_gamma_kernel_is_genuinely_periodic(self) -> None:
        self.assertTrue(self.result["kernel_is_periodic_mod_24"])
        self.assertTrue(
            all(
                record["kernel_period_sign"] == 1
                for record in self.result[
                    "kernel_periodicity_records"
                ]
            )
        )

    def test_only_finite_zak_descent_remains(self) -> None:
        self.assertTrue(
            self.result["published_beta_identity_is_continuous_discrete"]
        )
        self.assertFalse(self.result["finite_Zak_descent_proved"])


if __name__ == "__main__":
    unittest.main()
