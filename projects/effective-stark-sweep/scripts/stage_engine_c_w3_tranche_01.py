#!/usr/bin/env python3
"""Stage the smallest Engine-C e={2,4} closure without over-promotion.

This is deliberately a boundary audit, not a W3 certificate.  It
replays the exact e-value computation once for the shared packet field,
checks every member occurrence against the frozen geometry transcript,
and refuses promotion because the repository has no generic
exact-character-table / Arb-orbit / exact-bridge pipeline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "artifacts/engine-c-e-inventory-v1.json"
GEOMETRY = ROOT / "artifacts/engine-c-geometry-full-v1.transcript"
CENSUS = ROOT / "artifacts/frozen-ideal-census-v1.json"
OPEN_PLAN = ROOT / "artifacts/post-theorem-bulk-plan-v1.json"
E_SCRIPT = ROOT / "scripts/screen_engine_c_e_values.gp"
THEORY = ROOT / "data/engine-c-general-e-theory-v1.json"
OUTPUT = ROOT / "artifacts/engine-c-w3-tranche-01-boundary-v1.json"
TRANSCRIPT = (
    ROOT / "artifacts/engine-c-w3-tranche-01-e-replay-v1.transcript"
)
FAILED = (
    ROOT
    / "artifacts/engine-c-w3-tranche-01-e-replay-failed-v0.transcript"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> str:
    matches = re.findall(
        rf"^{re.escape(key)}=(.*)$", text, flags=re.MULTILINE
    )
    if len(matches) != 1:
        raise RuntimeError(f"{key}: expected one value, got {len(matches)}")
    return matches[0]


def geometry_block(text: str, case_id: str, packet_index: int) -> str:
    marker = f"===== {case_id} PACKET {packet_index} =====\n"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"missing geometry block {case_id}/{packet_index}")
    body_start = start + len(marker)
    end = text.find("\n===== ", body_start)
    if end < 0:
        end = len(text)
    return text[body_start:end]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replay the frozen Engine-C tranche-01 boundary."
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="perform the exact replay and rewrite the frozen outputs",
    )
    args = parser.parse_args()
    if not args.run:
        parser.error("no action selected; pass --run")

    inventory = json.loads(INVENTORY.read_text())
    census = json.loads(CENSUS.read_text())
    open_plan = json.loads(OPEN_PLAN.read_text())
    geometry = GEOMETRY.read_text()

    # "Smallest" is frozen as the first field in the polynomial-sorted,
    # hash-banked exact inventory whose minimum e is 2 or 4.
    candidates = [
        record
        for record in inventory["field_records"]
        if record["minimum_e"] in (2, 4)
    ]
    selected = min(candidates, key=lambda record: record["field_index"])
    if selected["field_index"] != 1:
        raise RuntimeError("smallest open closure changed")
    expected_occurrences = [
        {"case_id": "RQ-001280", "packet_index": 1},
        {"case_id": "RQ-001297", "packet_index": 1},
    ]
    if selected["occurrences"] != expected_occurrences:
        raise RuntimeError("tranche-01 occurrence identity changed")
    if selected["minimum_e"] != 2 or selected["e_pair"] != [2, 2]:
        raise RuntimeError("tranche-01 frozen e inventory changed")

    open_cases = set(
        open_plan["engine_c"]["open_on_banked_e_2_4"]["case_ids"]
    )
    if any(
        occurrence["case_id"] not in open_cases
        for occurrence in expected_occurrences
    ):
        raise RuntimeError("tranche occurrence left the open e={2,4} queue")

    census_by_id = {
        record["case_id"]: record for record in census["cases"]
    }
    member_records = []
    for occurrence in expected_occurrences:
        case_id = occurrence["case_id"]
        packet_index = occurrence["packet_index"]
        census_record = census_by_id[case_id]
        block = geometry_block(geometry, case_id, packet_index)
        prefix = f"PACKET_{packet_index}_"
        if scalar(block, "CASE_ID") != case_id:
            raise RuntimeError(f"{case_id}: geometry identity mismatch")
        if int(scalar(block, "D")) != census_record["D"]:
            raise RuntimeError(f"{case_id}: geometry D mismatch")
        if int(scalar(block, "FINITE_NORM")) != census_record["finite_norm"]:
            raise RuntimeError(f"{case_id}: finite norm mismatch")
        if int(scalar(block, prefix + "C_GEOMETRY_PASS")) != 1:
            raise RuntimeError(f"{case_id}: geometry pass disappeared")
        polynomial = scalar(block, prefix + "ABSOLUTE_POLYNOMIAL")
        if polynomial != selected["absolute_polynomial"]:
            raise RuntimeError(f"{case_id}: packet-field mismatch")
        member_records.append(
            {
                "case_id": case_id,
                "packet_index": packet_index,
                "D": census_record["D"],
                "field_discriminant": census_record[
                    "field_discriminant"
                ],
                "finite_ideal_hnf": census_record["finite_ideal_hnf"],
                "finite_norm": census_record["finite_norm"],
                "source_character": scalar(
                    block, prefix + "SOURCE_CHARACTER"
                ),
                "primitive_conductor": scalar(
                    block, prefix + "PRIMITIVE_CONDUCTOR"
                ),
                "primitive_character": scalar(
                    block, prefix + "PRIMITIVE_CHARACTER"
                ),
                "linear_reinduction_bases": scalar(
                    block, prefix + "LINEAR_REINDUCTION_BASES"
                ),
                "geometry_pass": True,
                "w3_state": "BLOCKED_MISSING_GENERIC_W3",
            }
        )

    representative = expected_occurrences[0]
    prelude = (
        f'CASE_ID="{representative["case_id"]}";'
        f'PACKET_INDEX={representative["packet_index"]};'
        f'D_VALUE='
        f'{census_by_id[representative["case_id"]]["field_discriminant"]};'
        f'SOURCE_POLYNOMIAL={selected["absolute_polynomial"]};\n'
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=prelude + E_SCRIPT.read_text(),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=600,
        check=False,
    )
    replay = completed.stdout + (
        "\nSTDERR:\n" + completed.stderr if completed.stderr else ""
    )
    if (
        completed.returncode != 0
        or "ENGINE_C_E_INVENTORY_VERIFIED=1" not in completed.stdout
    ):
        FAILED.write_text(replay)
        raise RuntimeError(
            f"exact e replay failed; preserved as {FAILED.name}"
        )
    TRANSCRIPT.write_text(replay)
    route_count = int(scalar(completed.stdout, "ROUTE_COUNT"))
    replay_e = sorted(
        int(scalar(completed.stdout, f"ROUTE_{index}_E"))
        for index in range(1, route_count + 1)
    )
    if replay_e != selected["e_pair"]:
        FAILED.write_text(replay)
        TRANSCRIPT.unlink(missing_ok=True)
        raise RuntimeError(
            "inventory e mismatch; replay preserved as failure"
        )

    missing = [
        {
            "component": "exact_character_table",
            "required": (
                "complete compatible CM ray-character enumeration and "
                "injective exact Dirichlet-coefficient signature"
            ),
            "available_generic_stage": (
                "geometry screen supplies source and primitive ray "
                "characters but not the CM-side exhaustive coefficient table"
            ),
        },
        {
            "component": "arb_orbit_isolation",
            "required": (
                "rigorous Arb evaluation of the analytic target and unique "
                "integral logarithmic-unit orbit isolation"
            ),
            "available_generic_stage": (
                "no generic certified partial-zeta/L-prime evaluator or "
                "unit-lattice isolator exists; current implementations are "
                "case-specific anchors"
            ),
        },
        {
            "component": "exact_packet_bridge",
            "required": (
                "Artin-labeled exact normal-closure identities mapping the "
                "isolated CM orbit to every real member packet"
            ),
            "available_generic_stage": (
                "geometry proves field-level reinduction bases only; it "
                "does not construct member-specific packet identities"
            ),
        },
    ]
    output = {
        "schema": "effective-stark-engine-c-w3-tranche-boundary-v1",
        "recorded_at_utc": "2026-07-30T05:50:38Z",
        "claim_tag": "VERIFIED_STAGING_ONLY",
        "promotion_state": "BLOCKED_MISSING_GENERIC_W3",
        "tranche": {
            "tranche_id": "C-W3-TRANCHE-01",
            "selection_rule": (
                "first polynomial-sorted distinct packet field with "
                "minimum e in {2,4}"
            ),
            "field_index": selected["field_index"],
            "absolute_polynomial": selected["absolute_polynomial"],
            "minimum_e_expected": selected["minimum_e"],
            "route_e_expected": selected["e_pair"],
            "route_e_replayed": replay_e,
            "inventory_e_assertion": replay_e == selected["e_pair"],
            "closure_occurrence_count": selected["occurrence_count"],
            "members": member_records,
        },
        "completed_boundary": [
            "closure-batched exact e replay (once per packet field)",
            "exact inventory-e assertion",
            "per-member modulus and packet-field identity assertion",
            "exact source/primitive character and reinduction-base staging",
        ],
        "missing_promotion_components": missing,
        "promotion_boundary": (
            "No occurrence is promoted without all three missing components "
            "as replayable per-case certificates."
        ),
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                INVENTORY,
                GEOMETRY,
                CENSUS,
                OPEN_PLAN,
                E_SCRIPT,
                THEORY,
            )
        },
        "replay": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha256(TRANSCRIPT),
        },
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"TRANCHE_ID={output['tranche']['tranche_id']}")
    print(f"ROUTE_E_REPLAYED={replay_e}")
    print("INVENTORY_E_ASSERTION=1")
    print("PROMOTED_CASE_COUNT=0")
    print("PROMOTION_STATE=BLOCKED_MISSING_GENERIC_W3")
    print(f"OUTPUT_SHA256={sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
