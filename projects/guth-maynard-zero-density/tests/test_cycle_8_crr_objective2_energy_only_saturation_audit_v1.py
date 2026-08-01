#!/usr/bin/env python3
"""Focused checks for the Objective-2 EO-LF4 saturation audit."""
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
ARTIFACT = PROJECT / "artifacts/cycle-8-crr-objective2-energy-only-saturation-audit-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_objective2_energy_only_saturation_v1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_objective2_eolf4_audit_builder_v1", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Objective-2 EO-LF4 audit builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_objective2_eolf4_audit_conventions_v1", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Objective-2 EO-LF4 audit conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Objective2EOLF4SaturationAuditV1Tests(unittest.TestCase):
    def test_exact_scale_rows_and_epsilon_absorption(self) -> None:
        c = load_conventions()
        checked = c.verify_all(8)
        self.assertEqual(checked["scales"]["H"], checked["scales"]["Q"] ** 3)
        self.assertEqual(checked["scales"]["R"], checked["scales"]["Q"] ** 2)
        rows = checked["extremizer_rows"]
        self.assertEqual(rows["central_exponent"], 20)
        self.assertEqual(rows["local_lower_constant"], Fraction(1, 20))
        allocation = c.epsilon_absorption(0.6)
        self.assertAlmostEqual(allocation["source_eta"], 0.025)
        self.assertAlmostEqual(allocation["H_to_v_exponent_loss"], 0.3)
        self.assertAlmostEqual(allocation["delta_cap"], 0.3)
        bridge = checked["base_bridge"]
        self.assertIn("lambda_(P,A)*Xi_(P,A)", bridge["exact_condition"])

    def test_scoped_objective2_decision_and_exclusions(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-8-crr-objective2-energy-only-saturation-audit-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        decision = data["objective_2_assessment"]
        self.assertEqual(decision["status"], "SATISFIED_FOR_EO_LF4_SCOPED_GM_SUBARCHITECTURE")
        self.assertIn("not a full-method", decision["full_method_boundary"])
        theorem = data["sharp_eolf4_theorem"]
        self.assertIn("for every fixed epsilon>0", theorem["upper_quantifier"])
        self.assertIn("every sufficiently large even v", theorem["lower_quantifier"])
        self.assertIn("(1/20)*v^20", theorem["lower_bound"])
        self.assertIn("limsup", theorem["sharpness"])
        self.assertIn("does not establish", data["bundle_boundary"]["statement"])
        missing = data["missing_base_full_crr_gate"]
        self.assertEqual(missing["epistemic_status"], "CONJECTURED")
        self.assertIn("lambda_(P,A)*Xi_(P,A)", missing["exact_equivalence"])

    def test_replay_hashes_tamper_and_no_asserts(self) -> None:
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
