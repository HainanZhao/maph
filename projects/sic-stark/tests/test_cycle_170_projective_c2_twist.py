from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"proof"))
from verify_cycle_170_projective_c2_twist import build_payload  # noqa: E402
class ProjectiveC2TwistTests(unittest.TestCase):
 def test_scalar_twist_barrier(self):
  s=build_payload()["summary"];self.assertEqual((s["normalized_2cochains_checked"],s["normalized_cocycle_count"],s["normalized_coboundary_count"]),(16,4,4));self.assertEqual(s["nontrivial_extension_class_count"],0);self.assertEqual(s["nontrivial_character_count"],0)
 def test_deterministic(self): self.assertEqual(json.loads((ROOT/"discovery/cycle-170-projective-c2-twist-prototype-v1.json").read_text()),build_payload())
