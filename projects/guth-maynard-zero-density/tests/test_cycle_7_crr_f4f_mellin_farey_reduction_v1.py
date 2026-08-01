#!/usr/bin/env python3
"""Focused checks for the sealed F4F Mellin--Farey reduction."""
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
ARTIFACT = PROJECT / "artifacts/cycle-7-crr-f4f-mellin-farey-reduction-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_7_crr_f4f_mellin_farey_reduction_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_f4f_mellin_farey_v1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_f4f_mellin_farey_builder_v1", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class F4FMellinFareyV1Tests(unittest.TestCase):
    def test_exact_conventions(self) -> None:
        spec = importlib.util.spec_from_file_location("crr_f4f_mellin_farey_conventions_v1", CONVENTIONS)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        checked = module.verify_all()
        self.assertEqual(checked["scales"]["H"], checked["scales"]["Q"] ** 3)
        rows = checked["exact_rows"]
        self.assertEqual(rows["log_jitter_kernel_at_zero"], 6)
        self.assertEqual(str(rows["farey_count_lower"]), "1/200")
        self.assertEqual(rows["wiener_no_go_lower"], __import__("fractions").Fraction(1, 1000))

    def test_artifact_reduction_and_no_go(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-7-crr-f4f-mellin-farey-reduction-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        expansion = data["exact_log_farey_expansion"]
        self.assertIn("J_H(tau)S_Q(tau)", expansion["kernel"])
        energy = data["energy_bin_reduction"]
        self.assertIn("(3/2)E(W)W_Q", energy["bound"])
        self.assertIn("F4F_(kappa/2)", energy["conditional_effect"])
        no_go = data["absolute_wiener_no_go"]
        self.assertEqual(no_go["statement"], "W_Q>=1/1000 for all sufficiently large Q")
        self.assertIn("cannot prove F4F", no_go["conclusion"])
        self.assertIn("CRR-U remains open", data["crr_u_effect"]["statement"])

    def test_mobius_and_continuum_boundary(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        continuum = data["continuum_scope"]
        self.assertIn("Q(1+|tau|)log", continuum["estimate"])
        self.assertIn("(1+|tau|)^2", continuum["valid_uniform_decay_range"])
        mobius = data["mobius_dirichlet_square"]
        self.assertIn("mu(d)", mobius["statement"])
        self.assertIn("does not by itself", mobius["scope"])

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
        original = module.INPUTS["farey_v2_artifact"]
        module.INPUTS["farey_v2_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: farey_v2_artifact"):
            module.seal()
        module.INPUTS["farey_v2_artifact"] = original
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
