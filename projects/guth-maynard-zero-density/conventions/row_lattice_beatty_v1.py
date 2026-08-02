"""Exact Cycle 43 AP-row resonance and Beatty-strip ledger."""
from __future__ import annotations

from fractions import Fraction as Q


SPACING = Q(3, 5)
TARGET_ROWS = Q(21, 25)
PRIME_SCALE = Q(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def target_ledger(row_exponent: Q = TARGET_ROWS) -> dict[str, Q]:
    require(row_exponent >= 0, "nonnegative row exponent")
    log_window = -(row_exponent + SPACING)
    shift_window = PRIME_SCALE + log_window
    small_k_shift = PRIME_SCALE - SPACING
    linearization_error = 2 * small_k_shift - PRIME_SCALE
    return {
        "row_exponent": row_exponent,
        "spacing": SPACING,
        "log_resonance_window": log_window,
        "integer_shift_window": shift_window,
        "small_k_shift_scale": small_k_shift,
        "linearization_error": linearization_error,
    }


def registered_scales() -> dict[str, object]:
    target = target_ledger()
    maximal = target_ledger(Q(9, 5))
    require(target["log_resonance_window"] == Q(-36, 25), "target log window")
    require(target["integer_shift_window"] == Q(-11, 25), "target shift window")
    require(target["small_k_shift_scale"] == Q(2, 5), "small-k shift")
    require(target["linearization_error"] == Q(-1, 5), "linearization error")
    require(target["linearization_error"] > target["integer_shift_window"], "linearization is too coarse")
    require(maximal["integer_shift_window"] == Q(-7, 5), "maximal shift window")
    return {"target": target, "maximal_occupancy": maximal}


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
