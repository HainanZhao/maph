"""Regression test for the Cycle-7 direct-feasibility performance gate."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_7_lrc_direct_feasibility as builder


class Cycle7DirectFeasibilityTest(unittest.TestCase):
    def test_performance_gate(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-7-b007-lrc-direct-feasibility-v1")
        self.assertEqual(payload["controls"]["k6_tuples"], 53)
        self.assertEqual(payload["controls"]["k7_tuples"], 50)
        self.assertGreater(payload["performance_gate"]["p99_nanoseconds_replay"], 100_000)
        self.assertEqual(payload["performance_gate"]["outcome"], "FAILED")


if __name__ == "__main__":
    unittest.main()
