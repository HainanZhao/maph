"""Regression test for the Cycle 15 LRAT slicing boundary."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_15_resolution_slicing import audit


class Cycle15ResolutionSlicingTest(unittest.TestCase):
    def test_exact_graph_and_models(self) -> None:
        self.assertEqual(audit(), {"empty_id": 722343, "reached_inputs": 2294, "root_children": 31, "dominator_candidates": 0, "sat_candidates": 6})


if __name__ == "__main__":
    unittest.main()
