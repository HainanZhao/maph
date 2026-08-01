from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-s06-primary-input-ledger-v2-lpoly-correction.json"
SCRIPT = ROOT / "proof/build_p6_s06_primary_input_ledger_v2_lpoly_correction.py"


class P6S06PrimaryInputLedgerV2LPolyCorrectionTests(unittest.TestCase):
    def test_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        corrected = data["corrected_input"]
        self.assertEqual(corrected["id"], "L_POLY_A")
        self.assertEqual(corrected["epistemic_status"], "PROVED")
        self.assertIn("3/2", corrected["statement"])
        self.assertEqual(data["retained_inputs"]["FOURTH_MOMENT_H"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(data["retained_inputs"]["LOCAL_MULTIPLICITY_COUNT_LC"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
