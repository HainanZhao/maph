from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/build_cycle_4_p1r_preregistration_v2.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v2.json"


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_v2_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle4P1RPreregistrationV2Tests(unittest.TestCase):
    def test_v2_status_and_v1_preservation(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "SEALED_PREREGISTRATION")
        self.assertEqual(data["discovery_authorization"], "PROHIBITED_PENDING_CRR_FORMALIZATION")
        self.assertTrue(data["correction"]["preserves_v1"])
        self.assertNotIn("plan", data["frozen_hashes"])
        # The sealed v2 JSON retains its historical field spelling; the live
        # program check is exercised separately below.
        self.assertFalse(data["current_plan_semantic_check"]["byte_hash_pinned"])

    def test_four_term_source_and_fs_gate_are_distinct(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        ledger = {item["id"]: item for item in data["source_hypothesis_ledger"]}
        self.assertEqual(ledger["GM-S3-REFINED-TWO-TERM"]["statement"], "two-term refined S3 upper bound")
        self.assertEqual(ledger["GM-S3-FOUR-TERM"]["hypotheses"], ["N >= T^(3/4)"])
        self.assertEqual(data["p1r_fs"]["identity_algebra"]["epistemic_status"], "PROVED")
        self.assertEqual(data["p1r_fs"]["gate_status"], "PREREGISTERED_UNEXECUTED")
        self.assertFalse(data["p1r_fs"]["completed_theorem"])

    def test_documented_command_is_verbatim_parser_command(self) -> None:
        document = (PROJECT / "docs/cycle-4-p1r-preregistration-v2-correction.md").read_text(encoding="utf-8")
        command = "python3 proof/build_cycle_4_p1r_preregistration_v2.py --check"
        self.assertIn(command, document)
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)

    def test_semantic_program_mutation_passes_but_clause_deletion_fails(self) -> None:
        module = load_module()
        program = (PROJECT / "PROGRAM.md").read_text(encoding="utf-8")
        harmless = program.replace("source-anchored recovery", "source informed recovery", 1)
        self.assertEqual(set(module.check_current_program_text(harmless)), {"p1r_active", "fs_branch", "crr_branch", "crr_pre_search", "no_p2_selection"})
        deleted = program.replace("Before any search, a versioned preregistration must freeze:", "", 1)
        with self.assertRaisesRegex(RuntimeError, "current PROGRAM semantic clause missing: crr_pre_search"):
            module.check_current_program_text(deleted)

    def test_runtime_overwrite_self_identity_and_source_tamper(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
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


if __name__ == "__main__":
    unittest.main()
