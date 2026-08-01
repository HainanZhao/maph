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
SCRIPT = PROJECT / "proof/build_cycle_5_crr_farey_log_gram_reduction_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_farey_log_gram_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v1.json"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_farey_log_gram_builder_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Farey-log Gram builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_farey_log_gram_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Farey-log Gram conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRFareyLogGramReductionV1Tests(unittest.TestCase):
    def test_actual_farey_geometry_is_not_an_alias_substitution(self) -> None:
        data = load_artifact()
        geometry = data["actual_farey_geometry"]
        self.assertEqual(geometry["epistemic_status"], "PROVED")
        self.assertTrue(geometry["cells_disjoint_at_frozen_scales"])
        self.assertEqual(geometry["central_count_lower"], "#F_Q >= Q^2/200 for Q>=4096")
        self.assertIn("actual reduced fractions", geometry["scope"])
        self.assertIn("Farey nodes", data["context"]["alias_exclusion"])

    def test_exact_cell_ray_and_exponent_bookkeeping(self) -> None:
        c = load_conventions()
        verified = c.verify_all(8)
        self.assertEqual(verified["scales"]["Q"], 8**4)
        self.assertEqual(verified["scales"]["H"], 8**12)
        self.assertEqual(verified["cells"]["all_cells_measure_scale"], Fraction(1, 8**4))
        self.assertLess(verified["cells"]["cell_diameter"], verified["cells"]["reduced_fraction_gap_lower"])
        self.assertEqual(verified["rays"]["integer_k_count_lower"], Fraction(8**6, 20))
        rows = c.exponent_rows()
        self.assertEqual(rows["farey_log_gram_bundle_lower"], (Fraction(26), Fraction(-3)))
        self.assertEqual(rows["base_coefficient_spectral_lambda_lower"], (Fraction(12), Fraction(-3)))
        certificate = c.farey_union_bound_certificate()
        self.assertGreater(certificate["residual_margin_at_Q0"], 0)

    def test_jittered_lift_and_labeled_cross_gram_identity(self) -> None:
        data = load_artifact()
        lift = data["rationalmass_to_jittered_farey_lift"]
        self.assertEqual(lift["epistemic_status"], "PROVED")
        self.assertEqual(lift["activated_fraction_count_lower"], "50*v^(8-delta(v))")
        self.assertEqual(lift["theta_range"], "|theta_(r,s)|<3")
        gram = data["multiplicative_ray_cross_gram"]
        self.assertEqual(gram["ray_count_lower"], "#K_(r,s)>=L/(20Q)=v^6/20")
        self.assertEqual(gram["labeled_entry_identity"], "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))")
        bundle = data["forced_bundle_lower"]
        self.assertEqual(bundle["lower_bound"], "B_v(W)>=(5/4)*v^(26-3*delta(v))")
        self.assertEqual(bundle["exponent_derivation"], "(8-delta)+(12-2delta)+6=26-3delta")

    def test_common_coefficient_coupling_and_conditional_gate(self) -> None:
        data = load_artifact()
        coupling = data["base_coefficient_coupling"]
        self.assertEqual(coupling["epistemic_status"], "PROVED")
        self.assertEqual(coupling["spectral_lower"], "lambda_max(M_W M_W^*)>=v^(12-3*delta(v))")
        self.assertIn("same measurement matrix", coupling["common_object_rule"])
        target = data["fari_target"]
        self.assertEqual(target["epistemic_status"], "CONJECTURED")
        reduction = data["conditional_incompatibility_reduction"]
        self.assertEqual(reduction["epistemic_status"], "PROVED")
        self.assertIn("FARI_eta", reduction["conditional_on"])
        self.assertIn("does not prove FARI_eta or CRR-U", reduction["scope"])

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
