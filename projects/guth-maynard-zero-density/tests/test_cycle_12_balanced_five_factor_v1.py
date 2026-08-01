#!/usr/bin/env python3
"""Focused checks for the Cycle 12 balanced five-factor theorem."""
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
ARTIFACT = PROJECT / "artifacts/cycle-12-balanced-five-factor-v1.json"
SCRIPT = PROJECT / "proof/build_cycle_12_balanced_five_factor_v1.py"
CONVENTIONS = PROJECT / "conventions/balanced_five_factor_v1.py"
SOURCE = PROJECT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BalancedFiveFactorV1Tests(unittest.TestCase):
    def test_combinatorics_and_balance(self) -> None:
        module = load_module(CONVENTIONS, "balanced_five_factor_test_v1")
        checked = module.verify_all()
        combinatorics = checked["combinatorics"]
        self.assertEqual(combinatorics["subset_count"], 10)
        self.assertEqual(combinatorics["selected_counts"], [4] * 5)
        self.assertEqual(combinatorics["geometric_exponent"], Fraction(12, 5))
        self.assertEqual(checked["balanced_lengths"]["minimum"], Fraction(12))
        self.assertEqual(checked["balanced_lengths"]["maximum"], Fraction(12))
        self.assertEqual(checked["balance_grid"]["checked"], 306)
        self.assertEqual(checked["balance_grid"]["uniformly_admissible"], [[Fraction(1)] * 5])
        self.assertEqual(checked["unbalanced_countermodel"]["maximum"], Fraction(13))

    def test_critical_exponent_budget(self) -> None:
        module = load_module(CONVENTIONS, "balanced_five_factor_test_v1_b")
        row = module.verify_all()["critical_exponents"]
        self.assertEqual(row["local_rows"], Fraction(36, 5))
        self.assertEqual(row["delta_loss"], Fraction(24, 5))
        self.assertEqual(row["local_gain"], Fraction(4, 5))
        self.assertEqual(row["global_rows"], Fraction(41, 5))
        self.assertEqual(row["density_coefficient"], Fraction(82, 39))
        self.assertEqual(row["coefficient_gain"], Fraction(8, 39))
        self.assertEqual(row["conditional_interval"], Fraction(43, 82))

    def test_source_and_artifact_boundaries(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("$N=T^{5/13}$", source)
        self.assertIn("a Dirichlet polynomial of length $N^2=T^{10/13}$", source)
        self.assertIn("$T_1=T^{12/13}$", source)
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["artifact_id"], "cycle-12-balanced-five-factor-v1")
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertIn("36/5", data["conditional_local_theorem"]["row_bound"])
        self.assertEqual(data["source_factorization"]["status"], "OPEN")
        self.assertEqual(data["density_effect"]["status"], "NO_PROMOTION")

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
        builder = load_module(SCRIPT, "balanced_five_factor_builder_test_v1")
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
