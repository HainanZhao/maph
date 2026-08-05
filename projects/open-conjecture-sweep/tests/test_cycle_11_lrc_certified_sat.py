"""Regression test for the sealed Cycle-11 certified finite exclusion."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_11_lrc_certified_sat as builder


class Cycle11CertifiedSatTest(unittest.TestCase):
    def test_certified_sample_boundary(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-11-b011-lrc-certified-sat-v1")
        self.assertEqual(payload["proved_controls"]["certified_unsat"], 293)
        self.assertEqual(payload["p199_finite_result"]["certified_unsat"], 100)
        self.assertEqual(len(payload["certificate_manifest"]), 393)
        self.assertEqual(payload["independent_replay"]["proofs_checked"], 393)


if __name__ == "__main__":
    unittest.main()
