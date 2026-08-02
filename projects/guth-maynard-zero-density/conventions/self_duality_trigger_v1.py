"""Exact Cycle 53 one-shot self-duality trigger ledger."""
from __future__ import annotations

from fractions import Fraction as Q


HARMONIC_RANGE = Q(3, 10)


def trigger_ledger(s: int) -> dict[str, Q | int | str]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive amplifier")
    ampr_total = Q(s) + Q(31, 10)
    selected_class = ampr_total - HARMONIC_RANGE
    one_shot_trigger = Q(2 * s + 2)
    gap = one_shot_trigger - selected_class
    return {
        "s": s,
        "ampr_total": ampr_total,
        "selected_r_plus_2v": selected_class,
        "one_shot_trigger": one_shot_trigger,
        "trigger_gap": gap,
        "status": "TRIGGERS" if gap < 0 else "NEEDS_MULTILINEARIZATION",
    }


def verify_all() -> dict[str, object]:
    s3 = trigger_ledger(3)
    s4 = trigger_ledger(4)
    if s3["trigger_gap"] != Q(11, 5):
        raise RuntimeError("s3 trigger gap")
    if s4["trigger_gap"] != Q(16, 5):
        raise RuntimeError("s4 trigger gap")
    return {"s3": s3, "s4": s4, "required_redesign": "coordinatewise_Bessel_or_centered_higher_trace"}


if __name__ == "__main__":
    print(verify_all())
