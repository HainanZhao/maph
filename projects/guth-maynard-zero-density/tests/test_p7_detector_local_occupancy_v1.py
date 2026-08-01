from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-detector-local-occupancy-v1.json"
BUILDER = ROOT / "proof/build_p7_detector_local_occupancy_v1.py"


class P7DetectorLocalOccupancyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_all_pins(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for row in self.data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        for row in self.data["source_integrity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_local_zero_geometry_and_exact_conductor_scope(self) -> None:
        local = self.data["individual_local_zero_count"]
        self.assertEqual(local["status"], "PROVED")
        geometry = local["finite_exact_geometry_check"]
        self.assertEqual(geometry["maximum_distance_squared"], "221/400")
        self.assertEqual(geometry["circle_radius_squared"], "9/16")
        self.assertEqual(geometry["strict_margin"], "1/100")
        self.assertIn("exact primitive conductor", self.data["exact_conductor_and_extension"]["selected_rows"])
        self.assertIn("zero extension", self.data["exact_conductor_and_extension"]["zero_extension"])

    def test_sharp_cross_character_obstruction(self) -> None:
        obstruction = self.data["sharp_detector_geometry_obstruction"]
        self.assertEqual(obstruction["status"], "PROVED")
        check = obstruction["finite_exact_check"]
        self.assertEqual(check["per_colour_unit_window_count"], 1)
        self.assertEqual(check["uncoloured_local_occupancy_M_Delta"], 3)
        self.assertEqual(check["time_projection_size_m"], 12)
        self.assertEqual(check["local_difference_multiplicity_D_Delta"], 36)
        self.assertEqual(check["sharp_upper_bound_m_times_M"], 36)
        self.assertIn("COMBINATORIAL_ONLY", check["model_status"])

    def test_joint_sampling_is_conditional_and_targeted(self) -> None:
        joint = self.data["conditional_common_detector_sampling"]
        self.assertEqual(joint["status"], "PROVED")
        self.assertEqual(joint["finite_exact_bookkeeping_check"]["deduced_selected_time_count"], 3)
        self.assertIn("one common", joint["hypotheses"][1])
        self.assertIn("D_target/m", joint["exact_required_detector_strength"])
        self.assertIn("no source-checked detector", joint["current_status"])
        occupancy = self.data["weakest_cross_character_occupancy_input"]
        self.assertIn("OCC_Delta(D_target/m)", occupancy["target_form"])
        self.assertIn("D_target<m", occupancy["target_form"])

    def test_gate_remains_open_and_replay_is_exact(self) -> None:
        self.assertEqual(self.data["gate_outcome"], "CONTAINED_DETECTOR_SIDE_OCCUPANCY_OBSTRUCTION_GATE_REMAINS_OPEN")
        self.assertIn("remains open", self.data["gate_assessment"]["gate_effect"])
        tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
