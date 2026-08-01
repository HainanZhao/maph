#!/usr/bin/env python3
"""Focused checks for the phase-lattice Base-saturation reduction."""
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
ARTIFACT = PROJECT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py"
CONVENTIONS = PROJECT / "conventions/crr_phase_lattice_base_saturation_v1.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("crr_phase_lattice_base_saturation_builder_v1", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PhaseLatticeBaseSaturationV1Tests(unittest.TestCase):
    def test_exact_anchor_alias_and_scale_rows(self) -> None:
        spec = importlib.util.spec_from_file_location("crr_phase_lattice_base_saturation_conventions_v1", CONVENTIONS)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        checked = module.verify_all()
        self.assertEqual(checked["scales"]["H"], checked["scales"]["Q"] ** 3)
        self.assertEqual(checked["scales"]["L"] * checked["scales"]["H"], checked["scales"]["R"] * checked["scales"]["V"] ** 2)
        anchor = module.actual_anchor(2**20)
        self.assertEqual(__import__("math").gcd(anchor["r"], anchor["s"]), 1)
        self.assertGreater(5 * anchor["r"], 4 * anchor["s"])
        self.assertLessEqual(6 * anchor["r"], 5 * anchor["s"])
        rows = checked["exact_rows"]
        self.assertEqual(rows["beta_lower"], Fraction(6, 5))
        self.assertEqual(rows["max_exact_alias_class_size"], 4)
        self.assertGreater(rows["beta_lower"] ** 4, 2)
        self.assertEqual(rows["base_product_main_exponent"], 12)
        self.assertEqual(rows["base_product_delta_loss"], 3)

    def test_artifact_alias_and_efficiency_boundaries(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-7-crr-phase-lattice-base-saturation-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        aliases = data["exact_alias_quotient"]
        self.assertIn("n/m=(s_Q/r_Q)^k", aliases["alias_relation"])
        self.assertIn("at most four", aliases["class_bound"])
        self.assertIn("only constant factors", aliases["conclusion"])
        efficiency = data["base_saturation_efficiency"]
        self.assertIn("0<=Xi_(P,A)<=1", efficiency["range"])
        self.assertIn("Gamma_(P,A)^2", efficiency["exact_identity"])
        self.assertIn("lambda_(P,A)*Xi_(P,A)", efficiency["base_equivalence"])
        saturation = data["base_necessary_saturation"]
        self.assertIn("v^(12-3delta(v))", saturation["lower_product"])
        self.assertIn("fixed kappa", saturation["fixed_power_exclusion"])
        self.assertIn("CRR-U remains open", data["crr_u_effect"]["statement"])

    def test_leading_vector_link_and_open_gate(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertIn("Xi_(P,A)>=rho*phi^2", data["leading_vector_link"]["statement"])
        self.assertEqual(data["remaining_gate"]["epistemic_status"], "CONJECTURED")
        self.assertIn("distinct-phase quotient norm", data["remaining_gate"]["statement"])
        document = (PROJECT / "docs/cycle-7-crr-phase-lattice-base-saturation-v1.md").read_text(encoding="utf-8")
        self.assertIn("Gamma_(P_Q,A)", document)
        self.assertIn("Exact rational aliases offer only constant factors", document)
        self.assertIn("necessary diagnostics, not by themselves a sufficient", document)

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
