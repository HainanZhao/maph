#!/usr/bin/env python3
"""Build the exact generic-interior C63 stationary polynomial system."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path

Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


def derivative(poly: Polynomial, index: int) -> Polynomial:
    result = {}
    for exponent, coefficient in poly.items():
        if exponent[index] == 0:
            continue
        target = list(exponent)
        target[index] -= 1
        result[tuple(target)] = coefficient * exponent[index]
    return result


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    result = defaultdict(Fraction, left)
    for exponent, coefficient in right.items():
        result[exponent] -= coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def lcm(left: int, right: int) -> int:
    return left // gcd(left, right) * right


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("elementary", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    poly: Polynomial = {}
    with args.elementary.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in ("e", "T1", "T2", "T3", "C1", "C2"))
            poly[exponent] = Fraction(int(row["numerator"]), int(row["denominator"]))

    derivatives = [derivative(poly, index) for index in range(6)]
    equations = {
        "dT2": derivatives[2],
        "dT3": derivatives[3],
        "dC2": derivatives[5],
        "de_minus_dT1": subtract(derivatives[0], derivatives[1]),
        "de_minus_dC1": subtract(derivatives[0], derivatives[4]),
        "normalization": {
            (1, 0, 0, 0, 0, 0): Fraction(1),
            (0, 1, 0, 0, 0, 0): Fraction(1),
            (0, 0, 0, 0, 1, 0): Fraction(1),
            (0, 0, 0, 0, 0, 0): Fraction(-1),
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "generic-stationary-system.tsv"
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("equation", "e", "T1", "T2", "T3", "C1", "C2", "numerator", "denominator"))
        for name, equation in equations.items():
            for exponent, coefficient in sorted(equation.items()):
                writer.writerow((name, *exponent, coefficient.numerator, coefficient.denominator))

    denominator_lcm = 1
    for equation in equations.values():
        for coefficient in equation.values():
            denominator_lcm = lcm(denominator_lcm, coefficient.denominator)
    summary = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "equations": {name: len(equation) for name, equation in equations.items()},
        "denominator_lcm": denominator_lcm,
        "derivation": ["dT2=0", "dT3=0", "dC2=0", "de=dT1", "de=dC1", "e+T1+C1=1"],
        "scope": "Generic full-support stationary stratum with three distinct transposition values and two distinct cycle values.",
        "claim_boundary": "Exact system construction only; dimension and feasible-root signs are not asserted.",
    }
    (args.output_dir / "generic-stationary-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
