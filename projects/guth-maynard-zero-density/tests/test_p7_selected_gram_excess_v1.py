from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-selected-gram-excess-v1.json"
BUILDER = ROOT / "proof/build_p7_selected_gram_excess_v1.py"


class P7SelectedGramExcessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_pins(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for row in self.data["artifact_identity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])
        for row in self.data["source_integrity"].values():
            self.assertEqual(hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest(), row["sha256"])

    def test_exact_psd_excess_and_cross_conductor_correction(self) -> None:
        excess = self.data["selected_psd_excess"]["finite_sharpness_check"]
        self.assertEqual((excess["variance_two"], excess["cubic_excess"]), ("2", "66"))
        self.assertEqual(excess["ratio"], "11/12")
        cross = self.data["cross_conductor_pinching"]["finite_sharpness_check"]
        self.assertEqual(cross["aggregate_cross_conductor_term"], cross["global_selected_excess"])
        self.assertEqual(cross["aggregate_cross_conductor_term"], "120")
        correction = self.data["correction"]
        self.assertIn("0<=X_cross<=G(K)", correction["repair"])
        self.assertIn("Individual block-expansion summands", correction["defect"])

    def test_completion_free_class_average_and_difference_boundary(self) -> None:
        reduction = self.data["fixed_ray_class_average_compression"]
        self.assertIn("no completion factor", reduction["selection_decomposition"])
        self.assertIn("tr(A)=tr(A_0)", reduction["trace_preservation"])
        self.assertIn("complete-character", reduction["difference_multiset_boundary"])
        check = reduction["finite_exact_check"]
        self.assertEqual(check["local_height_multiplicity"], 1)
        self.assertEqual(check["coloured_energy"], 6)
        self.assertEqual(check["selected_gram_excess"], "144")
        self.assertEqual(check["averaged_gram_excess"], "0")
        self.assertEqual(check["ray_class_delta_2_squared"], "14")
        self.assertEqual(check["complete_character_fourier_hs_squared"], "28")
        self.assertIn("28/2 = 14", check["parseval_delta_2_squared"])

    def test_l2_fallback_and_no_go_stay_contained(self) -> None:
        l2 = self.data["sampled_l2_consequence"]
        self.assertEqual(l2["status"], "PROVED")
        self.assertIn("raw-L2 fallback", l2["scope"])
        self.assertIn("no fixed R-saving", l2["sharp_raw_l2_barrier"])
        no_go = self.data["contained_no_go"]
        self.assertEqual(no_go["status"], "PROVED")
        self.assertIn("not P7 zero", no_go["non_overclaim"])
        self.assertEqual(
            self.data["gate_outcome"],
            "ADVANCED_SELECTED_GRAM_REDUCTION_CROSS_CONDUCTOR_CONTAINED",
        )

    def test_exact_replay_uses_no_float_literals(self) -> None:
        tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
