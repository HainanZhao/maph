from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_g1_route_decision_v2_hostile.py"
ARTIFACT = PROJECT / "artifacts/g1-route-decision-v2-hostile-audit-v1.json"


class G1RouteDecisionV2HostileAuditTests(unittest.TestCase):
    def test_sealed_pass_and_boundaries(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "PASS")
        self.assertTrue(all(value == "PASS" for value in data["checks"].values()))
        self.assertIn("not selected and not refuted", data["conclusion"])

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
