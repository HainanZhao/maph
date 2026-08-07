#!/usr/bin/env python3
"""Exact checks of the spin/parity Walsh intertwiner for Gate B5."""

from __future__ import annotations

import json
from pathlib import Path
import random
import sys

import sympy


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.lane_b_spin_parity_intertwiner import (  # noqa: E402
    even_masks,
    matmul_mod,
    parity_transfer_mod,
    quotient_spin_transfer_mod,
    spin_representatives,
    transverse_edges,
    walsh_pairing,
)


PRIME = 1_000_000_007


def _symbolic_w2() -> dict[str, object]:
    w = 2
    m = w * w
    transverse = sympy.symbols(f"a0:{len(transverse_edges(w))}")
    connector = sympy.symbols(f"u0:{m}")
    parity = even_masks(m)
    spins = spin_representatives(m)
    h = sympy.Matrix(walsh_pairing(m))

    boundary: dict[int, sympy.Expr] = {0: sympy.Integer(1)}
    for (left, right), weight in zip(transverse_edges(w), transverse):
        flip = (1 << left) | (1 << right)
        updated = dict(boundary)
        for mask, value in boundary.items():
            updated[mask ^ flip] = updated.get(mask ^ flip, 0) + value * weight
        boundary = updated
    k = sympy.Matrix([
        [boundary.get(x ^ y, 0) * sympy.prod(connector[j] for j in range(m) if y >> j & 1)
         for y in parity]
        for x in parity
    ])

    q_rows = []
    for spin in spins:
        intra = sympy.prod(
            1 + (-1 if ((spin >> u) ^ (spin >> v)) & 1 else 1) * weight
            for (u, v), weight in zip(transverse_edges(w), transverse)
        )
        row = []
        for target in spins:
            signs = [
                -1 if ((spin >> site) ^ (target >> site)) & 1 else 1
                for site in range(m)
            ]
            plus = sympy.prod(1 + signs[site] * connector[site] for site in range(m))
            minus = sympy.prod(1 - signs[site] * connector[site] for site in range(m))
            row.append(intra * (plus + minus))
        q_rows.append(row)
    q = sympy.Matrix(q_rows)
    residual = q * h - (1 << m) * h * k
    if any(sympy.expand(value) != 0 for value in residual):
        raise AssertionError("symbolic w=2 intertwiner failed")
    gram = h * h.T
    if gram != (1 << (m - 1)) * sympy.eye(1 << (m - 1)):
        raise AssertionError("Walsh pairing is not invertible")
    return {
        "width": w,
        "states": 1 << (m - 1),
        "identity": "Q H = 2^(w^2) H K",
        "symbolic_entries_checked": residual.rows * residual.cols,
        "walsh_gram": f"H H^T={1 << (m - 1)} I",
    }


def _modular_case(w: int, seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    m = w * w
    a = tuple(rng.randrange(1, PRIME) for _ in transverse_edges(w))
    u = tuple(rng.randrange(1, PRIME) for _ in range(m))
    k = parity_transfer_mod(w, a, u, PRIME)
    q = quotient_spin_transfer_mod(w, a, u, PRIME)
    h = tuple(tuple(value % PRIME for value in row) for row in walsh_pairing(m))
    qh = matmul_mod(q, h, PRIME)
    hk = matmul_mod(h, k, PRIME)
    scale = pow(2, m, PRIME)
    if qh != tuple(tuple(scale * value % PRIME for value in row) for row in hk):
        raise AssertionError(f"modular w={w} intertwiner failed")
    return {
        "width": w,
        "states": 1 << (m - 1),
        "seed": seed,
        "field": f"GF({PRIME})",
        "identity_holds": True,
    }


def verify() -> dict[str, object]:
    return {
        "claim_status": "PROVED algebraically; exact symbolic and modular replay controls",
        "theorem": (
            "For every w and arbitrary signed edge variables, the zero-field spin-slice "
            "transfer restricted to globally flip-even functions is intertwined with the "
            "even-parity frontier transfer by the finite Walsh character table."
        ),
        "proof": (
            "Substitute z=x+y in (H K H^T)[s,t]. The z sum factors over transverse "
            "edges and the even-y sum is half the sum of connector products for t and -t."
        ),
        "controls": [_symbolic_w2(), _modular_case(2, 5202), _modular_case(3, 5303)],
        "claim_boundary": (
            "The bridge identifies the physical frontier only. It does not identify the "
            "additional character variables or prove any favorable scaling in w."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

