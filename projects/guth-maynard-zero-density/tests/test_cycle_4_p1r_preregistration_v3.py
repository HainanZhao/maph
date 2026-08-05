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
SCRIPT = PROJECT / "proof/build_cycle_4_p1r_preregistration_v3.py"
ARTIFACT = PROJECT / "artifacts/cycle-4-p1r-preregistration-v3.json"
PREFLIGHT = PROJECT / "proof/preflight_cycle_4_p1r_current_plan_v1.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle4P1RPreregistrationV3Tests(unittest.TestCase):
    def test_status_identity_and_preserved_hostile_failures(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "SEALED_PREREGISTRATION")
        self.assertEqual(data["discovery_authorization"], "PROHIBITED_PENDING_CRR_FORMALIZATION")
        self.assertTrue(data["correction"]["preserves_v1"])
        self.assertTrue(data["correction"]["preserves_v2"])
        self.assertEqual(data["correction"]["pinned_hostile_failures"], {"v1": "FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS", "v2": "FAIL_PLAN_LIFECYCLE_SEMANTIC_COUPLING"})
        self.assertFalse(data["historical_replay"]["current_plan_read"])
        self.assertEqual(data["historical_replay"]["current_plan_eligibility"], "EXCLUDED_FROM_HISTORICAL_ARTIFACT")
        self.assertNotIn("plan", data["frozen_hashes"])
        self.assertEqual(data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())

    def test_source_attribution_fs_status_and_crr_prohibition(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        ledger = {item["id"]: item for item in data["source_hypothesis_ledger"]}
        self.assertEqual(ledger["GM-S3-REFINED-TWO-TERM"]["statement"], "two-term refined S3 upper bound")
        self.assertEqual(ledger["GM-S3-FOUR-TERM"]["locator"], "GM TeX lines 1828--1835, prpstn:S3")
        self.assertEqual(ledger["GM-S3-FOUR-TERM"]["hypotheses"], ["N >= T^(3/4)"])
        self.assertEqual(data["p1r_fs"]["identity_algebra"]["epistemic_status"], "PROVED")
        self.assertEqual(data["p1r_fs"]["gate_status"], "PREREGISTERED_UNEXECUTED")
        self.assertFalse(data["p1r_fs"]["completed_theorem"])
        self.assertFalse(data["p1r_crr"]["formalization_gate"]["search_authorized"])

    def test_historical_replay_ignores_legitimate_plan_lifecycle_changes(self) -> None:
        builder = load_module(SCRIPT, "p1r_v3_historical")
        preflight = load_module(PREFLIGHT, "p1r_v3_preflight")
        self.assertNotIn("PROGRAM.md", SCRIPT.read_text(encoding="utf-8"))
        active = """| P1R | ACTIVE |\nP1R-FS: fixed-splice obstruction\nP1R-CRR: critical rational/random compatibility\nBefore any search, a versioned preregistration must freeze:\nNo P2A/P2B/P2C route is presently selected.\n"""
        completed = active.replace("| P1R | ACTIVE |", "| P1R | COMPLETE |", 1)
        later_p2 = active.replace("No P2A/P2B/P2C route is presently selected.", "P2B is selected by a later affirmative route decision.", 1)
        initial_bytes = builder.render(builder.seal())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cases = {"active": (active, "ELIGIBLE_CURRENT_PLAN"), "completed": (completed, "INELIGIBLE_CURRENT_PLAN"), "later_p2": (later_p2, "INELIGIBLE_CURRENT_PLAN")}
            for label, (text, expected) in cases.items():
                path = root / f"{label}.md"
                path.write_text(text, encoding="utf-8")
                result = preflight.evaluate(path)
                self.assertEqual(result["status"], expected)
                self.assertEqual(builder.render(builder.seal()), initial_bytes)

    def test_documented_cli_runtime_overwrite_and_source_tamper(self) -> None:
        document = (PROJECT / "docs/cycle-4-p1r-preregistration-v3-lifecycle-correction.md").read_text(encoding="utf-8")
        self.assertIn("python3 proof/build_cycle_4_p1r_preregistration_v3.py --check", document)
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)
        overwrite = subprocess.run([sys.executable, str(SCRIPT), "--write"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(overwrite.returncode, 0)
        for flag in ("-O", "-OO"):
            result = subprocess.run([sys.executable, flag, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-optimized CPython 3.12.3", result.stderr)
        module = load_module(SCRIPT, "p1r_v3_tamper")
        original = module.INPUTS["gm_tex"]
        module.INPUTS["gm_tex"] = (original[0], "0" * 64)
        with self.assertRaisesRegex(RuntimeError, "frozen input hash mismatch: gm_tex"):
            module.seal()


if __name__ == "__main__":
    unittest.main()
