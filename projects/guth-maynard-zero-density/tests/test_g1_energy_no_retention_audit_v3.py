from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g1_energy_no_retention_v3.py"


class G1EnergyNoRetentionAuditV3Tests(unittest.TestCase):
    def test_machin_closed_energy_certificate(self) -> None:
        data = json.loads((PROJECT / "artifacts/g1-energy-no-retention-audit-v3.json").read_text())
        self.assertEqual(data["epistemic_status"], "CERTIFIED_NUMERICAL")
        self.assertEqual(data["summary"]["energy_retention_eligible_rows"], 0)
        identity = data["exact_method"]["W5_step"]["machin_identity_verified"]
        self.assertEqual(identity["tan_4atan_1_5"], "120/119")
        self.assertEqual(identity["tan_difference"], "1/1")
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
