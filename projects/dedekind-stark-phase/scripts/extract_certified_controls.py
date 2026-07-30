#!/usr/bin/env python3
"""Extract the five certified Engine-C controls without copying proofs."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "effective-stark-sweep"
OUTPUT = ROOT / "artifacts" / "certified-controls-v1.json"


def load(relative: str) -> dict:
    return json.loads((SOURCE / relative).read_text(encoding="utf-8"))


def sha(relative: str) -> str:
    return hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest()


def main() -> None:
    q35 = load("artifacts/engine-c-theta-targets-v1.json")
    e6 = load("artifacts/engine-c-e6-tranche-01-theta-v1.json")
    q6 = load("artifacts/q6-auxiliary-prime-independence-v1.json")
    theorem = load("artifacts/engine-c-w3-tranche-01-verified-v1.json")
    correction = load(
        "artifacts/engine-c-e6-primitive-packet-correction-v1.json"
    )
    q6_case = load("data/q6-norm8-case-v3.json")

    field_data = {
        "RQ-001280": {
            "D": 35,
            "field": "Q(sqrt(35))",
            "packet_polynomial": theorem["closure"]["packet_polynomial"],
            "status": "VERIFIED",
        },
        "RQ-001569": {
            "D": 42,
            "field": "Q(sqrt(42))",
            "packet_polynomial": correction["case_polynomials"]["RQ-001569"],
            "status": "VERIFIED_AFTER_CORRECTION",
        },
        "RQ-007519": {
            "D": 186,
            "field": "Q(sqrt(186))",
            "packet_polynomial": correction["case_polynomials"]["RQ-007519"],
            "status": "VERIFIED_AFTER_CORRECTION",
        },
        "RQ-001894": {
            "D": 51,
            "field": "Q(sqrt(51))",
            "packet_polynomial": correction["case_polynomials"]["RQ-001894"],
            "status": "VERIFIED_AFTER_CORRECTION",
        },
        "RQ-000129": {
            "D": 6,
            "field": "Q(sqrt(6))",
            "packet_polynomial": q6_case["cross_route"][
                "common_packet_polynomial"
            ],
            "status": "VERIFIED_E8_ROUTE",
        },
    }

    routes = []
    for row in q35["records"]:
        if row["case_id"] != "RQ-001280":
            continue
        routes.append(
            {
                "case_id": row["case_id"],
                "route_id": row["route_id"],
                "e": 2,
                "lprime_zero_ball": row["lprime_zero_ball"],
                "root_number_ball": row["root_number_ball"],
                "selected_cm_character": row["selected_cm_character"],
                "analytic_conductor": row["analytic_conductor"],
                "role": "CERTIFIED_CONTROL",
            }
        )
    for row in e6["records"]:
        routes.append(
            {
                "case_id": row["case_id"],
                "route_id": row["route_id"],
                "e": 6,
                "lprime_zero_ball": row["lprime_zero_ball"],
                "root_number_ball": row["root_number_ball"],
                "selected_cm_character": row["selected_cm_character"],
                "analytic_conductor": row["analytic_conductor"],
                "role": "CERTIFIED_CONTROL",
            }
        )
    for row in q6["route_records"]:
        routes.append(
            {
                "case_id": "RQ-000129",
                "route_id": row["route_id"],
                "e": row["e"],
                "lprime_zero_ball": row["primitive_lprime_ball"],
                "root_number_ball": None,
                "selected_cm_character": None,
                "analytic_conductor": None,
                "role": (
                    "CERTIFIED_CONTROL"
                    if row["e"] == 8
                    else "QUARANTINED_ROUTE_CROSSCHECK"
                ),
            }
        )

    routes.sort(key=lambda row: (row["case_id"], row["route_id"]))
    if len(routes) != 10:
        raise RuntimeError(f"expected ten route controls, found {len(routes)}")
    route_counts = {}
    for case_id in field_data:
        route_counts[case_id] = sum(
            row["case_id"] == case_id for row in routes
        )
    if set(route_counts.values()) != {2}:
        raise RuntimeError(f"each case must have two routes: {route_counts}")

    source_paths = [
        "artifacts/engine-c-theta-targets-v1.json",
        "artifacts/engine-c-e6-tranche-01-theta-v1.json",
        "artifacts/q6-auxiliary-prime-independence-v1.json",
        "artifacts/engine-c-w3-tranche-01-verified-v1.json",
        "artifacts/engine-c-e6-primitive-packet-correction-v1.json",
        "data/q6-norm8-case-v3.json",
    ]
    payload = {
        "schema": "dedekind-stark-certified-controls-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_SOURCE_EXTRACTION",
        "case_count": len(field_data),
        "route_count": len(routes),
        "cases": [
            {"case_id": case_id, **field_data[case_id]}
            for case_id in sorted(field_data)
        ],
        "routes": routes,
        "independence_warning": (
            "These are independent proof controls for route agreement, "
            "not independent values of a Roblot phase defect."
        ),
        "source_sha256": {path: sha(path) for path in source_paths},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("CERTIFIED_CONTROLS=5")
    print("ROUTE_CONTROLS=10")
    print(f"OUTPUT={OUTPUT}")


if __name__ == "__main__":
    main()
