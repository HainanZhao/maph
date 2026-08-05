#!/usr/bin/env python3
"""Read-only hostile audit of Cycle 4 P1R preregistration v2."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SCRIPT = ROOT / "proof/build_cycle_4_p1r_preregistration_v2.py"
ARTIFACT = ROOT / "artifacts/cycle-4-p1r-preregistration-v2.json"
DOCUMENT = ROOT / "docs/cycle-4-p1r-preregistration-v2-correction.md"
TESTS = ROOT / "tests/test_cycle_4_p1r_preregistration_v2.py"
SNAPSHOT = ROOT / "artifacts/cycle-4-p1r-authorization-snapshot-v1.json"
PROGRAM = ROOT / "PROGRAM.md"
PACKAGE = {
    "builder": "bee4c5fd044d4fed4db5c6907524e48c7c4a2c553beffce683dff685fa16cab0",
    "artifact": "2f988a4feea44f0bf88b7519d7eff80f120575c64c13c975a6660ee6d6f01853",
    "document": "31865f458d751c8a39258fb12e92b55e31b4fa0591a866c230efdef9220c11de",
    "tests": "132b4c0f82566c786d4514e7a341afae5145374390d8bd63e0778430e89c60f2",
    "snapshot": "cd42352b145f67af0289aa21b142f40fbc2aac891944bb49d054631384c176d0",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("p1r_v2_hostile_target", SCRIPT)
    require(spec is not None and spec.loader is not None, "cannot import P1R v2")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True).returncode


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3", "audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "audit requires non-optimized mode")
    paths = {"builder": SCRIPT, "artifact": ARTIFACT, "document": DOCUMENT, "tests": TESTS, "snapshot": SNAPSHOT}
    hashes: dict[str, str] = {}
    for label, path in paths.items():
        require(path.is_file(), f"v2 package member absent: {label}")
        actual = sha256(path)
        require(actual == PACKAGE[label], f"v2 package member hash mismatch: {label}")
        hashes[label] = actual

    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    require(payload["sealer"] == {"path": "proof/build_cycle_4_p1r_preregistration_v2.py", "sha256": PACKAGE["builder"]}, "v2 self identity is not bound")
    require(payload["p1r_fs"]["gate_status"] == "PREREGISTERED_UNEXECUTED" and payload["p1r_fs"]["completed_theorem"] is False, "FS unexecuted status mismatch")
    require(payload["p1r_crr"]["formalization_gate"]["search_authorized"] is False, "hidden CRR search authority")
    ledger = {entry["id"]: entry for entry in payload["source_hypothesis_ledger"]}
    require(ledger["GM-S3-FOUR-TERM"]["locator"].endswith("prpstn:S3") and ledger["GM-S3-FOUR-TERM"]["hypotheses"] == ["N >= T^(3/4)"], "four-term S3 correction mismatch")
    require(snapshot["observed_plan"]["historical_sha256"] == "ce8cfb2c4c196b53a0e823667da2ce4e840d7ce18c754a9be1423064d9fce479", "snapshot historical hash mismatch")
    require(set(snapshot["p1r_authorization"]) == {"crr_before_search", "crr_status", "fs_architecture", "fs_next_gate", "p1r_status"}, "snapshot authorization schema mismatch")

    documented = run([sys.executable, str(SCRIPT), "--check"])
    optimized = run([sys.executable, "-O", str(SCRIPT), "--check"])
    optimized_twice = run([sys.executable, "-OO", str(SCRIPT), "--check"])
    overwrite = run([sys.executable, str(SCRIPT), "--write"])
    require(documented == 0, "documented v2 replay fails")
    require(optimized != 0 and optimized_twice != 0, "v2 optimized mode does not fail closed")
    require(overwrite != 0, "v2 overwrite does not fail closed")

    module = load_module()
    program = PROGRAM.read_text(encoding="utf-8")
    p1r_complete = program.replace("| P1R | ACTIVE |", "| P1R | COMPLETE |", 1)
    later_p2 = program.replace("No P2A/P2B/P2C route is presently selected.", "P2B is selected by a later affirmative route decision.", 1)
    future_errors: dict[str, str] = {}
    for label, future in {"p1r_complete": p1r_complete, "later_affirmative_p2": later_p2}.items():
        try:
            module.check_current_program_text(future)
        except RuntimeError as error:
            future_errors[label] = str(error)
        else:
            raise RuntimeError(f"expected future PROGRAM status check failure absent: {label}")
    require("p1r_active" in future_errors["p1r_complete"], "P1R completion lifecycle defect was not exposed")
    require("no_p2_selection" in future_errors["later_affirmative_p2"], "later-P2 lifecycle defect was not exposed")

    with tempfile.TemporaryDirectory() as temporary:
        mutated = Path(temporary) / "gm-tex-tampered.tex"
        original = module.INPUTS["gm_tex"]
        mutated.write_bytes(original[0].read_bytes() + b"\n")
        module.INPUTS["gm_tex"] = (mutated, original[1])
        try:
            try:
                module.seal()
            except RuntimeError as error:
                require("frozen input hash mismatch: gm_tex" in str(error), "wrong source-tamper failure")
            else:
                raise RuntimeError("actual source tamper did not fail closed")
        finally:
            module.INPUTS["gm_tex"] = original

    return {
        "artifact_id": "cycle-4-p1r-preregistration-v2-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "FAIL_PLAN_LIFECYCLE_SEMANTIC_COUPLING",
        "claim_boundary": "Read-only audit of P1R v2. It records replay-lifecycle coupling and decides no P1R mathematical target.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audited_v2_hashes": hashes,
        "checks": {
            "documented_cli": "PASS",
            "self_identity": "PASS",
            "snapshot_hash_and_schema": "PASS",
            "four_term_source_and_range": "PASS",
            "FS_status": "PASS",
            "CRR_search_forbidden": "PASS",
            "actual_source_tamper": "PASS",
            "optimized_O": "PASS",
            "optimized_OO": "PASS",
            "overwrite": "PASS",
            "future_P1R_complete_replay": "FAIL",
            "future_affirmative_P2_replay": "FAIL",
        },
        "defect": "Although the authorization snapshot is immutable, v2 still executes a live PLAN semantic predicate requiring P1R ACTIVE and no P2 selection. Both are expected to change after legitimate future gates, so historic preregistration replay remains coupled to mutable operational state.",
        "future_errors": future_errors,
        "required_correction": [
            "For historical preregistration replay, validate only the immutable authorization snapshot and frozen source inputs; remove current PLAN state predicates from --check.",
            "Move live PLAN authorization compatibility into a separate operational preflight command that reports current eligibility but is not required to reproduce historic bytes.",
            "Add regressions for P1R ACTIVE->COMPLETE and later affirmative P2 selection, both of which must preserve historical replay while allowing operational preflight to change state.",
        ],
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    require(args.check.is_file(), "hostile audit artifact absent")
    recorded = json.loads(args.check.read_text(encoding="utf-8"))
    require(recorded.get("auditor") == result["auditor"], "hostile auditor identity mismatch")
    require(args.check.read_bytes() == render(result), "hostile audit artifact mismatch")
    print(json.dumps({"status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
