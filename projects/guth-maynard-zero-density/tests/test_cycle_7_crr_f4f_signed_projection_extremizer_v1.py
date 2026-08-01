#!/usr/bin/env python3
"""Focused checks for the sealed signed F4F projection/extremizer reduction."""
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
ARTIFACT = PROJECT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_f4f_signed_projection_extremizer_v1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_f4f_signed_projection_extremizer_builder_v1", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SignedF4FProjectionExtremizerV1Tests(unittest.TestCase):
    def test_exact_conventions_and_anchor(self) -> None:
        spec = importlib.util.spec_from_file_location("crr_f4f_signed_projection_extremizer_conventions_v1", CONVENTIONS)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        checked = module.verify_all()
        self.assertEqual(checked["scales"]["H"], checked["scales"]["Q"] ** 3)
        self.assertEqual(checked["scales"]["R"], checked["scales"]["Q"] ** 2)
        anchor = module.actual_anchor(2**20)
        self.assertEqual(__import__("math").gcd(anchor["r"], anchor["s"]), 1)
        self.assertGreater(5 * anchor["r"], 4 * anchor["s"])
        self.assertLessEqual(6 * anchor["r"], 5 * anchor["s"])
        rows = checked["exact_rows"]
        self.assertEqual(rows["close_pair_q_exponent"], Fraction(103, 100))
        self.assertEqual(rows["local_fourth_moment_lower_constant"], Fraction(1, 20))
        self.assertEqual(rows["energy_existence_upper_constant"], 2**16)

    def test_artifact_claim_boundary_and_no_go(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-7-crr-f4f-signed-projection-extremizer-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        signed = data["signed_pair_sum_form"]
        self.assertIn("nu_W", signed["statement"])
        self.assertIn("positive semidefinite", signed["positivity"])
        projection = data["ambient_projection_no_go"]
        self.assertIn("norm exactly one", projection["spectrum"])
        self.assertIn("finite collection", projection["finite_diagnostics"])
        extremizer = data["phase_lattice_extremizer"]
        self.assertIn("every sufficiently large even v", extremizer["quantifier"])
        self.assertIn("(1/20)v^20", extremizer["local_lower"])
        self.assertIn("not a disproof on the full Base class", extremizer["conclusion"])
        self.assertIn("CRR-U remains open", data["crr_u_effect"]["statement"])

    def test_inverse_and_scope_are_explicit(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        inverse = data["one_cell_inverse"]
        self.assertIn("pi^2*epsilon", inverse["statement"])
        self.assertIn("epsilon=0", inverse["endpoint"])
        remaining = data["remaining_gate"]
        self.assertEqual(remaining["epistemic_status"], "CONJECTURED")
        self.assertIn("atomic self-convolution", remaining["statement"])
        document = (PROJECT / "docs/cycle-7-crr-f4f-signed-projection-extremizer-v1.md").read_text(encoding="utf-8")
        self.assertIn("nu=lambda*lambda", document)
        self.assertIn("integral_(U_v)|R_(W_Q)(u)|^4 du", document)
        self.assertIn("F4F_eta fails on this energy/spaced/cardinality class", document)

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
        original = module.INPUTS["f4f_mellin_artifact"]
        module.INPUTS["f4f_mellin_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: f4f_mellin_artifact"):
            module.seal()
        module.INPUTS["f4f_mellin_artifact"] = original
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
