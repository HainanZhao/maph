"""Regression tests for the sealed Cycle-2 orbit-quotient boundary."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

import build_cycle_2_lrc_orbit_quotient as builder


class Cycle2ArtifactTest(unittest.TestCase):
    def test_payload_boundary_and_metrics(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["epistemic_status"], "OBSERVED")
        self.assertEqual(payload["frontier_gate"]["nodes"], 586_985_073)
        self.assertEqual(payload["frontier_gate"]["leaves"], 0)
        self.assertEqual(payload["frontier_gate"]["assigned_tasks"], 3)
        self.assertEqual(payload["baseline_validation"]["counts"], {"k6_p47": 53, "k7_p47": 50})


if __name__ == "__main__":
    unittest.main()
