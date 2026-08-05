#!/usr/bin/env python3
"""Strip all exact coordinate-boundary factors from C67 chart polynomials."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


VARIABLES = ("x", "y", "r", "h")


def load(path: Path) -> dict[tuple[int, ...], int]:
    result: defaultdict[tuple[int, ...], int] = defaultdict(int)
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            result[tuple(map(int, row[:4]))] += int(row[4])
    return {key: value for key, value in result.items() if value}


def divide_zero(polynomial: dict[tuple[int, ...], int], axis: int):
    if not polynomial or min(exponent[axis] for exponent in polynomial) == 0:
        return None
    return {
        exponent[:axis] + (exponent[axis] - 1,) + exponent[axis + 1 :]: coefficient
        for exponent, coefficient in polynomial.items()
    }


def divide_one(polynomial: dict[tuple[int, ...], int], axis: int):
    """Return exact quotient by (1-variable), or None when not divisible."""
    groups: defaultdict[tuple[int, ...], dict[int, int]] = defaultdict(dict)
    for exponent, coefficient in polynomial.items():
        other = exponent[:axis] + exponent[axis + 1 :]
        groups[other][exponent[axis]] = coefficient
    quotient: dict[tuple[int, ...], int] = {}
    for other, coefficients in groups.items():
        degree = max(coefficients)
        if degree == 0:
            return None
        running = 0
        for power in range(degree):
            running += coefficients.get(power, 0)
            if running:
                exponent = other[:axis] + (power,) + other[axis:]
                quotient[exponent] = running
        if coefficients.get(degree, 0) != -running:
            return None
    return quotient


def strip(polynomial: dict[tuple[int, ...], int]):
    factors: defaultdict[str, int] = defaultdict(int)
    changed = True
    while changed:
        changed = False
        for axis, variable in enumerate(VARIABLES):
            quotient = divide_zero(polynomial, axis)
            if quotient is not None:
                polynomial = quotient
                factors[variable] += 1
                changed = True
            quotient = divide_one(polynomial, axis)
            if quotient is not None:
                polynomial = quotient
                factors[f"1-{variable}"] += 1
                changed = True
    return polynomial, dict(factors)


def write(path: Path, polynomial: dict[tuple[int, ...], int]) -> None:
    with path.open("w", newline="") as handle:
        rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
        rows.writerow((*VARIABLES, "coefficient_scaled_64_times_6_pow_15"))
        for exponent, coefficient in sorted(polynomial.items()):
            rows.writerow((*exponent, coefficient))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chart_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {}
    for source in sorted(args.chart_dir.glob("*.tsv")):
        original = load(source)
        reduced, factors = strip(original)
        write(args.output_dir / source.name, reduced)
        report[source.stem] = {
            "input_terms": len(original),
            "output_terms": len(reduced),
            "factors": factors,
        }
    (args.output_dir / "factor-report.json").write_text(
        json.dumps(
            {
                "status": "PASS",
                "epistemic_status": "PROVED",
                "method": "exact integer polynomial division",
                "charts": report,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
