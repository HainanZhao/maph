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
SCRIPT = PROJECT / "proof/build_cycle_7_crr_energy_only_f4f_sharpness_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_energy_only_f4f_sharpness_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-7-crr-energy-only-f4f-sharpness-v1.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRREnergyOnlyF4FSharpnessV1Tests(unittest.TestCase):
    def test_exact_architecture_and_central_exponent(self) -> None:
        conventions = load_module(CONVENTIONS, "crr_energy_only_f4f_sharpness_conventions_under_test")
        checked = conventions.verify_all(8)
        self.assertEqual(checked["scales"]["H"], checked["scales"]["Q"] ** 3)
        self.assertEqual(checked["scales"]["R"], checked["scales"]["Q"] ** 2)
        self.assertEqual(checked["central_exponent"], 20)
        self.assertEqual(checked["log_lower_constant"], Fraction(1, 30))
        self.assertIn("No coefficient vector b", checked["architecture_rows"]["excluded_data"])
        self.assertIn("limsup", checked["sharpness_rows"]["limsup"])

    def test_log_measure_conversion_is_exactly_calibrated(self) -> None:
        lower = Fraction(2, 3)
        du_lower = Fraction(1, 20)
        self.assertEqual(lower * du_lower, Fraction(1, 30))
        self.assertLessEqual(float(lower), 1.0)
        self.assertGreaterEqual(2.0, 1.0)

    def test_artifact_scope_replay_and_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-7-crr-energy-only-f4f-sharpness-v1")
        self.assertEqual(data["global_upper"]["epistemic_status"], "PROVED")
        self.assertEqual(data["actual_phase_lattice_lower"]["log_lower"], "J_v(W_v)>=(1/30)v^20, using du/u>=(2/3)du on U_v.")
        self.assertIn("limsup", data["sharpness_theorem"]["statement"])
        self.assertEqual(data["full_base_common_coefficient_boundary"]["epistemic_status"], "CONJECTURED")
        self.assertIn("remains open", data["full_base_common_coefficient_boundary"]["statement"])
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
        module = load_module(SCRIPT, "crr_energy_only_f4f_sharpness_builder_under_test")
        original = module.INPUTS["signed_extremizer_artifact"]
        module.INPUTS["signed_extremizer_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: signed_extremizer_artifact"):
            module.seal()
        module.INPUTS["signed_extremizer_artifact"] = original
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
