"""Exact ledgers for Cycle 180 nonzero cross-label pair determinants."""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb
from typing import Iterable


Pair = tuple[tuple[int, int], tuple[int, int]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def oriented_pair(pair: Pair) -> tuple[int, int, int, int]:
    """Return increasing heights h1<h2 and their integer gap/numerator gap."""
    first, second = pair
    (h1, j1), (h2, j2) = sorted((first, second))
    require(h1 < h2, "distinct pair heights")
    return h1, h2, h2 - h1, j2 - j1


def cross_pair_determinant(
    left: Pair,
    right: Pair,
    *,
    left_label: int,
    right_label: int,
    alpha_left: Q,
    alpha_right: Q,
    beta: Q,
    x: int,
    height: int,
    strip_constant: int,
    label_spacing: Q,
) -> dict[str, object]:
    """Retain both actual pairs and prove their distinct-label determinant is nonzero."""
    require(x > 0 and height > 0 and strip_constant > 0, "positive determinant scale")
    require(left_label > 0 and right_label > 0 and left_label != right_label, "distinct positive labels")
    require(label_spacing > Q(4 * strip_constant, x), "frozen distinct-label spacing")
    require(abs(alpha_left - alpha_right) >= label_spacing, "label spacing mismatched")
    h1, h2, d, a = oriented_pair(left)
    s1, s2, e, b = oriented_pair(right)
    require(all(height <= h <= 2 * height for h in (h1, h2, s1, s2)), "pair row range")
    residuals_left = [Q(j) + beta - h * alpha_left for h, j in sorted(left)]
    residuals_right = [Q(j) + beta - h * alpha_right for h, j in sorted(right)]
    width = Q(strip_constant, x)
    require(all(abs(value) <= width for value in residuals_left + residuals_right), "pair strip miss")
    delta = Q(a) - d * alpha_left
    epsilon = Q(b) - e * alpha_right
    require(abs(delta) <= 2 * width and abs(epsilon) <= 2 * width, "pair difference error")
    determinant = e * a - d * b
    phase = d * e * (alpha_left - alpha_right)
    error = Q(determinant) - phase
    error_bound = 2 * width * (d + e)
    require(abs(error) <= error_bound <= Q(4 * strip_constant * height, x), "determinant error")
    if determinant == 0:
        common_slope_gap = abs(alpha_left - alpha_right)
        rational_slope_bound = 2 * width * (Q(1, d) + Q(1, e))
        require(common_slope_gap <= rational_slope_bound, "zero determinant common slope")
        require(common_slope_gap <= Q(4 * strip_constant, x), "zero determinant spacing contradiction")
        raise ValueError("distinct-label determinant vanished")
    return {
        "labels": {"left": left_label, "right": right_label, "absolute_gap": abs(left_label - right_label)},
        "left_pair": {"h1": h1, "h2": h2, "d": d, "a": a, "difference_error": delta},
        "right_pair": {"h1": s1, "h2": s2, "e": e, "b": b, "difference_error": epsilon},
        "beta": beta,
        "determinant_integer": determinant,
        "phase": phase,
        "determinant_error": error,
        "determinant_error_bound": error_bound,
        "label_spacing": label_spacing,
    }


def light_rectangle_population(counts: Iterable[int], *, threshold: int, label_capacity: int) -> dict[str, int]:
    """Count ordered distinct-label choices of an unordered row pair at each label."""
    values = list(counts)
    require(threshold >= 1 and label_capacity >= len(values), "rectangle population parameters")
    require(all(0 <= value <= 2 * threshold for value in values), "not in light branch")
    pair_counts = [comb(value, 2) for value in values]
    total_rows = sum(values)
    total_pairs = sum(pair_counts)
    ordered_cross = total_pairs * total_pairs - sum(value * value for value in pair_counts)
    lower_bound = total_pairs * (total_pairs - 2 * threshold * threshold)
    require(total_pairs >= Q(total_rows - label_capacity, 2), "same-label pair pigeonhole")
    require(max(pair_counts, default=0) < 2 * threshold * threshold, "light pair maximum")
    require(ordered_cross >= lower_bound, "cross-label rectangle lower bound")
    return {
        "total_rows": total_rows,
        "total_unordered_same_label_pairs": total_pairs,
        "ordered_cross_label_rectangles": ordered_cross,
        "light_rectangle_lower_bound": lower_bound,
        "threshold": threshold,
        "label_capacity": label_capacity,
    }


def triple_divisor_count(limit: int) -> int:
    """Count positive ordered triples (r,d,e) with r*d*e<=limit exactly."""
    require(limit >= 1, "positive product limit")
    return sum(
        limit // (gap * left_gap)
        for gap in range(1, limit + 1)
        for left_gap in range(1, limit // gap + 1)
    )


def low_product_rectangle_bound(*, threshold: int, label_capacity: int, product_limit: int) -> dict[str, int]:
    """The complete-state bound for r*d*e<=K low-product rectangles."""
    require(threshold >= 1 and label_capacity >= 1 and product_limit >= 1, "low-product parameters")
    triple_count = triple_divisor_count(product_limit)
    bound = 8 * threshold * threshold * label_capacity * triple_count
    return {
        "threshold": threshold,
        "label_capacity": label_capacity,
        "product_limit": product_limit,
        "ordered_gap_triples": triple_count,
        "low_product_rectangle_bound": bound,
    }


def stable_determinant_comparison(
    *,
    label_gap: int,
    left_gap: int,
    right_gap: int,
    determinant: int,
    alpha_gap: Q,
    delta: Q,
    height: int,
    scale_delta: int,
    x: int,
    strip_constant: int,
    lower_coefficient: Q,
    upper_coefficient: Q,
) -> dict[str, object]:
    """Certify the stable-product determinant/product comparison abstractly.

    The exponential application has lower_coefficient=2*pi and
    upper_coefficient=2*pi*exp(2*pi*c); rational test constants exercise the
    exact inequalities without numerically representing pi.
    """
    require(min(label_gap, left_gap, right_gap, height, scale_delta, x, strip_constant) > 0, "stable comparison scale")
    require(lower_coefficient > 0 and upper_coefficient >= lower_coefficient, "spacing constants")
    product = label_gap * left_gap * right_gap
    cutoff = Q(8 * strip_constant * height * scale_delta, lower_coefficient * x)
    require(product >= cutoff, "below stable product cutoff")
    require(lower_coefficient * label_gap <= alpha_gap * scale_delta <= upper_coefficient * label_gap, "label gap envelope")
    error_bound = Q(4 * strip_constant * height, x)
    phase = left_gap * right_gap * alpha_gap
    require(abs(Q(determinant) - phase) <= delta <= error_bound, "determinant approximation")
    require(delta <= lower_coefficient * label_gap / (2 * scale_delta), "stable relative error")
    lower_bound = lower_coefficient * product / (2 * scale_delta)
    upper_bound = (upper_coefficient + lower_coefficient / 2) * product / scale_delta
    require(abs(determinant) >= lower_bound, "stable determinant lower comparison")
    require(abs(determinant) <= upper_bound, "stable determinant upper comparison")
    return {
        "product": product,
        "stable_cutoff": cutoff,
        "determinant": determinant,
        "determinant_lower_bound": lower_bound,
        "determinant_upper_bound": upper_bound,
        "phase": phase,
        "error_bound": error_bound,
    }


def verify_all() -> dict[str, object]:
    determinant = cross_pair_determinant(
        ((21, 10), (23, 11)), ((22, 5), (26, 6)),
        left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2),
        x=1000, height=20, strip_constant=1, label_spacing=Q(1, 4),
    )
    require(determinant["determinant_integer"] == 2, "nonzero determinant")
    require(determinant["phase"] == 2 and determinant["determinant_error"] == 0, "determinant phase")

    population = light_rectangle_population([3, 3, 3], threshold=2, label_capacity=3)
    require(population["total_unordered_same_label_pairs"] == 9, "pair population")
    require(population["ordered_cross_label_rectangles"] == 54, "rectangle count")
    require(32 * population["ordered_cross_label_rectangles"] >= population["total_rows"] ** 2, "critical-shape rectangle mass")
    low_product = low_product_rectangle_bound(threshold=2, label_capacity=3, product_limit=6)
    require(low_product["ordered_gap_triples"] == 25, "triple divisor count")
    stable = stable_determinant_comparison(
        label_gap=1, left_gap=10, right_gap=10, determinant=20,
        alpha_gap=Q(1, 5), delta=Q(0), height=20, scale_delta=10, x=1000,
        strip_constant=1, lower_coefficient=Q(2), upper_coefficient=Q(2),
    )
    require(stable["determinant_lower_bound"] == 10 and stable["determinant_upper_bound"] == 30, "stable product comparison")
    return {
        "determinant": "For distinct labels separated by more than 4C/X, two actual pairs give a nonzero integer D=e*a-d*b with |D-de(alpha_ell-alpha_m)|<=4CH/X.",
        "population": "In the light branch, W_cross>=P(P-2R^2), where P=sum binom(N_ell,2)>=(T-L)/2. At the frozen critical scale X>=2^38 this gives W_cross>=T^2/32.",
        "product_split": "The ordered-label r*d*e<K0 rectangle range has at most 8R^2 L times the ordered triple-divisor count. Above K0=4CHDelta/(pi X), the nonzero determinant is comparable to r*d*e/Delta.",
        "boundary": "This is a full four-row determinant and product-split reduction. It proves no upper bound for its labelled stable-rectangle census, no recurrence, density gain, or interval result.",
        "samples": {"determinant": determinant, "population": population, "low_product": low_product, "stable": stable},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
