"""Regression test for the sealed Cycle-9 weighted-dual no-go."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_9_lrc_weighted_dual as builder


class Cycle9WeightedDualTest(unittest.TestCase):
    def test_h11_structural_no_go(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-9-b009-lrc-weighted-dual-v1")
        self.assertEqual(payload["exact_falsifier"]["l1_improper_bases"], 240)
        self.assertEqual(payload["exact_falsifier"]["mask_cover_falsifiers"], 240)
        self.assertEqual(payload["exact_falsifier"]["dual_certificates_possible"], 0)


if __name__ == "__main__":
    unittest.main()
