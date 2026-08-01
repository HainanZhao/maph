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
SCRIPT = PROJECT / "proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_afari_coupling_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_afari_coupling_builder_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load CRR AFARI coupling builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_afari_coupling_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load CRR AFARI coupling conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRAfarICouplingV1Tests(unittest.TestCase):
    def test_exact_actual_farey_geometry_and_ray_comparison(self) -> None:
        c = load_conventions()
        verified = c.verify_all(8)
        windows = verified["farey_windows"]
        rays = verified["rays"]
        self.assertEqual(windows["union_measure_lower"], Fraction(1, 50 * 8**4))
        self.assertEqual(windows["union_measure_upper"], Fraction(16, 8**4))
        self.assertEqual(rays["ray_weight_lower"], Fraction(8**6, 20))
        self.assertEqual(rays["ray_weight_upper"], 2 * 8**6)
        self.assertIn("coprime", windows["actual_label_rule"])
        self.assertIn("K_F", rays["loewner_comparison"])

    def test_critical_scalar_and_coefficient_exponents(self) -> None:
        c = load_conventions()
        rows = c.exponent_rows()
        self.assertEqual(rows["energy_cauchy_ray_bundle_upper_base_slack_only"], (Fraction(26), Fraction(1, 2)))
        self.assertEqual(rows["rationalmass_local_l4_lower"], (Fraction(20), Fraction(-6)))
        self.assertEqual(rows["base_phase_rayleigh_lower"], (Fraction(20), Fraction(-4)))
        self.assertEqual(rows["base_rationalmass_phase_farey_product_lower"], (Fraction(40), Fraction(-7)))
        constants = c.rationalmass_localization_constants()
        self.assertEqual(constants["theta_mass_lower_from_averaged_bundle"], Fraction(15, 16))
        self.assertEqual(constants["local_l2_lower_from_theta_mass"], Fraction(15, 32))
        self.assertEqual(constants["local_l4_lower_from_cauchy"], Fraction(225, 16384))
        scalar = c.scalar_envelope_rows(8)
        self.assertEqual(scalar["integral_f_star_squared"], 8**20)
        self.assertIn("not claimed", scalar["scope"])

    def test_artifact_boundary_and_conditional_gate(self) -> None:
        data = load_artifact()
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["actual_farey_kernel"]["epistemic_status"], "PROVED")
        self.assertEqual(data["energy_restricted_upper"]["epistemic_status"], "PROVED")
        self.assertEqual(data["rationalmass_localization"]["epistemic_status"], "PROVED")
        self.assertEqual(data["scalar_envelope_calibration"]["epistemic_status"], "PROVED")
        self.assertEqual(data["coefficient_phase_bridge"]["epistemic_status"], "PROVED")
        self.assertEqual(data["cfari_target"]["epistemic_status"], "CONJECTURED")
        self.assertIn("CFARI_eta", data["conditional_implication"]["conditional_on"])
        self.assertIn("does not prove", data["claim_boundary"])

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
