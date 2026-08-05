#!/usr/bin/env python3
"""Independent coefficientwise SymPy audit of the C68 secant cube charts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy


def load_invariant_secant(path: Path, symbols: tuple[sympy.Symbol, ...]) -> sympy.Poly:
    terms = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if int(row["w"]) != 0 or int(row["s2"]) == 0:
                continue
            exponent = tuple(int(row[name]) for name in ("e", "t", "c", "r2", "u", "s2"))
            shifted = exponent[:5] + (exponent[5] - 1,)
            coefficient = sympy.Rational(int(row["numerator"]), int(row["denominator"]))
            terms[shifted] = terms.get(shifted, 0) + coefficient
    return sympy.Poly.from_dict(terms, symbols)


def load_cube(path: Path, symbols: tuple[sympy.Symbol, ...]) -> sympy.Poly:
    terms = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in ("x", "y", "z", "v", "lambda"))
            coefficient = sympy.Rational(int(row["numerator"]), int(row["denominator"]))
            terms[exponent] = terms.get(exponent, 0) + coefficient
    return sympy.Poly.from_dict(terms, symbols)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("secant_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    e, t, c, r2, u, s2 = sympy.symbols("e t c r2 u s2")
    x, y, z, v, lam = sympy.symbols("x y z v lambda")
    invariant = load_invariant_secant(args.orbit, (e, t, c, r2, u, s2))
    base_t = (1 - x) * y / 3
    base_c = (1 - x) * (1 - y) / 2
    reports = {}
    for regime, Z in (("low", z / 2), ("high", (1 + z) / 2)):
        u_plus = 2 * base_t**3 * Z**3
        u_minus = -u_plus if regime == "low" else base_t**3 * (3 * Z**2 - 1)
        u_value = (1 - lam) * u_minus + lam * u_plus
        substitutions = {
            e: x,
            t: base_t,
            c: base_c,
            r2: 6 * base_t**2 * Z**2,
            u: u_value,
            s2: base_c**2 * v,
        }
        expanded = sympy.Poly(
            invariant.as_expr().subs(substitutions, simultaneous=True),
            x,
            y,
            z,
            v,
            lam,
        )
        candidate_path = args.secant_dir / f"secant-{regime}.tsv"
        candidate = load_cube(candidate_path, (x, y, z, v, lam))
        if expanded != candidate:
            difference = expanded - candidate
            raise AssertionError(f"{regime} coefficient mismatch: {len(difference.terms())} terms")
        reports[regime] = {
            "terms": len(expanded.terms()),
            "degrees": expanded.degree_list(),
            "coefficientwise_match": True,
            "candidate_sha256": digest(candidate_path),
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "sympy_version": sympy.__version__,
        "route": "independent simultaneous symbolic substitution",
        "charts": reports,
        "claim_boundary": "Independent coefficientwise construction audit; quotient signs are certified separately.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
