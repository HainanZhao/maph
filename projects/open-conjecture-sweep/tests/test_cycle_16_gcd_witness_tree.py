"""Regression test for Cycle 16's exact tree and transfer census."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_16_gcd_witness_tree import audit


class Cycle16GcdWitnessTreeTest(unittest.TestCase):
    def test_structural_outcome(self) -> None:
        result = audit(False)
        self.assertEqual(result["leaves"], 6084)
        self.assertEqual(result["selected_clauses"], 27)
        self.assertEqual(result["census_matches"], 34398)
        self.assertEqual(result["complete_bases"], 0)


if __name__ == "__main__":
    unittest.main()
