from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-detector-qt-tail-v2-status-correction.json"
SCRIPT = ROOT / "proof/p6_detector_qt_tail_v2_status_correction.py"


class P6DetectorTailV2StatusCorrectionTests(unittest.TestCase):
    def test_status_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["corrected_claim"]["epistemic_status"], "PROVED")
        self.assertEqual(set(data["corrected_claim"]["conditional_on"]), {"L_POLY_A", "FOURTH_MOMENT_H", "LOW_HEIGHT_MULTIPLICITY_COUNT"})
        self.assertIn("No CGL theorem", data["corrected_claim"]["not_promoted"])
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
