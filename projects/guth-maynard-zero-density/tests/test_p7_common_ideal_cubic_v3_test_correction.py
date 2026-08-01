from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-common-ideal-cubic-v3-test-correction.json"
BUILDER = ROOT / "proof/build_p7_common_ideal_cubic_v3_test_correction.py"
V2 = ROOT / "artifacts/p7-common-ideal-cubic-v2-correction.json"


class P7CommonIdealCubicV3TestCorrection(unittest.TestCase):
    def test_replay_and_integer_correction(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(ARTIFACT.read_text())
        for row in data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        v2 = json.loads(V2.read_text())
        replay = v2["corrected_claim"]["integer_replay"]
        self.assertEqual((replay["coloured_energy"], replay["orthogonality_parseval_count"], replay["uncoloured_time_energy_with_multiplicity"]), (34, 34, 62))
        self.assertIn("open coloured primitive cubic estimate", " ".join(v2["unchanged"]))


if __name__ == "__main__":
    unittest.main()
