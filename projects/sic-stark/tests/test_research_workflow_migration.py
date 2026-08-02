"""Regression coverage for the Cycle-162 workflow and strategic attachment."""
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


VERIFY = load_module(
    "cycle162_verify", ROOT / "proof" / "verify_cycle_162_workflow_migration.py"
)


class ResearchWorkflowMigrationTests(unittest.TestCase):
    def test_legacy_inventory_and_accelerated_gate(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(
            result["status"], "ACCELERATED_WORKFLOW_ATTACHMENT_VERIFIED"
        )
        self.assertEqual(result["q4_campaign_cap"], 100)
        self.assertEqual(result["phase0_order"], "interface_then_fusion_continuity")
        self.assertEqual(len(result["legacy_noncycle_artifacts"]), 4)
        self.assertEqual(
            result["effective_stark_dependency"]["results_doi"],
            "10.5281/zenodo.21713178",
        )
        self.assertEqual(
            result["effective_stark_dependency"]["shared_object"], "RQ-000692"
        )

    def test_preregistration_is_a_single_embedded_manifest(self) -> None:
        preregistration = (
            ROOT / "docs/cycle-162-workflow-migration-preregistration-v1.md"
        ).read_text()
        self.assertEqual(preregistration.count("research-freeze-v1"), 1)

    def test_sealed_record_excludes_mutable_workflow_state(self) -> None:
        record = json.loads(
            (ROOT / "artifacts/cycle-162-workflow-migration-v1.json").read_text()
        )
        frozen_paths = {
            row["path"] for row in record["frozen_hashes"].values()
        }
        self.assertTrue(
            set(record["workflow_result"]["mutable_workflow_paths_excluded"])
            .isdisjoint(frozen_paths)
        )
        self.assertIn("no mathematical theorem", record["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
