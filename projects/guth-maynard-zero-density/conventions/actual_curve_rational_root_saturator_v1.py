"""Exact ledgers for the Cycle 177 positive-exponential rational-root family.

The analytic identity is symbolic: for
Delta=2*pi*L/log(1+1/r), the label ell=L has alpha=1/r exactly.
This module checks the resulting integer sums and exponent bookkeeping; it
does not approximate pi, logarithms, or exponentials.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import ceil, floor


H_EXPONENT = Q(11, 25)
PAIR_EXPONENT = 2 * H_EXPONENT
PAIR_TARGET = Q(17, 25)
TRIPLE_TARGET = Q(16, 25)
CRITICAL_PACKET_DEPTH = Q(6, 25)


def rational_root_identity(r: int) -> dict[str, str]:
    """Record exp(2*pi*L/Delta)-1=1/r under the defining Delta relation."""
    if r <= 0:
        raise ValueError("r must be positive")
    return {
        "base": f"1+1/{r}",
        "delta_definition": f"2*pi*L/log(1+1/{r})",
        "label_ratio": f"log(1+1/{r})/(2*pi)",
        "alpha_at_label": f"1/{r}",
    }


def pair_weight(height: int, r: int) -> int:
    """Exact Cycle-63 pair weight from d=r,2r,...,floor(H/r)r."""
    if height <= 0 or r <= 0:
        raise ValueError("height and r must be positive")
    multiplier_count = height // r
    return multiplier_count * height - r * multiplier_count * (multiplier_count + 1) // 2


def pair_lower_bound(height: int, r: int) -> int:
    """A deliberately weak integer lower bound H^2/(8r), rounded down."""
    if height < 4 * r:
        raise ValueError("need H>=4r")
    return height * height // (8 * r)


def strip_rows(height: int, r: int) -> int:
    """Number of exact beta=0 rows h in [H,2H] with h/r integral."""
    if height <= 0 or r <= 0:
        raise ValueError("height and r must be positive")
    return floor(2 * height / r) - ceil(height / r) + 1


def seeded_packet(height: int, r: int) -> dict[str, int]:
    """Construct a central exact beta-zero packet with a robust in-range fan."""
    if height < 8 * r:
        raise ValueError("need H>=8r")
    depth = height // (4 * r)
    multiplier = ceil(Q(3 * height, 2 * r))
    h0 = r * multiplier
    j0 = multiplier
    if not (height <= h0 - r * depth <= h0 + r * depth <= 2 * height):
        raise RuntimeError("central packet leaves the row interval")
    return {
        "q": r,
        "a": 1,
        "depth": depth,
        "h0": h0,
        "j0": j0,
        "row_count": 2 * depth + 1,
    }


def exponent_ledger() -> dict[str, Q]:
    """The exponents are independent of the fixed rational root r."""
    return {
        "height": H_EXPONENT,
        "pair_mass": PAIR_EXPONENT,
        "pair_target": PAIR_TARGET,
        "pair_target_gap": PAIR_EXPONENT - PAIR_TARGET,
        "direct_triple_mass": H_EXPONENT,
        "triple_target": TRIPLE_TARGET,
        "triple_target_gap": TRIPLE_TARGET - H_EXPONENT,
        "seeded_packet_depth": H_EXPONENT,
        "critical_packet_depth": CRITICAL_PACKET_DEPTH,
        "packet_depth_surplus": H_EXPONENT - CRITICAL_PACKET_DEPTH,
    }


def verify_all() -> dict[str, object]:
    if pair_weight(80, 5) != 600:
        raise RuntimeError("pair-weight identity")
    if pair_weight(80, 5) < pair_lower_bound(80, 5):
        raise RuntimeError("pair lower bound")
    if strip_rows(80, 5) != 17:
        raise RuntimeError("strip-row count")
    packet = seeded_packet(80, 5)
    if packet != {"q": 5, "a": 1, "depth": 4, "h0": 120, "j0": 24, "row_count": 9}:
        raise RuntimeError("central seeded packet")
    ledger = exponent_ledger()
    if ledger["pair_mass"] != Q(22, 25) or ledger["pair_target_gap"] != Q(1, 5):
        raise RuntimeError("pair exponent")
    if ledger["direct_triple_mass"] != Q(11, 25) or ledger["triple_target_gap"] != Q(1, 5):
        raise RuntimeError("triple exponent")
    if ledger["packet_depth_surplus"] != Q(1, 5):
        raise RuntimeError("packet-depth surplus")
    return {
        "rational_root": "For Delta=2*pi*L/log(1+1/r), ell=L has alpha_ell=1/r exactly.",
        "pair": "All d=kr<=H are exact pair hits and have total weight at least H^2/(8r) for H>=4r.",
        "triple": "At beta=0, exact strip rows in [H,2H] are precisely the multiples of r and number H/r+O(1).",
        "packet": "For H>=8r, a central beta-zero seed gives an exact q=r, a=1 packet of depth floor(H/(4r)) wholly inside the row interval.",
        "exponents": ledger,
        "boundary": "This is a continuous-scale actual-positive-exponential rational-root family. It disproves a uniform raw Cycle-63 pair target, but its one-label triple mass is only X^(11/25+o(1)); it proves no density or interval result.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
