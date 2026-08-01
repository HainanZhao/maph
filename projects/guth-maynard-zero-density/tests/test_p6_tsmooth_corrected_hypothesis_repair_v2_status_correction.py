from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v2-status-correction.json"
SCRIPT = ROOT / "proof/p6_tsmooth_corrected_hypothesis_repair_v2_status_correction.py"


class P6TSmoothV2StatusCorrectionTests(unittest.TestCase):
    def test_status_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        for claim in data["corrected_claims"].values():
            self.assertEqual(claim["epistemic_status"], "PROVED")
            self.assertTrue(claim["conditional_on"])
        self.assertIn("No unconditional", data["corrected_claims"]["smooth_density_envelope"]["not_promoted"])
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
