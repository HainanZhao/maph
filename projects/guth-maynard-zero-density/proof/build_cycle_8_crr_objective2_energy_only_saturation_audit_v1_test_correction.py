#!/usr/bin/env python3
"""Seal the literal-test correction for the EO-LF4 Objective-2 audit v1."""
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
OUTPUT = ROOT / "artifacts/cycle-8-crr-objective2-energy-only-saturation-audit-v1-test-correction.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (ROOT / "artifacts/cycle-8-crr-objective2-energy-only-saturation-audit-v1.json", "e62388fcd1f62460f438d73743920f6209c71fc353254984f45d74e71e416746"),
    "v1_builder": (ROOT / "proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py", "96d45c1686526f220f1720bad65efdc20de97ae83a319dfa88b3b6e1e5dab021"),
    "v1_conventions": (ROOT / "conventions/crr_objective2_energy_only_saturation_v1.py", "7d435f56ca1a9ce7ec9b97760fb62bc11f1944e470e669575a5a0089e4de0ac1"),
    "v1_document": (ROOT / "docs/cycle-8-crr-objective-2-energy-only-saturation-audit-v1.md", "c5d70e76808f62589290f5098d813c933d177c0eb714acd756c6ff2bfd3c8f34"),
    "v1_test": (ROOT / "tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py", "18a9f8b9943f6e2aaf1184382fa62d17512a22e7f532f4374636877d1fd0dd26"),
    "correction_document": (ROOT / "docs/cycle-8-crr-objective-2-energy-only-saturation-audit-v1-test-correction.md", "9cef00f9b9d04375ea0d494b47e856065c3b6679cc5179f3d9a45e6d9ea264a2"),
    "correction_test": (ROOT / "tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py", "32d8899d0fa43da33a23c4ee94742965e1053c9abfcb447a6b90ce364debcee2"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "EO-LF4 Objective-2 audit test correction requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(expected != "AUTO", f"unfrozen input hash: {label}")
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def validate_correction() -> dict[str, str]:
    artifact = load_json(INPUTS["v1_artifact"][0])
    require(artifact.get("artifact_id") == "cycle-8-crr-objective2-energy-only-saturation-audit-v1", "v1 artifact identity mismatch")
    require(artifact.get("epistemic_status") == "PROVED", "v1 artifact status mismatch")
    original_test = INPUTS["v1_test"][0].read_text(encoding="utf-8")
    corrected_test = INPUTS["correction_test"][0].read_text(encoding="utf-8")
    original_assertion = 'self.assertIn("for every fixed epsilon>0", theorem["upper_quantifier"])'
    sealed_phrase = "For every fixed epsilon>0"
    corrected_assertion = 'self.assertIn("For every fixed epsilon>0", v1["sharp_eolf4_theorem"]["upper_quantifier"])'
    require(original_assertion in original_test, "historical v1 literal defect is absent")
    require(sealed_phrase in artifact.get("sharp_eolf4_theorem", {}).get("upper_quantifier", ""), "sealed v1 capitalization mismatch")
    require(corrected_assertion in corrected_test, "corrected literal assertion is absent")
    require(artifact.get("objective_2_assessment", {}).get("status") == "SATISFIED_FOR_EO_LF4_SCOPED_GM_SUBARCHITECTURE", "v1 objective-2 decision mismatch")
    return {"original_assertion": original_assertion, "sealed_phrase": sealed_phrase, "corrected_assertion": corrected_assertion}


def replay_v1() -> dict[str, str]:
    completed = subprocess.run([sys.executable, str(INPUTS["v1_builder"][0]), "--check"], cwd=ROOT, capture_output=True, text=True)
    require(completed.returncode == 0, f"v1 builder replay failed: {completed.stderr}")
    require("SEALED_OBJECTIVE2_EO_LF4_SCOPED_SATURATION_AUDIT_LIGHTWEIGHT_CHECKED" in completed.stdout, "v1 replay status missing")
    return {"epistemic_status": "PROVED", "command": "python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py --check", "result": "v1 builder --check passed without changing the immutable artifact"}


def observe_historical_test_failure() -> dict[str, str]:
    completed = subprocess.run([sys.executable, "-m", "unittest", str(INPUTS["v1_test"][0])], cwd=ROOT, capture_output=True, text=True)
    combined = completed.stdout + completed.stderr
    require(completed.returncode != 0, "historical v1 literal test unexpectedly passed")
    require("for every fixed epsilon>0" in combined, "historical failure signature mismatch")
    return {"epistemic_status": "OBSERVED", "command": "python3 -m unittest tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py", "result": "one expected case-only literal-string failure; no mathematical assertion failed"}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    wording = validate_correction()
    replay = replay_v1()
    historical = observe_historical_test_failure()
    return {
        "artifact_id": "cycle-8-crr-objective2-energy-only-saturation-audit-v1-test-correction",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_V1_EO_LF4_OBJECTIVE2_AUDIT_TEST_CORRECTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This correction records and repairs a case-only literal test expectation. It changes no mathematical statement, source anchor, objective-2 assessment, architecture, sharp exponent, exclusion, Base/full-CRR gate, v1 artifact field, or replay payload.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "immutable-artifact hash pinning, literal comparison, v1 replay, contained historical-test replay, corrected replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "preserved_v1": {"artifact_id": "cycle-8-crr-objective2-energy-only-saturation-audit-v1", "artifact_sha256": INPUTS["v1_artifact"][1], "statement": "The v1 artifact, builder, conventions, document, and original failing test are immutable inputs to this correction."},
        "correction": {"epistemic_status": "OBSERVED", "error": "The v1 test expected lower-case 'for every fixed epsilon>0'; the sealed theorem starts 'For every fixed epsilon>0'.", "cause": "A case-sensitive exact-string assertion was not aligned to the sealed sentence capitalization.", "affected_claims": "none", "mathematical_change": "none", "source_change": "none", "artifact_payload_change": "none", "resolution": "Preserve v1 and use a corrected test that checks the exact capitalized phrase."},
        "original_assertion": wording["original_assertion"],
        "sealed_phrase": wording["sealed_phrase"],
        "corrected_assertion": wording["corrected_assertion"],
        "v1_replay": replay,
        "historical_test_observation": historical,
        "replay": {"write_command": "python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py --write", "check_command": "python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py --check", "test_command": "python3 -m unittest tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite EO-LF4 Objective-2 audit v1 test-correction artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "EO-LF4 Objective-2 audit v1 test-correction artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "EO-LF4 Objective-2 audit v1 test-correction artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
