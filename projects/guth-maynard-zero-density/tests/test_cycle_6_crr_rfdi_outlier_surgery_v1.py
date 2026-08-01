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
SCRIPT = PROJECT / "proof/build_cycle_6_crr_rfdi_outlier_surgery_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_rfdi_outlier_surgery_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-rfdi-outlier-surgery-v1.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def additive_energy(times: list[float]) -> int:
    return sum(
        abs(t1 + t2 - t3 - t4) <= 1.0 + 1e-12
        for t1 in times
        for t2 in times
        for t3 in times
        for t4 in times
    )


class CRRRFDIOutlierSurgeryV1Tests(unittest.TestCase):
    def test_exact_convention_rows(self) -> None:
        conventions = load_module(CONVENTIONS, "crr_rfdi_outlier_surgery_conventions_under_test")
        verified = conventions.verify_all(64)
        self.assertEqual(verified["scales"]["H"], 64**12)
        self.assertEqual(verified["outlier_windows"]["energy_increment"], 4 * 64**8 - 3)
        self.assertEqual(verified["large_v_mean_value_coarse_tail_at_v64"], Fraction(81, 128))
        self.assertIn("32*L", verified["mean_value_rows"]["average_bound"])
        self.assertIn("8*g^(-2)", verified["spectral_surgery_rows"]["central_failure"])

    def test_exact_energy_surgery_on_a_separated_finite_model(self) -> None:
        core = [0.0, 3.0, 7.0, 12.0]
        tau = 80.0
        enlarged = core + [tau]
        self.assertEqual(additive_energy(enlarged), additive_energy(core) + 4 * len(core) + 1)

    def test_actual_log_dirichlet_average_and_block_coordinate_bound(self) -> None:
        # A finite literal log-row sanity check of the two proof mechanisms.
        # It is not a frozen-scale witness and is not entered as a research claim.
        L = 64
        indices = np.arange(L + 1, 2 * L, dtype=np.float64)
        weight = np.ones_like(indices)
        core_times = np.array([0.0, 2.0, 4.0], dtype=np.float64)
        matrix_core = np.exp(1j * np.outer(core_times, np.log(indices))) * weight
        gram_core = matrix_core @ matrix_core.conjugate().T
        values, vectors = np.linalg.eigh(gram_core)
        lam = float(values[-1])
        u = vectors[:, -1]
        x = matrix_core.conjugate().T @ u / np.sqrt(lam)
        interval = np.linspace(192.0, 256.0, 16001)
        polynomial = np.exp(-1j * np.outer(interval, np.log(indices))) @ (np.conjugate(x) * weight)
        selected = float(interval[np.argmin(np.abs(polynomial))])
        self.assertLessEqual(float(np.min(np.abs(polynomial) ** 2)), float(np.mean(np.abs(polynomial) ** 2)) + 1e-12)
        outlier_row = np.exp(1j * selected * np.log(indices)) * weight
        matrix = np.vstack([matrix_core, outlier_row])
        gram = matrix @ matrix.conjugate().T
        values_w, vectors_w = np.linalg.eigh(gram)
        u_w = vectors_w[:, -1]
        coupling = np.vdot(u, gram[:-1, -1])
        core_perp = np.eye(len(core_times), dtype=np.complex128) - np.outer(u, np.conjugate(u))
        b_perp = core_perp @ gram[:-1, -1]
        lambda_second = float(values[-2])
        S = float(np.real(gram[-1, -1]))
        B_bound = lambda_second + S + np.linalg.norm(b_perp)
        if B_bound < lam:
            gamma = lam - B_bound
            self.assertLessEqual(abs(u_w[-1]), abs(coupling) / gamma + 1e-8)

    def test_artifact_gate_and_replay_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["conditional_core"]["epistemic_status"], "CONJECTURED")
        self.assertEqual(data["row_deletion_failure"]["epistemic_status"], "PROVED_CONDITIONAL_ON_THE_CORE")
        self.assertIn("does not construct", data["claim_boundary"])
        self.assertIn("one common actual row set", data["scalar_and_farey_preservation"]["outlier_window"])
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
        module = load_module(SCRIPT, "crr_rfdi_outlier_surgery_builder_under_test")
        original = module.INPUTS["farey_log_v2_artifact"]
        module.INPUTS["farey_log_v2_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: farey_log_v2_artifact"):
            module.seal()
        module.INPUTS["farey_log_v2_artifact"] = original
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
