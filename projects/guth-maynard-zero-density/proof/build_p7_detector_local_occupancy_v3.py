#!/usr/bin/env python3
"""Seal the second versioned harness correction for P7 local occupancy."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_detector_local_occupancy_v3 as C
from conventions.proof_runtime_v2 import require_pinned_runtime
from proof import build_p7_detector_local_occupancy_v2 as V2


OUT = ROOT / "artifacts/p7-detector-local-occupancy-v3-correction.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_detector_local_occupancy_v3.py",
    "document": ROOT / "docs/p7-detector-local-occupancy-v3-correction.md",
    "corrected_companion": ROOT / "docs/p7-detector-local-occupancy-v2.md",
    "tests": ROOT / "tests/test_p7_detector_local_occupancy_v3.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_integrity() -> tuple[dict[str, object], dict[str, object]]:
    rows: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"pinned second-correction source mismatch: {label}")
        rows[label] = dict(row)
    base = V2.report()
    require(V2.OUT.is_file() and V2.OUT.read_bytes() == V2.render(base), "sealed v2 correction no longer replays")
    for label, row in base["source_integrity"].items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"v2 transitive source mismatch: {label}")
        rows[f"v2_{label}"] = dict(row)
    require(base["artifact_id"] == "p7-detector-local-occupancy-v2-correction", "unexpected v2 correction identity")
    require(base["gate_outcome"] == "CONTAINED_DETECTOR_SIDE_OCCUPANCY_OBSTRUCTION_GATE_REMAINS_OPEN", "v2 gate assessment changed")
    return rows, base


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    sources, base = source_integrity()
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    data = copy.deepcopy(base)
    data["artifact_id"] = "p7-detector-local-occupancy-v3-correction"
    data["claim_boundary"] = "Versioned correction of one remaining v2 regression-test prose assertion only. The v1 mathematical result, v2 corrected companion document, source pins, exact-conductor convention, zero extension, and gate assessment are unchanged."
    data["correction"] = {
        "status": "PROVED",
        "supersedes": {
            "artifact": "p7-detector-local-occupancy-v2-correction.json",
            "sha256": C.SOURCES["p7_detector_local_occupancy_v2"]["sha256"],
        },
        "defect": "The v2 test expected the literal phrase 'zero extension' in an artifact field whose mathematically equivalent wording ends 'this extension'.",
        "cause": "One remaining test inspected an incidental prose phrase rather than the semantic zero-extension convention.",
        "affected_claims": "None. The defect is confined to one v2 regression assertion; the v1/v2 builders, source pins, algebraic checks, corrected companion document, and mathematical statements remain valid.",
        "remedy": "The v3 test checks the invariant chi(a)=0 off the exact conductor's coprime ideals together with the field's explicit extension wording, rather than requiring an incidental adjacent phrase.",
    }
    data["source_integrity"] = sources
    data["artifact_identity"] = identities
    data["non_promotion"] = list(C.NON_PROMOTION)
    data["resource_contract"] = C.RESOURCE_LIMITS
    data["replay"] = {
        "script": str(SELF.relative_to(ROOT)),
        "script_sha256": digest(SELF),
        "runtime": runtime,
        "write_command": "python3 proof/build_p7_detector_local_occupancy_v3.py --write",
        "check_command": "python3 proof/build_p7_detector_local_occupancy_v3.py --check",
    }
    return data


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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7 detector occupancy second correction replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7 detector occupancy second correction replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 detector occupancy second correction artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7 detector occupancy second correction artifact mismatch; issue a further versioned correction")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
