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
SCRIPT = PROJECT / "proof/build_cycle_4_p1r_crr_u_formalization_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-crr-u-formalization-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("crr_u_formalization_v1_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load formalization builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CRRUFormalizationV1Tests(unittest.TestCase):
    def test_exact_scales_and_range(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        exact = data["exact_source_bound_compatibility"]
        self.assertEqual(exact["exponents_in_v"]["large_values"], ["6", "8", "8"])
        self.assertEqual(exact["exponents_in_v"]["energy"], ["20", "20", "20"])
        self.assertEqual(exact["exponents_in_v"]["s3"], ["36", "36", "36", "36"])
        self.assertEqual(exact["exponents_in_v"]["rational_moments"], ["8", "20"])
        self.assertEqual(exact["exponents_in_v"]["affine"], ["28", "28"])
        self.assertIn("H^(5/6)", exact["range_check"])

    def test_common_witness_quantifier_and_boundaries(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["classification"]["branch"], "CRR-U_UNIVERSAL_INCOMPATIBILITY")
        self.assertIn("sequence", data["classification"]["falsifier"])
        self.assertIn("One common pair", data["witness_schema"]["common_object_rule"])
        self.assertEqual(data["source_status"]["gm_rational_remark"].split()[0], "OBSERVED")
        self.assertEqual(data["source_status"]["new_rational_predicate"].split()[0], "CONJECTURED")
        self.assertIn("upper bounds only", data["source_status"]["positive_cubic_lower_bound"])

    def test_no_search_authority_and_complete_future_gate(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        policy = data["resource_policy"]
        self.assertFalse(policy["discovery_search_authorized"])
        self.assertEqual(policy["row_cap"], 0)
        self.assertIsNone(policy["rng_seed"])
        self.assertIsNone(policy["certification_margin"])
        for field in ("families", "ranges", "seed", "cap", "failed-row", "margin"):
            self.assertIn(field, policy["future_search_rule"])
        self.assertEqual(data["gate"]["mathematical_classification"], "OPEN")

    def test_replay_runtime_overwrite_and_tamper(self) -> None:
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
            original_self = module.SELF
            module.SELF = Path(handle.name)
            try:
                self.assertNotEqual(module.seal()["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
            finally:
                module.SELF = original_self


if __name__ == "__main__":
    unittest.main()

