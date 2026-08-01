from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g1_energy_no_retention_v2.py"


class G1EnergyNoRetentionAuditV2Tests(unittest.TestCase):
    def test_corrected_exact_energy_gate_has_no_retained_row(self) -> None:
        data = json.loads((PROJECT / "artifacts/g1-energy-no-retention-audit-v2.json").read_text())
        self.assertEqual(data["epistemic_status"], "CERTIFIED_NUMERICAL")
        self.assertEqual(data["summary"]["scheduled_rows"], 588)
        self.assertEqual(data["summary"]["feasible_rows"], 434)
        self.assertEqual(data["summary"]["energy_retention_eligible_rows"], 0)
        self.assertEqual(data["summary"]["closest_to_energy_band"], "G1-S002")
        self.assertEqual(data["exact_method"]["W5_step"]["value"], 15)
        self.assertTrue(all(row["set_points_sha256"] for row in data["rows"] if row["status"] == "COMPLETED"))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
