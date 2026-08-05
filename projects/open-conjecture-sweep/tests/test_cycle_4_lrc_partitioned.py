"""Regression test for the sealed Cycle-4 partition boundary."""

from __future__ import annotations
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_4_lrc_partitioned as builder


class Cycle4ArtifactTest(unittest.TestCase):
    def test_metrics(self) -> None:
        payload = builder.payload()
        gate = payload["frontier_gate"]
        self.assertEqual(gate["outcome"], "FAILED_LOGICAL_DISK_CAP")
        self.assertEqual(gate["peak_logical_disk_bytes"], 68_719_476_736)
        self.assertEqual(gate["expanded_states"], 319_603_355)
        self.assertEqual(payload["baseline_validation"]["counts"], {"k6_p47": 53, "k7_p47": 50})


if __name__ == "__main__":
    unittest.main()
