#!/usr/bin/env python3
"""Quarantined orientation scan for the frozen C77 three-qubit packet.

Floating-point values nominate candidates only.  This program never emits a
mathematical counterexample claim; exact certification is a separate stage.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


VALUES = (-2, -1, 0, 1, 2)
Q_NUMERATORS = tuple(range(9, 16))
CONTROL_NUMERATOR = 8
EPS = 1e-9


def primitive_canonical_vectors():
    for u in itertools.product(VALUES, repeat=8):
        support = sum(x != 0 for x in u)
        if not 2 <= support <= 4:
            continue
        first = next(x for x in u if x)
        if first < 0:
            continue
        gcd = math.gcd(*(abs(x) for x in u))
        if gcd != 1:
            continue
        yield u


def two_body_marginals(u: tuple[int, ...]):
    vec = np.asarray(u, dtype=np.float64)
    rho = np.outer(vec, vec) / float(np.dot(vec, vec))
    tensor = rho.reshape((2,) * 6)
    rho_ab = np.trace(tensor, axis1=2, axis2=5)
    rho_ac = np.trace(tensor, axis1=1, axis2=4)
    rho_bc = np.trace(tensor, axis1=0, axis2=3)
    return rho_ab, rho_ac, rho_bc


def alignment_operator(rho_ab, rho_ac, rho_bc, q: float):
    Q = np.diag((q, 1.0 - q))
    ab = np.kron(rho_ab.reshape(4, 4), Q)
    ac = np.einsum("acdf,be->abcdef", rho_ac.reshape(2, 2, 2, 2), Q).reshape(8, 8)
    bc = np.einsum("ad,bcef->abcdef", Q, rho_bc.reshape(2, 2, 2, 2)).reshape(8, 8)
    return (ab + ac + bc) / 3.0


def target_operator(q: float):
    z = np.zeros((4, 4))
    z[0, 0] = 1.0
    return alignment_operator(z, z, z, q)


def main() -> None:
    targets = {a: np.cumsum(np.linalg.eigvalsh(target_operator(a / 16.0))[::-1])
               for a in Q_NUMERATORS}
    control_target = np.cumsum(
        np.linalg.eigvalsh(target_operator(CONTROL_NUMERATOR / 16.0))[::-1]
    )
    candidates = []
    rows = 0
    control_rows = 0
    control_max_excess = -float("inf")
    for u in primitive_canonical_vectors():
        rho_ab, rho_ac, rho_bc = two_body_marginals(u)
        control_spectrum = np.linalg.eigvalsh(
            alignment_operator(rho_ab, rho_ac, rho_bc, CONTROL_NUMERATOR / 16.0)
        )[::-1]
        control_max_excess = max(
            control_max_excess,
            float(np.max(np.cumsum(control_spectrum) - control_target)),
        )
        control_rows += 1
        for a in Q_NUMERATORS:
            spectrum = np.linalg.eigvalsh(
                alignment_operator(rho_ab, rho_ac, rho_bc, a / 16.0)
            )[::-1]
            excess = np.cumsum(spectrum) - targets[a]
            rows += 1
            for k, value in enumerate(excess[:-1], start=1):
                if value > EPS:
                    candidates.append({"u": u, "q_numerator": a, "k": k,
                                       "recognized_excess": float(value)})
    print(json.dumps({"claim_tag": "OBSERVED", "state_rows": rows // len(Q_NUMERATORS),
                      "matrix_rows": rows, "control_rows": control_rows,
                      "control_max_recognized_excess": control_max_excess,
                      "candidate_count": len(candidates),
                      "candidates": candidates[:32]}, sort_keys=True))


if __name__ == "__main__":
    main()
