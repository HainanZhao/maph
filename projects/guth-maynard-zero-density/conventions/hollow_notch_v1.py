"""Exact Cycle 40 coherent-floor and target comparison ledger."""
from __future__ import annotations

from fractions import Fraction as Q


HARMONIC_RANGE = Q(3, 10)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def coherent_floor(s: int, harmonic_exponent: Q = HARMONIC_RANGE) -> dict[str, Q | int]:
    require(isinstance(s, int) and s >= 1, "fixed positive amplifier")
    require(harmonic_exponent >= 0, "nonnegative harmonic exponent")
    fixed_m_floor = Q(2 * s + 2) - harmonic_exponent
    vector_floor = Q(2 * s + 2)
    ampr_target = Q(s) + Q(31, 10)
    excess = vector_floor - ampr_target
    return {
        "amplifier": s,
        "fixed_m_floor": fixed_m_floor,
        "vector_floor": vector_floor,
        "ampr_target": ampr_target,
        "global_floor_excess_over_ampr": excess,
    }


def registered_scales() -> dict[str, object]:
    s3 = coherent_floor(3)
    s4 = coherent_floor(4)
    require(s3["fixed_m_floor"] == Q(77, 10), "s3 fixed-m floor")
    require(s3["vector_floor"] == Q(8), "s3 vector floor")
    require(s3["ampr_target"] == Q(61, 10), "s3 target")
    require(s3["global_floor_excess_over_ampr"] == Q(19, 10), "s3 excess")
    require(s4["fixed_m_floor"] == Q(97, 10), "s4 fixed-m floor")
    require(s4["vector_floor"] == Q(10), "s4 vector floor")
    require(s4["ampr_target"] == Q(71, 10), "s4 target")
    require(s4["global_floor_excess_over_ampr"] == Q(29, 10), "s4 excess")
    return {"s3": s3, "s4": s4}


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
