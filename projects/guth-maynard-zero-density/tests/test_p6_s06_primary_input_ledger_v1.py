from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-s06-primary-input-ledger-v1.json"
SCRIPT = ROOT / "proof/build_p6_s06_primary_input_ledger_v1.py"


class P6S06PrimaryInputLedgerV1Tests(unittest.TestCase):
    def test_ledger_scope_and_replay(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        inputs = data["input_ledger"]
        self.assertEqual(inputs["L_POLY_A"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(inputs["FOURTH_MOMENT_H"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(inputs["LOCAL_MULTIPLICITY_COUNT_LC"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(inputs["LOW_HEIGHT_MULTIPLICITY_COUNT"]["epistemic_status"], "PROVED")
        self.assertEqual(inputs["LOW_HEIGHT_MULTIPLICITY_COUNT"]["conditional_on"], ["LOCAL_MULTIPLICITY_COUNT_LC"])
        self.assertEqual(data["q1_sensitive_overlap"]["status"], "RETAINED_UNREPAIRED")
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
