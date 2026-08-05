from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_36_degree_one as check


class Cycle36DegreeOneTest(unittest.TestCase):
    def test_exact_degree_one_functional(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["all_generator_contractions_zero"])
        self.assertEqual(result["degree_one_generators"], 221646)
        self.assertEqual(result["independent_direct_set_replay"], "PASS")


if __name__ == "__main__":
    unittest.main()
