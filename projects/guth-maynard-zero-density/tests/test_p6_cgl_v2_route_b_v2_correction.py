from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/p6_cgl_v2_route_b_v2_correction.py"
ARTIFACT = ROOT / "artifacts/p6-cgl-v2-route-b-v2-correction.json"
V1 = ROOT / "proof/p6_cgl_v2_route_b_v1.py"


class P6CGLRouteBV2CorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text())

    def test_replay_and_v1_preservation(self) -> None:
        check = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(self.data["preserved_v1"]["script_sha256"], hashlib.sha256(V1.read_bytes()).hexdigest())

    def test_corrected_margin_is_the_actual_identity(self) -> None:
        defect = self.data["defect"]
        self.assertEqual(defect["v1_assertion"], "7 * 13 - 30 == 61")
        corrected = self.data["corrected_exact_checks"]["7/3-30/13"]
        self.assertEqual(corrected["cleared_integer_check"], "7*13-30*3=1")
        self.assertEqual(corrected["result"], "1/39")
        self.assertEqual(7 * 13 - 30 * 3, 1)

    def test_no_row_or_blocker_promotion(self) -> None:
        effect = self.data["row_level_effect"]
        self.assertEqual(effect["canonical_row_count_unchanged"], 46)
        self.assertEqual(effect["overall_disposition_unchanged"], "OPEN_ANALYTIC_INPUT")
        self.assertIn("Z03_TAIL_X_RANGE", effect["open_blockers_unchanged"])


if __name__ == "__main__":
    unittest.main()
