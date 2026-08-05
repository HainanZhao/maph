#!/usr/bin/env python3
"""Strip exact coordinate-boundary factors from C68 rational polynomials.

The quotient has the same sign on the open five-cube.  Boundary strata are
not discarded: the report records every removed factor so that degenerate
faces can be discharged by the C67 endpoint theorem or a separate restriction.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


VARIABLES = ("x", "y", "z", "v", "lambda")
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


def load(path: Path) -> Polynomial:
    result: defaultdict[Exponent, Fraction] = defaultdict(Fraction)
    with path.open(newline="") as handle:
        rows = csv.DictReader(handle, delimiter="\t")
        if tuple(rows.fieldnames or ()) != (*VARIABLES, "numerator", "denominator"):
            raise ValueError(f"unexpected header in {path}")
        for row in rows:
            exponent = tuple(int(row[name]) for name in VARIABLES)
            result[exponent] += Fraction(int(row["numerator"]), int(row["denominator"]))
    return {key: value for key, value in result.items() if value}


def divide_zero(polynomial: Polynomial, axis: int) -> Polynomial | None:
    if not polynomial or min(exponent[axis] for exponent in polynomial) == 0:
        return None
    return {
        exponent[:axis] + (exponent[axis] - 1,) + exponent[axis + 1 :]: coefficient
        for exponent, coefficient in polynomial.items()
    }


def divide_one(polynomial: Polynomial, axis: int) -> Polynomial | None:
    """Return the exact quotient by ``1 - variable``, if it exists."""
    groups: defaultdict[Exponent, dict[int, Fraction]] = defaultdict(dict)
    for exponent, coefficient in polynomial.items():
        other = exponent[:axis] + exponent[axis + 1 :]
        groups[other][exponent[axis]] = coefficient
    quotient: Polynomial = {}
    for other, coefficients in groups.items():
        degree = max(coefficients)
        if degree == 0:
            return None
        running = Fraction()
        for power in range(degree):
            running += coefficients.get(power, Fraction())
            if running:
                exponent = other[:axis] + (power,) + other[axis:]
                quotient[exponent] = running
        if coefficients.get(degree, Fraction()) != -running:
            return None
    return quotient


def strip(polynomial: Polynomial) -> tuple[Polynomial, dict[str, int]]:
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


def write(path: Path, polynomial: Polynomial) -> None:
    with path.open("w", newline="") as handle:
        rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
        rows.writerow((*VARIABLES, "numerator", "denominator"))
        for exponent, coefficient in sorted(polynomial.items()):
            rows.writerow((*exponent, coefficient.numerator, coefficient.denominator))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    report = {}
    for source in sorted(args.source_dir.glob("*.tsv")):
        original = load(source)
        reduced, factors = strip(original)
        write(args.output_dir / source.name, reduced)
        report[source.stem] = {
            "input_terms": len(original),
            "output_terms": len(reduced),
            "input_degrees": [max((e[i] for e in original), default=0) for i in range(5)],
            "output_degrees": [max((e[i] for e in reduced), default=0) for i in range(5)],
            "factors": factors,
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "method": "exact rational polynomial division",
        "claim_boundary": "Factorization only; removed-factor faces require separate coverage.",
        "charts": report,
    }
    (args.output_dir / "factor-report.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
