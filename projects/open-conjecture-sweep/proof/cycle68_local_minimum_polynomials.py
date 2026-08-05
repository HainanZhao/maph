#!/usr/bin/env python3
"""Construct exact C68 derivative/Hessian polynomials on both interior charts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy


def load_orbit(path: Path, symbols):
    result = 0
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
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
    parser.add_argument("--object", choices=("derivatives", "determinant"), required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    e, t, c, r2, u, s2 = sympy.symbols("e t c r2 u s2")
    x, y, z, v, lam = sympy.symbols("x y z v lambda")
    source = load_orbit(args.orbit, (e, t, c, r2, u, s2))
    Pu = sympy.diff(source, u)
    Ps = sympy.diff(source, s2)
    Puu = sympy.diff(Pu, u)
    if args.object == "determinant":
        Pss = sympy.diff(Ps, s2)
        Pus = sympy.diff(Pu, s2)
        objects = {"hessian_determinant": Puu * Pss - Pus**2}
    else:
        objects = {"P_u": Pu, "P_s2": Ps, "P_uu": Puu}

    base = {e: x, t: (1 - x) * y / 3, c: (1 - x) * (1 - y) / 2}
    summaries = {}
    control = {x: sympy.Rational(1, 5), y: sympy.Rational(2, 5), z: sympy.Rational(3, 7), v: sympy.Rational(4, 9), lam: sympy.Rational(5, 11)}
    for regime, Z in (("low", z / 2), ("high", (1 + z) / 2)):
        substitutions = dict(base)
        substitutions[r2] = 6 * base[t] ** 2 * Z**2
        substitutions[s2] = base[c] ** 2 * v
        u_plus = 2 * base[t] ** 3 * Z**3
        u_minus = -u_plus if regime == "low" else base[t] ** 3 * (3 * Z**2 - 1)
        substitutions[u] = (1 - lam) * u_minus + lam * u_plus
        for name, expression in objects.items():
            polynomial = sympy.Poly(expression.subs(substitutions), x, y, z, v, lam)
            expected = expression.subs(substitutions).subs(control)
            assert polynomial.as_expr().subs(control) == expected
            write_poly(args.output_dir / f"{name}-{regime}.tsv", polynomial)
            summaries[f"{name}-{regime}"] = {
                "terms": len(polynomial.terms()),
                "degrees": polynomial.degree_list(),
                "positive_coefficients": sum(1 for _, coefficient in polynomial.terms() if coefficient > 0),
                "negative_coefficients": sum(1 for _, coefficient in polynomial.terms() if coefficient < 0),
                "exact_rational_control": "PASS",
            }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "object": args.object,
        "sympy_version": sympy.__version__,
        "charts": summaries,
        "claim_boundary": "Exact derivative/Hessian polynomial construction only; no feasibility conclusion.",
    }
    (args.output_dir / f"{args.object}-summary.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
