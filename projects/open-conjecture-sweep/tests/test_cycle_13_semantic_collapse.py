"""Regression test for Cycle 13's exact semantic-family collapse."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_13_semantic_collapse import audit


class Cycle13SemanticCollapseTest(unittest.TestCase):
    def test_frozen_core_clause_partition(self) -> None:
        self.assertEqual(audit(), {
            "choice_at_most_one": 196,
            "color_invariant_coverage": 12,
            "x_implies_y2": 84,
            "y2_cardinality": 1,
        })


if __name__ == "__main__":
    unittest.main()
