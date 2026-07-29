from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_conditioning_comparison.py"


@unittest.skipUnless(
    os.environ.get("SIC_STARK_RUN_ARB") == "1",
    "set SIC_STARK_RUN_ARB=1 in the pinned python-flint environment",
)
class DimensionSixConditioningComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(ROOT / "scripts")},
        )
        cls.data = json.loads(completed.stdout)

    def test_slopes_replicate(self) -> None:
        summary = self.data["slope_summary"]
        self.assertGreater(
            summary["d6_decimal_digits_lost_per_one_over_s"], 2.7
        )
        self.assertLess(
            summary["d6_decimal_digits_lost_per_one_over_s"], 2.9
        )
        self.assertGreater(
            summary["d4_decimal_digits_lost_per_one_over_s"], 0.60
        )
        self.assertLess(
            summary["d4_decimal_digits_lost_per_one_over_s"], 0.69
        )

    def test_exponential_fit_is_not_promoted_to_theorem(self) -> None:
        self.assertEqual(
            self.data["empirical_model_verdict"],
            "ESSENTIAL_EXPONENTIAL_IN_ONE_OVER_S_ON_PINNED_WINDOWS",
        )
        self.assertTrue(self.data["not_an_intrinsic_exponent"])


if __name__ == "__main__":
    unittest.main()
