from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_33_odd_tensor as check


class Cycle33OddTensorTest(unittest.TestCase):
    def test_exact_field_boundaries(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["contradiction_sizes"], {"GF3": 802, "GF5": 985})
        self.assertEqual(result["degree_zero_identities"], {"GF3": False, "GF5": False})


if __name__ == "__main__":
    unittest.main()
