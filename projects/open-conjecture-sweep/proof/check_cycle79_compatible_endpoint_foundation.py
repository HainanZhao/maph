#!/usr/bin/env python3
"""Exact scalar audit for C79's compatible-endpoint proof.

This checks only finite algebraic parts stated in the proof note: the complete
Ky Fan target assembly and all affine D-spectrum bounds on the two polygon
polytope regimes.  It deliberately does not purport to certify the published
Higuchi--Sudbery--Szulc theorem or the general two-projection lemma.
"""

from itertools import combinations
import json
import sympy as sp


def idx(a, b, c):
    return 4 * a + 2 * b + c


def partial_one(matrix, subsystem):
    result = sp.zeros(2, 2)
    for i in range(2):
        for j in range(2):
            for x in range(2):
                for y in range(2):
                    coordinates = [None, None, None]
                    coordinates[subsystem] = i
                    other = [z for z in range(3) if z != subsystem]
                    coordinates[other[0]] = x
                    coordinates[other[1]] = y
                    row = idx(*coordinates)
                    coordinates[subsystem] = j
                    column = idx(*coordinates)
                    result[i, j] += matrix[row, column]
    return result


def partial_two(matrix, first, second):
    result = sp.zeros(4, 4)
    third = ({0, 1, 2} - {first, second}).pop()
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for ell in range(2):
                    for z in range(2):
                        row = [None, None, None]
                        column = [None, None, None]
                        row[first], row[second], row[third] = i, j, z
                        column[first], column[second], column[third] = k, ell, z
                        result[2 * i + j, 2 * k + ell] += matrix[idx(*row), idx(*column)]
    return result


def embed_two(matrix, first, second):
    result = sp.zeros(8, 8)
    third = ({0, 1, 2} - {first, second}).pop()
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for aa in range(2):
                    for bb in range(2):
                        for cc in range(2):
                            row, column = (a, b, c), (aa, bb, cc)
                            if row[third] == column[third]:
                                result[idx(*row), idx(*column)] = matrix[
                                    2 * row[first] + row[second],
                                    2 * column[first] + column[second],
                                ]
    return result


def embed_one(matrix, subsystem):
    result = sp.zeros(8, 8)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for aa in range(2):
                    for bb in range(2):
                        for cc in range(2):
                            row, column = (a, b, c), (aa, bb, cc)
                            if all(row[z] == column[z] for z in range(3) if z != subsystem):
                                result[idx(*row), idx(*column)] = matrix[row[subsystem], column[subsystem]]
    return result


def spin_flip_basis_check():
    """Verify the three-qubit spin-flip expansion on all 64 matrix units."""
    y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    y3 = sp.kronecker_product(y, y, y)
    identity = sp.eye(8)
    rows = 0
    for row in range(8):
        for column in range(8):
            rho = sp.zeros(8, 8)
            rho[row, column] = 1
            rhs = identity * sp.trace(rho)
            rhs -= embed_one(partial_one(rho, 0), 0)
            rhs -= embed_one(partial_one(rho, 1), 1)
            rhs -= embed_one(partial_one(rho, 2), 2)
            rhs += embed_two(partial_two(rho, 0, 1), 0, 1)
            rhs += embed_two(partial_two(rho, 0, 2), 0, 2)
            rhs += embed_two(partial_two(rho, 1, 2), 1, 2)
            rhs -= rho
            assert y3 * rho.T * y3 == rhs
            rows += 1
    return rows


def vertices(inequalities):
    """All rational vertices of {x: affine inequality <= 0}."""
    r = sp.Matrix(sp.symbols("rA rB rC", real=True))
    found = set()
    for selected in combinations(inequalities, 3):
        equations = [expr for expr in selected]
        solved = sp.solve(equations, tuple(r), dict=True)
        for row in solved:
            if len(row) != 3:
                continue
            point = tuple(sp.simplify(row[x]) for x in r)
            if all(sp.simplify(expr.subs(dict(zip(r, point)))) <= 0 for expr in inequalities):
                found.add(point)
    return sorted(found, key=str)


def main():
    spin_flip_rows = spin_flip_basis_check()
    a, b, c = sp.symbols("a b c", nonnegative=True)
    prefix_spectra = (
        (1, 1, 0, 0, 0, 0, 0, 0),
        (2, 1, 1, 0, 0, 0, 0, 0),
        (3, 1, 1, 1, 0, 0, 0, 0),
    )
    # Keep the normalization symbolic so the prefix equality is an identity,
    # rather than silently relying on a+b+c=1 in the checker.
    target = (a + b + c, a, b, c, 0, 0, 0, 0)
    target_rows = 0
    for k in range(1, 9):
        lhs = (a - b) * sum(prefix_spectra[0][:k])
        lhs += (b - c) * sum(prefix_spectra[1][:k])
        lhs += c * sum(prefix_spectra[2][:k])
        assert sp.simplify(lhs - sum(target[:k])) == 0
        target_rows += 1

    rA, rB, rC = sp.symbols("rA rB rC", real=True)
    rs = (rA, rB, rC)
    total = sum(rs)
    entries = (
        2 - total,
        1 - total + 2 * rC,
        1 - total + 2 * rB,
        1 - total + 2 * rA,
        total - 2 * rA,
        total - 2 * rB,
        total - 2 * rC,
        total - 1,
    )
    base = [
        -rA, -rB, -rC,
        rA - sp.Rational(1, 2), rB - sp.Rational(1, 2), rC - sp.Rational(1, 2),
        rA - rB - rC, rB - rA - rC, rC - rA - rB,
    ]
    lower_vertices = vertices(base + [total - 1])
    upper_vertices = vertices(base + [1 - total])
    assert lower_vertices and upper_vertices

    min_rows = 0
    for point in vertices(base):
        sub = dict(zip(rs, point))
        for entry in entries:
            assert sp.simplify((entry - (total - 1)).subs(sub)) >= 0
            min_rows += 1

    fan_rows = 0
    for regime_vertices, delta in ((lower_vertices, 1 - total), (upper_vertices, 0)):
        for k in (1, 2, 3):
            for subset in combinations(entries, k):
                gap = sp.expand(k + delta - sum(subset))
                for point in regime_vertices:
                    assert sp.simplify(gap.subs(dict(zip(rs, point)))) >= 0
                    fan_rows += 1

    print(json.dumps({
        "epistemic_status": "PROVED",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "target_ky_fan_rows": target_rows,
        "polygon_vertices": {"s_le_1": len(lower_vertices), "s_ge_1": len(upper_vertices)},
        "minimum_rows": min_rows,
        "D_fan_vertex_rows": fan_rows,
        "spin_flip_basis_rows": spin_flip_rows,
        "scope": "exact finite scalar audit only",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
