from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_25_quadratic_crt as check


class Cycle25QuadraticCRTTest(unittest.TestCase):
    def test_audit(self):
        self.assertEqual(check.audit()["status"], "PASS")
