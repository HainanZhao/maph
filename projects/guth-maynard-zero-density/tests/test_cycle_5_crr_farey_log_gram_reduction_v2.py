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
SCRIPT = PROJECT / "proof/build_cycle_5_crr_farey_log_gram_reduction_v2.py"
CONVENTIONS = PROJECT / "conventions/crr_farey_log_gram_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json"
V1_ARTIFACT = PROJECT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v1.json"
V1_ARTIFACT_SHA256 = "8f204d56a5609fa9c8a93b152a969a038bc13463d3a36ca746e842bfe21e5f40"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_farey_log_gram_v2_builder_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load averaged-jitter v2 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_farey_log_gram_v2_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load averaged-jitter v2 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRFareyLogGramReductionV2Tests(unittest.TestCase):
    def test_v1_is_preserved_by_hash_and_v2_is_distinct(self) -> None:
        data = load_artifact()
        self.assertEqual(hashlib.sha256(V1_ARTIFACT.read_bytes()).hexdigest(), V1_ARTIFACT_SHA256)
        self.assertEqual(data["preserves_v1"]["epistemic_status"], "PROVED")
        self.assertEqual(data["preserves_v1"]["v1_artifact_sha256"], V1_ARTIFACT_SHA256)
        self.assertEqual(data["frozen_hashes"]["farey_log_v1_artifact"]["sha256"], V1_ARTIFACT_SHA256)
        self.assertIn("averaged", data["preserves_v1"]["statement"])
        self.assertEqual(data["source_context"]["preserved_v1_fari_status"], "CONJECTURED")

    def test_expanded_cell_and_theta_geometry(self) -> None:
        conventions = load_conventions()
        verified = conventions.verify_all(8)
        geometry = verified["geometry"]
        self.assertLess(geometry["expanded_cell_diameter"], geometry["reduced_fraction_gap_lower"])
        self.assertLess(geometry["theta_neighborhood_diameter"], geometry["reduced_fraction_gap_lower"])
        self.assertGreater(geometry["upper_theta_cover_margin"], 0)
        self.assertGreater(geometry["lower_theta_cover_margin"], 0)
        self.assertEqual(geometry["raw_cell_u_upper"], Fraction(4, 3))
        self.assertEqual(geometry["rl2_containing_interval"], "[1/2,3/2]")
        constants = verified["constants"]
        self.assertEqual(constants["smoothing_incidence_upper"], Fraction(1, 50))
        self.assertEqual(constants["raw_cell_sum_factor"], 50)
        self.assertEqual(constants["averaged_bundle_prefactor"], Fraction(15, 8))

    def test_lower_and_raw_rl2_upper_rows_match_at_exponent_26(self) -> None:
        data = load_artifact()
        lower = data["averaged_actual_farey_lower"]
        self.assertEqual(lower["epistemic_status"], "PROVED")
        self.assertEqual(lower["lower_bound"], "A_v(W)>=(15/8)*v^(26-3*delta(v))")
        self.assertEqual(lower["raw_actual_farey_l2_sum_lower"], "sum_(r,s) integral_(J_(r,s)^+) |R_W(u)|^2 du >= 50*v^(8-3*delta(v))")
        self.assertEqual(lower["theta_mass_lower"], "sum_(r,s) integral_(-3)^3 |R_W((r/s)*exp(theta/H))|^2 dtheta >= (75/2)*H*v^(8-3*delta(v))")
        upper = data["raw_rl2_global_upper"]
        self.assertEqual(upper["epistemic_status"], "PROVED")
        self.assertIn("Lemma RL2", upper["source_anchor"])
        self.assertEqual(upper["global_bound"], "A_v(W) << (L/Q)*H*|W| << v^(26+delta(v))=v^(26+o(1))")
        rows = data["exact_replay"]["exponent_rows"]
        self.assertEqual(rows["averaged_actual_farey_bundle_lower"], "26-3*delta")
        self.assertEqual(rows["raw_rl2_global_upper_under_base"], "26+1*delta")

    def test_scope_requires_new_input_and_does_not_promote_afari(self) -> None:
        data = load_artifact()
        saturation = data["uncoupled_global_l2_saturation"]
        self.assertEqual(saturation["epistemic_status"], "PROVED")
        self.assertIn("4delta=o(1)", saturation["statement"])
        self.assertIn("Base/coefficient coupling", saturation["required_new_information_for_fixed_power_gain"])
        self.assertIn("not a proof", saturation["not_a_no_go"])
        target = data["afari_target"]
        self.assertEqual(target["epistemic_status"], "CONJECTURED")
        self.assertIn("not AFARI_eta", target["not_claimed"])
        reduction = data["conditional_incompatibility_reduction"]
        self.assertEqual(reduction["epistemic_status"], "PROVED")
        self.assertIn("does not prove AFARI_eta", reduction["scope"])

    def test_replay_hashes_tamper_and_no_asserts(self) -> None:
        data = load_artifact()
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        for path in (SCRIPT, CONVENTIONS):
            self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_builder()
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
