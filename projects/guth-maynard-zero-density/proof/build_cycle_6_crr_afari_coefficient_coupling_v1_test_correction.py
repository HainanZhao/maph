#!/usr/bin/env python3
"""Seal the narrow test correction for Cycle 6 CRR coefficient--Farey v1."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1-test-correction.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (
        ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json",
        "a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266",
    ),
    "v1_builder": (
        ROOT / "proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py",
        "42091bb6799e9357f840a77efede56b66d5c2c65a613bf3541779646466ec62e",
    ),
    "v1_conventions": (
        ROOT / "conventions/crr_afari_coupling_v1.py",
        "8d74815084b859a985de90cd1429bab734269f7373794dd81c5515fad49b6bbf",
    ),
    "v1_document": (
        ROOT / "docs/cycle-6-crr-afari-coefficient-coupling-v1.md",
        "5ed3d0d2c17e0e0766704e59c58d5a013f80a26243d13b8ff96fe6c63d54f9fe",
    ),
    "v1_test": (
        ROOT / "tests/test_cycle_6_crr_afari_coefficient_coupling_v1.py",
        "8e29c1a50b69c9e9574578e24f8a5cefa4c1862801efd35d1b0debdffe74bdb7",
    ),
    "correction_document": (
        ROOT / "docs/cycle-6-crr-afari-coefficient-coupling-v1-test-correction.md",
        "aa06602d62891627656fc9ed9429d5a6e2874ecbbbe1ab517b95efd3c8606b1a",
    ),
    "correction_test": (
        ROOT / "tests/test_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py",
        "07bfebc481cda3c3099b185ff41911e726c2c2bd1327314b8713cbdf6bb7973a",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "CRR AFARI test correction requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual_hash}
    return frozen


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def validate_correction() -> dict[str, str]:
    artifact = load_json(INPUTS["v1_artifact"][0])
    boundary = artifact.get("claim_boundary")
    require(isinstance(boundary, str) and "proves neither" in boundary, "v1 claim boundary wording mismatch")
    require(artifact.get("epistemic_status") == "PROVED", "v1 result status mismatch")
    original_test = INPUTS["v1_test"][0].read_text(encoding="utf-8")
    corrected_test = INPUTS["correction_test"][0].read_text(encoding="utf-8")
    original_assertion = 'self.assertIn("does not prove", data["claim_boundary"])'
    corrected_assertion = 'self.assertIn("proves neither", v1["claim_boundary"])'
    require(original_assertion in original_test, "historical v1 literal defect is absent")
    require(corrected_assertion in corrected_test, "corrected literal assertion is absent")
    return {
        "original_assertion": original_assertion,
        "corrected_assertion": corrected_assertion,
        "v1_boundary": boundary,
    }


def replay_v1() -> dict[str, str]:
    command = [sys.executable, str(INPUTS["v1_builder"][0]), "--check"]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    require(completed.returncode == 0, f"v1 builder replay failed: {completed.stderr}")
    require("SEALED_COEFFICIENT_FAREY_REDUCTION_LIGHTWEIGHT_CHECKED" in completed.stdout, "v1 replay status missing")
    return {
        "epistemic_status": "PROVED",
        "command": "python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py --check",
        "result": "v1 builder --check passed without changing the immutable artifact",
    }


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    wording = validate_correction()
    v1_replay = replay_v1()
    return {
        "artifact_id": "cycle-6-crr-afari-coefficient-coupling-v1-test-correction",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_V1_TEST_CORRECTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This correction records and repairs a literal test expectation only. It changes no mathematical statement, source anchor, convention, v1 artifact field, or replay payload, and it proves no new AFARI/CFARI/CRR-U result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {
            "lightweight_checks": "immutable-artifact hash pinning, literal-expectation check, v1 replay, corrected replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "preserved_v1": {
            "artifact_id": "cycle-6-crr-afari-coefficient-coupling-v1",
            "artifact_sha256": INPUTS["v1_artifact"][1],
            "statement": "The v1 artifact, builder, conventions, document, and original failing test are immutable inputs to this correction.",
        },
        "correction": {
            "epistemic_status": "OBSERVED",
            "error": "The v1 test expected the literal substring 'does not prove'; the sealed v1 claim boundary says 'proves neither'.",
            "cause": "A semantic paraphrase was encoded as an exact-string assertion.",
            "affected_claims": "none",
            "mathematical_change": "none",
            "source_change": "none",
            "artifact_payload_change": "none",
            "resolution": "Preserve v1; use a new corrected test that checks the exact sealed phrase 'proves neither'.",
        },
        "original_assertion": wording["original_assertion"],
        "corrected_assertion": wording["corrected_assertion"],
        "v1_claim_boundary": wording["v1_boundary"],
        "v1_replay": v1_replay,
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py",
        },
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite CRR AFARI v1 test-correction artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CRR AFARI v1 test-correction artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CRR AFARI v1 test-correction artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
