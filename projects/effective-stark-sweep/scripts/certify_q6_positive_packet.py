#!/usr/bin/env python3
"""Correct RQ-000129 by identifying the positive packet through both CM routes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
GENERIC = ROOT / "scripts/generic_engine_c_packet_bridge.gp"
OLD_CASE = ROOT / "data/q6-norm8-case-v2.json"
AUXILIARY = ROOT / "artifacts/q6-auxiliary-prime-independence-v1.json"
FIRST_CORRECTION = ROOT / "artifacts/q6-positive-packet-correction-v1.json"
OUTPUT = ROOT / "artifacts/q6-positive-packet-correction-v2.json"
TRANSCRIPT = ROOT / "artifacts/q6-positive-packet-correction-v2.transcript"

SELECTOR = "x^8-4*x^5-2*x^4-8*x^2-8*x-2"
ROUTES = [
    {
        "route_id": "Qsqrt(-2)",
        "character_field": "x^8-4*x^6-4*x^5+6*x^4+16*x^3+16*x^2+8*x+2",
        "isolated_coordinates": "[4,0]",
        "coordinate_divisor": 4,
        "root_coordinates": "[1,0]",
        "separator_prime": 3,
        "normalizing_power": 3,
    },
    {
        "route_id": "Qsqrt(-3)",
        "character_field": "x^8-2*x^6+5*x^4-4*x^2+1",
        "isolated_coordinates": "[6,0]",
        "coordinate_divisor": 6,
        "root_coordinates": "[1,0]",
        "separator_prime": 19,
        "normalizing_power": 2,
    },
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> str:
    values = re.findall(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
    if len(values) != 1:
        raise RuntimeError(f"{key}: expected one value, got {len(values)}")
    return values[0]


def run_bridge(
    source: str, route: dict, coordinates: str, normalizing_power: int | None
) -> tuple[dict, str]:
    marker = "  if(#Set(labeled_norms) != 4,"
    insertion = ""
    if normalizing_power is not None:
        insertion = (
            '  print("NORMALIZED_PACKET_POLYNOMIAL=", '
            f"minpoly(labeled_norms[1]^{normalizing_power}));\n"
        )
    if marker not in source:
        raise RuntimeError("generic bridge insertion marker changed")
    augmented = source.replace(marker, insertion + marker, 1)
    prelude = "\n".join(
        [
            'CASE_ID="RQ-000129";',
            f'ROUTE_ID="{route["route_id"]}";',
            f'CHARACTER_FIELD_POLYNOMIAL={route["character_field"]};',
            f"REAL_SELECTOR_FIELD_POLYNOMIAL={SELECTOR};",
            f"CANDIDATE_COORDINATES={coordinates};",
            f'SEPARATOR_PRIME={route["separator_prime"]};',
        ]
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=prelude + "\n" + augmented,
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=600,
        check=False,
    )
    if (
        completed.returncode != 0
        or "GENERIC_ENGINE_C_PACKET_BRIDGE_VERIFIED=1" not in completed.stdout
    ):
        raise RuntimeError(completed.stdout + completed.stderr)
    record = {
        "coordinates": coordinates,
        "anti_unit_minimal_polynomial": scalar(
            completed.stdout, "CANDIDATE_MINPOLY"
        ),
        "positive_norm_polynomial": scalar(
            completed.stdout, "ARTIN_LABELED_PACKET_POLYNOMIAL"
        ),
        "complex_conjugation_group_index": int(
            scalar(completed.stdout, "COMPLEX_CONJUGATION_GROUP_INDEX")
        ),
        "normal_sigma_group_index": int(
            scalar(completed.stdout, "NORMAL_SIGMA_GROUP_INDEX")
        ),
        "conjugation_fixed_norm_count": sum(
            int(
                scalar(
                    completed.stdout,
                    f"ARTIN_LABEL_{index}_CONJUGATION_FIXED",
                )
            )
            for index in range(4)
        ),
    }
    if normalizing_power is not None:
        record["normalized_packet_polynomial"] = scalar(
            completed.stdout, "NORMALIZED_PACKET_POLYNOMIAL"
        )
    return record, completed.stdout


def main() -> None:
    source = GENERIC.read_text(encoding="utf-8")
    records = []
    transcripts = []
    for route in ROUTES:
        isolated, isolated_transcript = run_bridge(
            source,
            route,
            route["isolated_coordinates"],
            route["normalizing_power"],
        )
        root, root_transcript = run_bridge(
            source, route, route["root_coordinates"], None
        )
        records.append(
            {
                **route,
                "isolated_stark_unit": isolated,
                "primitive_lattice_root": root,
            }
        )
        transcripts.append(
            f"===== {route['route_id']} isolated coordinates =====\n"
            f"{isolated_transcript}\n"
            f"===== {route['route_id']} primitive lattice root =====\n"
            f"{root_transcript}"
        )
    normalized = {
        row["isolated_stark_unit"]["normalized_packet_polynomial"]
        for row in records
    }
    if len(normalized) != 1:
        raise RuntimeError("the two routes do not give the same normalized packet")
    root_packets = {
        row["primitive_lattice_root"]["positive_norm_polynomial"]
        for row in records
    }
    if len(root_packets) != 1:
        raise RuntimeError("the two primitive lattice roots give different packets")
    normalized_power_packet = next(iter(normalized))
    packet = next(iter(root_packets))
    old = json.loads(OLD_CASE.read_text(encoding="utf-8"))
    old_polynomial = old["candidate_unit_minimal_polynomial"]
    root_check = subprocess.run(
        ["gp", "-q"],
        input=(
            f"p={packet};q={old_polynomial};\n"
            'print("NEW_REAL_ROOT_COUNT=",polsturm(p));\n'
            'print("NEW_NEGATIVE_ROOT_COUNT=",polsturm(p,-oo,0));\n'
            'print("NEW_POSITIVE_ROOTS=",polrootsreal(p));\n'
            'print("OLD_REAL_ROOT_COUNT=",polsturm(q));\n'
        ),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=60,
        check=False,
    )
    if root_check.returncode != 0:
        raise RuntimeError(root_check.stdout + root_check.stderr)
    new_real = int(scalar(root_check.stdout, "NEW_REAL_ROOT_COUNT"))
    new_negative = int(scalar(root_check.stdout, "NEW_NEGATIVE_ROOT_COUNT"))
    old_real = int(scalar(root_check.stdout, "OLD_REAL_ROOT_COUNT"))
    if new_real != 4 or new_negative != 0 or old_real != 0:
        raise RuntimeError("unexpected exact Sturm root count")
    transcripts.append("===== exact root check =====\n" + root_check.stdout)
    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-q6-positive-packet-correction-v1",
        "claim_tag": "VERIFIED_CORRECTION",
        "case_id": "RQ-000129",
        "field": "Q(sqrt(6))",
        "error_classification": (
            "The v2 record and results-paper equation (13) printed the "
            "minimal polynomial of the complex anti-unit epsilon and "
            "misidentified it as the positive packet."
        ),
        "normalization_correction": (
            "The first correction isolated the positive power identity "
            "q8^3=q12^2 but did not yet take the exact roots inside the "
            "certified anti-unit lattices. The isolated coordinates are "
            "divisible by 4 and 6. Dividing in the exact lattice and taking "
            "the positive CM norm gives the same X_A packet polynomial on "
            "both routes. The possible reciprocal has the same polynomial."
        ),
        "old_anti_unit_polynomial": old_polynomial,
        "old_anti_unit_real_root_count": old_real,
        "route_records": records,
        "exact_cross_route_identity": "q8^3=q12^2",
        "common_normalized_power_polynomial": normalized_power_packet,
        "correct_positive_packet_polynomial": packet,
        "correct_packet_real_root_count": new_real,
        "correct_packet_negative_root_count": new_negative,
        "correct_packet_positive_roots": scalar(
            root_check.stdout, "NEW_POSITIVE_ROOTS"
        ),
        "selector_field_signature": [4, 2],
        "verdict": "VERIFIED",
        "supersedes": {
            "case_record": {
                "path": str(OLD_CASE.relative_to(ROOT)),
                "sha256": sha(OLD_CASE),
            },
            "first_correction": {
                "path": str(FIRST_CORRECTION.relative_to(ROOT)),
                "sha256": sha(FIRST_CORRECTION),
            },
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (GENERIC, OLD_CASE, AUXILIARY, FIRST_CORRECTION, SELF)
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": "",
        },
    }
    payload["transcript"]["sha256"] = sha(TRANSCRIPT)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("ROUTE_COUNT=2")
    print("EXACT_CROSS_ROUTE_IDENTITY=q8^3=q12^2")
    print(f"NEW_REAL_ROOT_COUNT={new_real}")
    print(f"NEW_NEGATIVE_ROOT_COUNT={new_negative}")
    print(f"OLD_REAL_ROOT_COUNT={old_real}")
    print("Q6_POSITIVE_PACKET_CORRECTION_VERIFIED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
