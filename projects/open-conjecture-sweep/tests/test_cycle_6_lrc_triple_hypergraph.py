"""Regression test for the Cycle-6 triple-hypergraph discovery result."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import build_cycle_6_lrc_triple_hypergraph as builder


class Cycle6TripleHypergraphTest(unittest.TestCase):
    def test_scope_and_sample(self) -> None:
        payload = builder.payload()
        self.assertEqual(payload["artifact_id"], "cycle-6-b006-lrc-triple-hypergraph-v1")
        self.assertEqual(payload["global_relation"]["forbidden_triples"], 124_674)
        self.assertEqual(payload["sample_direct_feasibility"]["rejected_states"], 85_594)
        self.assertEqual(payload["sample_direct_feasibility"]["retained_states"], 14_406)
        self.assertEqual(payload["cycle_decision"]["outcome"], "SEALED_FOR_DISTINCT_DIRECT_ENGINE")


if __name__ == "__main__":
    unittest.main()
