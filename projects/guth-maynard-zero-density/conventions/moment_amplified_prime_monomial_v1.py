"""Exact Cycle 39 coefficient and exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q
from math import factorial


HEIGHT = Q(12, 5)
SPACING = Q(3, 5)
HARMONIC_RANGE = Q(3, 10)
THRESHOLD = Q(7, 10)
MASS = Q(1)
TARGET_COUNT = Q(21, 25)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def coefficient_ledger(s: int) -> dict[str, int | str]:
    require(isinstance(s, int) and s >= 1, "fixed positive moment amplifier")
    candidate_q_bound = 1 + s // 2
    ordered_residual_bound = factorial(s)
    coefficient_bound = candidate_q_bound * ordered_residual_bound
    return {
        "amplifier": s,
        "candidate_q_bound": candidate_q_bound,
        "ordered_residual_bound": ordered_residual_bound,
        "coefficient_bound": coefficient_bound,
        "coefficient_sum": "M^(s+1)",
        "coefficient_square_norm_lower": "M^(s+1)",
        "coefficient_square_norm_upper": "C_s*M^(s+1)",
        "uniform_harmonic_range": "every integer m>=2",
    }


def amplified_ledger(s: int, energy_decay: Q) -> dict[str, Q | int]:
    require(isinstance(s, int) and s >= 1, "fixed positive moment amplifier")
    require(energy_decay >= 0, "nonnegative harmonic-energy decay")
    per_row = 2 * s * THRESHOLD + 2 * MASS - energy_decay
    restriction_target = Q(s) + MASS + (HEIGHT - SPACING) + HARMONIC_RANGE
    count_bound = restriction_target - per_row
    margin = TARGET_COUNT - count_bound
    return {
        "amplifier": s,
        "energy_decay": energy_decay,
        "per_row_energy": per_row,
        "restriction_target": restriction_target,
        "conditional_count_bound": count_bound,
        "target_count": TARGET_COUNT,
        "closing_margin": margin,
    }


def least_closing_moment(energy_decay: Q, cap: int = 20) -> int:
    require(cap >= 1, "positive search cap")
    for s in range(1, cap + 1):
        if amplified_ledger(s, energy_decay)["closing_margin"] >= 0:
            return s
    raise RuntimeError("no closing moment below cap")


def registered_scales() -> dict[str, object]:
    r2_unamplified = amplified_ledger(1, Q(3, 5))
    r4_unamplified = amplified_ledger(1, Q(6, 5))
    r2 = amplified_ledger(3, Q(3, 5))
    r4 = amplified_ledger(4, Q(6, 5))
    require(r2["per_row_energy"] == Q(28, 5), "r2 amplified row energy")
    require(r2["restriction_target"] == Q(61, 10), "r2 restriction target")
    require(r2["conditional_count_bound"] == Q(1, 2), "r2 count")
    require(r2["closing_margin"] == Q(17, 50), "r2 margin")
    require(r4["per_row_energy"] == Q(32, 5), "r4 amplified row energy")
    require(r4["restriction_target"] == Q(71, 10), "r4 restriction target")
    require(r4["conditional_count_bound"] == Q(7, 10), "r4 count")
    require(r4["closing_margin"] == Q(7, 50), "r4 margin")
    require(r2_unamplified["conditional_count_bound"] == Q(13, 10), "unamplified r2")
    require(r4_unamplified["conditional_count_bound"] == Q(19, 10), "unamplified r4")
    require(least_closing_moment(Q(3, 5)) == 3, "least r2 moment")
    require(least_closing_moment(Q(6, 5)) == 4, "least r4 moment")
    return {
        "scale": {
            "height": HEIGHT,
            "spacing": SPACING,
            "harmonic_range": HARMONIC_RANGE,
            "threshold": THRESHOLD,
            "mass": MASS,
            "target_count": TARGET_COUNT,
        },
        "unamplified_r2": r2_unamplified,
        "unamplified_r4": r4_unamplified,
        "closing_r2": r2,
        "closing_r4": r4,
        "coefficients_s3": coefficient_ledger(3),
        "coefficients_s4": coefficient_ledger(4),
    }


def verify_all() -> dict[str, object]:
    rows = registered_scales()
    require(rows["coefficients_s3"]["coefficient_bound"] == 12, "s3 coefficient bound")
    require(rows["coefficients_s4"]["coefficient_bound"] == 72, "s4 coefficient bound")
    return rows


if __name__ == "__main__":
    print(verify_all())
