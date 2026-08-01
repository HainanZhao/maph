from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-s06-primary-input-ledger-v3-lc-correction.json"
SCRIPT = ROOT / "proof/build_p6_s06_primary_input_ledger_v3_lc_correction.py"


class P6S06PrimaryInputLedgerV3LCCorrectionTests(unittest.TestCase):
    def test_scope_geometry_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        corrected = data["corrected_input"]
        self.assertEqual(corrected["id"], "LOCAL_MULTIPLICITY_COUNT_LC")
        self.assertEqual(corrected["epistemic_status"], "PROVED")
        self.assertIn("multiplicity", corrected["statement"])
        self.assertEqual(data["geometry"]["max_distance_squared"], "221/400")
        self.assertEqual(data["geometry"]["radius_squared"], "9/16")
        self.assertEqual(data["geometry"]["strict_margin_squared"], "1/100")
        self.assertEqual(data["dependency_effect"]["LOW_HEIGHT_MULTIPLICITY_COUNT"]["epistemic_status"], "PROVED")
        self.assertEqual(data["dependency_effect"]["FOURTH_MOMENT_H"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
