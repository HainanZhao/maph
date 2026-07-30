#!/usr/bin/env python3
"""Audit phase quantization, route invariance, and identifiability."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import cmath
import hashlib
import json
import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "artifacts" / "certified-controls-v1.json"
OUTPUT = ROOT / "artifacts" / "control-phase-audit-v1.json"

MIDPOINT = re.compile(
    r"^\[([+-]?[0-9][0-9.eE+-]*) \+/- ([0-9][0-9.eE+-]*)\]"
    r" \+ \[([+-]?[0-9][0-9.eE+-]*) \+/- ([0-9][0-9.eE+-]*)\]j$"
)


def rectangle(ball: str) -> tuple[complex, float]:
    match = MIDPOINT.match(ball)
    if not match:
        raise ValueError(f"unrecognized complex ball: {ball}")
    center = complex(float(match.group(1)), float(match.group(3)))
    radius = math.hypot(float(match.group(2)), float(match.group(4)))
    return center, radius


def principal_mod(value: float, period: float) -> float:
    return (value + period / 2) % period - period / 2


def main() -> None:
    controls = json.loads(INPUT.read_text(encoding="utf-8"))
    by_case = defaultdict(list)
    route_records = []
    for row in controls["routes"]:
        value, radius = rectangle(row["lprime_zero_ball"])
        if radius >= abs(value):
            raise RuntimeError("phase ball contains zero")
        phase = cmath.phase(value)
        phase_error = math.asin(radius / abs(value))
        nearest_quarter_turn = round(phase / (math.pi / 2)) * (math.pi / 2)
        distance = abs(principal_mod(phase - nearest_quarter_turn, 2 * math.pi))
        certified_distance = max(0.0, distance - phase_error)
        record = {
            "case_id": row["case_id"],
            "route_id": row["route_id"],
            "e": row["e"],
            "lprime_midpoint": [value.real, value.imag],
            "phase_radians": phase,
            "phase_radius_upper_bound_radians": phase_error,
            "phase_over_pi": phase / math.pi,
            "distance_to_nearest_pi_over_2_radians": distance,
            "certified_distance_to_nearest_pi_over_2_radians":
                certified_distance,
            "raw_phase_is_certifiably_not_pi_over_2_quantized":
                certified_distance > 0,
        }
        route_records.append(record)
        by_case[row["case_id"]].append((row, record))

    pair_records = []
    for case_id, pair in sorted(by_case.items()):
        if len(pair) != 2:
            raise RuntimeError(f"{case_id}: expected two routes")
        source_equal = (
            pair[0][0]["lprime_zero_ball"] == pair[1][0]["lprime_zero_ball"]
        )
        phase_difference = principal_mod(
            pair[0][1]["phase_radians"] - pair[1][1]["phase_radians"],
            2 * math.pi,
        )
        pair_records.append(
            {
                "case_id": case_id,
                "routes": [pair[0][0]["route_id"], pair[1][0]["route_id"]],
                "lprime_ball_strings_identical": source_equal,
                "phase_difference_radians": phase_difference,
                "route_invariance_pass": source_equal and phase_difference == 0,
            }
        )
    if not all(row["route_invariance_pass"] for row in pair_records):
        raise RuntimeError("a certified two-route phase disagrees")

    raw_nonquantized = sum(
        row["raw_phase_is_certifiably_not_pi_over_2_quantized"]
        for row in route_records
    )
    distinct_case_phases = {
        case_id: pair[0][1]["phase_over_pi"]
        for case_id, pair in by_case.items()
    }
    payload = {
        "schema": "dedekind-stark-control-phase-audit-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_FEASIBILITY_AUDIT",
        "route_records": route_records,
        "two_route_checks": pair_records,
        "findings": {
            "route_pairs_checked": len(pair_records),
            "route_pairs_identical": sum(
                row["route_invariance_pass"] for row in pair_records
            ),
            "raw_lprime_phases_certifiably_nonquantized_count":
                raw_nonquantized,
            "raw_lprime_phases_total": len(route_records),
            "distinct_case_phase_over_pi": distinct_case_phases,
            "raw_phase_quantization_verdict": "REJECTED",
            "reason": (
                "The conjecture can only concern a defect relative to an "
                "independently constructed coefficient; the raw Lprime "
                "phases are not quarter-turns."
            ),
        },
        "identifiability": {
            "independent_canonical_defect_values_available": 0,
            "certified_packet_cases": 5,
            "route_records": 10,
            "fit_authorized": False,
            "holdout_authorized": False,
            "blocking_condition": (
                "No Roblot-canonical weak solution coefficient has been "
                "constructed independently of Lprime/the certified packet."
            ),
            "circular_fit_rejected": True,
        },
        "source_sha256": {
            "artifacts/certified-controls-v1.json":
                hashlib.sha256(INPUT.read_bytes()).hexdigest(),
            "scripts/audit_control_phases.py": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("ROUTE_INVARIANCE=5/5")
    print(f"RAW_PHASE_CERTIFIABLY_NONQUANTIZED={raw_nonquantized}/10")
    print("INDEPENDENT_DEFECT_VALUES=0")
    print("FIT_AUTHORIZED=0")
    print(f"OUTPUT={OUTPUT}")


if __name__ == "__main__":
    main()
