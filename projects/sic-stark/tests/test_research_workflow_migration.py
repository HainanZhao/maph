"""Regression coverage for the current SIC--Stark record workflow."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


VERIFY = load_module("cycle162_verify", ROOT / "proof" / "verify_cycle_162_workflow_migration.py")


class ResearchWorkflowMigrationTests(unittest.TestCase):
    def test_legacy_inventory_and_gate(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "WORKFLOW_MIGRATION_VERIFIED")
        self.assertEqual(len(result["legacy_noncycle_artifacts"]), 4)

    def test_preregistration_is_a_single_embedded_manifest(self) -> None:
        preregistration = (ROOT / "docs" / "cycle-162-workflow-migration-preregistration-v1.md").read_text()
        self.assertEqual(preregistration.count("research-freeze-v1"), 1)

    def test_sealed_record_has_no_mathematical_promotion(self) -> None:
        record = json.loads((ROOT / "artifacts" / "cycle-162-workflow-migration-v1.json").read_text())
        self.assertEqual(record["epistemic_status"], "PROVED")
        self.assertEqual(record["status"], "SEALED_WORKFLOW_MIGRATION_AND_INTERFACE_GATE")
        self.assertIn("no mathematical theorem", record["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
