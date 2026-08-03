from __future__ import annotations
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"proof"))
from verify_cycle_229_f3_square_divisor import audit  # noqa: E402
class DivisorTests(unittest.TestCase):
 def test_order_four_poles(self):
  r=audit(); self.assertEqual({x["pole_order_at_mu_zero"] for x in r["blocks"].values()},{4}); self.assertTrue(all(x["mu_zero_pole"] and not x["mu_zero_zero"] for x in r["rows"]))
if __name__=="__main__": unittest.main()
