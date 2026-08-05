"""Regression test for the corrected Cycle-4 combined-tranche boundary."""

from __future__ import annotations
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_4_lrc_partitioned_v2 as builder


class Cycle4CorrectionTest(unittest.TestCase):
    def test_corrected_boundary(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-4-b004-lrc-partitioned-v2")
        self.assertEqual(payload["frontier_gate"]["outcome"], "FAILED_EDGE_CAP")
        self.assertEqual(payload["frontier_gate"]["completed_depth"], 9)
        self.assertEqual(payload["frontier_gate"]["depth_9_states"], 354_931_861)
        self.assertEqual(payload["frontier_gate"]["generated_edges"], 5_869_850_727)


if __name__ == "__main__":
    unittest.main()
