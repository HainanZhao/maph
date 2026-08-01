#!/usr/bin/env python3
"""Seal the narrow literal-test correction for phase-lattice Base-saturation v1."""
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
OUTPUT = ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1-test-correction.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1.json", "3207a7764470d5512d20778e739e0e0bdc31535c0b2ac68b8366707304678534"),
    "v1_builder": (ROOT / "proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py", "bcd9d82eeb2cbb142258e166ce8dc29c4476528a59ed432a85701c17aa54f4d7"),
    "v1_conventions": (ROOT / "conventions/crr_phase_lattice_base_saturation_v1.py", "02d64afcb324858982042cd946ab66111d489eab65b45a9057ac57034e6ec8ef"),
    "v1_document": (ROOT / "docs/cycle-7-crr-phase-lattice-base-saturation-v1.md", "f6203aa929c354efcd65bce00f5b33864f2ebaccce99af6bf3770298fd364f81"),
    "v1_test": (ROOT / "tests/test_cycle_7_crr_phase_lattice_base_saturation_v1.py", "614f84fce97194c14ac10b3d2f938a69a3b8c4006f0949e2b4446732720693f6"),
    "correction_document": (ROOT / "docs/cycle-7-crr-phase-lattice-base-saturation-v1-test-correction.md", "40a0592f97ebc17a0c131f3f7458be58dd73cde8aa57ce4eb585ff512ec49df4"),
    "correction_test": (ROOT / "tests/test_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py", "b0a2fc66f91d46ea3fb78db672218eff39b4109a8b9abf2cf6f3eee1c146eda7"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "phase-lattice Base-saturation test correction requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(expected_hash != "AUTO", f"unfrozen input hash: {label}")
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
    require(artifact.get("artifact_id") == "cycle-7-crr-phase-lattice-base-saturation-v1", "v1 artifact identity mismatch")
    require(artifact.get("epistemic_status") == "PROVED", "v1 artifact status mismatch")
    original_test = INPUTS["v1_test"][0].read_text(encoding="utf-8")
    document = INPUTS["v1_document"][0].read_text(encoding="utf-8")
    corrected_test = INPUTS["correction_test"][0].read_text(encoding="utf-8")
    original_assertion = 'self.assertIn("Exact rational aliases offer only constant factors", document)'
    sealed_phrase = "exact aliases can therefore provide at most constant factors"
    corrected_assertion = 'self.assertIn("exact aliases can therefore provide at most constant factors", document)'
    require(original_assertion in original_test, "historical v1 literal defect is absent")
    require(sealed_phrase in document, "sealed v1 alias phrase mismatch")
    require(corrected_assertion in corrected_test, "corrected literal assertion is absent")
    return {"original_assertion": original_assertion, "sealed_phrase": sealed_phrase, "corrected_assertion": corrected_assertion}


def replay_v1() -> dict[str, str]:
    completed = subprocess.run([sys.executable, str(INPUTS["v1_builder"][0]), "--check"], cwd=ROOT, capture_output=True, text=True)
    require(completed.returncode == 0, f"v1 builder replay failed: {completed.stderr}")
    require("SEALED_PHASE_LATTICE_BASE_SATURATION_REDUCTION_LIGHTWEIGHT_CHECKED" in completed.stdout, "v1 replay status missing")
    return {"epistemic_status": "PROVED", "command": "python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py --check", "result": "v1 builder --check passed without changing the immutable artifact"}


def observe_historical_test_failure() -> dict[str, str]:
    completed = subprocess.run([sys.executable, "-m", "unittest", str(INPUTS["v1_test"][0])], cwd=ROOT, capture_output=True, text=True)
    combined = completed.stdout + completed.stderr
    require(completed.returncode != 0, "historical v1 literal test unexpectedly passed")
    require("Exact rational aliases offer only constant factors" in combined, "historical failure signature mismatch")
    return {"epistemic_status": "OBSERVED", "command": "python3 -m unittest tests/test_cycle_7_crr_phase_lattice_base_saturation_v1.py", "result": "one expected literal-string failure; no mathematical assertion failed"}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    wording = validate_correction()
    v1_replay = replay_v1()
    historical = observe_historical_test_failure()
    return {
        "artifact_id": "cycle-7-crr-phase-lattice-base-saturation-v1-test-correction",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_V1_PHASE_LATTICE_BASE_SATURATION_TEST_CORRECTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This correction records and repairs a literal test expectation only. It changes no mathematical statement, source anchor, convention, actual reduced-Farey label, alias quotient, Base-efficiency identity, v1 artifact field, or replay payload, and it proves no new Base/F4F/AFARI/CFARI/CRR-U result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "immutable-artifact hash pinning, literal-expectation comparison, v1 replay, contained historical-test replay, corrected replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "preserved_v1": {"artifact_id": "cycle-7-crr-phase-lattice-base-saturation-v1", "artifact_sha256": INPUTS["v1_artifact"][1], "statement": "The v1 artifact, builder, conventions, document, and original failing test are immutable inputs to this correction."},
        "correction": {"epistemic_status": "OBSERVED", "error": "The v1 test expected the literal 'Exact rational aliases offer only constant factors'; the sealed document says 'exact aliases can therefore provide at most constant factors'.", "cause": "A semantic paraphrase was encoded as an exact-string assertion.", "affected_claims": "none", "mathematical_change": "none", "source_change": "none", "artifact_payload_change": "none", "resolution": "Preserve v1 and use a new test that checks the exact sealed phrase."},
        "original_assertion": wording["original_assertion"],
        "sealed_phrase": wording["sealed_phrase"],
        "corrected_assertion": wording["corrected_assertion"],
        "v1_replay": v1_replay,
        "historical_test_observation": historical,
        "replay": {"write_command": "python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py --write", "check_command": "python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py --check", "test_command": "python3 -m unittest tests/test_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite phase-lattice Base-saturation v1 test-correction artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "phase-lattice Base-saturation v1 test-correction artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "phase-lattice Base-saturation v1 test-correction artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
