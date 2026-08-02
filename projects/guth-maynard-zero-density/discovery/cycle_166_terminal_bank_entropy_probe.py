#!/usr/bin/env python3
"""Finite exact prototype for Cycle-166 primitive rank-one fibre accounting.

Discovery-only: this checks the integer parametrization, not the exponential
curve count or any analytic bound.
"""
from __future__ import annotations

from itertools import combinations
from fractions import Fraction
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions.anchored_fibre_product_determinant_v1 import Anchor, difference_data, primitive_rank_one_data


ETA = Fraction(1, 100)
H_EXPONENT = Fraction(11, 25)
DELTA_EXPONENT = Fraction(3, 5)


def gcd_many(values: tuple[int, ...]) -> int:
    answer = 0
    for value in values:
        answer = gcd(answer, abs(value))
    return answer


def primitive_four_count(parameters: set[int]) -> int:
    """Count canonical four-anchor parameter sets with least value zero."""
    if 0 not in parameters:
        raise ValueError("canonical fibre must contain zero")
    return sum(gcd_many(tuple(choice)) == 1 for choice in combinations(sorted(n for n in parameters if n > 0), 3))


def integer_collapse_holds(a_upper: Fraction, z_upper: Fraction, strip_error: Fraction) -> bool:
    """Check the sole hypothesis needed to force the integer B to vanish."""
    return a_upper * z_upper + strip_error < 1


def reduced_shift_packet(r: int, s: int) -> tuple[int, int, int]:
    """Return positive (q,a,g) for r/s after the near-shift sign forcing."""
    if r == 0 or s == 0 or r * s < 0:
        raise ValueError("near shift must have same nonzero signs")
    g = gcd(abs(r), abs(s))
    return abs(s) // g, (1 if s > 0 else -1) * r // g, g


def transverse_entropy_ledger() -> dict[str, Fraction]:
    """Exact exponent ledger for the Cycle-166 transverse projection bound."""
    transverse_a = -Fraction(2, 5) + ETA
    increment = transverse_a - DELTA_EXPONENT
    projection_count = DELTA_EXPONENT + 2 * H_EXPONENT
    witness_bound = projection_count + ETA
    registered_target = Fraction(38, 25) - ETA
    return {
        "eta": ETA,
        "transverse_a": transverse_a,
        "consecutive_increment": increment,
        "strip_error": Fraction(-1),
        "projection_count": projection_count,
        "witness_bound": witness_bound,
        "registered_target": registered_target,
        "saving_margin": registered_target - witness_bound,
    }


def seeded_packet_entropy_ledger() -> dict[str, Fraction]:
    """Exact exponent ledger for canonical fixed-beta seeded packet states."""
    state_count = DELTA_EXPONENT + 2 * Fraction(1, 5) + H_EXPONENT
    witness_bound = state_count + ETA
    registered_target = Fraction(38, 25) - ETA
    return {
        "state_count": state_count,
        "witness_bound": witness_bound,
        "registered_target": registered_target,
        "saving_margin": registered_target - witness_bound,
    }


def low_plane_shift_entropy_ledger() -> dict[str, Fraction]:
    """Exact exponent ledger for (u,R,S) low-plane shift states."""
    state_count = DELTA_EXPONENT + 2 * H_EXPONENT
    witness_bound = state_count + ETA
    registered_target = Fraction(38, 25) - ETA
    return {
        "state_count": state_count,
        "witness_bound": witness_bound,
        "registered_target": registered_target,
        "saving_margin": registered_target - witness_bound,
    }


def near_shift_entropy_ledger() -> dict[str, Fraction]:
    """Near shifts have the same state count once t=s-r is forced."""
    return low_plane_shift_entropy_ledger()


def multiplicative_transport_residual(*, h: int, j: int, beta: Fraction, y: Fraction, q: int, a: int, e_shift: Fraction) -> Fraction:
    """Exact residual after h'=qh/a, y'=((a+e_shift)/q)y, j'=j+h-h'."""
    if (q * h) % a:
        raise ValueError("a does not divide q*h")
    hp = q * h // a
    jp = j + h - hp
    yp = Fraction(a + e_shift, q) * y
    return jp + beta - hp * (yp - 1)


def low_plane_shift_residual(d: int, n: int, np: int, y: Fraction, yp: Fraction, e_shift: Fraction) -> Fraction:
    """Check S-E R from Cramer plane data, with E=yp/y+e_shift."""
    r, s = d + n, d + np
    return s - (yp / y + e_shift) * r


