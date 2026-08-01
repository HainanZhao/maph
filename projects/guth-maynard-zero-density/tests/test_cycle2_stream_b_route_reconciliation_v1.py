"""Regression tests for hostile Stream-B Route A/Route B reconciliation."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "reconcile_cycle2_stream_b_routes_v1.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-b-route-reconciliation-v1.json"


class StreamBReconciliationTests(unittest.TestCase):
    def replay(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True, text=True)

    def test_certificate_is_byte_stable(self) -> None:
        self.replay("--check", str(ARTIFACT))

    def test_mapping_covers_every_requested_comparison_node(self) -> None:
        data = json.loads(self.replay().stdout)
        table = {row["id"]: row for row in data["canonical_mapping_table"]}
        self.assertEqual(len(table), 16)
        for identifier in ("R3-detector-and-complement", "R4-multiplicity-local-count", "R6-smoothing-and-extraction", "R8-both-k-regimes", "R10-theorem-1-1-three-terms", "R11-montgomery-theorem-and-polarity", "R13-mvt-strict-residual", "R15-final-dyadic-reassembly"):
            self.assertIn(identifier, table)
        self.assertEqual(table["R10-theorem-1-1-three-terms"]["status"], "ROUTE_A_COVERAGE_GAP")

    def test_open_mismatches_are_retained_not_silently_promoted(self) -> None:
        data = json.loads(self.replay().stdout)
        issues = {row["id"]: row for row in data["mismatch_and_falsifier_rows"]}
        self.assertEqual(issues["M2-route-a-theorem-1-1-coverage"]["status"], "OPEN")
        self.assertEqual(issues["M3-route-a-mvt-residual-coverage"]["status"], "OPEN")
        self.assertEqual(issues["M4-route-a-reassembly-coverage"]["status"], "OPEN")
        self.assertEqual(data["agreement_summary"]["formula_contradictions"], 0)

    def test_pass_scope_is_contained(self) -> None:
        data = json.loads(self.replay().stdout)
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertIn("G0 remains OBSERVED", data["canonical_status"])
        table = {row["id"]: row for row in data["canonical_mapping_table"]}
        self.assertEqual(table["R16-pass-label-scope"]["status"], "LABEL_SCOPE_MISMATCH")

    def test_preregistered_tar_and_all_shared_sources_are_hashed(self) -> None:
        data = json.loads(self.replay().stdout)
        hashes = data["frozen_source_hashes"]
        self.assertEqual(hashes["gm_tar"], "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc")
        self.assertEqual(hashes["gm_tex"], "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428")
        self.assertEqual(hashes["montgomery_pdf"], "b240c7c07d32201ced906bd0fdc4d36cca3c11999084afeb658ffca3f978534e")

    def test_route_a_uses_canonical_identity_not_mutable_timing_bytes(self) -> None:
        data = json.loads(self.replay().stdout)
        defect = data["historical_reproducibility_defect"]
        self.assertEqual(defect["status"], "OBSERVED")
        self.assertIn("wall_time_ns", defect["cause"])
        self.assertIn("canonical audit hash", defect["containment"])
        self.assertIn("route_a_v2_artifact", data["input_byte_hashes_at_seal"])


if __name__ == "__main__":
    unittest.main()
