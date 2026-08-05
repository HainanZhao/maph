from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/build_cycle_4_p1r_preregistration_v4.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v4.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_v4_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle4P1RPreregistrationV4Tests(unittest.TestCase):
    def test_direct_large_values_attribution(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        ledger = {row["id"]: row for row in data["source_hypothesis_ledger"]}
        theorem = ledger["GM-T1.1"]
        self.assertEqual(theorem["locator"], "GM TeX lines 68--79, thrm:LargeValues")
        self.assertEqual(theorem["hypotheses"], ["|b_n| <= 1", "t_r are 1-separated points in [0,T]", "|sum_{n=N}^{2N} b_n n^(i t_r)| >= V for all r <= R"])
        self.assertEqual(theorem["statement"], "R <= T^(o(1))(N^2 V^(-2) + N^(18/5) V^(-4) + T N^(12/5) V^(-4))")
        self.assertEqual(data["p1r_crr"]["scale_bookkeeping"]["large_values_term_exponents_in_v"], ["6", "8", "8"])

    def test_v3_failure_is_pinned_and_lifecycle_stays_decoupled(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertTrue(data["correction"]["preserves_v1_v3"])
        self.assertEqual(data["correction"]["pinned_v3_hostile_failure"], "FAIL_SOURCE_ATTRIBUTION_COMPLETENESS")
        self.assertFalse(data["historical_replay"]["current_plan_read"])
        self.assertEqual(data["historical_replay"]["current_plan_eligibility"], "EXCLUDED_FROM_HISTORICAL_ARTIFACT")
        self.assertNotIn("PROGRAM.md", SCRIPT.read_text(encoding="utf-8"))
        self.assertNotIn("preflight", data["frozen_hashes"])

    def test_cli_runtime_overwrite_identity_and_source_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
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
            tampered = Path(handle.name)
            original_self = module.SELF
            module.SELF = tampered
            try:
                self.assertNotEqual(module.seal()["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
            finally:
                module.SELF = original_self


if __name__ == "__main__":
    unittest.main()
