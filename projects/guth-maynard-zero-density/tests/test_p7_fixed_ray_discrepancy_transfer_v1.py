from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-fixed-ray-discrepancy-transfer-v1.json"
BUILDER = ROOT / "proof/build_p7_fixed_ray_discrepancy_transfer_v1.py"


class P7FixedRayDiscrepancyTransferTests(unittest.TestCase):
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

    def test_zero_extension_transfer_and_thorner_scope(self) -> None:
        transfer = self.data["complete_to_primitive_transfer"]
        self.assertEqual(transfer["status"], "PROVED")
        check = transfer["finite_zero_extension_check"]
        self.assertEqual(check["complete_zero_extended_F_eta_at_v_zero"], "2")
        self.assertEqual(check["primitive_reindexed_F_eta_star_with_u_f_at_v_zero"], "2")
        self.assertEqual(check["incorrect_unrestricted_primitive_expression_at_v_zero"], "-1")
        self.assertIn("No tau(f)", transfer["loss_accounting"])
        self.assertIn("q^2B^2", transfer["continuous_L2"])

    def test_sharp_difference_sampling_and_energy_cost(self) -> None:
        fibre = self.data["per_character_separation"]["finite_exact_check"]
        self.assertEqual(fibre["local_difference_multiplicity"], fibre["fibrewise_upper_bound_mP"])
        self.assertEqual(fibre["minimum_same_colour_gap"], 3)
        progression = self.data["difference_energy_boundary"]["finite_exact_check"]
        self.assertEqual(progression["local_difference_multiplicity"], 5)
        self.assertEqual(progression["local_difference_energy_at_2Delta"], 85)
        self.assertIn("m^(1/2)", progression["asymptotic_sampling_loss"])
        self.assertIn("m^(1/4)", self.data["difference_energy_boundary"]["progression_countercost"])

    def test_cubic_budget_and_scoped_no_go(self) -> None:
        budget = self.data["selected_cubic_budget"]["finite_exact_check"]
        self.assertEqual(budget["exact_budget_3H_cubed_delta_a3_plus_delta_squared"], 864)
        self.assertEqual(budget["delta_multiplier"], 4)
        self.assertEqual(budget["delta_dominant_cubic_multiplier"], 64)
        no_go = self.data["scoped_no_go"]
        self.assertEqual(no_go["status"], "PROVED")
        self.assertIn("D_Delta", no_go["minimal_missing_statistic"])
        self.assertIn("does not rule out", no_go["non_overclaim"])
        self.assertEqual(self.data["gate_outcome"], "ADVANCED_COMPLETE_TO_PRIMITIVE_L2_TRANSFER_DIFFERENCE_SAMPLING_OPEN")

    def test_exact_replay_uses_no_float_literals(self) -> None:
        tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
