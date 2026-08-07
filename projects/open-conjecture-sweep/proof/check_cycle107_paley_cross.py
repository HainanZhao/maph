#!/usr/bin/env python3
"""Exact C107 Paley-cross identities and forced-equation controls."""
from __future__ import annotations

import json
from fractions import Fraction


def legendre(a: int, q: int) -> int:
    a %= q
    if a == 0:
        return 0
    return 1 if pow(a, (q - 1) // 2, q) == 1 else -1


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def shift(q: int, c: int):
    return [[int(j == (i + c) % q) for j in range(q)] for i in range(q)]


def translation_block(q: int, positives):
    positives = {x % q for x in positives}
    return [[0 if i == j else (1 if (j - i) % q in positives else -1) for j in range(q)] for i in range(q)]


def control(q: int):
    one = [[1] * q for _ in range(q)]
    ident = [[int(i == j) for j in range(q)] for i in range(q)]
    t = [[legendre(j - i, q) for j in range(q)] for i in range(q)]
    Q = [[ident[i][j] - t[i][j] for j in range(q)] for i in range(q)]
    qt = transpose(Q)
    p0 = translation_block(q, {*range(1, (q - 3) // 4 + 1), *range(q - (q - 3) // 4, q)})
    p1 = translation_block(q, {*range(2, (q - 3) // 4 + 2), *range(q - ((q - 3) // 4 + 1), q - 1)})
    # q=7,23 controls: both sets are symmetric and each has (q-3)/2 positives.
    assert p0 != p1
    assert all(sum(row) == -2 for row in p0 + p1)
    assert p0 == transpose(p0) and p1 == transpose(p1)
    assert matmul(Q, one) == one
    assert matmul(Q, qt) == [[(q + 1 if i == j else 0) - 1 for j in range(q)] for i in range(q)]
    inverse_numerator = add(qt, one)
    assert matmul(Q, inverse_numerator) == [[q + 1 if i == j else 0 for j in range(q)] for i in range(q)]
    cross_direct = add(matmul(p0, Q), matmul(Q, p1))
    cross_commuted = matmul(Q, add(p0, p1))
    assert cross_direct == cross_commuted
    forced = []
    for c in range(q):
        rhs_num = matmul(inverse_numerator, shift(q, c))
        rhs = [[Fraction(-4 * rhs_num[i][j], q + 1) for j in range(q)] for i in range(q)]
        nonzero = {x for row in rhs for x in row if x}
        assert nonzero == {Fraction(-8, q + 1)}
        assert any(x.denominator != 1 or x.numerator % 2 for x in nonzero)
        forced.append({"shift": c, "nonzero_value": str(next(iter(nonzero))), "even_integral": False})
    return {
        "q": q,
        "q_identity": True,
        "full_cross_identity": True,
        "independent_blocks": True,
        "shifts_checked": len(forced),
        "forced_nonzero_values": sorted({row["nonzero_value"] for row in forced}),
        "all_forced_values_non_even_integral": all(not row["even_integral"] for row in forced),
    }


def main():
    rows = [control(q) for q in (7, 23)]
    assert all(row["shifts_checked"] == row["q"] for row in rows)
    print(json.dumps({"status": "PASS", "controls": rows}, sort_keys=True))


if __name__ == "__main__":
    main()
