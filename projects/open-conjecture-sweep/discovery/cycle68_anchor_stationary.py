#!/usr/bin/env python3
"""Exact resultant plus numerical candidate selection at one C68 outer anchor."""

from __future__ import annotations

import argparse
import csv
import json
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--x", type=parse_fraction, required=True)
    parser.add_argument("--y", type=parse_fraction, required=True)
    parser.add_argument("--z", type=parse_fraction, required=True)
    args = parser.parse_args()

    x, y, z = map(sp.Rational, (args.x, args.y, args.z))
    e = x
    t = (1 - x) * y / 3
    c = (1 - x) * (1 - y) / 2
    r2 = 6 * t**2 * z**2
    u_plus = 2 * t**3 * z**3
    u_minus = max(t * r2 / 2 - t**3, -u_plus)
    s, u = sp.symbols("s u")
    polynomial = 0
    with args.orbit.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            coefficient = sp.Rational(int(row["numerator"]), int(row["denominator"]))
            coefficient *= e ** int(row["e"]) * t ** int(row["t"])
            coefficient *= c ** int(row["c"]) * r2 ** int(row["r2"])
            polynomial += coefficient * u ** int(row["u"]) * s ** int(row["s2"])
    P = sp.Poly(polynomial, u, s)
    Pu, Ps = P.diff(u), P.diff(s)
    start = time.monotonic()
    resultant = sp.Poly(sp.resultant(Pu.as_expr(), Ps.as_expr(), u), s)
    seconds = time.monotonic() - start
    endpoint_values = (resultant.eval(0), resultant.eval(c**2))
    exact_feasible_s_roots = int(sp.count_roots(resultant, 0, c**2))
    roots = sp.nroots(resultant, n=30, maxsteps=300)
    candidates = []
    for root in roots:
        if abs(float(sp.im(root))) > 1e-15:
            continue
        sv = float(sp.re(root))
        if not (0 < sv < float(c**2)):
            continue
        pu_at_s = sp.Poly(Pu.as_expr().subs(s, sv), u)
        for ur in sp.nroots(pu_at_s, n=30, maxsteps=300):
            if abs(float(sp.im(ur))) > 1e-12:
                continue
            uv = float(sp.re(ur))
            if not (float(u_minus) < uv < float(u_plus)):
                continue
            ps_value = float(Ps.as_expr().subs({u: uv, s: sv}))
            if abs(ps_value) > 1e-10:
                continue
            p_value = float(P.as_expr().subs({u: uv, s: sv}))
            puu = float(P.diff(u, 2).as_expr().subs({u: uv, s: sv}))
            pss = float(P.diff(s, 2).as_expr().subs({u: uv, s: sv}))
            pus = float(P.diff(u).diff(s).as_expr().subs({u: uv, s: sv}))
            determinant = puu * pss - pus * pus
            candidates.append({
                "u": uv,
                "s2": sv,
                "P": p_value,
                "P_uu": puu,
                "hessian_determinant": determinant,
                "local_minimum_candidate": puu >= 0 and determinant >= 0,
                "Ps_residual": ps_value,
            })
    payload = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "outer": {"e": str(e), "t": str(t), "c": str(c), "r2": str(r2)},
        "fiber": {"u_minus": str(u_minus), "u_plus": str(u_plus), "s2_max": str(c**2)},
        "resultant": {
            "degree_s2": resultant.degree(),
            "terms": len(resultant.terms()),
            "seconds": seconds,
            "endpoint_values_nonzero": [value != 0 for value in endpoint_values],
            "exact_roots_on_closed_s2_interval": exact_feasible_s_roots,
            "root_count_epistemic_status": "PROVED",
        },
        "candidates": candidates,
        "claim_boundary": "Exact specialized resultant; approximate candidate selection only.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
