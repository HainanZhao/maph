from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-norm-aggregation-v3-status-correction.json"
SCRIPT = ROOT / "proof/p7_norm_aggregation_v3_status_correction.py"


class P7NormAggregationV3StatusCorrectionTests(unittest.TestCase):
    def test_status_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["corrected_claim"]["epistemic_status"], "PROVED")
        self.assertEqual(data["corrected_claim"]["hypothesis"], "N<=T^C for a fixed C")
        self.assertIn("No unrestricted", data["corrected_claim"]["uncovered"])
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
