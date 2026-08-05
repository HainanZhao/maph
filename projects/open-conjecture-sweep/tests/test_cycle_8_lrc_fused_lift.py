"""Regression test for the sealed Cycle-8 fused lift result."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_8_lrc_fused_lift as builder


class Cycle8FusedLiftTest(unittest.TestCase):
    def test_controls_and_capped_sample(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-8-b008-lrc-fused-lift-v1")
        self.assertEqual(payload["proved_controls"]["p47_f1_survivors"], 0)
        self.assertEqual(payload["p199_performance"]["v1"]["status_counts"], {"CAP": 100})
        self.assertEqual(payload["p199_performance"]["v2"]["status_counts"], {"CAP": 100})
        self.assertEqual(payload["p199_performance"]["v2"]["node_counter_per_row"], 1_000_001)


if __name__ == "__main__":
    unittest.main()
