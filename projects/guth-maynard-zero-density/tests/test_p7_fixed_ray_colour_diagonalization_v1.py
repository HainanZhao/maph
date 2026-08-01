from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/p7-fixed-ray-colour-diagonalization-v1.json"
BUILDER = ROOT / "proof/build_p7_fixed_ray_colour_diagonalization_v1.py"


class P7FixedRayColourDiagonalizationTests(unittest.TestCase):
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

    def test_exact_fixed_ray_cubic_and_fourier_projector(self) -> None:
        cubic = self.data["fixed_modulus_coloured_cubic"]["finite_exact_check"]
        self.assertEqual((cubic["direct_trace"], cubic["regrouped_trace"]), (72, 72))
        transform = self.data["complete_group_diagonalization"]["finite_exact_check"]
        self.assertEqual(transform["unnormalized_transformed_design"], [[2, 0, 2], [0, 2, 0]])
        rows = transform["projector_rows"]
        self.assertEqual([row["ray_class_diagonal"] for row in rows], [True, False, True])
        self.assertEqual(rows[1]["off_diagonal_hs_squared"], "1/2")
        self.assertIn("every A_t is empty or all of X", self.data["complete_group_diagonalization"]["diagonalization_criterion"])

    def test_coloured_energy_and_completion_barrier_are_sharp(self) -> None:
        energy = self.data["coloured_energy"]["finite_exact_check"]
        self.assertEqual(energy["one_height"]["coloured_energy"], energy["one_height"]["maximal_cubic_scale"])
        self.assertEqual(energy["progression"]["coloured_energy"], energy["progression"]["formula_value"])
        completion = self.data["completion_barrier"]["finite_exact_check"]
        self.assertEqual(completion["sharp_disjoint_support"]["completion_factor"], "3")
        self.assertEqual(completion["colour_complete_support"]["completion_factor"], "1")
        diagonal = completion["diagonal_trace_model"]
        self.assertEqual(diagonal["selected_cubic_excess"], "0")
        self.assertEqual(diagonal["completed_upper_trace_minus_selected_diagonal"], diagonal["expected_uncancelled_diagonal"])

    def test_shell_and_fallback_boundaries(self) -> None:
        shell = self.data["dyadic_shell"]
        self.assertIn("12Q^2", shell["complete_character_bound"])
        fallback = self.data["fixed_character_fallback"]
        self.assertEqual(fallback["status"], "PROVED")
        self.assertIn("N<=T^C", " ".join(fallback["hypotheses"]))
        self.assertIn("F_prim(Q)", fallback["summed_bound"])
        self.assertIn("12Q^2", fallback["summed_bound"])
        self.assertIn("not a lower bound", fallback["exact_loss_boundary"])
        self.assertIn("automatic", fallback["non_promotion"])

    def test_conditional_reduction_and_open_statistic_are_scoped(self) -> None:
        reduction = self.data["conditional_shell_reduction"]
        self.assertEqual(reduction["epistemic_status"], "PROVED")
        self.assertIn("no separate number-of-moduli factor", reduction["conclusion"])
        missing = self.data["missing_analytic_statistic"]
        self.assertEqual(missing["epistemic_status"], "CONJECTURED")
        self.assertIn("selected-side primitive cubic estimate", missing["not_supplied_by_pinned_sources"])
        self.assertEqual(self.data["gate_outcome"], "CONTAINED_FIXED_MODULUS_CHARACTER_AWARE_REDUCTION_AND_COMPLETION_LOSS")

    def test_exact_replay_uses_no_float_literals(self) -> None:
        tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
        floats = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)]
        self.assertEqual(floats, [])


if __name__ == "__main__":
    unittest.main()
