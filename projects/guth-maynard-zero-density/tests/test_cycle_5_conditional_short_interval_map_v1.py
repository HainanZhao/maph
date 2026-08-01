from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/build_cycle_5_conditional_short_interval_map_v1.py"
ARTIFACT = ROOT / "artifacts/cycle-5-conditional-density-to-short-interval-map-v1.json"


class ConditionalShortIntervalMapV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_claim_is_conditional_and_not_a_new_theorem(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "PROVED")
        boundary = self.data["claim_boundary"]
        self.assertIn("conditional", boundary.lower())
        self.assertIn("No density gain", boundary)

    def test_symbolic_formulas_and_positive_samples(self) -> None:
        self.assertEqual(self.data["symbolic_identities"]["uniform_theta"], "(17-13*eta)/(30-13*eta)")
        self.assertEqual(self.data["symbolic_identities"]["almost_all_theta"], "(4-13*eta)/(30-13*eta)")
        self.assertEqual(len(self.data["exact_rows"]), 4)
        for row in self.data["exact_rows"]:
            self.assertNotEqual(row["uniform_improvement"], "0")
            self.assertNotEqual(row["almost_all_improvement"], "0")

    def test_frozen_g0_inputs_and_sealer(self) -> None:
        self.assertEqual(self.data["frozen_hashes"]["cycle-2-stream-c-two-route-reconciliation-v2.json"]["sha256"], "b69e0caeb5d5ed5c8072acb62263d15c2b02470df0c10889287508837c9e706d")
        self.assertEqual(self.data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())

    def test_replay_and_no_asserts(self) -> None:
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
