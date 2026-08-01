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

import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/build_cycle_6_crr_spectral_phase_lift_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_spectral_phase_lift_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-spectral-phase-lift-v1.json"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_spectral_phase_lift_builder_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load spectral phase-lift builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_spectral_phase_lift_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load spectral phase-lift conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRSpectralPhaseLiftV1Tests(unittest.TestCase):
    def test_leading_phase_certificate_on_a_finite_complex_matrix(self) -> None:
        matrix = np.array(
            [
                [1.0 + 0.0j, 0.5 + 0.5j, -0.25j],
                [0.75 - 0.25j, -0.5 + 0.25j, 1.0 + 0.0j],
                [0.25 + 0.75j, 1.0 - 0.5j, 0.5 + 0.5j],
            ],
            dtype=np.complex128,
        )
        eigenvalues, left_vectors = np.linalg.eigh(matrix @ matrix.conjugate().T)
        lam = float(eigenvalues[-1])
        u = left_vectors[:, -1]
        x = matrix.conjugate().T @ u / np.sqrt(lam)
        b_phase = np.divide(x, np.abs(x), out=np.zeros_like(x), where=np.abs(x) > 0)
        values = matrix @ b_phase
        n = matrix.shape[1]
        r = matrix.shape[0]
        rho = float(np.sum(np.abs(x)) ** 2 / n)
        phi = float(np.sqrt(r) * np.min(np.abs(values)) / np.linalg.norm(values))
        lower = lam * n * rho * phi**2 / r
        self.assertLessEqual(lower, float(np.min(np.abs(values)) ** 2) + 1e-12)
        self.assertTrue(np.all(np.abs(b_phase) <= 1.0 + 1e-15))

    def test_exact_central_scale_and_support_rows(self) -> None:
        conventions = load_conventions()
        verified = conventions.verify_all(8)
        scales = verified["scales"]
        self.assertEqual(scales["L"] * scales["H"], scales["R"] * scales["V"] ** 2)
        self.assertEqual(verified["support"]["support_count_N"], scales["L"] - 1)
        rows = verified["exponents"]
        self.assertEqual(rows["base_pointwise_square"], (Fraction(14), Fraction(-2)))
        self.assertEqual(rows["central_top_eigenvalue"], (Fraction(12), Fraction()))
        self.assertEqual(rows["strict_closure_condition"], "ell+r+2s<=2-gamma for fixed gamma>0")

    def test_artifact_has_exact_phase_program_and_scoped_gate(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        phase = data["phase_lift"]
        self.assertEqual(phase["epistemic_status"], "PROVED")
        self.assertIn("max_(z in T^W) min_(p in Delta(W))", phase["exact_identity"])
        self.assertIn("Uniform p", phase["minimum_value_warning"])
        gate = data["leading_eigenvector_gate"]
        self.assertEqual(gate["epistemic_status"], "PROVED")
        self.assertEqual(gate["certificate"], "Gamma(W)^2>=lambda*N*rho*phi^2/|W|")
        central = data["central_asymptotic_gate"]
        self.assertIn("ell+r+2s<=2-gamma", central["assumptions"][-1])
        self.assertIn("not a no-go", central["boundary_limit"])
        self.assertEqual(data["context"]["afari_status"], "CONJECTURED")

    def test_replay_tamper_and_no_asserts(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
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
        original = module.INPUTS["crr_v2_artifact"]
        module.INPUTS["crr_v2_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: crr_v2_artifact"):
            module.seal()
        module.INPUTS["crr_v2_artifact"] = original
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
