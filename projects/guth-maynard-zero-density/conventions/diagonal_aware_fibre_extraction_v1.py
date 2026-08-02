"""Exact finite ledgers for Cycle 178 fixed-beta fibre extraction.

The theorem is algebraic and applies to real alpha and beta.  This module
uses rational instances only to replay every integer/floor branch; its
determinant calculation is the convention source for the symbolic proof.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd
from typing import Iterable


Row = tuple[int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _ordered_rows(rows: Iterable[Row], *, height: int) -> list[Row]:
    ordered = sorted(rows)
    require(len(ordered) >= 3, "need at least three distinct fibre rows")
    require(len({h for h, _ in ordered}) == len(ordered), "one retained j per h")
    require(all(height <= h <= 2 * height for h, _ in ordered), "row leaves [H,2H]")
    return ordered


def extract_seeded_packet(
    rows: Iterable[Row],
    *,
    alpha: Q,
    beta: Q,
    x: int,
    height: int,
    strip_constant: int,
) -> dict[str, object]:
    """Extract a primitive seeded packet from an actual fixed-beta fibre.

    Preconditions are the exact rational analogue of the preregistered strip
    and the strict cutoff 4*C*H/X<1.  The output verifies every conclusion,
    including the zero- and negative-numerator branches.
    """
    require(x > 0 and height > 0 and strip_constant > 0, "positive scale data")
    require(Q(4 * strip_constant * height, x) < 1, "integer-forcing cutoff")
    ordered = _ordered_rows(rows, height=height)
    width = Q(strip_constant, x)
    require(
        all(abs(Q(j) + beta - h * alpha) <= width for h, j in ordered),
        "row misses fixed-beta strip",
    )

    gaps = [
        (ordered[index + 1][0] - ordered[index][0], index)
        for index in range(len(ordered) - 1)
    ]
    d0, gap_index = min(gaps)
    h_anchor, j_anchor = ordered[gap_index]
    h_next, j_next = ordered[gap_index + 1]
    a0 = j_next - j_anchor
    require(d0 > 0, "positive first gap")
    require(abs(d0 * alpha - a0) <= 2 * width, "first difference strip")
    common_rows: list[dict[str, int]] = []
    for h, j in ordered:
        d, b = h - h_anchor, j - j_anchor
        determinant = d0 * b - d * a0
        determinant_bound = 2 * width * (d0 + abs(d))
        require(determinant_bound < 1, "determinant not integer-forced")
        require(determinant == 0, "fixed-beta determinant failure")
        common_rows.append({"h": h, "j": j, "d": d, "b": b})

    divisor = gcd(d0, a0)
    require(divisor > 0, "primitive reduction divisor")
    q, a = d0 // divisor, a0 // divisor
    require(gcd(q, a) == 1, "primitive pair")
    for row in common_rows:
        require(row["d"] % q == 0, "common residue class")
        require(row["b"] == (row["d"] // q) * a, "common rational slope")

    first_h, first_j = ordered[0]
    last_h, last_j = ordered[-1]
    require((last_h - first_h) % q == 0, "integral endpoint span")
    span_multiple = (last_h - first_h) // q
    fibre_size = len(ordered)
    require(span_multiple >= fibre_size - 1, "integer span lower bound")
    require((fibre_size - 1) * d0 <= last_h - first_h <= height, "minimum-gap span bound")
    approximation_error = abs(q * alpha - a)
    require(
        approximation_error <= Q(2 * strip_constant, span_multiple * x),
        "span approximation bound",
    )
    depth = (fibre_size - 1) // 2
    require(depth >= 1, "positive extracted depth")
    require(q * depth <= height, "packet admissibility")
    require(
        approximation_error <= Q(strip_constant, depth * x),
        "Cycle-67 approximation bound",
    )

    progression: list[dict[str, object]] = []
    for k in range(depth + 1):
        h, j = first_h + k * q, first_j + k * a
        residual = abs(Q(j) + beta - h * alpha)
        require(h <= last_h <= 2 * height, "progression range")
        require(residual <= 2 * width, "propagated enlarged strip")
        progression.append({"k": k, "h": h, "j": j, "residual": residual})
    require(progression[-1]["h"] <= last_h, "forward fan lies in fibre span")
    require(last_j - first_j == span_multiple * a, "endpoint slope")

    return {
        "fibre_size": fibre_size,
        "seed": {"h": first_h, "j": first_j, "residual": abs(Q(first_j) + beta - first_h * alpha)},
        "minimum_gap": {"d0": d0, "a0": a0, "left_row_index": gap_index},
        "primitive_packet": {"q": q, "a": a, "depth": depth, "q_depth": q * depth},
        "approximation_error": approximation_error,
        "span_multiple": span_multiple,
        "integer_determinants": common_rows,
        "propagated_progression": progression,
        "enlarged_strip_constant": 2 * strip_constant,
    }


def cross_label_remainder(counts: Iterable[int], *, threshold: int) -> dict[str, int | bool]:
    """Exact diagonal extraction for counts indexed by distinct labels."""
    values = list(counts)
    require(threshold > 0, "positive heavy threshold")
    require(all(value >= 0 for value in values), "nonnegative fibre count")
    total = sum(values)
    diagonal = sum(value * value for value in values)
    cross = total * total - diagonal
    light = all(value <= 2 * threshold for value in values)
    lower_bound = total * (total - 2 * threshold)
    if light:
        require(diagonal <= 2 * threshold * total, "light diagonal bound")
        require(cross >= lower_bound, "cross-label remainder bound")
    return {
        "total": total,
        "diagonal": diagonal,
        "ordered_cross_label_mass": cross,
        "threshold": threshold,
        "light": light,
        "light_cross_lower_bound": lower_bound,
        "has_heavy_fibre": not light,
    }


def verify_all() -> dict[str, object]:
    common = dict(alpha=Q(1, 5), beta=Q(0), x=1000, height=20, strip_constant=1)
    positive = extract_seeded_packet([(20, 4), (30, 6), (40, 8)], **common)
    require(positive["primitive_packet"] == {"q": 5, "a": 1, "depth": 1, "q_depth": 5}, "positive primitive packet")
    require(positive["span_multiple"] == 4, "positive span")

    nonfirst_minimum = extract_seeded_packet(
        [(20, 10), (26, 13), (28, 14), (40, 20)],
        alpha=Q(1, 2),
        beta=Q(0),
        x=1000,
        height=20,
        strip_constant=1,
    )
    require(nonfirst_minimum["minimum_gap"] == {"d0": 2, "a0": 1, "left_row_index": 1}, "minimum gap selection")
    require(nonfirst_minimum["seed"]["h"] == 20, "left endpoint seed")

    zero = extract_seeded_packet(
        [(20, 0), (30, 0), (40, 0)],
        alpha=Q(1, 100000),
        beta=Q(0),
        x=1000,
        height=20,
        strip_constant=1,
    )
    require(zero["primitive_packet"] == {"q": 1, "a": 0, "depth": 1, "q_depth": 1}, "zero numerator packet")

    negative = extract_seeded_packet(
        [(20, -10), (22, -11), (24, -12)],
        alpha=Q(-1, 2),
        beta=Q(0),
        x=1000,
        height=20,
        strip_constant=1,
    )
    require(negative["primitive_packet"] == {"q": 2, "a": -1, "depth": 1, "q_depth": 2}, "negative numerator packet")

    light = cross_label_remainder([6, 6], threshold=3)
    require(light == {
        "total": 12,
        "diagonal": 72,
        "ordered_cross_label_mass": 72,
        "threshold": 3,
        "light": True,
        "light_cross_lower_bound": 72,
        "has_heavy_fibre": False,
    }, "light cross remainder")
    heavy = cross_label_remainder([7, 1], threshold=3)
    require(heavy["has_heavy_fibre"] and not heavy["light"], "heavy threshold")
    return {
        "theorem": "Under 4CH/X<1, every N>=3 actual fixed-beta fibre yields a primitive seeded q,a packet of depth floor((N-1)/2), retained error at most C/(KX), and an in-range one-sided 2C/X fan of K+1 rows.",
        "diagonal_extraction": "With R=ceil(X^(6/25)), either a fibre has N>=2R+1 and hence depth at least R, or U_cross=T^2-sum N_ell^2 is at least T(T-2R).",
        "boundary": "This is an actual-row inverse and exact heavy/light reduction. It gives no cross-label analytic upper bound, E7/E9 skeleton bound, density improvement, or interval result.",
        "samples": {"positive": positive, "nonfirst_minimum": nonfirst_minimum, "zero_numerator": zero, "negative_numerator": negative, "light": light, "heavy": heavy},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
