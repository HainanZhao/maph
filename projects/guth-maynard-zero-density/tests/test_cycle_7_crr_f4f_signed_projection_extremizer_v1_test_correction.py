#!/usr/bin/env python3
"""Checks the narrow literal-test correction for signed F4F extremizer v1."""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
V1_ARTIFACT = PROJECT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json"
V1_BUILDER = PROJECT / "proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py"
V1_DOCUMENT = PROJECT / "docs/cycle-7-crr-f4f-signed-projection-extremizer-v1.md"
V1_TEST = PROJECT / "tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction.json"
SCRIPT = PROJECT / "proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_f4f_signed_projection_extremizer_test_correction_builder", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load correction builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SignedF4FExtremizerV1TestCorrectionTests(unittest.TestCase):
    def test_preserves_immutable_v1_and_checks_exact_phrase(self) -> None:
        correction = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        v1 = json.loads(V1_ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(correction["artifact_id"], "cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction")
        self.assertEqual(correction["epistemic_status"], "OBSERVED")
        self.assertEqual(correction["preserved_v1"]["artifact_sha256"], hashlib.sha256(V1_ARTIFACT.read_bytes()).hexdigest())
        self.assertEqual(v1["artifact_id"], "cycle-7-crr-f4f-signed-projection-extremizer-v1")
        original_test = V1_TEST.read_text(encoding="utf-8")
        document = V1_DOCUMENT.read_text(encoding="utf-8")
        self.assertIn('self.assertIn("F4F_eta fails on this energy/spaced/cardinality class", document)', original_test)
        self.assertIn("of `F4F_eta` fails on this energy/spaced/cardinality class", document)
        self.assertIn("refutes `F4F_eta` on the actual Base class", document)
        correction_data = correction["correction"]
        self.assertEqual(correction_data["affected_claims"], "none")
        self.assertEqual(correction_data["mathematical_change"], "none")

    def test_historical_failure_is_contained_and_replay_passes(self) -> None:
        historical = subprocess.run([sys.executable, "-m", "unittest", str(V1_TEST)], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(historical.returncode, 0)
        self.assertIn("F4F_eta fails on this energy/spaced/cardinality class", historical.stdout + historical.stderr)
        subprocess.run([sys.executable, str(V1_BUILDER), "--check"], cwd=PROJECT, check=True)
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)

    def test_replay_tamper_and_no_asserts(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))))
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
