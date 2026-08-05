"""Regression test for Cycle 22's direct-CNF width-four replay."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_22_width_four import audit


class Cycle22WidthFourTest(unittest.TestCase):
    def test_exact_leaf(self) -> None:
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["certified_leaves"][0]["margin"], 88)
        self.assertEqual(result["remaining_leaves"], 60)


if __name__ == "__main__":
    unittest.main()
