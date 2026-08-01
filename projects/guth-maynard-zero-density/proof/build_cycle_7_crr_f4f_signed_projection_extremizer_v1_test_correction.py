#!/usr/bin/env python3
"""Seal the narrow literal-test correction for signed F4F extremizer v1."""
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
OUTPUT = ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json", "9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796"),
    "v1_builder": (ROOT / "proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py", "3778d85bca3559861b3fb0167b2d0b65eb8ead9e7a9b50e1685d3326fe2477c1"),
    "v1_conventions": (ROOT / "conventions/crr_f4f_signed_projection_extremizer_v1.py", "62e569e2e63ecd4b02671157866f0b71872264d4367e0ff8d443cde9fae582a1"),
    "v1_document": (ROOT / "docs/cycle-7-crr-f4f-signed-projection-extremizer-v1.md", "fabe2df4b91d4b38eca3cfb9e2357f430033ae4ad1c671beb341775b463340a2"),
    "v1_test": (ROOT / "tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1.py", "a063e0abbcfbac9568f0317681e4335ead39561ff394c4347ce3d3fcf05ffbf5"),
    "correction_document": (ROOT / "docs/cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction.md", "22f159dd953e9a4bb5b80a6bb38f580e6354fbbc602c4b7c238253246945cd9d"),
    "correction_test": (ROOT / "tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py", "39332402637c7a98c9cba53ef7b499c97d5f9080646226f7188f9b955cdb4304"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "signed F4F extremizer test correction requires non-optimized CPython 3.12.3")
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
    require(artifact.get("artifact_id") == "cycle-7-crr-f4f-signed-projection-extremizer-v1", "v1 artifact identity mismatch")
    require(artifact.get("epistemic_status") == "PROVED", "v1 artifact status mismatch")
    original_test = INPUTS["v1_test"][0].read_text(encoding="utf-8")
    document = INPUTS["v1_document"][0].read_text(encoding="utf-8")
    corrected_test = INPUTS["correction_test"][0].read_text(encoding="utf-8")
    original_assertion = 'self.assertIn("F4F_eta fails on this energy/spaced/cardinality class", document)'
    sealed_phrase = "of `F4F_eta` fails on this energy/spaced/cardinality class"
    corrected_assertion = 'self.assertIn("of `F4F_eta` fails on this energy/spaced/cardinality class", document)'
    require(original_assertion in original_test, "historical v1 literal defect is absent")
    require(sealed_phrase in document, "sealed v1 formatted phrase mismatch")
    require(corrected_assertion in corrected_test, "corrected literal assertion is absent")
    require("refutes `F4F_eta` on the actual Base class" in document, "v1 Base boundary wording mismatch")
    return {"original_assertion": original_assertion, "sealed_phrase": sealed_phrase, "corrected_assertion": corrected_assertion}


def replay_v1() -> dict[str, str]:
    completed = subprocess.run([sys.executable, str(INPUTS["v1_builder"][0]), "--check"], cwd=ROOT, capture_output=True, text=True)
    require(completed.returncode == 0, f"v1 builder replay failed: {completed.stderr}")
    require("SEALED_SIGNED_F4F_PROJECTION_AND_ENERGY_ONLY_NO_GO_LIGHTWEIGHT_CHECKED" in completed.stdout, "v1 replay status missing")
    return {"epistemic_status": "PROVED", "command": "python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py --check", "result": "v1 builder --check passed without changing the immutable artifact"}


def observe_historical_test_failure() -> dict[str, str]:
    completed = subprocess.run([sys.executable, "-m", "unittest", str(INPUTS["v1_test"][0])], cwd=ROOT, capture_output=True, text=True)
    combined = completed.stdout + completed.stderr
    require(completed.returncode != 0, "historical v1 literal test unexpectedly passed")
    require("F4F_eta fails on this energy/spaced/cardinality class" in combined, "historical failure signature mismatch")
    return {"epistemic_status": "OBSERVED", "command": "python3 -m unittest tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1.py", "result": "one expected literal-string failure; no mathematical assertion failed"}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    wording = validate_correction()
    v1_replay = replay_v1()
    historical = observe_historical_test_failure()
    return {
        "artifact_id": "cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_V1_SIGNED_F4F_EXTREMIZER_TEST_CORRECTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This correction records and repairs a literal test expectation only. It changes no mathematical statement, source anchor, convention, actual Farey label, jitter interval, v1 artifact field, or replay payload, and it proves no new F4F/AFARI/CFARI/CRR-U result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "immutable-artifact hash pinning, literal-expectation comparison, v1 replay, contained historical-test replay, corrected replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "preserved_v1": {"artifact_id": "cycle-7-crr-f4f-signed-projection-extremizer-v1", "artifact_sha256": INPUTS["v1_artifact"][1], "statement": "The v1 artifact, builder, conventions, document, and original failing test are immutable inputs to this correction."},
        "correction": {"epistemic_status": "OBSERVED", "error": "The v1 test expected an unformatted literal; the sealed document says 'of `F4F_eta` fails on this energy/spaced/cardinality class'.", "cause": "A semantically related paraphrase was encoded as an exact-string assertion.", "affected_claims": "none", "mathematical_change": "none", "source_change": "none", "artifact_payload_change": "none", "resolution": "Preserve v1 and use a new test that checks the exact sealed formatted phrase."},
        "original_assertion": wording["original_assertion"],
        "sealed_phrase": wording["sealed_phrase"],
        "corrected_assertion": wording["corrected_assertion"],
        "v1_replay": v1_replay,
        "historical_test_observation": historical,
        "replay": {"write_command": "python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py --write", "check_command": "python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py --check", "test_command": "python3 -m unittest tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite signed F4F extremizer v1 test-correction artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "signed F4F extremizer v1 test-correction artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "signed F4F extremizer v1 test-correction artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
