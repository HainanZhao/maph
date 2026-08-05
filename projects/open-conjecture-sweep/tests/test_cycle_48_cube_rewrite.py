import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_48_cube_rewrite import audit


class Cycle48CubeRewriteTest(unittest.TestCase):
    def test_complete_serialized_classification(self):
        checked = audit()
        self.assertEqual(checked["status"], "PASS")
        self.assertEqual(checked["faces"], 512)
        self.assertEqual(checked["repair_status_counts"], {"STRONG_REPAIR": 12, "TARGETED_REPAIR": 500})
        self.assertEqual(checked["confluence_status_counts"], {
            "NONCONFLUENT": 314,
            "NO_NONJOINABLE_REACHED_DIAMOND": 198,
        })

    def test_generic_negative_controls(self):
        controls = json.loads((ROOT / "discovery/out/cycle48-cube-rewrite/generic-controls.json").read_text())
        self.assertEqual(controls["status"], "PASS")
        self.assertEqual(controls["cube_kernel_checks"], 729)
        self.assertEqual(controls["unrepaired_structural_zero"]["status"], "UNREPAIRED")
        self.assertEqual(controls["literal_nonjoinable_diamond"]["status"], "NONJOINABLE")
        self.assertTrue(controls["nonkernel_move_rejected"])

    def test_aggregate_caps_and_outcomes(self):
        actual = json.loads((ROOT / "discovery/out/cycle48-cube-rewrite/actual.json").read_text())
        self.assertEqual(actual["mobius_defect_faces"], 314)
        self.assertEqual(actual["aggregate_forbidden_cells"], 136442)
        self.assertEqual(actual["aggregate_cube_candidates"], 88110100)
        self.assertEqual(actual["aggregate_repair_steps"], 2177)
        self.assertEqual(actual["aggregate_critical_diamonds"], 5830)


if __name__ == "__main__":
    unittest.main()
