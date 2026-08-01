"""Regression tests for Stream-B independent-route reconciliation v2."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/reconcile_cycle2_stream_b_routes_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-2-stream-b-route-reconciliation-v2.json"


class StreamBReconciliationV2Tests(unittest.TestCase):
    def replay(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True, text=True, cwd=PROJECT)

    def test_artifact_is_byte_stable(self):
        self.replay("--check", str(ARTIFACT))

    def test_all_v1_coverage_gaps_are_resolved_before_pass(self):
        data = json.loads(self.replay().stdout)
        resolved = {row["id"]: row for row in data["resolved_prior_gaps"]}
        for identifier in ("M2-route-a-theorem-1-1-coverage", "M3-route-a-mvt-residual-coverage", "M4-route-a-reassembly-coverage"):
            self.assertEqual(resolved[identifier]["epistemic_status"], "PROVED")
            self.assertEqual(resolved[identifier]["workflow_status"], "RESOLVED")
        self.assertEqual(data["agreement_summary"]["coverage_gaps_open"], 0)
        self.assertTrue(data["agreement_summary"]["independent_route_pass_permitted"])

    def test_scope_and_containment_tags(self):
        data = json.loads(self.replay().stdout)
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertIn("INDEPENDENT_ROUTE_NARROW_PASS", data["canonical_status"])
        self.assertIn("G0 remains OBSERVED", data["canonical_status"])
        contained = {row["id"]: row for row in data["resolved_prior_gaps"]}["M1-route-a-pass-scope"]
        self.assertEqual(contained["epistemic_status"], "OBSERVED")
        self.assertEqual(contained["containment_status"], "CONTAINED")


if __name__ == "__main__":
    unittest.main()
