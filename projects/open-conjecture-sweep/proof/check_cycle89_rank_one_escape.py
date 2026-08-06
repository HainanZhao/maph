#!/usr/bin/env python3
"""Exact C89 rank-one escape geometry on the frozen 3x3 step bigraphon."""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json


N = 3
ALPHA = BETA = (F(1, 3),) * N
R, C = (F(1, 4), F(1, 2), F(3, 4)), (F(1, 3), F(1, 2), F(2, 3))
EDGES = tuple((i, j) for j in range(5) for i in ((j % 5), ((j + 1) % 5), ((j + 2) % 5)))
W0 = tuple(R[i] * C[j] for i in range(N) for j in range(N))
MAP_WEIGHT = F(1, 3**10)


def add(a, b): return [x + y for x, y in zip(a, b)]
def dot(a, b): return sum((x * y for x, y in zip(a, b)), F(0))
def matvec(a, x): return [dot(row, x) for row in a]
def qform(a, x): return dot(x, matvec(a, x))


def rref_nullspace(rows):
    """Deterministic rational nullspace basis for the given row vectors."""
    a = [list(row) for row in rows if any(row)]
    pivots = []
    col = 0
    for target in range(len(a)):
        while col < len(a[0]):
            source = next((i for i in range(target, len(a)) if a[i][col]), None)
            if source is None:
                col += 1; continue
            a[target], a[source] = a[source], a[target]
            scale = a[target][col]
            a[target] = [x / scale for x in a[target]]
            for i in range(len(a)):
                if i != target and a[i][col]:
                    q = a[i][col]; a[i] = [x - q * y for x, y in zip(a[i], a[target])]
            pivots.append(col); col += 1; break
        else: break
    free = [j for j in range(len(a[0])) if j not in pivots]
    basis = []
    for f in free:
        v = [F(0)] * len(a[0]); v[f] = F(1)
        for i, p in enumerate(pivots): v[p] = -a[i][f]
        basis.append(v)
    return basis


def poly_for_direction(z):
    p = [F(1)]
    for index in _MAP_EDGE_INDICES:
        q = [F(0)] * (len(p) + 1)
        for k, coeff in enumerate(p):
            q[k] += coeff * W0[index]
            q[k + 1] += coeff * z[index]
        p = q
    return [MAP_WEIGHT * x for x in p]


def full_line(z):
    total = [F(0)] * 16
    for indices in _ALL_MAP_EDGE_INDICES:
        global _MAP_EDGE_INDICES
        _MAP_EDGE_INDICES = indices
        total = add(total, poly_for_direction(z))
    density0, densityz = dot(DENSITY, W0), dot(DENSITY, z)
    # In this restricted space densityz=0, but retain the full formula as an audit.
    for k in range(16):
        from math import comb
        total[k] -= F(comb(15, k)) * density0 ** (15-k) * densityz ** k
    return total


def principal_minors_psd(matrix):
    """Exact all-principal-minor test; n=7 so 127 determinants is tiny."""
    n = len(matrix)
    def det(indices):
        a = [[matrix[i][j] for j in indices] for i in indices]
        value = F(1)
        for col in range(len(a)):
            pivot = next((r for r in range(col, len(a)) if a[r][col]), None)
            if pivot is None: return F(0)
            if pivot != col: a[col], a[pivot] = a[pivot], a[col]; value = -value
            q = a[col][col]; value *= q
            for r in range(col + 1, len(a)):
                if a[r][col]:
                    ratio = a[r][col] / q
                    for c in range(col + 1, len(a)): a[r][c] -= ratio * a[col][c]
        return value
    values = []
    for mask in range(1, 1 << n):
        indices = [i for i in range(n) if mask >> i & 1]
        values.append((indices, det(indices)))
    return values


