from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-multiplicity-transfer-v1.json"
SCRIPT = ROOT / "proof/p6_multiplicity_transfer_v1.py"


class P6MultiplicityTransferV1Tests(unittest.TestCase):
    def test_claim_boundary(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["external_unproved_input"]["epistemic_status"], "CONJECTURED")
        self.assertIn("no density theorem", data["gate_effect"])
        self.assertTrue(data["source"]["anchors_only"])

    def test_exact_examples(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        for row in data["finite_exact_examples"]:
            self.assertLessEqual(row["multiplicity_weighted"], row["upper_bound"])

    def test_replay_and_script_hash(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
