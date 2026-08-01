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
SCRIPT = PROJECT / "proof/build_cycle_6_crr_rfdi_outlier_surgery_v2.py"
CONVENTIONS = PROJECT / "conventions/crr_rfdi_outlier_surgery_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-rfdi-outlier-surgery-v2.json"
V1_ARTIFACT = PROJECT / "artifacts/cycle-6-crr-rfdi-outlier-surgery-v1.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def energy(times: list[float]) -> int:
    return sum(abs(a + b - c - d) <= 1.0 + 1e-12 for a in times for b in times for c in times for d in times)


class CRRRFDIOutlierSurgeryV2Tests(unittest.TestCase):
    def test_exact_rows_and_correction_record(self) -> None:
        conventions = load_module(CONVENTIONS, "outlier_surgery_v2_conventions_under_test")
        verified = conventions.verify_all(64)
        self.assertEqual(verified["scales"]["L"] ** 2, verified["scales"]["R"] * verified["scales"]["H"])
        self.assertEqual(verified["large_v_mean_value_coarse_tail_at_v64"], Fraction(81, 128))
        self.assertIn("ell+r+2s<2", verified["selection_rows"]["failure"])
        self.assertEqual(len(verified["correction_rows"]["v1_artifact"]), 64)

    def test_energy_surgery_and_actual_log_selection_sanity(self) -> None:
        core = [0.0, 3.0, 7.0, 12.0]
        self.assertEqual(energy(core + [80.0]), energy(core) + 4 * len(core) + 1)
        length = 64
        indices = np.arange(length + 1, 2 * length, dtype=np.float64)
        times = np.array([0.0, 2.0, 4.0])
        matrix = np.exp(1j * np.outer(times, np.log(indices)))
        gram = matrix @ matrix.conjugate().T
        values, vectors = np.linalg.eigh(gram)
        u = vectors[:, -1]
        x = matrix.conjugate().T @ u / np.sqrt(values[-1])
        trial = np.linspace(192.0, 256.0, 16001)
        d = np.exp(-1j * np.outer(trial, np.log(indices))) @ np.conjugate(x)
        self.assertLessEqual(float(np.min(np.abs(d) ** 2)), float(np.mean(np.abs(d) ** 2)) + 1e-12)

    def test_artifact_replay_and_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["correction"]["v1_artifact_sha256"], hashlib.sha256(V1_ARTIFACT.read_bytes()).hexdigest())
        self.assertEqual(data["conditional_theorem"]["epistemic_status"], "PROVED_CONDITIONAL_ON_A_CONJECTURED_CORE")
        self.assertIn("does not construct", data["claim_boundary"])
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
        module = load_module(SCRIPT, "outlier_surgery_v2_builder_under_test")
        original = module.INPUTS["v1_artifact"]
        module.INPUTS["v1_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: v1_artifact"):
            module.seal()
        module.INPUTS["v1_artifact"] = original
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
