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
SCRIPT = PROJECT / "proof/build_cycle_4_p1r_crr_u_formalization_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json"


def load_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def load_module():
    spec = importlib.util.spec_from_file_location("crr_u_v2_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load v2 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRUFormalizationV2Tests(unittest.TestCase):
    def test_v1_failure_preserved_and_witness_not_narrowed(self) -> None:
        data = load_artifact()
        correction = data["correction"]
        self.assertTrue(correction["preserves_v1"])
        self.assertEqual(correction["v1_status"], "CONTAINED_FAIL")
        self.assertFalse(correction["witness_class_narrowed"])
        self.assertEqual(len(correction["defects_corrected"]), 4)

    def test_all_exact_slack_rows(self) -> None:
        rows = load_artifact()["exact_slack_bookkeeping"]["rows"]
        self.assertEqual(rows["large_values_upper"], ["6+2*delta", "8+4*delta", "8+4*delta"])
        self.assertEqual(rows["energy_upper_at_cardinality_upper"], ["20+5*delta", "20+37/8*delta", "20+5*delta"])
        self.assertEqual(rows["s3_upper_at_cardinality_upper"], ["36+3/2*delta", "36+3*delta", "36+3*delta", "36+45/16*delta"])
        self.assertEqual(rows["rational_lower_moments"], ["8-3*delta", "20-5*delta"])
        self.assertEqual(rows["rational_induced_affine_lower"], ["28-6*delta", "28-5*delta"])
        self.assertEqual(rows["source_affine_upper_from_base"], ["28+2*delta", "28+1*delta"])
        self.assertEqual(load_artifact()["conventions"]["sigma_for_admitted_base"], "7/10-1/10*delta")

    def test_phase_and_arbitrary_bump_bridge(self) -> None:
        data = load_artifact()
        phase = data["conventions"]["s3_reality_involution"]
        self.assertEqual(phase, "conjugate(I_(m1,m2,m3))=I_(-m3,-m2,-m1), after reversing t2 and t3")
        self.assertIn("raw-R RL2/RL4", data["moment_bridge"]["source_use"])
        self.assertIn("do not identify", data["moment_bridge"]["source_use"])
        self.assertIn("no incompatibility", data["moment_bridge"]["consequence"])

    def test_research_review_policy_and_no_search(self) -> None:
        data = load_artifact()
        self.assertEqual(data["research_stage_review_policy"]["hostile_audit"], "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION")
        self.assertEqual(data["gate"]["formalization"], "RESEARCH_STAGE_SEALED_LIGHTWEIGHT_CHECKED")
        self.assertEqual(data["gate"]["mathematical_classification"], "OPEN")
        self.assertEqual(data["gate"]["search"], "PROHIBITED")
        self.assertFalse(data["resource_policy"]["discovery_search_authorized"])

    def test_runtime_replay_overwrite_tamper_and_no_asserts(self) -> None:
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
        module = load_module()
        original = module.INPUTS["gm_tex"]
        module.INPUTS["gm_tex"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: gm_tex"):
            module.seal()
        module.INPUTS["gm_tex"] = original
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

