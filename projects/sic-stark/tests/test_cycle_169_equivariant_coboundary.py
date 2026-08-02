from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_169_equivariant_coboundary import build_payload  # noqa: E402
class EquivariantCoboundaryTests(unittest.TestCase):
    def test_exact_obstruction(self):
        summary = build_payload()["summary"]
        self.assertEqual((summary["states"], summary["defect_equations"], summary["total_equations"]), (36, 1296, 1335))
        self.assertTrue(summary["f2_inconsistent"] and summary["f3_inconsistent"])
        self.assertFalse(summary["normalized_t_invariant_coboundary_exists"])
    def test_payload_is_deterministic(self):
        self.assertEqual(json.loads((ROOT / "discovery/cycle-169-equivariant-coboundary-prototype-v1.json").read_text()), build_payload())
