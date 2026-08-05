from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_37_degree_two as check


class Cycle37DegreeTwoTest(unittest.TestCase):
    def test_exact_degree_two_functional(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["all_generator_contractions_zero"])
        self.assertEqual(result["degree_two_generators"], 16170400)
        self.assertEqual(result["independent_full_raw_replay"], "PASS")


if __name__ == "__main__":
    unittest.main()
