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
SCRIPT = PROJECT / "proof/build_cycle_4_crr_alias_model_barrier_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-crr-alias-model-barrier-v1.json"
CONVENTIONS = PROJECT / "conventions/crr_alias_model_barrier_v1.py"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_module(path: Path = SCRIPT):
    spec = importlib.util.spec_from_file_location("crr_alias_model_barrier_v1_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load alias-model barrier builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_conventions():
    spec = importlib.util.spec_from_file_location("crr_alias_model_barrier_v1_conventions_under_test", CONVENTIONS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load alias-model conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRAliasModelBarrierV1Tests(unittest.TestCase):
    def test_real_energy_is_not_modular_and_carries_are_closed(self) -> None:
        data = load_artifact()["construction"]["real_energy"]
        self.assertIn("tolerance <=1 is exact equality", data["tolerance_reduction"])
        self.assertIn("not modular energy", data["tolerance_reduction"])
        self.assertIn("A+A subset [0,K/2)", data["no_carry_factorization"])
        self.assertEqual(data["exact_formula"], "E_R,1(W)=E(A)*(2L^3+L)/3")
        c = load_conventions()
        for q in (256, 257, 1024):
            row = c.scales(q)
            self.assertLess(row["A_max_upper"], row["K"] // 4)
            self.assertGreaterEqual(row["minimum_A_gap"], 6 * q)
            self.assertEqual(c.interval_energy(row["L"]), (2 * row["L"] ** 3 + row["L"]) // 3)

    def test_probabilistic_A_and_parseval_paley_rows(self) -> None:
        c = load_conventions()
        for q in (256, 257, 1024):
            row = c.scales(q)
            self.assertLessEqual(c.energy_expectation_upper(q), 3 * row["m"] ** 2)
            self.assertEqual(c.alias_count_lower(q), Fraction(2 * row["K"], 3))
        alias = load_artifact()["alias_and_smoothing"]
        self.assertIn("sum|Ahat|^2=Km", alias["fourier_count"])
        self.assertIn(">=2K/3", alias["fourier_count"])

    def test_smoothing_scale_and_scope_boundary(self) -> None:
        data = load_artifact()
        alias = data["alias_and_smoothing"]
        self.assertIn("height asymp H and width asymp H^(-1)", alias["positive_smoothing"])
        self.assertIn("integral_U F_H >>q^2", alias["packet"])
        self.assertIn("integral_U F_H^2 >>q^5", alias["packet"])
        exclusions = " ".join(data["scope_exclusions"])
        self.assertIn("Farey", exclusions)
        self.assertIn("coefficient sequence", exclusions)
        self.assertIn("CRR witness", exclusions)
        self.assertEqual(data["research_stage_review_policy"]["hostile_audit"], "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION")

    def test_exponent_algebra_and_replay(self) -> None:
        rows = load_artifact()["exact_replay"]["q_exponents"]
        self.assertEqual(rows, {
            "K": "2",
            "L": "1",
            "H": "3",
            "cardinality_R": "2",
            "real_energy": "5",
            "alias_amplitude": "3/2",
            "alias_packet_measure": "-1",
            "first_smoothed_moment": "2",
            "second_smoothed_moment": "5",
        })
        data = load_artifact()
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))))
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)

    def test_frozen_input_tamper_rejection(self) -> None:
        module = load_module()
        original = module.INPUTS["gm_source_tex"]
        module.INPUTS["gm_source_tex"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: gm_source_tex"):
            module.seal()
        module.INPUTS["gm_source_tex"] = original
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
