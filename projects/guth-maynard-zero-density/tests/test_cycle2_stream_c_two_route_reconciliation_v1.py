"""Regression tests for hostile two-route Stream-C reconciliation."""
from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "reconcile_cycle2_stream_c_two_routes_v1.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-c-two-route-reconciliation-v1.json"


class StreamCTwoRouteReconciliationTests(unittest.TestCase):
    def historical_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)], check=False, capture_output=True, text=True)

    def test_timed_legacy_input_fails_closed_instead_of_rewriting_v1(self) -> None:
        result = self.historical_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("certificate mismatch", result.stderr)
        # v1 sealed a raw Route-A-v1 byte.  That artifact is intentionally
        # timing-mutable, so a successful v1 replay cannot be promoted to a
        # byte-stable certificate.  Do not invoke --write here.
        self.assertIn("wall_time_ns", (PROJECT / "artifacts/cycle-2-stream-c-route-a-v1.json").read_text())

    def test_historical_semantic_gap_content_is_preserved(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["exact_agreements"]["uniform_theta"], "17/30")
        self.assertEqual(data["exact_agreements"]["almost_all_theta"], "2/15")
        self.assertEqual(data["full_independent_route_pass"]["result"], "NOT PASS")
        self.assertEqual(data["full_independent_route_pass"]["open_coverage_labels"], [
            "formula theorem", "formula arbitrary-T range", "formula remainder",
            "formula endpoint/half-weight", "formula multiplicity", "formula |rho|-|gamma| bridge",
        ])
        self.assertIn("access-ledger v1", data["source_authority_correction"]["finding"])

    def test_recomputed_v1_semantics_still_exhibit_the_same_six_gaps(self) -> None:
        spec = importlib.util.spec_from_file_location("stream_c_reconciliation_v1", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        current = module.certificate()
        self.assertEqual(current["full_independent_route_pass"]["open_coverage_labels"], [
            "formula theorem", "formula arbitrary-T range", "formula remainder",
            "formula endpoint/half-weight", "formula multiplicity", "formula |rho|-|gamma| bridge",
        ])

    def test_v2_is_the_deterministic_replacement(self) -> None:
        successor = PROJECT / "proof/reconcile_cycle2_stream_c_two_routes_v2.py"
        result = subprocess.run([sys.executable, str(successor), "--check"], check=True, capture_output=True, text=True)
        self.assertIn('"verified": true', result.stdout)


if __name__ == "__main__":
    unittest.main()
