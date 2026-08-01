from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-post-repair-reconciliation-v1.json"
SCRIPT = ROOT / "proof/build_p6_post_repair_reconciliation_v1.py"


class P6PostRepairReconciliationV1Tests(unittest.TestCase):
    def test_coverage_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["original_registry"]["count"], 46)
        rows = data["row_reconciliation"]
        self.assertEqual(len(rows), 46)
        self.assertEqual({row["id"] for row in rows}, set(data["original_registry"]["ids"]))
        by_id = {row["id"]: row["post_repair"] for row in rows}
        self.assertEqual(by_id["Z03"]["epistemic_status"], "PROVED")
        self.assertEqual(by_id["Z05"]["epistemic_status"], "PROVED")
        self.assertEqual(by_id["F03"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(data["general_7_over_3_envelope"]["verdict"], "NOT_PROMOTED")
        self.assertEqual(data["q_equals_one"]["verdict"], "SEPARATELY_COVERED_BY_G0_AT_30_OVER_13")
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
