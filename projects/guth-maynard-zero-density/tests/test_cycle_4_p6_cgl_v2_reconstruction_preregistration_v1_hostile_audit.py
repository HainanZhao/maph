from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_cycle_4_p6_cgl_v2_preregistration_v1_hostile.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1-hostile-audit-v1.json"


class Cycle4P6CGLV2PreregistrationV1HostileAuditTests(unittest.TestCase):
    def test_sealed_pass_and_nonpromotion_boundary(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "PASS")
        self.assertEqual(data["checks"]["tex_tar_pdf_bytes_and_pdf_anchors"], "PASS")
        self.assertEqual(data["checks"]["46_rows_L12_subchecks_retired_L13"], "PASS")
        self.assertIn("proves no CGL theorem", data["claim_boundary"])

    def test_replay(self) -> None:
        subprocess.run(
            [sys.executable, str(AUDIT), "--check", str(ARTIFACT)],
            cwd=PROJECT,
            check=True,
            timeout=60,
        )


if __name__ == "__main__":
    unittest.main()
