from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_34_rational_tensor as check


class Cycle34RationalTensorTest(unittest.TestCase):
    def test_exact_rational_obstruction(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["integer_left_null"])
        self.assertFalse(result["rational_degree_zero_identity"])
        self.assertEqual(result["independent_direct_set_replay"], "PASS")


if __name__ == "__main__":
    unittest.main()
