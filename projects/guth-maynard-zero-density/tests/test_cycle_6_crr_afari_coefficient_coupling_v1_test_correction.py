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
V1_SCRIPT = PROJECT / "proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py"
SCRIPT = PROJECT / "proof/build_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py"
CONVENTIONS = PROJECT / "conventions/crr_afari_coupling_v1.py"
V1_TEST = PROJECT / "tests/test_cycle_6_crr_afari_coefficient_coupling_v1.py"
V1_ARTIFACT = PROJECT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json"
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1-test-correction.json"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_afari_coupling_test_correction_builder_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load CRR AFARI test-correction builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_afari_coupling_test_correction_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load CRR AFARI conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRAfarICouplingV1TestCorrectionTests(unittest.TestCase):
    def test_v1_is_immutable_and_defect_is_exactly_scoped(self) -> None:
        v1 = json.loads(V1_ARTIFACT.read_text(encoding="utf-8"))
        original = V1_TEST.read_text(encoding="utf-8")
        correction = load_artifact()
        self.assertIn("proves neither", v1["claim_boundary"])
        self.assertIn('self.assertIn("does not prove", data["claim_boundary"])', original)
        self.assertEqual(correction["correction"]["epistemic_status"], "OBSERVED")
        self.assertEqual(correction["correction"]["mathematical_change"], "none")
        self.assertEqual(correction["correction"]["affected_claims"], "none")
        self.assertEqual(correction["v1_replay"]["epistemic_status"], "PROVED")

    def test_corrected_exact_rows_and_boundary(self) -> None:
        c = load_conventions()
        rows = c.exponent_rows()
        self.assertEqual(rows["rationalmass_local_l4_lower"], (Fraction(20), Fraction(-6)))
        self.assertEqual(rows["base_rationalmass_phase_farey_product_lower"], (Fraction(40), Fraction(-7)))
        correction = load_artifact()
        self.assertEqual(correction["corrected_assertion"], 'self.assertIn("proves neither", v1["claim_boundary"])')
        self.assertEqual(correction["preserved_v1"]["artifact_sha256"], hashlib.sha256(V1_ARTIFACT.read_bytes()).hexdigest())

    def test_replay_hashes_tamper_and_no_asserts(self) -> None:
        correction = load_artifact()
        self.assertEqual(correction["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(V1_SCRIPT), "--check"], cwd=PROJECT, check=True)
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_builder()
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
