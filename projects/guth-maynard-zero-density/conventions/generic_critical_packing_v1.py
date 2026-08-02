"""Cycle 101 compact rational packing for generic critical fibers."""

from __future__ import annotations

from fractions import Fraction
from math import exp, gcd, sqrt

from conventions.critical_fiber_atlas_v1 import divisor_count


def validate_labels(labels: list[Fraction], L: float) -> None:
    if L < 0:
        raise ValueError("L must be nonnegative")
    if len(set(labels)) != len(labels):
        raise ValueError("labels must be distinct")
    lower, upper = exp(-L), exp(L)
    for label in labels:
        if label <= 0 or not lower <= float(label) <= upper:
            raise ValueError("label outside compact ratio interval")


def packing_record(labels: list[Fraction], L: float) -> dict[str, object]:
    validate_labels(labels, L)
    compactness = exp(L)
    heights = sorted(min(label.numerator, label.denominator) for label in labels)
    reciprocal_sum = sum(1.0 / height for height in heights)
    bound = 2.0 * compactness * sqrt(len(labels))
    return {
        "count": len(labels),
        "K_L": compactness,
        "ordered_min_heights": heights,
        "reciprocal_height_sum": reciprocal_sum,
        "reciprocal_height_bound": bound,
        "passes": reciprocal_sum <= bound + 1e-12,
    }


def aggregate_generic_bound(Q: int, M: int, L: float, label_count: int) -> dict[str, object]:
    if min(Q, M) <= 0 or not 0 <= label_count <= 4 * M:
        raise ValueError("invalid aggregate parameters")
    max_tau = max(divisor_count(n) for n in range(1, 2 * M + 1))
    compactness = exp(L)
    count_bound = 4.0 * compactness * Q * max_tau * sqrt(label_count)
    uniform_bound = 8.0 * compactness * Q * max_tau * sqrt(M)
    return {
        "T_M": max_tau,
        "label_count": label_count,
        "count_sensitive_bound": count_bound,
        "uniform_bound": uniform_bound,
        "actual_exponent": "1/3+(1/2)(3/5)=19/30",
    }


def reduced_compact_labels(height: int, L: float) -> list[Fraction]:
    labels = {
        Fraction(numerator, denominator)
        for numerator in range(1, height + 1)
        for denominator in range(1, height + 1)
        if gcd(numerator, denominator) == 1
        and exp(-L) <= numerator / denominator <= exp(L)
    }
    return sorted(labels)


def theorem_record() -> dict[str, object]:
    return {
        "height_count": "#{j:min(N_j,R_j)<=Y}<=K_L^2*Y^2",
        "ordered_height": "z_j>=sqrt(j)/K_L",
        "reciprocal_sum": "sum_j 1/z_j<=2*K_L*sqrt(J)",
        "cycle100_input": "F_generic(j)<=2*Q*tau(abs(w_j))/z_j",
        "aggregate": "sum_j F_generic(j)<=4*K_L*Q*T_M*sqrt(J)",
        "uniform": "J<=4*M gives <=8*K_L*Q*T_M*sqrt(M)",
        "actual_exponent": "Q*M^(1/2+o(1))=X^(19/30+o(1))",
        "boundary": "cross-valuation, weak, and simple-root rows are excluded",
    }
