import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_47_affine_descent import audit


class Cycle47AffineDescentTest(unittest.TestCase):
    def test_complete_serialized_section(self):
        checked = audit()
        self.assertEqual(checked["status"], "PASS")
        self.assertEqual(checked["selected_quadruples"], 256)
        self.assertGreater(checked["incidence_cycle_rank"], 0)
        self.assertEqual(set(checked["fill_routes"]), {"EXPLICIT_CONE", "LOCAL_INCIDENCE", "FULL_EXACT"})

    def test_negative_descent_control(self):
        controls = json.loads((ROOT / "discovery/out/cycle47-affine-descent/generic-controls.json").read_text())
        loop = controls["inconsistent_three_stalk_loop"]
        self.assertEqual(loop["local_stalks_nonempty"], 3)
        self.assertEqual(loop["primitive_dual"], [1, 1, 1])
        self.assertEqual(loop["pairing"], 1)
        self.assertTrue(controls["orientation_reversal_rejected"])

    def test_raw_compressed_rank_control(self):
        replay = json.loads((ROOT / "discovery/out/cycle47-affine-descent/independent-replay.json").read_text())
        rank = replay["descent_rank_control"]
        self.assertEqual(rank["raw_face_variables"] - rank["compressed_face_variables"], rank["gluing_rank"])
        self.assertTrue(rank["raw_and_compressed_section_verified"])


if __name__ == "__main__":
    unittest.main()
