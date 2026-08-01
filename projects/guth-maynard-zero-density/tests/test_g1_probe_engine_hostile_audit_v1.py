from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g1_probe_engine_hostile_v1.py"


class G1ProbeEngineHostileAuditV1Tests(unittest.TestCase):
    def test_v1_defects_are_preserved_and_replayable(self) -> None:
        data = json.loads((PROJECT / "artifacts/g1-probe-engine-hostile-audit-v1.json").read_text())
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["decision"]["status"], "V1_CONTAINED_NOT_G1_AUTHORITY")
        self.assertEqual([row["id"] for row in data["checks"]], [
            "RUNTIME_PIN_NOT_ENFORCED",
            "VALIDATION_SCORE_LOSS_NOT_ADJUDICATED",
            "GENERIC_ROW_EXCEPTION_ABORTS_RUN",
        ])
        self.assertTrue(all(row["status"] == "FAIL" for row in data["checks"]))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
