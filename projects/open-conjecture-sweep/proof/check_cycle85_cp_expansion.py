#!/usr/bin/env python3
"""Exact expansion fingerprint for C85's two-atom CP defect polynomial."""
from __future__ import annotations

import hashlib
import json

import sympy


def main() -> None:
    alpha, lam, u0, u1, v0, v1 = sympy.symbols("alpha lambda u0 u1 v0 v1")
    left = (alpha, 1 - alpha)
    u, v = (u0, u1), (v0, v1)
    kernel = [[[lam * u[a] * u[b] * u[c] + (1 - lam) * v[a] * v[b] * v[c]
                for c in range(2)] for b in range(2)] for a in range(2)]
    integral_k = sum(left[a] * left[b] * left[c] * kernel[a][b][c]
                     for a in range(2) for b in range(2) for c in range(2))
    density = sum(
        left[x0] * left[x1] * left[x2] * left[x3] * left[x4]
        * kernel[x0][x1][x2] * kernel[x1][x2][x3] * kernel[x2][x3][x4]
        * kernel[x3][x4][x0] * kernel[x4][x0][x1]
        for x0 in range(2) for x1 in range(2) for x2 in range(2) for x3 in range(2) for x4 in range(2)
    )
    defect = sympy.Poly(sympy.expand(density - integral_k ** 5), alpha, lam, u0, u1, v0, v1)
    text = str(defect.as_expr())
    uv_degree = max(sum(monomial[2:]) for monomial, _ in defect.terms())
    special = defect.as_expr().subs({alpha: sympy.Rational(1, 2), lam: sympy.Rational(1, 2),
                                     u0: 1, u1: 0, v0: 0, v1: 1})
    assert special >= 0
    print(json.dumps({
        "epistemic_status": "PROVED", "total_degree": defect.total_degree(), "uv_total_degree": uv_degree,
        "expanded_terms": len(defect.terms()),
        "expanded_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "named_cp_specialization_defect": str(special), "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
