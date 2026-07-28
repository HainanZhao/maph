#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixBetaFourierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/dimension_six_beta_fourier.py"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_specialization_has_all_discrete_frequencies(self) -> None:
        self.assertTrue(self.result["all_discrete_frequencies_occur"])
        self.assertEqual(
            {
                record["frequency_mod_24"]
                for record in self.result["frequency_records"]
            },
            set(range(24)),
        )

    def test_fixed_scalar_is_finite_and_nonzero(self) -> None:
        audit = self.result["fixed_scalar_divisor_audit"]
        self.assertFalse(audit["pole_possible"])
        self.assertFalse(audit["zero_possible"])
        self.assertTrue(audit["Gamma_M_Q_0_is_finite_nonzero"])

    def test_contour_specialization_is_not_overclaimed(self) -> None:
        self.assertFalse(
            self.result["direct_convergence_at_g_equals_Q_claimed"]
        )
        self.assertTrue(
            self.result["meromorphic_continuation_required"]
        )
        self.assertFalse(self.result["finite_Zak_descent_proved"])


if __name__ == "__main__":
    unittest.main()
