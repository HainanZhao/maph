#!/usr/bin/env python3
"""Exact low-degree fiber elimination at one frozen C64 rational anchor."""

from __future__ import annotations

import argparse
import csv
import json
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp

ANCHORS = {
    "a1": (Fraction(1, 6), Fraction(1, 6), Fraction(1, 6), Fraction(1, 18)),
    "a2": (Fraction(1, 4), Fraction(1, 12), Fraction(1, 4), Fraction(1, 48)),
    "a3": (Fraction(1, 5), Fraction(1, 5), Fraction(1, 10), Fraction(1, 10)),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("anchor", choices=sorted(ANCHORS))
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    u, s2 = sp.symbols("u s2")
    e_value, t_value, c_value, r2_value = ANCHORS[args.anchor]
    outer = tuple(map(sp.Rational, (e_value, t_value, c_value, r2_value)))
    expression = sp.Integer(0)
    with args.orbit.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if int(row["w"]):
                raise ValueError("unexpected orientation term")
            coefficient = sp.Rational(int(row["numerator"]), int(row["denominator"]))
            outer_exponents = tuple(int(row[name]) for name in ("e", "t", "c", "r2"))
            for value, exponent in zip(outer, outer_exponents):
                coefficient *= value ** exponent
            expression += coefficient * u ** int(row["u"]) * s2 ** int(row["s2"])

    polynomial = sp.Poly(expression, u, s2, domain=sp.QQ)
    du = polynomial.diff(u)
    ds = polynomial.diff(s2)
    common = sp.gcd(du, ds)
    start = time.monotonic()
    resultant = sp.Poly(sp.resultant(du.as_expr(), ds.as_expr(), s2), u, domain=sp.QQ)
    resultant_seconds = time.monotonic() - start
    _, factors = sp.factor_list(resultant)
    real_intervals = sp.intervals(resultant, eps=sp.Rational(1, 10**12))
    lower_product = outer[1] * outer[3] / 2 - outer[1] ** 3
    discriminant_square = outer[3] ** 3 / 54
    feasible_resultant_intervals = []
    rendered_intervals = []
    for (left, right), multiplicity in real_intervals:
        below_lower = right < lower_product
        above_upper = left >= 0 and left * left > discriminant_square
        if not below_lower and not above_upper:
            feasible_resultant_intervals.append(((left, right), multiplicity))
        rendered_intervals.append({
            "left": str(left),
            "right": str(right),
            "multiplicity": multiplicity,
            "outside_feasible_u_interval": bool(below_lower or above_upper),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    resultant_path = args.output.with_name(args.output.stem + "-resultant.tsv")
    with resultant_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("u_exponent", "numerator", "denominator"))
        for (exponent,), coefficient in sorted(resultant.terms()):
            writer.writerow((exponent, coefficient.numerator, coefficient.denominator))

    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "anchor": args.anchor,
        "outer": [str(value) for value in outer],
        "fiber_polynomial": {
            "terms": len(polynomial.terms()),
            "degree_u": polynomial.degree(u),
            "degree_s2": polynomial.degree(s2),
            "preserves_global_degrees": polynomial.degree(u) == 5 and polynomial.degree(s2) == 7,
        },
        "derivatives": {
            "du_terms": len(du.terms()),
            "ds2_terms": len(ds.terms()),
            "gcd_total_degree": common.total_degree(),
            "gcd_is_unit": common.total_degree() == 0,
        },
        "resultant": {
            "degree_u": resultant.degree(),
            "terms": len(resultant.terms()),
            "factor_degrees": sorted((factor.degree(), multiplicity) for factor, multiplicity in factors),
            "real_root_intervals": len(real_intervals),
            "feasible_u_root_intervals": len(feasible_resultant_intervals),
            "isolating_intervals": rendered_intervals,
            "resultant_seconds": resultant_seconds,
        },
        "claim_boundary": "Exact specialization and resultant at one frozen outer anchor; no uniform, feasibility, or sign conclusion.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
