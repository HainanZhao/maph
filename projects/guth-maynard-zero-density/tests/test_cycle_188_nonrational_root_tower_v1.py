import unittest
from conventions.nonrational_root_tower_v1 import light_tower_bound,verify_all
class Cycle188RootTowerTest(unittest.TestCase):
 def test_light_tower_subcritical(self):
  r=light_tower_bound(T=3,a=10); self.assertLess(r["mass"]["ordered_cross_mass"],r["parameters"]["critical_target"]); self.assertEqual(r["fibres"]["N3"],1)
 def test_boundary(self): self.assertIn("No arbitrary",verify_all()["boundary"])
if __name__=="__main__": unittest.main()
