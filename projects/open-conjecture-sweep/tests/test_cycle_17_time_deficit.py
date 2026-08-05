"""Regression test for Cycle 17 exact weighted deficit certificates."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_17_time_deficit import audit


class Cycle17TimeDeficitTest(unittest.TestCase):
    def test_exact_certificate_counts(self) -> None:
        result = audit()
        self.assertEqual(result["lp_certified"], 397)
        self.assertEqual(result["post_lp_base4_uncovered"], 40)
        self.assertEqual(result["post_lp_base3_uncovered"], 40)


if __name__ == "__main__":
    unittest.main()
