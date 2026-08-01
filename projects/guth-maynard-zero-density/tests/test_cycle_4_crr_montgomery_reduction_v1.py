from __future__ import annotations

import ast
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/build_cycle_4_crr_montgomery_reduction_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-crr-montgomery-reduction-v1.json"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_module():
    spec = importlib.util.spec_from_file_location("crr_montgomery_reduction_v1_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load CRR-to-Montgomery reduction builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRMontgomeryReductionV1Tests(unittest.TestCase):
    def test_conjectural_premise_and_strict_claim_boundary(self) -> None:
        data = load_artifact()
        premise = data["montgomery_fixed_epsilon_premise"]
        self.assertEqual(premise["epistemic_status"], "CONJECTURED")
        self.assertTrue(premise["not_a_theorem_in_this_artifact"])
        self.assertIn("neither Montgomery's conjecture nor CRR-U", data["claim_boundary"])
        self.assertEqual(data["research_stage_review_policy"]["hostile_audit"], "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION")

    def test_fixed_sigma_anchor_exact_exponents(self) -> None:
        exact = load_artifact()["fixed_sigma_reduction"]["exact_exponents"]
        self.assertEqual(exact["sigma"], "13/20")
        self.assertEqual(exact["epsilon"], "1/24")
        self.assertEqual(exact["threshold_exponent_in_v"], "13/2")
        self.assertEqual(exact["pointwise_margin_before_delta"], "1/2")
        self.assertEqual(exact["montgomery_length_exponent"], "7")
        self.assertEqual(exact["epsilon_height_exponent"], "1/2")
        self.assertEqual(exact["upper_exponent_in_v"], "15/2")
        self.assertEqual(exact["cardinality_gap_before_delta"], "1/2")

    def test_general_interval_and_endpoint_exclusion(self) -> None:
        data = load_artifact()["general_sigma_reduction"]
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertIn("conditional_on", data)
        self.assertIn("sigma=3/5", data["endpoint_exclusion"])
        self.assertIn("sigma=7/10", data["endpoint_exclusion"])
        rows = {row["sigma"]: row for row in data["rational_samples"]}
        self.assertEqual(rows["13/20"]["pointwise_margin_p"], "1/2")
        self.assertEqual(rows["13/20"]["cardinality_gap_g"], "1")
        self.assertEqual(rows["13/20"]["epsilon_g_over_48"], "1/48")
        self.assertEqual(rows["13/20"]["upper_exponent_in_v"], "29/4")
        module = load_module()
        with self.assertRaisesRegex(RuntimeError, "strictly"):
            module.general_interval(Fraction(3, 5))
        with self.assertRaisesRegex(RuntimeError, "strictly"):
            module.general_interval(Fraction(7, 10))

    def test_joint_saving_and_one_saving_limit(self) -> None:
        data = load_artifact()
        bridge = data["joint_saving_bridge"]
        self.assertEqual(bridge["epistemic_status"], "PROVED")
        self.assertIn("CONJECTURED upper bound", bridge["conditional_on"])
        self.assertEqual(bridge["exact_example"]["kappa"], "1/5")
        self.assertEqual(bridge["exact_example"]["epsilon"], "1/20")
        self.assertEqual(bridge["exact_example"]["joint_upper_exponent"], "157/20")
        limit = data["one_saving_limit"]
        self.assertEqual(limit["epistemic_status"], "PROVED")
        self.assertEqual(limit["example"]["dominant_exponent"], "8")
        self.assertTrue(limit["not_a_universal_no_go"])

    def test_replay_hashes_tamper_and_no_asserts(self) -> None:
        data = load_artifact()
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_module()
        original = module.INPUTS["gm_source_tex"]
        module.INPUTS["gm_source_tex"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: gm_source_tex"):
            module.seal()
        module.INPUTS["gm_source_tex"] = original
        with tempfile.NamedTemporaryFile(dir=PROJECT / "proof", suffix=".py") as handle:
            handle.write(SCRIPT.read_bytes() + b"\n# self tamper\n")
            handle.flush()
            original_self = module.SELF
            module.SELF = Path(handle.name)
            try:
                self.assertNotEqual(module.seal()["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
            finally:
                module.SELF = original_self


if __name__ == "__main__":
    unittest.main()
