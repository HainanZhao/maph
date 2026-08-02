#!/usr/bin/env python3
"""Exact smallest prototype for Cycle 163's fixed-full-ray selector.

This is intentionally only finite integer arithmetic.  In particular it
does not evaluate a spectral packet, choose a logarithm branch, or invoke a
ray-class implementation.  A non-coprime principal ideal is already an
exact falsifier of the named fixed-full-ray direct-selector class.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


DIMENSION = 6
DISCRIMINANT = 21
ANCHORS = {(3, 5): 1, (3, 4): 2}


def is_positive_at_selected_embedding(b: int, lift: int) -> bool:
    """Exactly decide b*(5-sqrt(21))/2 - lift > 0 for b >= 0."""

    left = 5 * b - 2 * lift
    if left <= 0:
        return False
    return left * left > DISCRIMINANT * b * b


def positive_lift(a: int, b: int) -> int:
    """Largest lift congruent to a mod 6 that is positive at beta'."""

    for candidate in range(a, a - 4 * DIMENSION, -DIMENSION):
        if is_positive_at_selected_embedding(b, candidate):
            if is_positive_at_selected_embedding(b, candidate + DIMENSION):
                raise AssertionError("positive lift was not maximal")
            return candidate
    raise AssertionError("positive lift search exceeded frozen finite range")


def norm(lift: int, b: int) -> int:
    return lift * lift - 5 * lift * b + b * b


def shintani_step(point: tuple[int, int]) -> tuple[int, int]:
    a, b = point
    return ((5 * a + b) % DIMENSION, (-a) % DIMENSION)


def orbit(point: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    result: list[tuple[int, int]] = []
    current = point
    while current not in result:
        result.append(current)
        current = shintani_step(current)
    if current != point:
        raise AssertionError("Shintani action did not close at initial point")
    return tuple(result)


def build_payload() -> dict[str, object]:
    rows = []
    row_by_point = {}
    for a in range(DIMENSION):
        for b in range(DIMENSION):
            lift = positive_lift(a, b)
            value = norm(lift, b)
            record = {
                "characteristic": [a, b],
                "positive_lift": lift,
                "norm": value,
                "coprime_to_6": math.gcd(abs(value), DIMENSION) == 1,
            }
            rows.append(record)
            row_by_point[(a, b)] = record

    seen: set[tuple[int, int]] = set()
    orbit_records = []
    for point in row_by_point:
        if point in seen:
            continue
        points = orbit(point)
        seen.update(points)
        flags = [row_by_point[item]["coprime_to_6"] for item in points]
        orbit_records.append(
            {
                "orbit": [list(item) for item in points],
                "length": len(points),
                "fixed_full_ray_eligibility": flags,
                "eligibility_constant": len(set(flags)) == 1,
            }
        )

    ineligible = [
        record["characteristic"] for record in rows if not record["coprime_to_6"]
    ]
    anchors = {
        f"{a},{b}": {
            "frozen_ray_log": label,
            "eligible": row_by_point[(a, b)]["coprime_to_6"],
        }
        for (a, b), label in ANCHORS.items()
    }
    totality = not ineligible
    orbit_invariance = all(record["eligibility_constant"] for record in orbit_records)
    return {
        "schema": "sic-stark-cycle-163-fixed-full-ray-selector-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "This exact finite computation only tests the fixed-full-ray "
            "direct-selector domain. It does not define a logarithm, finite "
            "part, AFK cocycle, ray-monoid lift, Stark value, or TCC identity."
        ),
        "conventions": {
            "field": "Q(sqrt(21)); beta^2-5*beta+1=0",
            "selected_embedding": "beta'=(5-sqrt(21))/2",
            "positive_lift": "largest p*=a mod 6 with b*beta'-p*>0",
            "norm": "p*^2-5*p*b+b^2",
            "full_modulus": "(6)infinity_2",
            "shintani_action": "T(a,b)=(5a+b,-a) mod 6",
            "orientation": "arithmetic Frobenius g=[(4beta+1)]",
        },
        "rows": rows,
        "summary": {
            "rows_checked": len(rows),
            "eligible_rows": len(rows) - len(ineligible),
            "ineligible_rows": len(ineligible),
            "ineligible_characteristics": ineligible,
            "fixed_full_ray_total": totality,
            "shintani_orbit_count": len(orbit_records),
            "all_orbits_have_length_three": all(
                record["length"] == 3 for record in orbit_records
            ),
            "eligibility_is_shintani_invariant": orbit_invariance,
            "orientation_anchors": anchors,
            "label_multiplicity_test": (
                "NOT_REACHED: fixed-full-ray totality is a prerequisite"
                if not totality
                else "REQUIRES_RAY_DISCRETE_LOG_IMPLEMENTATION"
            ),
        },
        "shintani_orbits": orbit_records,
        "gate_outcome": {
            "fixed_full_ray_direct_selector": (
                "FALSIFIED_BY_NONCOPRIME_ROWS" if not totality else "SURVIVES_DOMAIN_TEST"
            ),
            "next_engine_if_falsified": (
                "characteristic-dependent conductor-lowering/ray-monoid lift "
                "with orientation-preserving common-target map"
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = build_payload()
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
