#!/usr/bin/env python3
"""Independent finite-step replay of C89's rank-one Hessian formula.

This intentionally does not import the frozen-control script.  It compares a
direct labelled-map second derivative against the three-square expression at
two positive rational rank-one controls, coefficient by coefficient.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json
from math import lcm


E = tuple((i, j) for j in range(5) for i in (j % 5, (j + 1) % 5, (j + 2) % 5))


def fmt(q: F) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def direct_hessian(alpha, beta, a, b):
    """Enumerate labelled maps and ordered distinct edge derivatives."""
    n = len(alpha)
    # All labelled-map terms have a common denominator.  Accumulate integral
    # numerators, so this independent route does not spend the whole cap in
    # Fraction normalization inside its 12 million ordered-edge updates.
    alpha_den = lcm(*(x.denominator for x in alpha))
    beta_den = lcm(*(x.denominator for x in beta))
    a_den = lcm(*(x.denominator for x in a))
    b_den = lcm(*(x.denominator for x in b))
    alpha_int = [int(x * alpha_den) for x in alpha]
    beta_int = [int(x * beta_den) for x in beta]
    base = [int(a[i] * a_den) * int(b[j] * b_den) for i in range(n) for j in range(n)]
    denominator = alpha_den ** 5 * beta_den ** 5 * (a_den * b_den) ** 13
    h = [[0 for _ in range(n * n)] for _ in range(n * n)]
    for left in product(range(n), repeat=5):
        for right in product(range(n), repeat=5):
            atom_weight = 1
            for i in left:
                atom_weight *= alpha_int[i]
            for j in right:
                atom_weight *= beta_int[j]
            labels = [n * left[i] + right[j] for i, j in E]
            factors = [base[k] for k in labels]
            total = 1
            for factor in factors:
                total *= factor
            for p, x in enumerate(labels):
                for q, y in enumerate(labels):
                    if p != q:
                        h[x][y] += atom_weight * (total // factors[p] // factors[q])
    return [[F(x, denominator) for x in row] for row in h]


def formula_quadratic(alpha, beta, a, b, u):
    """The proposed rank-one formula evaluated on a step direction u."""
    n = len(alpha)
    a3 = sum((alpha[i] * a[i] ** 3 for i in range(n)), F(0))
    b3 = sum((beta[j] * b[j] ** 3 for j in range(n)), F(0))
    r = [sum((beta[j] * b[j] ** 2 * u[n * i + j] for j in range(n)), F(0)) for i in range(n)]
    c = [sum((alpha[i] * a[i] ** 2 * u[n * i + j] for i in range(n)), F(0)) for j in range(n)]
    ell = sum((alpha[i] * beta[j] * a[i] ** 2 * b[j] ** 2 * u[n * i + j]
               for i in range(n) for j in range(n)), F(0))
    return (30 * a3 ** 4 * b3 ** 3 * sum((alpha[i] * a[i] * r[i] ** 2 for i in range(n)), F(0))
            + 30 * a3 ** 3 * b3 ** 4 * sum((beta[j] * b[j] * c[j] ** 2 for j in range(n)), F(0))
            + 150 * a3 ** 3 * b3 ** 3 * ell ** 2)


def formula_hessian(alpha, beta, a, b):
    n = len(alpha)
    size = n * n
    basis = [[F(int(i == j)) for i in range(size)] for j in range(size)]
    diagonal = [formula_quadratic(alpha, beta, a, b, v) for v in basis]
    return [[(formula_quadratic(alpha, beta, a, b, [basis[i][k] + basis[j][k] for k in range(size)])
              - diagonal[i] - diagonal[j]) / 2 for j in range(size)] for i in range(size)]


def run_control(name, alpha, beta, a, b):
    direct = direct_hessian(alpha, beta, a, b)
    predicted = formula_hessian(alpha, beta, a, b)
    mismatches = [(i, j, direct[i][j], predicted[i][j])
                  for i in range(9) for j in range(9) if direct[i][j] != predicted[i][j]]
    return {"name": name, "map_count": 3 ** 10, "mismatch_count": len(mismatches),
            "first_mismatch": None if not mismatches else [mismatches[0][0], mismatches[0][1],
                                                               fmt(mismatches[0][2]), fmt(mismatches[0][3])],
            "hessian_00": fmt(direct[0][0]), "hessian_08": fmt(direct[0][8])}


def main():
    rows = [
        run_control("frozen_equal_atoms", (F(1, 3),) * 3, (F(1, 3),) * 3,
                    (F(1, 4), F(1, 2), F(3, 4)), (F(1, 3), F(1, 2), F(2, 3))),
        run_control("asymmetric_atoms", (F(1, 6), F(1, 3), F(1, 2)), (F(1, 2), F(1, 3), F(1, 6)),
                    (F(2, 5), F(3, 5), F(4, 5)), (F(1, 4), F(1, 2), F(3, 4))),
    ]
    assert all(row["mismatch_count"] == 0 for row in rows)
    print(json.dumps({"status": "COEFFICIENTWISE_REPLAY_PASS", "epistemic_status": "PROVED",
                      "ordered_edge_pairs": 210, "controls": rows,
                      "claim_boundary": "Exact finite-step verification of the proposed formula at two controls; the general identity is justified separately by the displayed edge-pair factorization."}, sort_keys=True))


if __name__ == "__main__":
    main()
