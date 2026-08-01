from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_cycle_4_p1r_preregistration_v2_hostile.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v2-hostile-audit-v1.json"


class Cycle4P1RPreregistrationV2HostileAuditTests(unittest.TestCase):
    def test_sealed_lifecycle_failure(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "FAIL_PLAN_LIFECYCLE_SEMANTIC_COUPLING")
        self.assertEqual(data["checks"]["future_P1R_complete_replay"], "FAIL")
        self.assertEqual(data["checks"]["future_affirmative_P2_replay"], "FAIL")

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
