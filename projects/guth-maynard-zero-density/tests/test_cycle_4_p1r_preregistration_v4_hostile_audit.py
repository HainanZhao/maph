from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_cycle_4_p1r_preregistration_v4_hostile.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v4-hostile-audit-v1.json"


class Cycle4P1RPreregistrationV4HostileAuditTests(unittest.TestCase):
    def test_sealed_pass(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["checks"]["GM_T1_1_exact_formula_hypotheses_and_permitted_use"], "PASS")
        self.assertEqual(data["checks"]["runtime_zero_PLAN_read"], "PASS")

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
