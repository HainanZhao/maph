"""Exact Cycle 41 annular sampling exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


HEIGHT = Q(12, 5)
SPACING = Q(3, 5)
HARMONIC_RANGE = Q(3, 10)
ROW_CAP = HEIGHT - SPACING
DECAY_ORDER = 9


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def leakage(s: int, decay_order: int = DECAY_ORDER) -> dict[str, Q | int]:
    require(isinstance(s, int) and s >= 1, "fixed positive amplifier")
    require(isinstance(decay_order, int) and decay_order >= 1, "positive decay order")
    exponent = Q(2 * s + 2) + ROW_CAP + HARMONIC_RANGE - decay_order * SPACING
    target = Q(s) + Q(31, 10)
    margin = target - exponent
    return {
        "amplifier": s,
        "decay_order": decay_order,
        "leakage_exponent": exponent,
        "ampr_target": target,
        "leakage_margin": margin,
    }


def registered_scales() -> dict[str, object]:
    s3 = leakage(3)
    s4 = leakage(4)
    require(s3["leakage_exponent"] == Q(47, 10), "s3 leakage")
    require(s3["leakage_margin"] == Q(7, 5), "s3 leakage margin")
    require(s4["leakage_exponent"] == Q(67, 10), "s4 leakage")
    require(s4["leakage_margin"] == Q(2, 5), "s4 leakage margin")
    return {
        "decay_order": DECAY_ORDER,
        "s3": s3,
        "s4": s4,
        "annular_vector_target_s3": Q(61, 10),
        "annular_vector_target_s4": Q(71, 10),
    }


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
