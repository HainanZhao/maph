from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_32_gf2_tensor as check


class Cycle32GF2TensorTest(unittest.TestCase):
    def test_exact_boundary(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["h11_certificate_weight"], 1)
        self.assertFalse(result["p199_degree_zero_identity"])


if __name__ == "__main__":
    unittest.main()
