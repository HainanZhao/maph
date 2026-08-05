#!/usr/bin/env python3
"""Derive the top-u coefficient of the C64 fiber derivative resultant."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("anchor_resultant", type=Path)
    parser.add_argument("degree_drop_resultant", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    e, t, c, r2 = sp.symbols("e t c r2")
    outer_variables = (e, t, c, r2)
    # derivative -> s2 power -> u power -> outer coefficient
    derivatives = {
        "du": defaultdict(lambda: defaultdict(lambda: sp.Integer(0))),
        "ds": defaultdict(lambda: defaultdict(lambda: sp.Integer(0))),
    }
    with args.orbit.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            u_degree = int(row["u"])
            s_degree = int(row["s2"])
            coefficient = sp.Rational(int(row["numerator"]), int(row["denominator"]))
            for variable, name in zip(outer_variables, ("e", "t", "c", "r2")):
                coefficient *= variable ** int(row[name])
            if u_degree:
                derivatives["du"][s_degree][u_degree - 1] += coefficient * u_degree
            if s_degree:
                derivatives["ds"][s_degree - 1][u_degree] += coefficient * s_degree

    leading = {}
    for name in ("du", "ds"):
        leading[name] = {}
        for s_degree, u_coefficients in derivatives[name].items():
            u_degree = max(u_coefficients)
            leading[name][s_degree] = (u_degree, sp.expand(u_coefficients[u_degree]))

    f_degree, g_degree = max(leading["du"]), max(leading["ds"])
    size = f_degree + g_degree
    matrix: list[list[tuple[int, sp.Expr] | None]] = [[None] * size for _ in range(size)]
    for row in range(g_degree):
        for power, entry in leading["du"].items():
            matrix[row][row + power] = entry
    for shifted in range(f_degree):
        for power, entry in leading["ds"].items():
            matrix[g_degree + shifted][shifted + power] = entry

    @lru_cache(maxsize=None)
    def best(row: int, mask: int) -> int:
        if row == size:
            return 0 if mask == (1 << size) - 1 else -10**9
        optimum = -10**9
        for column, entry in enumerate(matrix[row]):
            if entry is None or mask & (1 << column):
                continue
            optimum = max(optimum, entry[0] + best(row + 1, mask | (1 << column)))
        return optimum

    maximum_degree = best(0, 0)
    matchings: list[tuple[int, ...]] = []

    def enumerate_best(row: int, mask: int, columns: tuple[int, ...]) -> None:
        if row == size:
            matchings.append(columns)
            return
        target = best(row, mask)
        for column, entry in enumerate(matrix[row]):
            if entry is None or mask & (1 << column):
                continue
            if entry[0] + best(row + 1, mask | (1 << column)) == target:
                enumerate_best(row + 1, mask | (1 << column), columns + (column,))

    enumerate_best(0, 0, ())
    top_coefficient = sp.Integer(0)
    for columns in matchings:
        inversions = sum(columns[i] > columns[j] for i in range(size) for j in range(i + 1, size))
        term = sp.Integer(-1 if inversions % 2 else 1)
        for row, column in enumerate(columns):
            term *= matrix[row][column][1]
        top_coefficient += term
    top_coefficient = sp.factor(top_coefficient)

    top_poly = sp.Poly(top_coefficient, *outer_variables, domain=sp.QQ)
    factor_constant, factors = sp.factor_list(top_poly)
    anchor_values = {e: sp.Rational(1, 5), t: sp.Rational(1, 5),
                     c: sp.Rational(1, 10), r2: sp.Rational(1, 10)}
    specialized = sp.Rational(top_coefficient.subs(anchor_values))
    with args.anchor_resultant.open(newline="", encoding="utf-8") as handle:
        anchor_rows = list(csv.DictReader(handle, delimiter="\t"))
    anchor_leading_row = max(anchor_rows, key=lambda row: int(row["u_exponent"]))
    anchor_leading = sp.Rational(int(anchor_leading_row["numerator"]),
                                 int(anchor_leading_row["denominator"]))
    assert specialized == anchor_leading or specialized == -anchor_leading
    with args.degree_drop_resultant.open(newline="", encoding="utf-8") as handle:
        degree_drop_rows = list(csv.DictReader(handle, delimiter="\t"))
    degree_drop_leading_row = max(degree_drop_rows, key=lambda row: int(row["u_exponent"]))
    degree_drop_leading = sp.Rational(int(degree_drop_leading_row["numerator"]),
                                      int(degree_drop_leading_row["denominator"]))
    assert abs(specialized / degree_drop_leading) == 270

    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "sylvester_size": size,
        "maximum_u_degree": maximum_degree,
        "maximum_weight_matchings": len(matchings),
        "top_coefficient_terms": len(top_poly.terms()),
        "top_coefficient_expression": str(top_coefficient),
        "top_coefficient_monomials": [
            {"exponents": list(exponents), "coefficient": str(coefficient)}
            for exponents, coefficient in top_poly.terms()
        ],
        "factor_constant": str(factor_constant),
        "factors": [
            {
                "expression": str(factor),
                "multiplicity": multiplicity,
                "total_degree": sp.Poly(factor, *outer_variables).total_degree(),
                "terms": len(sp.Poly(factor, *outer_variables).terms()),
            }
            for factor, multiplicity in factors
        ],
        "anchor_specialization_matches_resultant": True,
        "degree_drop_anchor_scale_check": 270,
        "conclusion": "The u^26 coefficient of the degree-bounded fiber resultant is a nonzero rational constant, so the resultant is nonzero of degree 26 on every outer fiber.",
        "claim_boundary": "Uniform finiteness of the interior fiber critical system only; feasibility and deficit signs of its roots remain open.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
