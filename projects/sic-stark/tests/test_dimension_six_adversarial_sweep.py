from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dimension_six_adversarial_sweep.py"


class DimensionSixAdversarialSweepTests(unittest.TestCase):
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

    def test_independent_frequency_ledger(self) -> None:
        audit = self.data["independent_reimplementations"]
        self.assertEqual(audit["helical_records_checked"], 36 * 41)
        self.assertTrue(audit["all_frequency_labels_match"])

    def test_boundary_shortcuts_remain_excluded(self) -> None:
        audit = self.data["independent_reimplementations"]
        self.assertEqual(audit["annulus_edge_exchange"], "EXCLUDED")
        self.assertEqual(audit["slater_boundary_applicability"], "EXCLUDED")

    def test_every_perturbation_is_detected(self) -> None:
        self.assertTrue(self.data["all_perturbations_detected"])
        for record in self.data["perturbations"].values():
            self.assertTrue(record["detected"])

    def test_trace_corruption_distinguishes_the_two_fusions(self) -> None:
        record = self.data["perturbations"]["trace_5_to_6"]
        self.assertTrue(record["standard_pair_still_fuses"])
        self.assertFalse(record["lens_pair_still_fuses"])


if __name__ == "__main__":
    unittest.main()
