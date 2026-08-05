from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_23_adaptive_width_four as check


class Cycle23AdaptiveWidthFourTest(unittest.TestCase):
    def test_audit(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
