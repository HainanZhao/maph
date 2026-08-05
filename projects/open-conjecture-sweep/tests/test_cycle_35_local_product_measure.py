from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_35_local_product_measure as check


class Cycle35LocalProductMeasureTest(unittest.TestCase):
    def test_exact_product_measure(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["all_predicates_annihilated"])
        self.assertEqual(result["global_mass"], 1)
        self.assertEqual(result["independent_direct_mask_replay"], "PASS")


if __name__ == "__main__":
    unittest.main()
