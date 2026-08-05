import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_51_conjugacy_averaging import audit


class Cycle51ConjugacyAveragingTest(unittest.TestCase):
    def test_frozen_exact_corpus_and_replay(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["rows"], 840)
        self.assertEqual(result["negative_rows"], 0)
        self.assertLess(result["normalized_left_assignments"], 100_000_000)


if __name__ == "__main__":
    unittest.main()
