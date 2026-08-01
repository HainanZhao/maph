from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/adjudicate_g1_route_selection_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-3-g1-route-decision-v1.json"


class G1RouteSelectionV1Tests(unittest.TestCase):
    def test_sealed_decision_and_rejected_routes(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["decision"], "NO_SELECTION")
        self.assertEqual(data["gate_status"], "G1_CLOSED_NO_SELECTION")
        self.assertEqual(data["evidence_summary"]["retained_rows"], 0)
        self.assertEqual(data["evidence_summary"]["validation_rows"], 0)
        self.assertTrue(all(not row["selected"] for row in data["routes"].values()))

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)

    def test_optimized_mode_fails_closed(self) -> None:
        result = subprocess.run([sys.executable, "-O", str(SCRIPT), "--check", str(ARTIFACT)], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-optimized CPython 3.12.3", result.stderr)


if __name__ == "__main__":
    unittest.main()
