from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-s06-primary-input-ledger-v4-fourth-moment-correction.json"
SCRIPT = ROOT / "proof/build_p6_s06_primary_input_ledger_v4_fourth_moment_correction.py"


class P6S06PrimaryInputLedgerV4FourthMomentCorrectionTests(unittest.TestCase):
    def test_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        corrected = data["corrected_input"]
        self.assertEqual(corrected["id"], "FOURTH_MOMENT_H")
        self.assertEqual(corrected["epistemic_status"], "PROVED")
        self.assertIn("primitive", corrected["precise_scope"])
        self.assertIn("q=1", corrected["compact_and_endpoint_handling"])
        self.assertEqual(data["source"]["submitted_chourasiya_simonic"]["epistemic_status"], "OBSERVED")
        self.assertEqual(data["dependency_effect"]["FOURTH_MOMENT_H_for_primitive_detector"]["epistemic_status"], "PROVED")
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
