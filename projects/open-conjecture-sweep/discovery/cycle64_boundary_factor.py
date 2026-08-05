#!/usr/bin/env python3
"""Exact exploratory factorization of named C64 outer-degeneracy fibers."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy as sp


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", choices=("t_zero", "c_zero", "r_zero", "r_max"))
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    e, t, c, r2, u, s2 = sp.symbols("e t c r2 u s2")
    variables = (e, t, c, r2, u, s2)
    substitutions = {
        "t_zero": {t: 0, r2: 0, u: 0},
        "c_zero": {c: 0, s2: 0},
        "r_zero": {r2: 0, u: 0},
        "r_max": {r2: 6*t**2, u: 2*t**3},
    }[args.boundary]
    expression = sp.Integer(0)
    with args.orbit.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            coefficient = sp.Rational(int(row["numerator"]), int(row["denominator"]))
            term = coefficient
            for variable, name in zip(variables, ("e", "t", "c", "r2", "u", "s2")):
                term *= variable ** int(row[name])
            expression += term
    expression = sp.expand(expression.subs(substitutions))
    active = tuple(variable for variable in variables if variable not in substitutions)
    polynomial = sp.Poly(expression, *active, domain=sp.QQ)
    coefficient, factors = sp.factor_list(polynomial)
    payload = {
        "boundary": args.boundary,
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "active_variables": [str(variable) for variable in active],
        "terms": len(polynomial.terms()),
        "total_degree": polynomial.total_degree(),
        "positive_coefficients": sum(int(bool(value > 0)) for _, value in polynomial.terms()),
        "negative_coefficients": sum(int(bool(value < 0)) for _, value in polynomial.terms()),
        "factor_coefficient": str(coefficient),
        "factors": [
            {
                "multiplicity": multiplicity,
                "degree": factor.total_degree(),
                "terms": len(factor.terms()),
                "expression": str(factor.as_expr()) if len(factor.terms()) <= 100 else "OMITTED_OVER_100_TERMS",
            }
            for factor, multiplicity in factors
        ],
        "claim_boundary": "Exact factorization of one named outer-degeneracy fiber; sign is unproved unless the recorded factor coefficients make it immediate.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
