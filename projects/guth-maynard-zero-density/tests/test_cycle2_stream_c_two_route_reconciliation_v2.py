"""Regression tests for hostile timing-free Stream-C reconciliation v2."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "reconcile_cycle2_stream_c_two_routes_v2.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-two-route-reconciliation-v2.json"


class StreamCTwoRouteReconciliationV2Tests(unittest.TestCase):
    def test_deterministic_replay(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "--check"], check=True, capture_output=True, text=True)
        self.assertIn('"verified": true', result.stdout)

    def test_every_declared_label_is_exactly_reconciled(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        labels = {row["label"] for row in data["preregistered_label_coverage"]}
        required = {
            "formula theorem", "formula range", "formula remainder", "formula endpoints/half-weight", "formula multiplicity", "formula height bridge",
            "Huxley theorem", "Huxley range/log loss", "VK high-height", "VK local completion", "VK cutoff weakening", "local-pair count",
            "uniform theta", "uniform truncation", "uniform epsilon", "uniform range", "uniform error", "uniform prime conversion",
            "almost-all theta", "almost-all truncation", "almost-all epsilon", "almost-all range", "almost-all local-pair reduction", "almost-all error", "almost-all exceptional conversion", "almost-all prime conversion",
        }
        self.assertEqual(labels, required)
        self.assertTrue(all(row["agreement"] == "EXACT" for row in data["preregistered_label_coverage"]))
        passed = data["independent_narrow_stream_c_pass"]
        self.assertEqual((passed["status"], passed["result"], passed["gaps"]), ("PROVED", "PASS", []))
        self.assertIn("no G0 PASS", passed["not_promoted"])

    def test_source_hashes_and_timing_containment(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertTrue(all(row["equal"] for row in data["source_hash_agreement"].values()))
        self.assertEqual(data["independent_sword_audit"]["status"], "OBSERVED")
        legacy = data["timing_free_legacy_identities"]
        self.assertIn("semantic", json.dumps(legacy))
        self.assertNotIn("wall_time_ns", json.dumps(data))
        self.assertNotIn("cycle-2-stream-c-route-a-v1.json", json.dumps(data))


if __name__ == "__main__":
    unittest.main()
