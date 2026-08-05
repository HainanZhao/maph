from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_31_convolution_quotient as check


class Cycle31ConvolutionQuotientTest(unittest.TestCase):
    def test_exact_split(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["convolution_quotient"])
        self.assertEqual(result["first_splitting_pair_profile"], 198)


if __name__ == "__main__":
    unittest.main()
