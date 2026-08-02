"""Exact ledgers for the beta-anchored Cycle-165 determinant compiler.

This module records finite integer identities only.  Its asymptotic use keeps
the fixed-beta strip rows and their labels outside the module; no density or
transport count is asserted here.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb, gcd
from typing import Iterable


def pair_mass(fibre_sizes: Iterable[int]) -> int:
    """Return sum_{i<j} t_i t_j, with input validation."""
    sizes = tuple(fibre_sizes)
    if any(t < 0 for t in sizes):
        raise ValueError("negative fibre size")
    total = sum(sizes)
    return (total * total - sum(t * t for t in sizes)) // 2


def convex_four_anchor_lower(total_anchor_mass: int, label_pairs: int) -> int:
    """Exact minimum of sum binom(P_i,4) for nonnegative integral P_i."""
    if total_anchor_mass < 0 or label_pairs <= 0:
        raise ValueError("invalid convexity inputs")
    quotient, remainder = divmod(total_anchor_mass, label_pairs)
    return (label_pairs - remainder) * comb(quotient, 4) + remainder * comb(quotient + 1, 4)


def determinant3(a: tuple[int, int, int], b: tuple[int, int, int], c: tuple[int, int, int]) -> int:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def cross(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


@dataclass(frozen=True)
class Anchor:
    h: int
    hp: int
    j: int
    jp: int


@dataclass(frozen=True)
class RankTwoData:
    minor_indices: tuple[int, int]
    denominator: int
    numerator: int
    numerator_prime: int
    content: int
    content_prime: int


def difference_data(anchors: tuple[Anchor, Anchor, Anchor, Anchor]) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    base = anchors[0]
    d = tuple(row.h - base.h for row in anchors[1:])
    dp = tuple(row.hp - base.hp for row in anchors[1:])
    k = tuple((row.j - base.j) - (row.jp - base.jp) for row in anchors[1:])
    return d, dp, k


def first_rank_two_data(d: tuple[int, int, int], dp: tuple[int, int, int], k: tuple[int, int, int]) -> RankTwoData | None:
    for i, j in ((0, 1), (0, 2), (1, 2)):
        denominator = d[i] * dp[j] - d[j] * dp[i]
        if denominator:
            numerator = k[i] * dp[j] - k[j] * dp[i]
            numerator_prime = d[j] * k[i] - d[i] * k[j]
            return RankTwoData(
                (i, j), denominator, numerator, numerator_prime,
                gcd(abs(numerator), abs(denominator)),
                gcd(abs(numerator_prime), abs(denominator)),
            )
    return None


def determinant_integer_forcing_bound(strip_constant: int, h_diameter: int, x: int) -> tuple[int, int]:
    """Bound |(d cross d') dot error| by numerator/x for four strip anchors."""
    if strip_constant <= 0 or h_diameter < 0 or x <= 0:
        raise ValueError("invalid forcing inputs")
    # Three difference errors have size <=4C/X; each cross coordinate <=2H^2.
    return 24 * strip_constant * h_diameter * h_diameter, x


def cramer_error_bound(strip_constant: int, h_diameter: int, x: int) -> tuple[int, int]:
    """Bound either |D alpha-N| by numerator/x."""
    if strip_constant <= 0 or h_diameter < 0 or x <= 0:
        raise ValueError("invalid Cramer inputs")
    return 8 * strip_constant * h_diameter, x


def packet_depth(content: int, strip_constant: int, h_diameter: int) -> int:
    """A conservative integer depth satisfying the Cycle-67 error interface."""
    if content < 0 or strip_constant <= 0 or h_diameter <= 0:
        raise ValueError("invalid packet inputs")
    return content // (16 * strip_constant * h_diameter)


def reduced_fraction(denominator: int, numerator: int) -> tuple[int, int, int]:
    """Return the positive denominator, signed reduced numerator, and gcd."""
    if denominator == 0:
        raise ValueError("zero denominator")
    content = gcd(abs(numerator), abs(denominator))
    return abs(denominator) // content, (1 if denominator > 0 else -1) * numerator // content, content


def packet_safety(denominator: int, numerator: int, *, strip_constant: int, h_diameter: int) -> dict[str, int | bool]:
    """Conservative Cycle-67 ledger after normalizing C_* = max(1,C)."""
    if strip_constant <= 0 or h_diameter <= 0:
        raise ValueError("invalid packet inputs")
    c_star = max(1, strip_constant)
    q, a, content = reduced_fraction(denominator, numerator)
    depth = packet_depth(content, c_star, h_diameter)
    return {
        "C_star": c_star,
        "q": q,
        "a": a,
        "content": content,
        "depth": depth,
        "q_times_depth": q * depth,
        "denominator_bound": abs(denominator) <= 2 * h_diameter * h_diameter,
        "range_safe": q * depth <= h_diameter,
        "error_interface": depth == 0 or 8 * c_star * h_diameter * depth <= content,
    }


def primitive_rank_one_data(d: tuple[int, int, int], dp: tuple[int, int, int], k: tuple[int, int, int]) -> tuple[int, int, int, tuple[int, int, int]]:
    """Recover d=r*v, d'=s*v, k=t*v when the three vectors are parallel."""
    direction = d if any(d) else dp
    if not any(direction):
        raise ValueError("coincident four-anchor differences")
    scale = gcd(gcd(abs(direction[0]), abs(direction[1])), abs(direction[2]))
    v = tuple(entry // scale for entry in direction)
    index = next(i for i, entry in enumerate(v) if entry)
    def coefficient(vector: tuple[int, int, int]) -> int:
        if vector[index] % v[index]:
            raise ValueError("not integral along primitive direction")
        value = vector[index] // v[index]
        if vector != tuple(value * entry for entry in v):
            raise ValueError("vectors not parallel")
        return value
    return coefficient(d), coefficient(dp), coefficient(k), v


def terminal_bank(d: tuple[int, int, int], dp: tuple[int, int, int], k: tuple[int, int, int], *, high_content: int) -> str:
    """Disjoint priority routing of a labelled four-anchor witness."""
    if high_content <= 0:
        raise ValueError("nonpositive high-content threshold")
    data = first_rank_two_data(d, dp, k)
    if data is None:
        return "rank_one_resonance"
    if data.content >= high_content:
        return "rank_two_high_first_seeded_packet"
    if data.content_prime >= high_content:
        return "rank_two_high_second_seeded_packet"
    return "rank_two_low_content_plane"


def theorem_record() -> dict[str, object]:
    return {
        "epistemic_status": "PROVED",
        "pair_mass": "sum_{ell<ell'} t_ell t_ell'=(T^2-sum t_ell^2)/2",
        "convexity": "the balanced integral allocation exactly minimizes sum binom(P_(ell,ell'),4)",
        "integer_forcing": "four fixed-beta strip anchors force det[d|-d'|k]=0 once 24*C*H^2/X<1",
        "cramer": "each coordinate has |D*alpha-N|<=8*C*H/X before gcd reduction",
        "packet_safety": "with C_*=max(1,C), K=floor(g/(16*C_*H)) has error <=1/(KX) and qK<=H when |D|<=2H^2",
        "terminal_split": "rank one; high first content; high second content; low-low plane are disjoint and exhaustive",
        "boundary": "This is a finite labelled inverse compiler. It does not bound any terminal bank or prove a density or interval gain.",
    }
