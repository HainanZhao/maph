from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_196_endpoint_contour_geometry.py"


class Cycle196EndpointContourGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True
        )
        cls.result = json.loads(completed.stdout)

    def test_attracting_path_has_a_uniform_central_gap(self) -> None:
        geometry = self.result["attracting_path_geometry"]
        self.assertEqual(geometry["Re_omega_1_lower_bound"], 55)
        self.assertEqual(geometry["Re_Q_lower_bound"], 56)
        self.assertEqual(geometry["Re_contour_lower_bound"], "28")

    def test_all_kernel_labels_have_zero_finite_crossings(self) -> None:
        cones = self.result["kernel_pole_cones"]
        self.assertEqual(len(cones["records"]), 24)
        self.assertTrue(cones["all_24_labels_pole_free_on_C_s"])
        self.assertEqual(cones["total_finite_kernel_crossings"], 0)

    def test_all_anti_residue_jumps_are_zero_but_infinity_remains_open(self) -> None:
        jumps = self.result["anti_residue_jumps"]
        self.assertEqual(jumps["finite_anti_residue_jump_vector"], [0] * 6)
        self.assertTrue(jumps["finite_anti_residues_preserved_under_contour_motion"])
        regular = self.result["regular_part_boundary"]
        self.assertEqual(regular["T_to_infinity_limit"], "OPEN")
        self.assertFalse(regular["endpoint_continuation_claimed"])


if __name__ == "__main__":
    unittest.main()
