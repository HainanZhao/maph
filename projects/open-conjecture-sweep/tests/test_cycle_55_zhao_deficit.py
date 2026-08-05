from __future__ import annotations
import unittest
from proof.check_cycle_55_zhao_deficit import audit
class C55(unittest.TestCase):
 def test_packet(self):self.assertEqual(audit()["negative_rays"],0)
if __name__=="__main__":unittest.main()
