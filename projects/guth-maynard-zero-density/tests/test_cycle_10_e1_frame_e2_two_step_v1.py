#!/usr/bin/env python3
"""Focused exact checks for the Cycle 10 E1/E2 engine theorem."""
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
ARTIFACT = PROJECT / "artifacts/cycle-10-e1-frame-e2-two-step-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_10_e1_frame_e2_two_step_v1.py"
CONVENTIONS = PROJECT / "conventions/e1_e2_engine_v1.py"
SOURCE = PROJECT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class E1FrameE2TwoStepV1Tests(unittest.TestCase):
    def test_exact_e1_trace_rows(self) -> None:
        module = load_module(CONVENTIONS, "e1_e2_engine_test_v1")
        checked = module.verify_all()
        for exponent in range(1, 5):
            row = checked["e1_rows"][str(exponent)]
            self.assertGreaterEqual(row["margin"], Fraction(0))
            self.assertGreaterEqual(row["trace_power"], row["diagonal_power_sum"])
        self.assertEqual(checked["e1_rows"]["1"]["margin"], Fraction(0))

    def test_exact_e2_identity_and_countermodel(self) -> None:
        module = load_module(CONVENTIONS, "e1_e2_engine_test_v1_b")
        checked = module.verify_all()
        row = checked["e2_example"]
        self.assertEqual(row["c2_frobenius_square"], row["trace_a4"] - row["return_square_sum"])
        result = checked["nb4_search"]
        self.assertEqual(result["status"], "NB4_SIGN_COUNTERMODEL")
        self.assertEqual(result["order"], 4)
        self.assertEqual(result["nb4"], Fraction(-128))
        self.assertEqual(result["counts"], {"3": 125, "4": 5})

    def test_source_and_artifact_boundaries(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("There are $O(\\log{T})$ choices of $N$", source)
        self.assertIn("\\tr((M_WM_W^*)^3)-\\frac{\\tr(M_WM_W^*)^3}{k^{2}}", source)
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-10-e1-frame-e2-two-step-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertIn("K^r", data["e1_frame_trace"]["colour_cost"])
        self.assertIn("max_i r_i", data["e2_two_step"]["spectral_bound"])
        self.assertEqual(data["nb4_sign"]["countermodel"]["nb4"], "-128")
        self.assertEqual(data["density_effect"]["status"], "NO_ANALYTIC_GAIN")

    def test_replay_tamper_and_no_asserts(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        for path in (SCRIPT, CONVENTIONS):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        builder = load_module(SCRIPT, "e1_e2_builder_test_v1")
        original = builder.INPUTS["source"]
        builder.INPUTS["source"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: source"):
            builder.seal()
        builder.INPUTS["source"] = original
        with tempfile.NamedTemporaryFile(dir=PROJECT / "proof", suffix=".py") as handle:
            handle.write(SCRIPT.read_bytes() + b"\n# self tamper\n")
            handle.flush()
            original_self = builder.SELF
            builder.SELF = Path(handle.name)
            try:
                self.assertNotEqual(builder.seal()["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
            finally:
                builder.SELF = original_self


if __name__ == "__main__":
    unittest.main()
