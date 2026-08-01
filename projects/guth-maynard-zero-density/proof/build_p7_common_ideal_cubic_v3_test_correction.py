#!/usr/bin/env python3
"""Seal the label-only test correction for P7-3 correction v2."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_common_ideal_cubic_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-common-ideal-cubic-v3-test-correction.json"
SELF = Path(__file__)
V2 = ROOT / "artifacts/p7-common-ideal-cubic-v2-correction.json"
V2_BUILDER = ROOT / "proof/build_p7_common_ideal_cubic_v2_correction.py"
FILES = {"document": ROOT / "docs/p7-common-ideal-cubic-v3-test-correction.md", "tests": ROOT / "tests/test_p7_common_ideal_cubic_v3_test_correction.py"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    require(V2.is_file(), "P7-3 v2 correction is absent")
    v2 = json.loads(V2.read_text())
    require(v2["corrected_claim"]["integer_replay"]["coloured_energy"] == 34, "P7-3 v2 corrected integer replay missing")
    require(v2["corrected_claim"]["integer_replay"]["orthogonality_parseval_count"] == 34, "P7-3 v2 Parseval replay missing")
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    return {
        "artifact_id": "p7-common-ideal-cubic-v3-test-correction",
        "epistemic_status": "OBSERVED",
        "immutable_v2": {"path": str(V2.relative_to(ROOT)), "sha256": digest(V2)},
        "defect": "The v2 test searched the unchanged-list for the literal phrase 'remains open'; that list instead says 'the open coloured primitive cubic estimate'. The builder and the substantive integer replay both pass.",
        "repair": "This v3 test checks the exact corrected integers and the semantic open-estimate phrase, not an accidental literal substring.",
        "unchanged": "No mathematical statement, source pin, v1/v2 artifact, or P7-3 gate boundary changes.",
        "artifact_identity": identities,
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/build_p7_common_ideal_cubic_v3_test_correction.py --write", "check_command": "python3 proof/build_p7_common_ideal_cubic_v3_test_correction.py --check"},
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    started = time.monotonic_ns()
    data = render(report())
    elapsed = time.monotonic_ns() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7-3 v3 correction exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7-3 v3 correction exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7-3 v3 correction")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7-3 v3 correction mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
