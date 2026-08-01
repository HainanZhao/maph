from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_cycle_4_p1r_preregistration_v1_hostile.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v1-hostile-audit-v1.json"


class Cycle4P1RPreregistrationV1HostileAuditTests(unittest.TestCase):
    def test_sealed_failure_and_correct_boundaries(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS")
        self.assertEqual(data["checks"]["FS_authorized_after_preregistration"], "PASS")
        self.assertEqual(data["checks"]["CRR_search_forbidden"], "PASS")
        self.assertEqual(data["checks"]["documented_check_command_verbatim"], "FAIL")

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
