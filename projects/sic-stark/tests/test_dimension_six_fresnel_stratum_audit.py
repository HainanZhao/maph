from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_fresnel_stratum_audit.py"


class DimensionSixFresnelStratumAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.data = json.loads(completed.stdout)

    def test_fresnel_set_matches_qgamma_tame_set(self) -> None:
        self.assertTrue(
            self.data[
                "analytic_classification_matches_qgamma_cancellation"
            ]
        )
        for record in self.data["shift_records"].values():
            self.assertTrue(record["fresnel_equals_qgamma_tame"])

    def test_fresnel_set_is_not_the_lower_conductor_stratum(self) -> None:
        self.assertFalse(
            self.data[
                "analytic_classification_matches_arithmetic_lower_stratum"
            ]
        )
        for record in self.data["shift_records"].values():
            self.assertEqual(
                record["fresnel_denominator_counts"],
                {"1": 1, "2": 1, "3": 2, "6": 2},
            )
            self.assertEqual(
                record["growing_denominator_counts"],
                {"1": 0, "2": 2, "3": 6, "6": 22},
            )


if __name__ == "__main__":
    unittest.main()
