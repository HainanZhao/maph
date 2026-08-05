"""Regression tests for the sealed Cycle-3 coverage-level boundary."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

import build_cycle_3_lrc_coverage_levels as builder


class Cycle3ArtifactTest(unittest.TestCase):
    def test_payload_boundary_and_metrics(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["epistemic_status"], "OBSERVED")
        self.assertEqual(payload["frontier_gate"]["outcome"], "FAILED_MEMORY_CAP")
        self.assertEqual(payload["frontier_gate"]["last_completed_depth"], 7)
        self.assertEqual(payload["frontier_gate"]["depth_7_states"], 2_982_862)
        self.assertEqual(payload["baseline_validation"]["counts"], {"k6_p47": 53, "k7_p47": 50})


if __name__ == "__main__":
    unittest.main()
