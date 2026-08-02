"""Exact exponent ledger for the Cycle 35 prime-kernel engines."""
from __future__ import annotations

from fractions import Fraction as Q


MASS = Q(1)
HEIGHT = Q(12, 5)
SPACING = Q(3, 5)
THRESHOLD = Q(7, 10)
TARGET_COUNT = Q(21, 25)
FRACTIONAL_ORDER = Q(24, 5)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def hollow_fractional() -> dict[str, Q]:
    threshold_mass = FRACTIONAL_ORDER * THRESHOLD
    target_bound = threshold_mass + TARGET_COUNT
    global_bound = FRACTIONAL_ORDER
    saving = global_bound - target_bound
    coherent_zero = FRACTIONAL_ORDER * MASS
    require(threshold_mass == Q(84, 25), "fractional threshold exponent")
    require(target_bound == Q(21, 5), "hollow target exponent")
    require(saving == SPACING, "hollow saving must equal spacing")
    require(coherent_zero - target_bound == SPACING, "zero spike obstruction")
    return {
        "threshold_mass": threshold_mass,
        "target_bound": target_bound,
        "global_bound": global_bound,
        "required_saving": saving,
        "coherent_zero": coherent_zero,
    }


def curvature(eta: Q = Q(1, 100)) -> dict[str, Q]:
    time = SPACING + eta
    aggregate_correlation = Q(2) - time
    diagonal = MASS
    kernel_square = max(diagonal, aggregate_correlation)
    kernel = kernel_square / 2
    boundary_count = eta
    require(eta > 0 and eta < Q(2, 5), "eta range")
    require(kernel == THRESHOLD - eta / 2, "curvature pointwise saving")
    require(boundary_count < TARGET_COUNT, "boundary count must be subtarget")
    return {
        "time": time,
        "aggregate_correlation": aggregate_correlation,
        "diagonal": diagonal,
        "kernel_square": kernel_square,
        "kernel": kernel,
        "boundary_count": boundary_count,
    }


def phase_entropy() -> dict[str, Q]:
    normalized_bias = THRESHOLD - MASS
    per_row_entropy = 2 * normalized_bias
    accumulation_budget = TARGET_COUNT + per_row_entropy
    require(normalized_bias == Q(-3, 10), "normalized bias")
    require(per_row_entropy == -SPACING, "entropy defect exponent")
    require(accumulation_budget == Q(6, 25), "entropy budget")
    return {
        "normalized_bias": normalized_bias,
        "arc_count": -normalized_bias,
        "per_row_entropy": per_row_entropy,
        "target_accumulation_budget": accumulation_budget,
        "residual_shift_match": accumulation_budget,
    }


def histogram_pinsker(bias: Q, arc_error: Q) -> dict[str, Q]:
    """Exact algebra after the geometric arc-centre error is bounded."""
    require(bias > 0, "positive Fourier bias")
    require(0 <= arc_error <= bias / 2, "arc approximation error")
    l1_lower = bias - arc_error
    entropy_lower = l1_lower * l1_lower / 2
    coarse_entropy_lower = bias * bias / 8
    require(entropy_lower >= coarse_entropy_lower, "Pinsker lower bound")
    return {
        "bias": bias,
        "arc_error": arc_error,
        "l1_lower": l1_lower,
        "entropy_lower": entropy_lower,
        "coarse_entropy_lower": coarse_entropy_lower,
    }


def verify_all() -> dict[str, object]:
    rows = {
        "scale": {
            "mass": MASS,
            "height": HEIGHT,
            "spacing": SPACING,
            "threshold": THRESHOLD,
            "target_count": TARGET_COUNT,
        },
        "hollow_fractional": hollow_fractional(),
        "curvature": curvature(),
        "phase_entropy": phase_entropy(),
        "histogram_pinsker": histogram_pinsker(Q(1, 10), Q(1, 20)),
    }
    require(rows["hollow_fractional"]["required_saving"] == rows["scale"]["spacing"], "cross-engine spacing")
    require(rows["phase_entropy"]["target_accumulation_budget"] == Q(6, 25), "cross-engine entropy")
    return rows


if __name__ == "__main__":
    print(verify_all())
