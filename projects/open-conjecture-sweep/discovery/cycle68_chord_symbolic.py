#!/usr/bin/env python3
"""Construct exact C68 concavity and u-chord polynomials on two cube charts."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

import sympy


def load_orbit(path: Path, symbols):
    e, t, c, r2, u, s2 = symbols
    result = 0
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            assert int(row["w"]) == 0
            coefficient = sympy.Rational(int(row["numerator"]), int(row["denominator"]))
            term = coefficient
            for variable, name in zip(symbols, ("e", "t", "c", "r2", "u", "s2"), strict=True):
                term *= variable ** int(row[name])
            result += term
    return result


def write_poly(path: Path, polynomial: sympy.Poly) -> None:
    with path.open("w", newline="") as handle:
        rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
        rows.writerow(("x", "y", "z", "v", "lambda", "numerator", "denominator"))
        for exponent, coefficient in sorted(polynomial.terms()):
            rows.writerow((*exponent, int(coefficient.p), int(coefficient.q)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--object", choices=("concavity", "chord"), required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    e, t, c, r2, u, s2 = sympy.symbols("e t c r2 u s2")
    x, y, z, v, lam = sympy.symbols("x y z v lambda")
    source = load_orbit(args.orbit, (e, t, c, r2, u, s2))
    base = {
        e: x,
        t: (1 - x) * y / 3,
        c: (1 - x) * (1 - y) / 2,
    }
    summaries = {}
    for regime, Z in (("low", z / 2), ("high", (1 + z) / 2)):
        substitutions = dict(base)
        substitutions[r2] = 6 * base[t] ** 2 * Z**2
        substitutions[s2] = base[c] ** 2 * v
        u_plus = 2 * base[t] ** 3 * Z**3
        u_minus = -u_plus if regime == "low" else base[t] ** 3 * (3 * Z**2 - 1)
        u_value = (1 - lam) * u_minus + lam * u_plus
        if args.object == "concavity":
            expression = -sympy.diff(source, u, 2).subs(substitutions).subs(u, u_value)
            polynomial = sympy.Poly(expression, x, y, z, v, lam)
            removed = "none"
        else:
            at_value = source.subs(substitutions).subs(u, u_value)
            at_minus = source.subs(substitutions).subs(u, u_minus)
            at_plus = source.subs(substitutions).subs(u, u_plus)
            difference = sympy.Poly(at_value - (1 - lam) * at_minus - lam * at_plus, x, y, z, v, lam)
            divisor = sympy.Poly(lam * (1 - lam), x, y, z, v, lam)
            polynomial, remainder = sympy.div(difference, divisor)
            assert remainder.is_zero
            removed = "lambda*(1-lambda)"
        write_poly(args.output_dir / f"{args.object}-{regime}.tsv", polynomial)
        summaries[regime] = {
            "terms": len(polynomial.terms()),
            "degrees": polynomial.degree_list(),
            "positive_coefficients": sum(1 for _, coefficient in polynomial.terms() if coefficient > 0),
            "negative_coefficients": sum(1 for _, coefficient in polynomial.terms() if coefficient < 0),
            "removed_factor": removed,
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "object": args.object,
        "sympy_version": sympy.__version__,
        "charts": summaries,
        "claim_boundary": "Exact polynomial construction only; no sign conclusion.",
    }
    (args.output_dir / f"{args.object}-summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
