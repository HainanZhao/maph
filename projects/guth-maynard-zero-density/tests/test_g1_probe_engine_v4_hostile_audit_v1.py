from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g1_probe_engine_v4_hostile_v1.py"


class G1ProbeEngineV4HostileAuditV1Tests(unittest.TestCase):
    def test_v4_promotion_boundary_is_replayable(self) -> None:
        data = json.loads((PROJECT / "artifacts/g1-probe-engine-v4-hostile-audit-v1.json").read_text())
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["decision"]["status"], "V4_READY_FOR_TWO_FRESH_UNVERIFIED_RUNS")
        self.assertTrue(all(value.startswith("PASS") for value in data["checks"].values()))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
