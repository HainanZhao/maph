from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p6-conductor-q1-reset-v1.json"
SCRIPT = ROOT / "proof/p6_conductor_q1_reset_v1.py"


class P6ConductorQ1ResetV1Tests(unittest.TestCase):
    def test_claim_boundary_and_gate_effect(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["external_input"]["epistemic_status"], "CONJECTURED")
        self.assertIn("removed as an independent", data["gate_effect"])
        self.assertIn("S06 remain open", data["gate_effect"])

    def test_exact_exponent_domination(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(len(data["exact_exponent_rows"]), 4)
        for row in data["exact_exponent_rows"]:
            self.assertEqual(row["first_q_exponent"], row["uniform_qt_exponent"])

    def test_replay_and_hashes(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        for relative, expected in data["frozen_inputs"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
