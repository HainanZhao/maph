"""Regression test for Cycle 20's exact CRT interface."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_20_crt_diagonal import audit


class Cycle20CrtDiagonalTest(unittest.TestCase):
    def test_complete_controls(self) -> None:
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["claim_tag"], "PROVED")
        self.assertEqual(result["total_comparisons"], 7_871_973)
        self.assertTrue(all(row["mismatches"] == 0 for row in result["domains"]))


if __name__ == "__main__":
    unittest.main()
