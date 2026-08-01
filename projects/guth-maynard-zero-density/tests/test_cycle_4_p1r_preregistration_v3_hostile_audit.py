from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_cycle_4_p1r_preregistration_v3_hostile.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v3-hostile-audit-v1.json"


class Cycle4P1RPreregistrationV3HostileAuditTests(unittest.TestCase):
    def test_sealed_source_attribution_failure(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "FAIL_SOURCE_ATTRIBUTION_COMPLETENESS")
        self.assertEqual(data["checks"]["runtime_zero_PLAN_read"], "PASS")
        self.assertEqual(data["checks"]["large_values_direct_source_attribution"], "FAIL")

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
