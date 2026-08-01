"""Regression tests for the authoritative G0 reconstruction decision."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
ARTIFACT = PROJECT / "artifacts/g0-full-reconstruction-v1.json"
SCRIPT = PROJECT / "proof/reconcile_g0_full_v1.py"


class G0FullReconstructionV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_authoritative_decision_and_claim_boundary(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "PROVED")
        self.assertEqual(self.data["decision"]["status"], "PASS")
        self.assertEqual(self.data["decision"]["open_blockers"], [])
        self.assertIn("not a new zero-density theorem", self.data["claim_boundary"])
        self.assertEqual(len(self.data["non_promotions"]), 5)

    def test_every_frozen_gate_and_dependency_node_is_closed(self) -> None:
        self.assertTrue(all(row["status"] == "PASS" for row in self.data["gate_rows"]))
        self.assertEqual(len(self.data["inherited_dependency_nodes"]), 15)
        self.assertTrue(all(row["status"] == "CLOSED" for row in self.data["inherited_dependency_nodes"].values()))
        self.assertEqual(self.data["counts"], {
            "cycle1_exact_labels": 24,
            "stream_b_reconciliation_rows": 7,
            "stream_c_reconciliation_labels": 26,
            "inherited_graph_nodes": 15,
            "selected_source_gates": 8,
            "source_manifest_items": 41,
            "resource_routes": 4,
        })

    def test_corrections_are_preserved_and_plan_is_not_frozen(self) -> None:
        self.assertEqual(len(self.data["corrections_preserved"]), 4)
        relatives = [value[0] for value in self.data["frozen_dependencies"].values() if isinstance(value, list)]
        self.assertNotIn("PLAN.md", relatives)
        self.assertNotIn("plan", self.data["frozen_dependencies"])

    def test_certificate_replays_byte_for_byte(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"], cwd=PROJECT,
            check=True, capture_output=True, text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["verified"])


if __name__ == "__main__":
    unittest.main()
