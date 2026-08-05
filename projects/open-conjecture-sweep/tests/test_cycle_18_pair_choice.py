"""Regression test for Cycle 18 pair-choice certificates."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_18_pair_choice import audit


class Cycle18PairChoiceTest(unittest.TestCase):
    def test_exact_outcome(self) -> None:
        self.assertEqual(audit(), {"rows": 80, "base4_certified": 0, "base3_certified": 4, "unresolved": 76})


if __name__ == "__main__":
    unittest.main()
