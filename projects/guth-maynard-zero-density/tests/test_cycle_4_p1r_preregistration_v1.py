from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/build_cycle_4_p1r_preregistration_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_preregistration_v1_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle4P1RPreregistrationV1Tests(unittest.TestCase):
    def test_sealed_artifact_has_no_search_authority(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "SEALED_PREREGISTRATION_NO_SEARCH_AUTHORIZED")
        self.assertFalse(data["p1r_crr"]["formalization_gate"]["search_authorized"])
        self.assertEqual(data["p1r_crr"]["formalization_gate"]["status"], "FORMALIZATION_REQUIRED_NO_SEARCH")
        self.assertIsNone(data["resource_policy"]["rng_seed"])

    def test_source_ledger_separates_theorem_and_heuristic(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        ledger = {row["id"]: row for row in data["source_hypothesis_ledger"]}
        self.assertEqual(ledger["GM-T1.1"]["epistemic_status"], "PROVED")
        self.assertEqual(ledger["GM-P11.1"]["epistemic_status"], "PROVED")
        self.assertEqual(ledger["GM-S3"]["epistemic_status"], "PROVED")
        self.assertEqual(ledger["GM-AFF"]["epistemic_status"], "PROVED")
        self.assertEqual(ledger["GM-CRITICAL-REMARK"]["epistemic_status"], "OBSERVED")

    def test_exact_scale_bookkeeping(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        bookkeeping = data["p1r_crr"]["scale_bookkeeping"]
        self.assertEqual(bookkeeping["monomial_scales"], {"E_formal": 20, "H": 12, "L": 10, "M": 2, "Q": 4, "R_cardinality": 8, "R_over_M": 6, "T_global": 13, "U": 12, "V": 7})
        self.assertEqual(bookkeeping["large_values_term_exponents_in_v"], ["6", "8", "8"])
        self.assertEqual(bookkeeping["energy_term_exponents_in_v"], ["20", "20", "20"])
        self.assertEqual(bookkeeping["refined_s3_term_exponents_in_v"], ["36", "36", "36", "36"])
        self.assertEqual(bookkeeping["source_variable_relabeling"]["source_R_function"], "mathcal_R_W")

    def test_replay_and_executable_identity(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["path"], "proof/build_cycle_4_p1r_preregistration_v1.py")
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)

    def test_optimized_modes_fail_closed(self) -> None:
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)

    def test_frozen_hash_tamper_fails_closed(self) -> None:
        module = load_module()
        original = module.INPUTS["gm_tex"]
        module.INPUTS["gm_tex"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: gm_tex"):
            module.seal()

    def test_unsealed_formalization_cannot_be_promoted(self) -> None:
        module = load_module()
        payload = module.seal()
        tampered = copy.deepcopy(payload)
        tampered["p1r_crr"]["formalization_gate"]["search_authorized"] = True
        self.assertNotEqual(module.render(tampered), module.render(payload))
        self.assertFalse(payload["p1r_crr"]["formalization_gate"]["search_authorized"])


if __name__ == "__main__":
    unittest.main()
