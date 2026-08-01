#!/usr/bin/env python3
"""Focused checks for the Cycle 11 E1+E2 block-variance reduction."""
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
ARTIFACT = PROJECT / "artifacts/cycle-11-e1-e2-block-variance-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_11_e1_e2_block_variance_v1.py"
CONVENTIONS = PROJECT / "conventions/e1_e2_block_variance_v1.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class E1E2BlockVarianceV1Tests(unittest.TestCase):
    def test_exact_decomposition_and_rank_one_rows(self) -> None:
        module = load_module(CONVENTIONS, "e1_e2_block_variance_test_v1")
        checked = module.verify_all()
        decomposition = checked["decomposition"]
        self.assertEqual(decomposition["frame"], module.add(decomposition["rank_one"], decomposition["variance"]))
        self.assertTrue(all(entry == 0 for row in checked["zero_variance"]["variance"] for entry in row))
        constant = checked["constant_rank_one"]
        self.assertEqual(constant["lambda_p"], Fraction(35, 3))
        self.assertEqual(constant["lambda_c2_top"], Fraction(196, 3))
        self.assertEqual(constant["lambda_c2_other"], Fraction(-49, 3))

    def test_random_colouring_enumeration(self) -> None:
        module = load_module(CONVENTIONS, "e1_e2_block_variance_test_v1_b")
        rows = module.verify_all()["random_colouring"]
        self.assertEqual(set(rows), {f"n{width}_k{colours}" for width in range(2, 6) for colours in (2, 3)})
        self.assertEqual(rows["n5_k3"]["colourings"], 243)
        for row in rows.values():
            self.assertEqual(row["expectation"], row["formula"])

    def test_artifact_boundaries(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-11-e1-e2-block-variance-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertIn("F=P+Z", data["block_variance"]["identity"])
        self.assertIn("R^(r-1)", data["raw_trace_boundary"]["excess_factor"])
        self.assertIn("v^(44-8delta)", data["rank_one_two_step"]["critical_lower"])
        self.assertEqual(data["density_effect"]["status"], "NO_ANALYTIC_GAIN")

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
        builder = load_module(SCRIPT, "e1_e2_block_variance_builder_test_v1")
        original = builder.INPUTS["cycle10_artifact"]
        builder.INPUTS["cycle10_artifact"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: cycle10_artifact"):
            builder.seal()
        builder.INPUTS["cycle10_artifact"] = original
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