def canonical_rank_one(anchors: tuple[Anchor, Anchor, Anchor, Anchor]) -> dict[str, object]:
    """Return the unique primitive direction/base convention for four anchors."""
    d, dp, k = difference_data(anchors)
    r, s, t, direction = primitive_rank_one_data(d, dp, k)
    raw_parameters = (0, *direction)
    if next(value for value in (r, s) if value != 0) < 0:
        r, s, t = -r, -s, -t
        raw_parameters = tuple(-value for value in raw_parameters)
    offset = min(raw_parameters)
    parameters = tuple(value - offset for value in raw_parameters)
    base = anchors[raw_parameters.index(offset)]
    if gcd_many(tuple(value for value in parameters if value)) != 1:
        raise RuntimeError("nonprimitive parameter direction")
    return {"base": base, "r": r, "s": s, "t": t, "parameters": parameters}


def exact_examples() -> dict[str, object]:
    # alpha=1/3, alpha'=1/5, beta=0, with common parameter n=0,1,2,3.
    ordinary = (
        Anchor(3, 5, 1, 1), Anchor(6, 10, 2, 2),
        Anchor(9, 15, 3, 3), Anchor(12, 20, 4, 4),
    )
    ordinary_data = canonical_rank_one(ordinary)
    if (ordinary_data["r"], ordinary_data["s"], ordinary_data["t"], ordinary_data["parameters"]) != (3, 5, 0, (0, 1, 2, 3)):
        raise RuntimeError("ordinary primitive direction")
    # The same geometric line sampled at 0,2,4,6 must rescale its direction.
    rescaled = (
        Anchor(3, 5, 1, 1), Anchor(9, 15, 3, 3),
        Anchor(15, 25, 5, 5), Anchor(21, 35, 7, 7),
    )
    rescaled_data = canonical_rank_one(rescaled)
    if (rescaled_data["r"], rescaled_data["s"], rescaled_data["t"], rescaled_data["parameters"]) != (6, 10, 0, (0, 1, 2, 3)):
        raise RuntimeError("rescaled primitive direction")
    if primitive_four_count({0, 1, 2, 3, 4}) != 4:
        raise RuntimeError("primitive-four count")
    if not integer_collapse_holds(Fraction(1, 100), Fraction(5), Fraction(1, 100)):
        raise RuntimeError("integer-collapse threshold")
    if reduced_shift_packet(6, 10) != (5, 3, 2):
        raise RuntimeError("shift packet reduction")
    ledger = transverse_entropy_ledger()
    if ledger["consecutive_increment"] <= ledger["strip_error"]:
        raise RuntimeError("transverse increment has no margin")
    if ledger["witness_bound"] >= ledger["registered_target"]:
        raise RuntimeError("transverse count misses registered target")
    packet_ledger = seeded_packet_entropy_ledger()
    if packet_ledger["witness_bound"] >= packet_ledger["registered_target"]:
        raise RuntimeError("packet-state count misses registered target")
    plane_ledger = low_plane_shift_entropy_ledger()
    if plane_ledger["witness_bound"] >= plane_ledger["registered_target"]:
        raise RuntimeError("plane-shift state count misses registered target")
    near_ledger = near_shift_entropy_ledger()
    if near_ledger["witness_bound"] >= near_ledger["registered_target"]:
        raise RuntimeError("near-shift state count misses registered target")
    # y=3/2, E=5/3, y'=5/2; an exact beta-preserving multiplicative shift.
    if multiplicative_transport_residual(h=10, j=5, beta=Fraction(0), y=Fraction(3, 2), q=3, a=5, e_shift=Fraction(0)) != 0:
        raise RuntimeError("multiplicative beta transport")
    # D alpha=N and D alpha'=N' imply S=E R exactly in this finite model.
    if low_plane_shift_residual(6, 3, 9, Fraction(3, 2), Fraction(5, 2), Fraction(0)) != 0:
        raise RuntimeError("low plane shift elimination")
    return {
        "ordinary": {"r": 3, "s": 5, "t": 0, "parameters": [0, 1, 2, 3]},
        "rescaled": {"r": 6, "s": 10, "t": 0, "parameters": [0, 1, 2, 3]},
        "primitive_four_count_on_0_to_4": 4,
        "integer_collapse_example": True,
        "reduced_shift_packet_example": {"q": 5, "a": 3, "g": 2},
        "transverse_entropy_ledger": {key: str(value) for key, value in ledger.items()},
        "seeded_packet_entropy_ledger": {key: str(value) for key, value in packet_ledger.items()},
        "low_plane_shift_entropy_ledger": {key: str(value) for key, value in plane_ledger.items()},
        "near_shift_entropy_ledger": {key: str(value) for key, value in near_ledger.items()},
        "multiplicative_beta_transport_example": "exact",
        "low_plane_shift_elimination_example": "exact",
    }


if __name__ == "__main__":
    print(exact_examples())
