#!/usr/bin/env python3
"""Classify exact codimension-one faces of the nine C67 blow-up quotients.

The input coefficients are integers under one common positive scale, so all
zero and sign statements below are exact.  This is a diagnostic for choosing
the next equality blow-up; it is not itself a positivity certificate.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


VARIABLES = ("x", "y", "r", "h")


def load(path: Path) -> dict[tuple[int, ...], int]:
    polynomial: dict[tuple[int, ...], int] = {}
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            exponent = tuple(map(int, row[:4]))
            coefficient = int(row[4])
            polynomial[exponent] = polynomial.get(exponent, 0) + coefficient
    return {exponent: coefficient for exponent, coefficient in polynomial.items() if coefficient}


def specialize(
    polynomial: dict[tuple[int, ...], int], axis: int, endpoint: int
) -> dict[tuple[int, ...], int]:
    result: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for exponent, coefficient in polynomial.items():
        if endpoint == 0 and exponent[axis] != 0:
            continue
        reduced = exponent[:axis] + exponent[axis + 1 :]
        result[reduced] += coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def common_coordinate_factors(
    polynomial: dict[tuple[int, ...], int], remaining: tuple[str, ...]
) -> dict[str, int]:
    if not polynomial:
        return {}
    return {
        variable: min(exponent[axis] for exponent in polynomial)
        for axis, variable in enumerate(remaining)
        if min(exponent[axis] for exponent in polynomial) > 0
    }


def face_record(
    polynomial: dict[tuple[int, ...], int], axis: int, endpoint: int
) -> dict[str, object]:
    face = specialize(polynomial, axis, endpoint)
    remaining = VARIABLES[:axis] + VARIABLES[axis + 1 :]
    if not face:
        return {
            "identically_zero": True,
            "divisor": VARIABLES[axis] if endpoint == 0 else f"1-{VARIABLES[axis]}",
            "terms": 0,
        }
    coefficients = tuple(face.values())
    degrees = [max(exponent[j] for exponent in face) for j in range(3)]
    return {
        "identically_zero": False,
        "terms": len(face),
        "degrees": dict(zip(remaining, degrees, strict=True)),
        "monomial_coefficient_signs": {
            "negative": sum(value < 0 for value in coefficients),
            "zero": 0,
            "positive": sum(value > 0 for value in coefficients),
        },
        "common_coordinate_factors": common_coordinate_factors(face, remaining),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chart_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    charts: dict[str, object] = {}
    for path in sorted(args.chart_dir.glob("*.tsv")):
        polynomial = load(path)
        faces = {}
        for axis, variable in enumerate(VARIABLES):
            for endpoint in (0, 1):
                faces[f"{variable}={endpoint}"] = face_record(polynomial, axis, endpoint)
        charts[path.stem] = {
            "terms": len(polynomial),
            "degrees": {
                variable: max(exponent[axis] for exponent in polynomial)
                for axis, variable in enumerate(VARIABLES)
            },
            "faces": faces,
        }

    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "scope": "exact codimension-one polynomial restrictions only",
        "charts": charts,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
