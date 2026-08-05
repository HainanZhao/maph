#!/usr/bin/env python3
"""Rewrite the C63 orbit deficit in elementary class invariants."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

import cycle63_reduce_orbit as sparse


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    # Output order: e,T1,T2,T3,C1,C2.
    e, t1, t2, t3, c1, c2 = (sparse.variable(index) for index in range(6))
    t1_squared = sparse.multiply(t1, t1)
    t1_cubed = sparse.multiply(t1_squared, t1)
    forms = [
        e,
        sparse.scale(t1, Fraction(1, 3)),
        sparse.scale(c1, Fraction(1, 2)),
        sparse.add(sparse.scale(t1_squared, Fraction(2, 3)), sparse.scale(t2, -2)),
        sparse.add(
            sparse.add(t3, sparse.scale(t1_cubed, Fraction(2, 27))),
            sparse.scale(sparse.multiply(t1, t2), Fraction(-1, 3)),
        ),
        sparse.add(sparse.scale(sparse.multiply(c1, c1), Fraction(1, 4)), sparse.scale(c2, -1)),
    ]
    powers = [[sparse.power(form, degree, 6) for degree in range(16)] for form in forms]
    result = {}
    with args.orbit.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if int(row["w"]):
                raise ValueError("elementary reduction requires the proved zero-w form")
            exponents = [int(row[name]) for name in ("e", "t", "c", "r2", "u", "s2")]
            term = {(0,) * 6: Fraction(int(row["numerator"]), int(row["denominator"]))}
            for index, exponent in enumerate(exponents):
                term = sparse.multiply(term, powers[index][exponent])
            result = sparse.add(result, term)

    # The deficit must vanish after replacing both classes by equal entries.
    central_forms = [
        sparse.variable(0, 3),
        sparse.variable(1, 3),
        sparse.scale(sparse.power(sparse.variable(1, 3), 2, 3), Fraction(1, 3)),
        sparse.scale(sparse.power(sparse.variable(1, 3), 3, 3), Fraction(1, 27)),
        sparse.variable(2, 3),
        sparse.scale(sparse.power(sparse.variable(2, 3), 2, 3), Fraction(1, 4)),
    ]
    central_powers = [[sparse.power(form, degree, 3) for degree in range(16)]
                      for form in central_forms]
    central = {}
    for exponents, coefficient in result.items():
        term = {(0,) * 3: coefficient}
        for index, exponent in enumerate(exponents):
            term = sparse.multiply(term, central_powers[index][exponent])
        central = sparse.add(central, term)
    if central:
        raise ValueError("elementary polynomial fails exact central-vanishing check")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "elementary-polynomial.tsv"
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("e", "T1", "T2", "T3", "C1", "C2", "numerator", "denominator"))
        for exponents, coefficient in sorted(result.items()):
            writer.writerow((*exponents, coefficient.numerator, coefficient.denominator))

    summary = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "terms": len(result),
        "weighted_degrees": sorted({
            exponent[0] + exponent[1] + 2 * exponent[2] + 3 * exponent[3]
            + exponent[4] + 2 * exponent[5]
            for exponent in result
        }),
        "central_substitution": "IDENTICALLY_ZERO",
        "claim_boundary": "Exact elementary-invariant conversion only; no sign conclusion.",
    }
    (args.output_dir / "elementary-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
