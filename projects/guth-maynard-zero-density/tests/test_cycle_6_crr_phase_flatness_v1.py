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
SCRIPT = PROJECT / "proof/build_cycle_6_crr_phase_flatness_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_phase_flatness_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-phase-flatness-v1.json"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_phase_flatness_builder_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load phase-flatness builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_phase_flatness_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load phase-flatness conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRPhaseFlatnessV1Tests(unittest.TestCase):
    def test_exact_countermodel_bookkeeping(self) -> None:
        conventions = load_conventions()
        block = conventions.block_countermodel_bounds()
        self.assertEqual(block["right_rho"], Fraction(1))
        self.assertEqual(block["relative_phase_leakage"], Fraction(0))
        self.assertEqual(block["phi_square_upper"], Fraction(101, 980100))
        self.assertEqual(block["left_l1_participation_lower"], Fraction(98010000, 98990201))
        cancellation = conventions.cancellation_countermodel()
        self.assertEqual(cancellation["minimum_top_leverage"], Fraction(1))
        self.assertEqual(cancellation["phi_square"], Fraction(0))
        self.assertEqual(cancellation["spectral_gap"], Fraction(74, 243))
        self.assertEqual(cancellation["row_diagonal"], Fraction(206, 243))

    def test_block_family_has_uniform_diagonal_flat_right_mode_and_small_phi(self) -> None:
        m = 101
        n = m - 1
        tau = 0.01
        epsilon = 0.01
        base = np.empty((m, m), dtype=np.float64)
        base[:n, :n] = 1.0
        base[:n, n] = tau
        base[n, :n] = tau
        base[n, n] = 1.0
        gram = (base + epsilon * np.eye(m)) / (1.0 + epsilon)
        values, vectors = np.linalg.eigh(gram)
        lam = float(values[-1])
        u = vectors[:, -1]
        if np.sum(u) < 0:
            u = -u
        x = np.ones(m, dtype=np.float64) / np.sqrt(m)
        householder_vector = x - u
        householder_vector /= np.linalg.norm(householder_vector)
        right_unitary = np.eye(m) - 2.0 * np.outer(householder_vector, householder_vector)
        self.assertTrue(np.allclose(right_unitary @ x, u, atol=1e-10))
        square_root = vectors @ np.diag(np.sqrt(np.maximum(values, 0.0))) @ vectors.T
        matrix = square_root @ right_unitary
        recovered_x = matrix.T @ u / np.sqrt(lam)
        self.assertTrue(np.allclose(recovered_x, x, atol=2e-8))
        output = matrix @ np.ones(m, dtype=np.float64)
        rho = np.sum(np.abs(recovered_x)) ** 2 / m
        phi = np.sqrt(m) * np.min(np.abs(output)) / np.linalg.norm(output)
        left_participation = np.sum(np.abs(u)) ** 2 / m
        self.assertTrue(np.allclose(np.diag(gram), np.ones(m), atol=1e-12))
        self.assertGreater(lam, 10000.0 / 101.0)
        self.assertAlmostEqual(float(rho), 1.0, places=7)
        self.assertLess(phi**2, 101.0 / 980100.0 + 2e-10)
        self.assertGreater(left_participation, 98010000.0 / 98990201.0 - 2e-8)

    def test_cancellation_family_has_flat_top_mode_but_zero_phase_row(self) -> None:
        x = np.array([10.0, 1.0, 1.0, 1.0], dtype=np.float64) / np.sqrt(103.0)
        b_phase = np.ones(4, dtype=np.float64)
        u = np.array([1.0, 1.0], dtype=np.float64) / np.sqrt(2.0)
        z = np.array([1.0, -1.0], dtype=np.float64) / np.sqrt(2.0)
        q = b_phase - np.dot(x, b_phase) * x
        y = q / np.linalg.norm(q)
        matrix = np.outer(u, x) + np.sqrt(169.0 / 243.0) * np.outer(z, y)
        gram = matrix @ matrix.T
        values, vectors = np.linalg.eigh(gram)
        lam = float(values[-1])
        recovered_u = vectors[:, -1]
        if np.dot(recovered_u, u) < 0:
            recovered_u = -recovered_u
        recovered_x = matrix.T @ recovered_u / np.sqrt(lam)
        recovered_b = np.divide(recovered_x, np.abs(recovered_x), out=np.zeros_like(recovered_x), where=np.abs(recovered_x) > 0)
        output = matrix @ recovered_b
        rho = np.sum(np.abs(recovered_x)) ** 2 / 4.0
        mu_top = 2.0 * np.min(np.abs(recovered_u)) ** 2
        phi = np.sqrt(2.0) * np.min(np.abs(output)) / np.linalg.norm(output)
        residual = matrix @ (recovered_b - np.sum(np.abs(recovered_x)) * recovered_x)
        chi = np.max(np.abs(residual) / (np.sum(np.abs(recovered_x)) * np.sqrt(lam) * np.abs(recovered_u)))
        self.assertTrue(np.allclose(np.diag(gram), np.full(2, 206.0 / 243.0), atol=1e-12))
        self.assertAlmostEqual(lam, 1.0, places=12)
        self.assertAlmostEqual(float(values[0]), 169.0 / 243.0, places=12)
        self.assertAlmostEqual(float(rho), 169.0 / 412.0, places=12)
        self.assertAlmostEqual(mu_top, 1.0, places=12)
        self.assertLess(phi, 1e-10)
        self.assertAlmostEqual(float(chi), 1.0, places=10)

    def test_phase_flatness_lower_bound_on_a_rank_one_matrix(self) -> None:
        u = np.ones(3, dtype=np.float64) / np.sqrt(3.0)
        x = np.array([2.0, 1.0, 1.0], dtype=np.float64) / np.sqrt(6.0)
        matrix = np.outer(u, x)
        lam = 1.0
        b_phase = np.ones(3, dtype=np.float64)
        c = float(np.sum(np.abs(x)))
        residual = matrix @ (b_phase - c * x)
        mu_top = 3.0 * float(np.min(np.abs(u)) ** 2)
        chi = float(np.max(np.abs(residual) / (c * np.sqrt(lam) * np.abs(u))))
        phi = float(np.sqrt(3.0) * np.min(np.abs(matrix @ b_phase)) / np.linalg.norm(matrix @ b_phase))
        lower = (1.0 - chi) / np.sqrt(1.0 + chi**2) * np.sqrt(mu_top)
        self.assertAlmostEqual(chi, 0.0, places=12)
        self.assertGreaterEqual(phi + 1e-12, lower)
        self.assertAlmostEqual(phi, 1.0, places=12)

    def test_artifact_gate_and_replay_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["phase_flatness_lemma"]["epistemic_status"], "PROVED")
        self.assertIn("chi_ph<=kappa<1", data["actual_log_conditional_gate"]["assumptions"])
        self.assertIn("ell+r+2*s<=2-gamma", data["actual_log_conditional_gate"]["assumptions"][-2])
        self.assertIn("actual reduced labels", data["actual_log_conditional_gate"]["farey_preservation"])
        self.assertEqual(data["countermodel_minimum_top_leverage"]["exact_sample"]["right_rho"], "1")
        self.assertEqual(data["countermodel_phase_cancellation"]["exact_data"]["phi_square"], "0")
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
