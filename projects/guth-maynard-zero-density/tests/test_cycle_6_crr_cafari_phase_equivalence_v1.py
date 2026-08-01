#!/usr/bin/env python3
"""Focused checks for the sealed CFARI/AFARI phase-equivalence reduction."""
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
ARTIFACT = PROJECT / "artifacts/cycle-6-crr-cfari-phase-equivalence-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_6_crr_cafari_phase_equivalence_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_cafari_phase_equivalence_v1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_cafari_phase_equivalence_builder_v1", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CFARIPhaseEquivalenceV1Test(unittest.TestCase):
    def test_exact_conventions(self) -> None:
        spec = importlib.util.spec_from_file_location("crr_cafari_phase_equivalence_conventions_v1", CONVENTIONS)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        checked = module.verify_all()
        self.assertEqual(checked["scales"]["H"], checked["scales"]["L"] * checked["scales"]["v"] ** 2)
        rows = checked["affine_rows"]
        self.assertEqual(tuple(map(str, rows["base_phase_rayleigh_lower"])), ("20", "-4"))
        self.assertEqual(tuple(map(str, rows["sampled_mean_value_phase_upper"])), ("20", "1"))
        self.assertIn("eta/2", checked["fixed_power_maps"]["cfari_eta_to_afari"])
        self.assertIn("zeta/3", checked["fixed_power_maps"]["f4f_zeta_to_cafari"])

    def test_artifact_claim_boundary_and_maps(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-6-crr-cfari-phase-equivalence-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        enclosure = data["phase_scale_enclosure"]
        self.assertEqual(enclosure["lower"], "a^*G_W*a>=v^(20-4*delta(v))")
        self.assertIn("C*v^(20+delta(v))", enclosure["upper"])
        equivalence = data["fixed_power_equivalence"]
        self.assertIn("AFARI_(eta/2)", equivalence["cfari_to_afari"])
        self.assertIn("CFARI_(eta/2)", equivalence["afari_to_cafari"])
        self.assertIn("if and only if", equivalence["equivalence"])
        self.assertEqual(data["crr_u_effect"]["statement"], "The truth status of CRR-U does not advance. A proof of either fixed-saving target would still imply CRR-U through the averaged-jitter reduction.")

    def test_tensor_and_schur_scope(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        mixed = data["tensor_and_schur"]
        self.assertIn("tensor", mixed["tensor_identity"])
        self.assertIn("independent", mixed["four_linear_structure"])
        self.assertIn("n*(r/s)*exp(theta/H)", mixed["schur_identity"])
        energy = data["extra_energy_gate"]
        self.assertEqual(energy["epistemic_status"], "CONJECTURED")
        self.assertIn("CFARI_(zeta/3)", energy["proved_conditional_effect"])
        self.assertTrue(energy["positive_cubic_boundary"].startswith("No proved bridge"))

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
