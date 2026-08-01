from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-common-ideal-cubic-v2-correction.json"
BUILDER = ROOT / "proof/build_p7_common_ideal_cubic_v2_correction.py"


class P7CommonIdealCubicCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_pins(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for row in self.data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_integer_replay_and_scope(self) -> None:
        replay = self.data["corrected_claim"]["integer_replay"]
        self.assertEqual(replay["coloured_energy"], 34)
        self.assertIsInstance(replay["orthogonality_parseval_count"], int)
        self.assertEqual(replay["orthogonality_parseval_count"], 34)
        self.assertEqual(replay["uncoloured_time_energy_with_multiplicity"], 62)
        self.assertEqual(self.data["corrected_claim"]["epistemic_status"], "PROVED")
        self.assertIn("remains open", " ".join(self.data["unchanged"]))


if __name__ == "__main__":
    unittest.main()
