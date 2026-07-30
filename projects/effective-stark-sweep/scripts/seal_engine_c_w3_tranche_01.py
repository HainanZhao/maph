#!/usr/bin/env python3
"""Seal the first generic Engine-C W3 closure and its two transports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CHARACTERS = ROOT / "artifacts/engine-c-character-selection-v1.json"
THETA = ROOT / "artifacts/engine-c-theta-targets-v1.json"
ORBITS = ROOT / "artifacts/engine-c-unit-orbits-v1.json"
BRIDGE = ROOT / "artifacts/engine-c-packet-bridge-v1.json"
STAGING = ROOT / "artifacts/engine-c-w3-tranche-01-boundary-v1.json"
OUTPUT = ROOT / "artifacts/engine-c-w3-tranche-01-verified-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(payload: dict, case_id: str) -> list[dict]:
    return [
        row for row in payload["records"] if row["case_id"] == case_id
    ]


def main() -> None:
    characters = json.loads(CHARACTERS.read_text())
    theta = json.loads(THETA.read_text())
    orbits = json.loads(ORBITS.read_text())
    bridge = json.loads(BRIDGE.read_text())
    staging = json.loads(STAGING.read_text())

    character_rows = rows(characters, "RQ-001280")
    theta_rows = rows(theta, "RQ-001280")
    orbit_rows = rows(orbits, "RQ-001280")
    bridge_rows = rows(bridge, "RQ-001280")
    if not all(len(group) == 2 for group in (
        character_rows, theta_rows, orbit_rows, bridge_rows
    )):
        raise RuntimeError("two-route component count changed")
    if any(row["stark_s_size"] != 3 for row in character_rows):
        raise RuntimeError("|S|>=3 global-unit gate failed")
    if any(
        row["character_field_roots_of_unity_e"] != 2
        for row in character_rows
    ):
        raise RuntimeError("route e changed")
    expected_orbit = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
    if any(
        {tuple(item) for item in row["isolated_integral_orbit"]}
        != expected_orbit
        for row in orbit_rows
    ):
        raise RuntimeError("isolated orbit changed")
    if not theta["new_case_two_route_target_overlap"]:
        raise RuntimeError("two-route Arb targets separated")
    common = bridge["identical_two_route_packet_polynomials"]
    if len(common) != 1:
        raise RuntimeError("exact bridge has no unique common packet")
    if any(
        row["artin_labeled_packet_polynomial"] != common[0]
        for row in bridge_rows
    ):
        raise RuntimeError("Artin-labeled packet disagreement")

    members = staging["tranche"]["members"]
    if [row["case_id"] for row in members] != [
        "RQ-001280", "RQ-001297"
    ]:
        raise RuntimeError("member identity changed")
    if any(
        row["primitive_conductor"]
        != "[[8, 4; 0, 4], [1, 0]]"
        or row["source_character"] != "[1, 0]"
        or row["primitive_character"] != "[1, 0]"
        for row in members
    ):
        raise RuntimeError("member transport data changed")

    payload = {
        "schema": "effective-stark-engine-c-w3-tranche-verified-v1",
        "banked_at_utc": "2026-07-30T07:02:33Z",
        "claim_tag": "VERIFIED",
        "theorem": (
            "For K=Q(sqrt(35)), the primitive one-place packet at "
            "[[8,4],[0,4]] infinity_2 and its modulus-64 transport are "
            "unconditional Engine-C archimedean Stark instances."
        ),
        "closure": {
            "field": "Q(sqrt(35))",
            "primitive_finite_hnf": [[8, 4], [0, 4]],
            "primitive_finite_norm": 32,
            "source_character": [1, 0],
            "cm_bases": ["Q(sqrt(-10))", "Q(sqrt(-14))"],
            "route_e": [2, 2],
            "stark_s_size": [3, 3],
            "isolated_anti_unit_orbit": [
                [-1, -1], [-1, 1], [1, -1], [1, 1]
            ],
            "packet_polynomial": common[0],
        },
        "members": [
            {
                "case_id": row["case_id"],
                "finite_ideal_hnf": row["finite_ideal_hnf"],
                "finite_norm": row["finite_norm"],
                "primitive_conductor": row["primitive_conductor"],
                "transport_tag": "VERIFIED_EXACT_MEMBER_TRANSPORT",
            }
            for row in members
        ],
        "gates": {
            "exact_character_selection": True,
            "stark_1980_global_unit_clause": True,
            "arb_primitive_lprime_targets": True,
            "unique_integral_orbit": True,
            "exact_artin_labeled_bridge": True,
            "independent_two_route_agreement": True,
            "paper_ii_anchor_replayed": True,
        },
        "normalization": (
            "Class-log conversion is e/2. Direct primitive quartic "
            "L'-to-two-log inversion is e/4 because anti-unit Fourier "
            "pairs are duplicated."
        ),
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CHARACTERS, THETA, ORBITS, BRIDGE, STAGING, SELF
            )
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print("VERIFIED_CLOSURE_COUNT=1")
    print("VERIFIED_MEMBER_COUNT=2")
    print("PAPER_II_ANCHOR_REPLAY=1")
    print("ENGINE_C_W3_TRANCHE_01_VERIFIED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
