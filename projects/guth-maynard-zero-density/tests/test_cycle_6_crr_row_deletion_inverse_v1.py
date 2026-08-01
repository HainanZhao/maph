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
SCRIPT = PROJECT / "proof/build_cycle_6_crr_row_deletion_inverse_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_row_deletion_inverse_v1.py"
ACTUAL_PROBE_CONVENTIONS = PROJECT / "conventions/crr_actual_log_spectral_probe_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-row-deletion-inverse-v1.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_builder():
    return load_module(SCRIPT, "crr_row_deletion_builder_under_test")


def deletion_bounds(matrix: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    gram = matrix @ matrix.conjugate().T
    values, vectors = np.linalg.eigh(gram)
    lam = float(values[-1])
    u = vectors[:, -1]
    lower = []
    for t in range(matrix.shape[0]):
        keep = [index for index in range(matrix.shape[0]) if index != t]
        lambda_minus = float(np.linalg.eigvalsh(gram[np.ix_(keep, keep)])[-1])
        deficit = max(0.0, lam - lambda_minus)
        beta = float(np.linalg.norm(gram[keep, t]))
        lower.append(0.0 if deficit == 0.0 and beta == 0.0 else deficit**2 / (deficit**2 + beta**2))
    return lam, u, np.asarray(lower)


class CRRRowDeletionInverseV1Tests(unittest.TestCase):
    def test_exact_convention_rows_and_rank_one_sharpness(self) -> None:
        conventions = load_module(CONVENTIONS, "crr_row_deletion_conventions_under_test")
        verified = conventions.verify_all(8)
        self.assertEqual(verified["rank_one_sharpness"]["minimum_top_leverage"], Fraction(3, 14))
        self.assertEqual(verified["cancellation_projection_calibration"]["chi_ph_square"], Fraction(1))
        self.assertEqual(verified["plateau_l2_bounds"]["gram_diagonal_S_lower"], Fraction(8**10, 2))
        self.assertIn("d_t^2", verified["deletion_rows"]["coordinate_lower"])
        self.assertIn("average Delta_F>=75*v^(12", verified["farey_deletion_rows"]["rationalmass_average"])

    def test_deletion_bound_is_exact_for_rank_one_gram(self) -> None:
        vector = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        matrix = vector[:, None]
        lam, u, lower = deletion_bounds(matrix)
        expected = np.abs(vector) ** 2 / np.dot(vector, vector)
        self.assertAlmostEqual(lam, 14.0, places=12)
        self.assertTrue(np.allclose(np.abs(u) ** 2, expected, atol=1e-12))
        self.assertTrue(np.allclose(lower, expected, atol=1e-12))

    def test_deletion_bound_on_the_literal_actual_log_matrix(self) -> None:
        actual = load_module(ACTUAL_PROBE_CONVENTIONS, "actual_log_probe_conventions_for_deletion_test")
        indices, weight = actual.coefficient_indices_and_weight()
        times = np.array([0, 2, 4], dtype=np.float64)
        matrix = actual.measurement_matrix(times, indices, weight)
        gram = matrix @ matrix.conjugate().T
        diagonal = float(np.sum(weight**2))
        self.assertTrue(np.allclose(np.diag(gram), np.full(3, diagonal), atol=1e-9))
        _, u, lower = deletion_bounds(matrix)
        self.assertTrue(np.all(np.abs(u) ** 2 + 1e-10 >= lower))
        self.assertTrue(np.all(lower >= 0.0))

    def test_projection_phase_leakage_bound_is_exact_on_cancellation_model(self) -> None:
        x = np.array([10.0, 1.0, 1.0, 1.0], dtype=np.float64) / np.sqrt(103.0)
        b_phase = np.ones(4, dtype=np.float64)
        u = np.array([1.0, 1.0], dtype=np.float64) / np.sqrt(2.0)
        z = np.array([1.0, -1.0], dtype=np.float64) / np.sqrt(2.0)
        c = float(np.sum(np.abs(x)))
        q = b_phase - c * x
        y = q / np.linalg.norm(q)
        matrix = np.outer(u, x) + np.sqrt(169.0 / 243.0) * np.outer(z, y)
        gram = matrix @ matrix.T
        lam = 1.0
        residual = matrix @ q
        eta = np.linalg.norm(q) ** 2 / c**2
        chi_square = np.max(np.abs(residual) ** 2 / (lam * c**2 * np.abs(u) ** 2))
        projection_square = eta * np.max(np.diag(gram) / (lam * np.abs(u) ** 2) - 1.0)
        self.assertAlmostEqual(eta, 243.0 / 169.0, places=12)
        self.assertAlmostEqual(chi_square, 1.0, places=12)
        self.assertAlmostEqual(projection_square, 1.0, places=12)

    def test_artifact_and_replay_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["row_deletion_leverage"]["epistemic_status"], "PROVED")
        self.assertIn("DelCov(W)", data["row_deletion_leverage"]["consequence"])
        self.assertIn("eta_ph", data["phase_projection"]["combined_actual_test"])
        self.assertIn("actual reduced labels", data["conditional_actual_gate"]["farey_preservation"])
        self.assertEqual(data["rfd_inverse_target"]["epistemic_status"], "CONJECTURED")
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
