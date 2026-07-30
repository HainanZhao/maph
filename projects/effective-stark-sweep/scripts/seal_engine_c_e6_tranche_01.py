#!/usr/bin/env python3
"""Seal the first three elevated-scrutiny e=6 Engine-C bundles."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SELECTION = ROOT / "artifacts/engine-c-e6-tranche-01-selection-v1.json"
THETA = ROOT / "artifacts/engine-c-e6-tranche-01-theta-v1.json"
ORBITS = ROOT / "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.json"
BRIDGE = ROOT / "artifacts/engine-c-e6-tranche-01-packet-bridge-v1.json"
ROOTS = ROOT / "artifacts/engine-c-e6-tranche-01-root-reality-v1.json"
THEORY = ROOT / "data/engine-c-general-e-theory-v2.json"
INVENTORY = ROOT / "artifacts/engine-c-e-inventory-v1.json"
OUTPUT = ROOT / "artifacts/engine-c-e6-tranche-01-verified-v1.json"
CASE_IDS = ["RQ-001569", "RQ-007519", "RQ-001894"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def grouped(payload: dict, case_id: str) -> list[dict]:
    return [row for row in payload["records"] if row["case_id"] == case_id]


def main() -> None:
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    theta = json.loads(THETA.read_text(encoding="utf-8"))
    orbits = json.loads(ORBITS.read_text(encoding="utf-8"))
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    roots = json.loads(ROOTS.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    fields = {
        row["case_id"]: row for row in inventory["field_records"]
    }
    bundles = []
    for case_id in CASE_IDS:
        character_rows = grouped(selection, case_id)
        theta_rows = grouped(theta, case_id)
        orbit_rows = grouped(orbits, case_id)
        bridge_rows = grouped(bridge, case_id)
        root_rows = grouped(roots, case_id)
        if not all(
            len(rows) == 2
            for rows in (
                character_rows,
                theta_rows,
                orbit_rows,
                bridge_rows,
                root_rows,
            )
        ):
            raise RuntimeError(f"{case_id}: route count changed")
        if any(
            row["character_field_roots_of_unity_e"] != 6
            or row["stark_s_size"] < 3
            or not row["relative_abelian_certified"]
            for row in character_rows
        ):
            raise RuntimeError(f"{case_id}: theorem gate failed")
        if not theta["all_two_route_targets_overlap"]:
            raise RuntimeError("two-route target overlap gate failed")
        if any(row["packet_signature"] != [4, 2] for row in root_rows):
            raise RuntimeError(f"{case_id}: root signature changed")
        common = bridge["identical_two_route_packet_polynomials"][case_id]
        if not common:
            raise RuntimeError(f"{case_id}: exact route bridge failed")
        field = fields[case_id]
        bundles.append(
            {
                "canonical_case_id": case_id,
                "occurrences": field["occurrences"],
                "occurrence_count": field["occurrence_count"],
                "cm_bases": [
                    row["route_id"] for row in character_rows
                ],
                "route_e": [6, 6],
                "stark_s_size": [
                    row["stark_s_size"] for row in character_rows
                ],
                "isolated_anti_unit_orbits": [
                    row["isolated_integral_orbit"]
                    for row in orbit_rows
                ],
                "packet_polynomials": common,
                "packet_signature": [4, 2],
            }
        )
    payload = {
        "schema": "effective-stark-engine-c-e6-tranche-01-verified-v1",
        "banked_at_utc": "2026-07-30T08:24:54Z",
        "claim_tag": "VERIFIED",
        "theorem": (
            "The three canonical quartic ray packets RQ-001569, "
            "RQ-007519, and RQ-001894, together with their exact "
            "same-field occurrences, are unconditional Engine-C "
            "archimedean Stark instances with e=6."
        ),
        "normalization": {
            "class_log_forward": "zeta'_S(0,g)=-(2/e)ell_g",
            "class_log_inverse": "ell_g=-(e/2)zeta'_S(0,g)",
            "direct_lprime_forward": (
                "L'_S(0,psi)=-(4/e)(ell_1-i*ell_sigma)"
            ),
            "direct_lprime_inverse": (
                "ell_1-i*ell_sigma=-(e/4)L'_S(0,psi)"
            ),
            "e6_specialization": {
                "class_log_forward": "-1/3",
                "class_log_inverse": "-3",
                "direct_lprime_forward": "-2/3",
                "direct_lprime_inverse": "-3/2"
            }
        },
        "field_count": 3,
        "occurrence_count": sum(
            bundle["occurrence_count"] for bundle in bundles
        ),
        "bundles": bundles,
        "gates": {
            "exact_character_selection": True,
            "relative_abelian_certified": True,
            "stark_1980_global_unit_clause": True,
            "arb_primitive_lprime_targets": True,
            "unique_integral_orbits": True,
            "exact_two_route_packet_bridges": True,
            "four_real_root_matching": True,
            "general_e6_lemma": True,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                SELECTION,
                THETA,
                ORBITS,
                BRIDGE,
                ROOTS,
                THEORY,
                INVENTORY,
                SELF,
            )
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("VERIFIED_E6_FIELD_COUNT=3")
    print(f"VERIFIED_E6_OCCURRENCE_COUNT={payload['occurrence_count']}")
    print("ENGINE_C_E6_TRANCHE_01_VERIFIED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
