from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_28_portfolio_cyclic_width_five as check


class Cycle28PortfolioCyclicWidthFiveTest(unittest.TestCase):
    def test_audit(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["certified_leaves"], [])


if __name__ == "__main__":
    unittest.main()
