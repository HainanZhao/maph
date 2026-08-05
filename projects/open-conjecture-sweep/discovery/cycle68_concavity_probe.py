#!/usr/bin/env python3
"""Fast candidate selection plus exact replay for C68 sign polynomials."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

import numpy as np


def load(path: Path):
    rows = []
    with path.open(newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader)
        for row in reader:
            rows.append((tuple(map(int, row[:5])), Fraction(int(row[5]), int(row[6]))))
    return rows


def exact_value(rows, point):
    return sum(
        coefficient * np.prod([point[i] ** exponent[i] for i in range(5)])
        for exponent, coefficient in rows
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--object", choices=("concavity", "chord"), default="concavity")
    parser.add_argument("--samples", type=int, default=100_000)
    args = parser.parse_args()
    rng = np.random.default_rng(680068)
    report = {}
    for regime in ("low", "high"):
        source = args.input_dir / f"{args.object}-{regime}.tsv"
        if not source.exists():
            continue
        rows = load(source)
        degrees = [max(exponent[axis] for exponent, _ in rows) for axis in range(5)]
        best_value = float("inf")
        best_point = None
        remaining = args.samples
        while remaining:
            count = min(10_000, remaining)
            points = rng.random((count, 5))
            values = np.zeros(count)
            powers = [
                [points[:, axis] ** degree for degree in range(degrees[axis] + 1)]
                for axis in range(5)
            ]
            for exponent, coefficient in rows:
                term = float(coefficient)
                for axis, degree in enumerate(exponent):
                    term = term * powers[axis][degree]
                values += term
            index = int(np.argmin(values))
            if values[index] < best_value:
                best_value = float(values[index])
                best_point = points[index]
            remaining -= count
        rational_point = tuple(Fraction(float(value)).limit_denominator(10**6) for value in best_point)
        exact = exact_value(rows, rational_point)
        report[regime] = {
            "floating_minimum": best_value,
            "rational_point": [f"{value.numerator}/{value.denominator}" for value in rational_point],
            "exact_numerator": exact.numerator,
            "exact_denominator": exact.denominator,
            "exact_sign": -1 if exact < 0 else (1 if exact > 0 else 0),
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "samples_per_regime": args.samples,
        "object": args.object,
        "charts": report,
        "claim_boundary": "Floating selection; exact sign only at the two reported rational points.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
