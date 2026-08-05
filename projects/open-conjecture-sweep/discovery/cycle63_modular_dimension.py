#!/usr/bin/env python3
"""Exploratory modular dimension test for the C63 generic stationary ideal."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

import sympy as sp


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("system", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--prime", type=int, default=32003)
    args = parser.parse_args()

    names = ("e", "T1", "T2", "T3", "C1", "C2")
    variables = sp.symbols(" ".join(names))
    equations: dict[str, dict[tuple[int, ...], int]] = defaultdict(dict)
    with args.system.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            exponent = tuple(int(row[name]) for name in names)
            numerator = int(row["numerator"]) % args.prime
            denominator = int(row["denominator"]) % args.prime
            coefficient = numerator * pow(denominator, -1, args.prime) % args.prime
            equations[row["equation"]][exponent] = coefficient

    polys = [sp.Poly.from_dict(equation, variables, modulus=args.prime).as_expr()
             for equation in equations.values()]
    start = time.monotonic()
    basis = sp.groebner(polys, *variables, modulus=args.prime, order="grevlex", method="f5b")
    elapsed = time.monotonic() - start
    payload = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "prime": args.prime,
        "equations": len(polys),
        "basis_polynomials": len(basis.polys),
        "zero_dimensional_mod_prime": bool(basis.is_zero_dimensional),
        "elapsed_seconds": elapsed,
        "claim_boundary": "Exploratory modular dimension test only; no characteristic-zero or feasible-root sign claim.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
