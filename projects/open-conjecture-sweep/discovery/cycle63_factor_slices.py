#!/usr/bin/env python3
"""Exploratory exact factorization of frozen C63 orbit-polynomial slices."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slice", choices=("cycle_only", "trans_only"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    e, t, c, r2, u, s2 = sp.symbols("e t c r2 u s2")
    variables = (e, t, c, r2, u, s2)
    expression = sp.Integer(0)
    with args.input.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if int(row["w"]):
                raise ValueError("unexpected w term")
            exponents = [int(row[name]) for name in ("e", "t", "c", "r2", "u", "s2")]
            if args.slice == "cycle_only" and (exponents[3] or exponents[4]):
                continue
            if args.slice == "trans_only" and exponents[5]:
                continue
            coefficient = sp.Rational(int(row["numerator"]), int(row["denominator"]))
            term = coefficient
            for variable, exponent in zip(variables, exponents):
                term *= variable ** exponent
            expression += term

    active = (e, t, c, s2) if args.slice == "cycle_only" else (e, t, c, r2, u)
    polynomial = sp.Poly(expression, *active, domain=sp.QQ)
    coefficient, factors = sp.factor_list(polynomial)
    payload = {
        "slice": args.slice,
        "epistemic_status": "OBSERVED",
        "input_terms": len(polynomial.terms()),
        "total_degree": polynomial.total_degree(),
        "coefficient": str(coefficient),
        "factors": [
            {
                "multiplicity": multiplicity,
                "total_degree": factor.total_degree(),
                "terms": len(factor.terms()),
                "expression": str(factor.as_expr()) if len(factor.terms()) <= 80 else "OMITTED_OVER_80_TERMS",
            }
            for factor, multiplicity in factors
        ],
        "claim_boundary": "Exploratory exact factorization of one coordinate slice only.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