def feasible_interval(z):
    lo, hi = None, None
    for w, direction in zip(W0, z):
        if not direction: continue
        a, b = -w / direction, (F(1) - w) / direction
        if a > b: a, b = b, a
        lo = a if lo is None or a > lo else lo
        hi = b if hi is None or b < hi else hi
    return lo, hi


def fmt(x): return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main():
    global _ALL_MAP_EDGE_INDICES, _MAP_EDGE_INDICES, DENSITY
    DENSITY = tuple(F(1, 9) for _ in range(9))
    _ALL_MAP_EDGE_INDICES = []
    for left in product(range(3), repeat=5):
        for right in product(range(3), repeat=5):
            _ALL_MAP_EDGE_INDICES.append(tuple(3 * left[i] + right[j] for i, j in EDGES))
    _MAP_EDGE_INDICES = _ALL_MAP_EDGE_INDICES[0]
    # Route A: exact derivative enumeration at W0.
    gradient = [F(0)] * 9; hessian = [[F(0)] * 9 for _ in range(9)]
    t0 = F(0)
    for indices in _ALL_MAP_EDGE_INDICES:
        factors = [W0[x] for x in indices]; total = __import__('functools').reduce(lambda a,b:a*b, factors, F(1))
        t0 += MAP_WEIGHT * total
        for e, a in enumerate(indices): gradient[a] += MAP_WEIGHT * total / factors[e]
        for e, a in enumerate(indices):
            for f, b in enumerate(indices):
                if e != f: hessian[a][b] += MAP_WEIGHT * total / factors[e] / factors[f]
    density0 = dot(DENSITY, W0)
    grad_delta = [gradient[a] - 15 * density0**14 * DENSITY[a] for a in range(9)]
    h_delta = [[hessian[a][b] - 15*14*density0**13*DENSITY[a]*DENSITY[b] for b in range(9)] for a in range(9)]
    basis = rref_nullspace([DENSITY, grad_delta])
    restricted = [[qform(h_delta, [basis[i][k] + basis[j][k] for k in range(9)]) for j in range(len(basis))] for i in range(len(basis))]
    # Polarization corrects the compact expression above.
    for i in range(len(basis)):
        for j in range(len(basis)):
            restricted[i][j] = (restricted[i][j] - qform(h_delta, basis[i]) - qform(h_delta, basis[j])) / 2
    minors = principal_minors_psd(restricted)
    negative_minors = [(idx, value) for idx, value in minors if value < 0]
    # Route B independently expands one generic deterministic direction through
    # all degree 15 coefficients.  The derivative route above handles every
    # basis direction; this full expansion guards the product/normalization
    # implementation without turning the frozen packet into a slow grid.
    validation_direction = [sum(v[k] for v in basis) for k in range(9)]
    line = full_line(validation_direction)
    line_checks = [{"linear": fmt(line[1]), "quadratic_times_2": fmt(2*line[2]),
                    "gradient": fmt(dot(grad_delta, validation_direction)),
                    "hessian": fmt(qform(h_delta, validation_direction)),
                    "all_coefficients": [fmt(x) for x in line]}]
    assert line_checks[0]["linear"] == line_checks[0]["gradient"]
    assert line_checks[0]["quadratic_times_2"] == line_checks[0]["hessian"]
    result = {"status": "PSD_CONTROL_PASS" if not negative_minors else "PSD_MECHANISM_REFUTED",
              "epistemic_status": "PROVED", "claim_boundary": "Exact result only for the frozen 3x3 rank-one control; no curvature result is a Sidorenko theorem.",
              "edges": len(EDGES), "labelled_maps": len(_ALL_MAP_EDGE_INDICES), "density": fmt(density0),
              "deficit_at_base": fmt(t0-density0**15), "tangent_dimension": len(basis),
              "basis": [[fmt(x) for x in v] for v in basis], "restricted_hessian": [[fmt(x) for x in row] for row in restricted],
              "negative_principal_minors": [[idx, fmt(value)] for idx,value in negative_minors], "line_checks": line_checks}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__": main()
