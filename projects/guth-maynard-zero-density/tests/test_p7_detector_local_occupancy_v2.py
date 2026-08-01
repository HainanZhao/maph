from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-detector-local-occupancy-v2-correction.json"
BUILDER = ROOT / "proof/build_p7_detector_local_occupancy_v2.py"


class P7DetectorLocalOccupancyCorrectionTests(unittest.TestCase):
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

    def test_correction_is_narrow_and_v1_replays(self) -> None:
        correction = self.data["correction"]
        self.assertEqual(correction["status"], "PROVED")
        self.assertEqual(correction["supersedes"]["artifact"], "p7-detector-local-occupancy-v1.json")
        self.assertEqual(correction["affected_claims"], "None. The defects are confined to two test assertions and v1 prose rendering; v1's builder replay, source pins, algebraic checks, and all mathematical statements remain valid.")
        self.assertIn("case-sensitively", correction["cause"])
        self.assertIn("TeX backslashes", correction["defect"])

    def test_exact_conductor_obstruction_and_detector_condition(self) -> None:
        self.assertIn("exact finite conductor", self.data["exact_conductor_and_extension"]["selected_rows"])
        self.assertIn("zero extension", self.data["exact_conductor_and_extension"]["zero_extension"])
        obstruction = self.data["sharp_detector_geometry_obstruction"]["finite_exact_check"]
        self.assertEqual(obstruction["local_difference_multiplicity_D_Delta"], 36)
        self.assertEqual(obstruction["sharp_upper_bound_m_times_M"], 36)
        joint = self.data["conditional_common_detector_sampling"]
        self.assertIn("One common", joint["hypotheses"][1])
        self.assertIn("D_target/m", joint["exact_required_detector_strength"])
        self.assertIn("OCC_Delta(D_target/m)", self.data["weakest_cross_character_occupancy_input"]["target_form"])

    def test_gate_remains_open_and_replay_has_no_float_literals(self) -> None:
        self.assertEqual(self.data["gate_outcome"], "CONTAINED_DETECTOR_SIDE_OCCUPANCY_OBSTRUCTION_GATE_REMAINS_OPEN")
        self.assertIn("remains open", self.data["gate_assessment"]["gate_effect"])
        tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
