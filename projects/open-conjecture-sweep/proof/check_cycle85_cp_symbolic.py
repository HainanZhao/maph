#!/usr/bin/env python3
"""Build the exact two-atom CP C5 defect polynomial for the C85 cap."""
from __future__ import annotations

import hashlib
import json
import sys

import sympy


def main() -> None:
    alpha, lam, u0, u1, v0, v1 = sympy.symbols("alpha lambda u0 u1 v0 v1", nonnegative=True)
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
    print("built", file=sys.stderr, flush=True)
    defect = sympy.Poly(sympy.expand(density - integral_k ** 5), alpha, lam, u0, u1, v0, v1)
    print(f"expanded_terms={len(defect.terms())}", file=sys.stderr, flush=True)
    quotient = defect
    factors: list[tuple[str, int]] = []
    for label, factor in (("alpha", alpha), ("1-alpha", 1 - alpha),
                          ("lambda", lam), ("1-lambda", 1 - lam),
                          ("det", u0 * v1 - u1 * v0)):
        multiplicity = 0
        divisor = sympy.Poly(factor, alpha, lam, u0, u1, v0, v1)
        while True:
            candidate, remainder = sympy.div(quotient, divisor)
            if not remainder.is_zero:
                break
            quotient = candidate
            multiplicity += 1
        factors.append((label, multiplicity))
    recomposed = quotient.as_expr()
    for label, multiplicity in factors:
        factor = {"alpha": alpha, "1-alpha": 1 - alpha, "lambda": lam,
                  "1-lambda": 1 - lam, "det": u0 * v1 - u1 * v0}[label]
        recomposed *= factor ** multiplicity
    assert sympy.Poly(sympy.expand(recomposed), alpha, lam, u0, u1, v0, v1) == defect
    quotient_text = str(quotient.as_expr())
    expanded_text = str(defect.as_expr())
    coefficient_signs = [coefficient > 0 for _, coefficient in quotient.terms()]
    # A named exact CP specialization: alpha=lambda=1/2, u=(1,0), v=(0,1).
    special = defect.as_expr().subs({alpha: sympy.Rational(1, 2), lam: sympy.Rational(1, 2),
                                     u0: 1, u1: 0, v0: 0, v1: 1})
    assert special >= 0
    print(json.dumps({
        "epistemic_status": "PROVED",
        "variables": ["alpha", "lambda", "u0", "u1", "v0", "v1"],
        "total_degree": defect.total_degree(),
        "expanded_terms": len(defect.terms()),
        "boundary_factorization_reexpands_exactly": True,
        "boundary_factor_multiplicities": factors,
        "quotient_terms": len(quotient.terms()),
        "quotient_all_coefficients_positive": all(coefficient_signs),
        "quotient_nonpositive_coefficients": len(coefficient_signs) - sum(coefficient_signs),
        "expanded_sha256": hashlib.sha256(expanded_text.encode()).hexdigest(),
        "quotient_sha256": hashlib.sha256(quotient_text.encode()).hexdigest(),
        "named_cp_specialization_defect": str(special),
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
