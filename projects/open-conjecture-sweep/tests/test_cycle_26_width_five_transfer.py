from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_26_width_five_transfer as check


class Cycle26WidthFiveTransferTest(unittest.TestCase):
    def test_audit(self):
        self.assertEqual(check.audit()["status"], "PASS")
