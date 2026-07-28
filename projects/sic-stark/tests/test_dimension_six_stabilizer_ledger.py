from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dimension_six_stabilizer_ledger.py"


class DimensionSixStabilizerLedgerTests(unittest.TestCase):
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

    def test_stabilizer_fixes_every_characteristic(self) -> None:
        self.assertEqual(self.data["A6_mod_6"], [[1, 0], [0, 1]])
        self.assertTrue(self.data["all_36_characteristics_fixed"])
        self.assertEqual(self.data["record_count"], 36)

    def test_odd_multiplier_and_phase_ledger(self) -> None:
        self.assertEqual(self.data["psi_squared_A6"], "-1")
        self.assertTrue(self.data["all_multiplier_comparisons_match"])

    def test_closure_is_still_conditional_and_not_circular(self) -> None:
        self.assertEqual(
            self.data["conditional_closure"]["status"],
            "CONDITIONAL",
        )
        audit = self.data["circularity_audit"]
        self.assertTrue(audit["fusion_implies_earlier_target"])
        self.assertTrue(
            audit["earlier_target_implies_pointwise_boundary_packet"]
        )
        self.assertFalse(
            audit["earlier_target_implies_full_flow_continuity"]
        )


if __name__ == "__main__":
    unittest.main()
