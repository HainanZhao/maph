"""Exact Cycle 80 primal phase-occupancy exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
K_MIN = Q(4, 15)
K_MAX = Q(83, 75)
RAW_TARGET = Q(31, 25)
OCCUPANCY = Q(22, 45)
PER_K = Q_EXP + (OCCUPANCY + D_EXP) / 2
NEW_CUTOFF = RAW_TARGET - PER_K


def occupancy_terms(xi: Q) -> dict[str, Q]:
    if xi < 0 or xi > K_MAX:
        raise ValueError("Fourier exponent outside support")
    derivative = D_EXP + (xi - 3 * D_EXP) / 6
    tube = D_EXP - Q_EXP / 3
    ratio = (-Q_EXP - (xi - 3 * D_EXP)) / 3
    bound = max(Q(0), derivative, tube, ratio)
    return {
        "xi": xi,
        "derivative_term": derivative,
        "tube_term": tube,
        "ratio_term": ratio,
        "occupancy_exponent": bound,
        "per_k_exponent": Q_EXP + (bound + D_EXP) / 2,
        "block_l1_exponent": xi + Q_EXP + (bound + D_EXP) / 2,
        "strictly_closed": xi + Q_EXP + (bound + D_EXP) / 2 < RAW_TARGET,
    }


def verify_all() -> dict[str, object]:
    bottom = occupancy_terms(K_MIN)
    top = occupancy_terms(K_MAX)
    boundary = occupancy_terms(NEW_CUTOFF)
    if bottom["occupancy_exponent"] != OCCUPANCY:
        raise RuntimeError("bottom occupancy")
    if top["occupancy_exponent"] != OCCUPANCY:
        raise RuntimeError("top occupancy")
    if PER_K != Q(79, 90):
        raise RuntimeError("per-k exponent")
    if NEW_CUTOFF != Q(163, 450):
        raise RuntimeError("new cutoff")
    if not bottom["strictly_closed"] or boundary["strictly_closed"]:
        raise RuntimeError("strict boundary convention")
    return {
        "occupancy": "A_k<=X^(22/45+o(1)) uniformly for 0<=xi<=83/75",
        "large_sieve": "sum_q|sum_d b_d e(qx_d)|^2<<X^o(1)*Q*A_k*sum_d|b_d|^2",
        "per_k": "|S_k|<=X^(79/90+o(1))",
        "closed_band": "4/15<=xi<163/450",
        "band_width": "43/450",
        "boundary": "xi=163/450 ties 31/25 and is not promoted",
        "gate": "remove the primal occupancy band; use double B-process for xi>=163/450",
    }


if __name__ == "__main__":
    print(verify_all())
