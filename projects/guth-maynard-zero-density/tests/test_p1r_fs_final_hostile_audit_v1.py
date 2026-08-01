from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_p1r_fs_final_v1.py"
ARTIFACT = PROJECT / "artifacts/p1r-fs-final-hostile-audit-v1.json"


class P1RFSFinalHostileAuditV1Tests(unittest.TestCase):
    def test_sealed_promotion_pass(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["checks"]["exact_real_supremum_and_epsilon_quantifier"], "PASS")
        self.assertEqual(data["checks"]["extended_real_right_branch"], "PASS")

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
