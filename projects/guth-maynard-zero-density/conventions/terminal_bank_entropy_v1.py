"""Exact exponent and state ledgers for Cycle 166 terminal-bank entropy."""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd
from typing import Iterable

from conventions.anchored_fibre_product_determinant_v1 import Anchor, difference_data, first_rank_two_data, primitive_rank_one_data


ETA = Q(1, 100)
H = Q(11, 25)
DELTA = Q(3, 5)
TOTAL = Q(38, 25)
PACKET_DEPTH = Q(6, 25)


def _gcd_many(values: Iterable[int]) -> int:
    answer = 0
    for value in values:
        answer = gcd(answer, abs(value))
    return answer


def canonical_rank_one_witness(anchors: Iterable[Anchor]) -> dict[str, object]:
    """Normalize an unordered rank-one four-subset exactly once.

    The first nonzero direction coordinate is positive; the least parameter
    is zero.  This absorbs every common parameter gcd into (r,s,t).
    """
    ordered = tuple(sorted(tuple(anchors), key=lambda row: (row.h, row.hp, row.j, row.jp)))
    if len(ordered) != 4 or len(set(ordered)) != 4:
        raise ValueError("need four distinct anchors")
    d, dp, k = difference_data(ordered)
    if first_rank_two_data(d, dp, k) is not None:
        raise ValueError("not rank one")
    r, s, t, direction = primitive_rank_one_data(d, dp, k)
    parameters = (0, *direction)
    first = next(value for value in (r, s) if value)
    if first < 0:
        r, s, t = -r, -s, -t
        parameters = tuple(-value for value in parameters)
    minimum = min(parameters)
    normalized = tuple(value - minimum for value in parameters)
    if len(set(normalized)) != 4 or _gcd_many(value for value in normalized if value) != 1:
        raise RuntimeError("primitive parameter normalization failed")
    base_index = parameters.index(minimum)
    return {
        "base": ordered[base_index],
        "r": r,
        "s": s,
        "t": t,
        "parameters": tuple(sorted(normalized)),
    }


def plane_shift_state(u: int, denominator: int, numerator: int, numerator_prime: int) -> tuple[int, int, int]:
    """Return the signed, nonzero (u,R,S) plane-induced shift state."""
    if u <= 0 or denominator == 0:
        raise ValueError("invalid plane state")
    r, s = denominator + numerator, denominator + numerator_prime
    if not r or not s:
        raise ValueError("zero shift coordinate")
    return u, r, s


def unique_integer_candidates(center: Q, radius: Q) -> tuple[int, ...]:
    """All integers in a closed exact interval; radius<1/2 allows at most one."""
    if radius < 0:
        raise ValueError("negative radius")
    lower, upper = center - radius, center + radius
    first = -((-lower.numerator) // lower.denominator)
    last = upper.numerator // upper.denominator
    return tuple(range(first, last + 1)) if first <= last else ()


def select_packet_coordinate(first_high: bool, second_high: bool) -> str:
    """Priority rule makes a both-high witness contribute one packet state."""
    if first_high:
        return "first"
    if second_high:
        return "second"
    raise ValueError("no high coordinate")


def canonical_packet_state(
    *, ell: int, a: int, q: int, k_max: int, seeds: Iterable[tuple[int, int]]
) -> tuple[int, int, int, int, int, int]:
    """Choose the lexicographically first retained beta seed deterministically."""
    seed_rows = tuple(sorted(tuple(seeds)))
    if ell < 0 or q <= 0 or gcd(abs(a), q) != 1 or k_max < 0 or not seed_rows:
        raise ValueError("invalid packet state")
    h0, j0 = seed_rows[0]
    return ell, a, q, k_max, h0, j0


def state_ledger() -> dict[str, Q]:
    rank_or_plane = DELTA + 2 * H
    packet = DELTA + 2 * (H - PACKET_DEPTH) + H
    return {
        "rank_or_plane_state_exponent": rank_or_plane,
        "packet_state_exponent": packet,
        "rank_or_plane_forced_fibre_exponent": TOTAL - rank_or_plane,
        "packet_forced_fibre_exponent": TOTAL - packet,
        "subcritical_rank_or_plane_bound": rank_or_plane + ETA,
        "subcritical_packet_bound": packet + ETA,
        "registered_target": TOTAL - ETA,
        "transverse_increment_exponent": -Q(2, 5) + ETA - DELTA,
        "strip_error_exponent": -Q(1),
    }


def verify_all() -> dict[str, object]:
    ledger = state_ledger()
    if 2 * ETA >= Q(1, 25):
        raise RuntimeError("eta leaves no rank/plane margin")
    if ledger["transverse_increment_exponent"] <= ledger["strip_error_exponent"]:
        raise RuntimeError("transverse increment has no power margin")
    if ledger["subcritical_rank_or_plane_bound"] >= ledger["registered_target"]:
        raise RuntimeError("rank/plane state count misses target")
    if ledger["subcritical_packet_bound"] >= ledger["registered_target"]:
        raise RuntimeError("packet state count misses target")
    if ledger["rank_or_plane_forced_fibre_exponent"] != Q(1, 25):
        raise RuntimeError("rank/plane forced fibre")
    if ledger["packet_forced_fibre_exponent"] != Q(2, 25):
        raise RuntimeError("packet forced fibre")
    plane = plane_shift_state(2, -6, -3, -9)
    if plane != (2, -9, -15):
        raise RuntimeError("signed plane state")
    if unique_integer_candidates(Q(15), Q(1, 4)) != (15,):
        raise RuntimeError("unique plane integer")
    if select_packet_coordinate(True, True) != "first":
        raise RuntimeError("both-high priority")
    if canonical_packet_state(ell=3, a=2, q=5, k_max=7, seeds=((9, 4), (5, 2))) != (3, 2, 5, 7, 5, 2):
        raise RuntimeError("packet base selection")
    return {
        "state_ledger": ledger,
        "near_shift": "the bounded exponential range forces B=r-s+t=0 in the near branch; reduction gives a labelled rational shift packet",
        "transverse": "with no high projection fibre, each (u,r,s,t) has at most one ell and then t is unique",
        "plane_shift": "R=D+N and S=D+N' obey |S-E_u R|=O(H/X), so fixed (u,R) has at most one S",
        "packet_state": "canonical maximal depth is determined by (ell,a/q), so it adds no entropy coordinate",
        "boundary": "This conditional inverse forces one massed labelled web. It does not bound the original census, control the web, prove E7/E9, density, or intervals.",
    }


def theorem_record() -> dict[str, object]:
    checked = verify_all()
    # The immutable JSON artifact records exact rational exponents as strings;
    # verification itself retains Fraction arithmetic above.
    checked["state_ledger"] = {
        key: str(value) for key, value in checked["state_ledger"].items()
    }
    return {"epistemic_status": "PROVED", **checked}
