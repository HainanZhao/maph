"""Regression test for the Cycle-5 pairwise-packing no-go."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_5_lrc_packing_cut as builder


class Cycle5PackingCutTest(unittest.TestCase):
    def test_structural_no_go_and_frontier(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-5-b005-lrc-packing-cut-v1")
        self.assertEqual(payload["structural_no_go"]["difference_set_size"], 99)
        self.assertEqual(payload["structural_no_go"]["incompatibility_edge_count"], 0)
        self.assertEqual(payload["frontier_gate"]["packing_prunes"], 0)
        self.assertEqual(payload["frontier_gate"]["depth_9_states"], 354_931_861)
        self.assertEqual(payload["frontier_gate"]["outcome"], "FAILED_NO_REDUCTION_AND_EDGE_CAP")


if __name__ == "__main__":
    unittest.main()
