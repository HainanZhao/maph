"""Regression test for the sealed Cycle-10 gcd-pattern performance gate."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_10_lrc_gcd_pattern as builder


class Cycle10GcdPatternTest(unittest.TestCase):
    def test_controls_and_p199_boundary(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-10-b010-lrc-gcd-pattern-v1")
        self.assertEqual(payload["proved_controls"]["p47_eliminated"], 53)
        self.assertEqual(payload["p199_performance"]["status_counts"], {"CAP": 100})
        self.assertEqual(payload["p199_performance"]["node_counter_total"], 200_000_100)
        self.assertEqual(payload["p199_performance"]["node_counter_per_row"], 2_000_001)


if __name__ == "__main__":
    unittest.main()
