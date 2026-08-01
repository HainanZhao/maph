#!/usr/bin/env python3
"""Seal the versioned correction for P7 detector local occupancy v1."""
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
from conventions import p7_detector_local_occupancy_v2 as C
from conventions.proof_runtime_v2 import require_pinned_runtime
from proof import build_p7_detector_local_occupancy_v1 as V1


OUT = ROOT / "artifacts/p7-detector-local-occupancy-v2-correction.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_detector_local_occupancy_v2.py",
    "document": ROOT / "docs/p7-detector-local-occupancy-v2.md",
    "correction_document": ROOT / "docs/p7-detector-local-occupancy-v2-correction.md",
    "tests": ROOT / "tests/test_p7_detector_local_occupancy_v2.py",
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
        require(path.is_file() and digest(path) == row["sha256"], f"pinned correction source mismatch: {label}")
        rows[label] = dict(row)
    base = V1.report()
    require(V1.OUT.is_file() and V1.OUT.read_bytes() == V1.render(base), "sealed v1 result no longer replays")
    for label, row in base["source_integrity"].items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"v1 transitive source mismatch: {label}")
        rows[f"v1_{label}"] = dict(row)
    require(base["artifact_id"] == "p7-detector-local-occupancy-v1", "unexpected v1 artifact identity")
    require(base["gate_outcome"] == "CONTAINED_DETECTOR_SIDE_OCCUPANCY_OBSTRUCTION_GATE_REMAINS_OPEN", "v1 gate assessment changed")
    return rows, base


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    sources, base = source_integrity()
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    data = copy.deepcopy(base)
    data["artifact_id"] = "p7-detector-local-occupancy-v2-correction"
    data["claim_boundary"] = "Versioned correction of two regression-test string assertions only. The v1 mathematical result, source pins, exact-conductor convention, zero extension, and gate assessment are unchanged."
    data["correction"] = {
        "status": "PROVED",
        "supersedes": {
            "artifact": "p7-detector-local-occupancy-v1.json",
            "sha256": C.SOURCES["p7_detector_local_occupancy_v1"]["sha256"],
        },
        "defect": "The sealed v1 test used two lower-case substring expectations while the v1 artifact uses sentence-initial 'One common' and the precise phrase 'exact finite conductor'. Its Markdown source also lost several TeX backslashes during generation, including mathfrak commands and two beta commands rendered as control characters.",
        "cause": "Regression assertions were written case-sensitively against prose rather than normalized semantic fields; the v1 Markdown was passed through a string layer that interpreted backslash escapes.",
        "affected_claims": "None. The defects are confined to two test assertions and v1 prose rendering; v1's builder replay, source pins, algebraic checks, and all mathematical statements remain valid.",
        "remedy": "The v2 test checks the actual artifact wording, the v2 companion document restates every mathematical formula with literal TeX escapes, and the v2 builder replays the sealed v1 artifact byte-for-byte before emitting this correction.",
    }
    data["source_integrity"] = sources
    data["artifact_identity"] = identities
    data["non_promotion"] = list(C.NON_PROMOTION)
    data["resource_contract"] = C.RESOURCE_LIMITS
    data["replay"] = {
        "script": str(SELF.relative_to(ROOT)),
        "script_sha256": digest(SELF),
        "runtime": runtime,
        "write_command": "python3 proof/build_p7_detector_local_occupancy_v2.py --write",
        "check_command": "python3 proof/build_p7_detector_local_occupancy_v2.py --check",
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7 detector occupancy correction replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7 detector occupancy correction replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 detector occupancy correction artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7 detector occupancy correction artifact mismatch; issue a further versioned correction")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
