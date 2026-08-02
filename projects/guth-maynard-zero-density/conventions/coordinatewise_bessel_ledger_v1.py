"""Exact Cycle 54 conditional coordinatewise-Bessel exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


Q_POWERED_SAVING = Q(7, 50)


def exposure_row(s: int, ordinary_exposures: int, use_q_saving: bool) -> dict[str, Q | int | bool | str]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive amplifier")
    if not isinstance(ordinary_exposures, int) or not 0 <= ordinary_exposures <= s:
        raise RuntimeError("ordinary exposure range")
    selected_level = Q(s) + Q(14, 5)
    saving = Q_POWERED_SAVING if use_q_saving else Q(0)
    candidate_trigger = Q(2 * s + 2 - ordinary_exposures) - saving
    signed_gap = candidate_trigger - selected_level
    return {
        "s": s,
        "ordinary_exposures": ordinary_exposures,
        "q_powered_saving_used": use_q_saving,
        "q_powered_saving": saving,
        "selected_r_plus_2v": selected_level,
        "candidate_trigger": candidate_trigger,
        "signed_gap_trigger_minus_selected": signed_gap,
        "status": "TRIGGERS" if signed_gap < 0 else "MISSES_STRICT_TRIGGER",
    }


def amplifier_ledger(s: int) -> dict[str, object]:
    without_q = [exposure_row(s, j, False) for j in range(s + 1)]
    with_q = [exposure_row(s, j, True) for j in range(s + 1)]
    first_trigger = next((row["ordinary_exposures"] for row in with_q if row["status"] == "TRIGGERS"), None)
    if first_trigger is None:
        outcome = "CONTRACT_INSUFFICIENT"
    elif first_trigger == s:
        outcome = "FULL_ORDINARY_EXPOSURE_NECESSARY"
    else:
        outcome = "EARLY_TRIGGER"
    return {
        "s": s,
        "without_q_saving": without_q,
        "with_q_saving": with_q,
        "first_trigger_with_q_saving": first_trigger,
        "outcome": outcome,
    }


def verify_all() -> dict[str, object]:
    s3 = amplifier_ledger(3)
    s4 = amplifier_ledger(4)
    for data in (s3, s4):
        s = data["s"]
        penultimate = data["with_q_saving"][s - 1]
        final = data["with_q_saving"][s]
        if penultimate["signed_gap_trigger_minus_selected"] != Q(3, 50):
            raise RuntimeError("penultimate gap")
        if final["signed_gap_trigger_minus_selected"] != -Q(47, 50):
            raise RuntimeError("full exposure margin")
        if data["outcome"] != "FULL_ORDINARY_EXPOSURE_NECESSARY":
            raise RuntimeError("design outcome")
    return {
        "s3": s3,
        "s4": s4,
        "design_conclusion": "all_s_ordinary_coordinates_required_even_after_q_powered_saving",
    }


if __name__ == "__main__":
    print(verify_all())
