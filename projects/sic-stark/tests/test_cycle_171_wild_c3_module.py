from __future__ import annotations
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"proof"))
from verify_cycle_171_wild_c3_module import build_payload  # noqa: E402
class WildC3ModuleTests(unittest.TestCase):
 def test_exact_obstruction(self):
  s=build_payload()["summary"];self.assertEqual((s["states"],s["module_dimension"],s["equations"],s["rank"]),(36,2,5340,72));self.assertTrue(s["inconsistent"]);self.assertFalse(s["wild_module_lift_exists"])
 def test_deterministic(self):self.assertEqual(json.loads((ROOT/"discovery/cycle-171-wild-c3-module-prototype-v1.json").read_text()),build_payload())
