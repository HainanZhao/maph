#!/usr/bin/env python3
"""Seal the exact direct coprime-Euler geometry classification."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "artifacts/engine-b-transport-ledger-v4.json"
FEATURES = ROOT / "discovery/engine-b-global-coprime-geometry-v1.json"
PREREG = ROOT / "docs/cycle-133-engine-b-global-geometry-preregistration.md"
CORRECTION = ROOT / "docs/cycle-134-engine-b-integral-basis-correction.md"
OUT = ROOT / "artifacts/engine-b-global-coprime-geometry-audit-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-artifact", action="store_true")
    args = parser.parse_args()
    ledger, features = load(LEDGER), load(FEATURES)
    for relative, expected in features["source_hashes"].items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"feature source drift: {relative}")
    if sha256(ROOT / features["transcript"]["path"]) != features["transcript"]["sha256"]:
        raise RuntimeError("feature transcript drift")
    if ledger["counts"] != {"v5_engine_b_rows": 232, "member_transport_completed": 12, "member_transport_open": 220}:
        raise RuntimeError("transport population drift")
    if features["population"] != {"closures": 88, "members": 232, "directions": 1012}:
        raise RuntimeError("geometry population drift")
    pairs = [pair for closure in features["closures"] for pair in closure["pairs"]]
    statuses = Counter(pair["status"] for pair in pairs)
    expected = {"GEOMETRICALLY_ELIGIBLE": 145, "NORM_OBSTRUCTED": 758, "SOURCE_PRIME_OBSTRUCTED": 109}
    if dict(statuses) != expected or len(pairs) != 1012:
        raise RuntimeError("global geometry counts changed")
    if any(pair["status"] == "TOOL_FAILURE" for pair in pairs):
        raise RuntimeError("tool failure prevents route-impossibility classification")

    open_ids = {row["case_id"] for row in ledger["members"] if row["transport_status"] != "PROVED_EXACT_MEMBER_TRANSPORT"}
    incoming = {case_id: [] for case_id in open_ids}
    for pair in pairs:
        if pair["status"] == "GEOMETRICALLY_ELIGIBLE" and pair["target_case_id"] in incoming:
            incoming[pair["target_case_id"]].append(pair["source_case_id"])
    geometric_open = sorted(case_id for case_id, sources in incoming.items() if sources)
    route_obstructed = sorted(case_id for case_id, sources in incoming.items() if not sources)
    if (len(geometric_open), len(route_obstructed)) != (104, 116):
        raise RuntimeError("open-member classification drift")
    expected_corrections = {
        "B5-021": ("RQ-002057", ["RQ-002079"]),
        "B5-033": ("RQ-002955", ["RQ-002964", "RQ-002983"]),
        "B5-086": ("RQ-001107", ["RQ-001115", "RQ-001125", "RQ-001132", "RQ-001133", "RQ-001149", "RQ-001164", "RQ-001172"]),
    }
    corrections = {}
    for closure_id, (source, targets) in expected_corrections.items():
        actual = sorted(pair["target_case_id"] for closure in features["closures"] if closure["closure_id"] == closure_id for pair in closure["pairs"] if pair["status"] == "GEOMETRICALLY_ELIGIBLE" and pair["source_case_id"] == source)
        if actual != targets:
            raise RuntimeError(f"{closure_id} integral-basis correction drift")
        corrections[closure_id] = {"source_case_id": source, "eligible_target_case_ids": actual}
    result = {
        "schema": "effective-stark-engine-b-global-coprime-geometry-audit-v1",
        "status": "PASS_EXACT_GEOMETRY_CLASSIFICATION",
        "claim_boundary": "This seals only the direct coprime-deletion geometry route. GEOMETRICALLY_ELIGIBLE directions require a separate source, Euler-factor, Artin-label, and orientation proof; ROUTE_OBSTRUCTED is not a packet no-go.",
        "claim_tag": "PROVED_EXACT_TRANSPORT_GEOMETRY",
        "population": features["population"],
        "direction_status_counts": dict(sorted(statuses.items())),
        "open_member_partition": {"open_members": 220, "proved_new_transports": 0, "route_obstructed_direct_coprime": len(route_obstructed), "source_or_proof_open": len(geometric_open), "route_obstructed_case_ids": route_obstructed, "source_or_proof_open_case_ids": geometric_open},
        "integral_basis_correction": {"claim_tag": "PROVED_EXACT_GEOMETRY", "affected_closures": corrections, "withdrawn_artifacts": ["artifacts/b5086-transport-geometry-v1.json", "artifacts/final-direct-source-coprime-screen-v1.json"]},
        "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (LEDGER, FEATURES, PREREG, CORRECTION, Path(__file__))},
    }
    if args.write_artifact:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    elif not OUT.exists() or load(OUT) != result:
        raise RuntimeError("sealed geometry audit differs from replay")
    print("ENGINE_B_GLOBAL_COPRIME_GEOMETRY_AUDIT=PASS")
    print("ENGINE_B_DIRECT_ROUTE_OBSTRUCTED=116")
    print("ENGINE_B_SOURCE_OR_PROOF_OPEN=104")


if __name__ == "__main__":
    main()
