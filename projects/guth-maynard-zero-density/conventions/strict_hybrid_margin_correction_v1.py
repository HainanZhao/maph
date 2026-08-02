"""Exact Cycle 58 strict hybrid-trigger correction."""
from __future__ import annotations

from fractions import Fraction as Q


PENULTIMATE_GAP_WITH_Q = Q(3, 50)
PENULTIMATE_GAP_WITHOUT_Q = Q(1, 5)
Q_SAVING = Q(7, 50)


def adjusted_gap(hybrid_saving: Q, with_q_saving: bool = True) -> dict[str, object]:
    hybrid_saving = Q(hybrid_saving)
    if hybrid_saving < 0:
        raise RuntimeError("nonnegative hybrid saving")
    original_gap = PENULTIMATE_GAP_WITH_Q if with_q_saving else PENULTIMATE_GAP_WITHOUT_Q
    gap_after_saving = original_gap - hybrid_saving
    return {
        "with_cycle48_q_saving": with_q_saving,
        "original_gap": original_gap,
        "hybrid_saving": hybrid_saving,
        "adjusted_trigger_minus_selected": gap_after_saving,
        "strictly_triggers": gap_after_saving < 0,
        "status": "STRICTLY_TRIGGERS" if gap_after_saving < 0 else ("TIES_NO_TRIGGER" if gap_after_saving == 0 else "MISSES"),
    }


def verify_all() -> dict[str, object]:
    below = adjusted_gap(Q(1, 20), True)
    tie = adjusted_gap(Q(3, 50), True)
    above = adjusted_gap(Q(3, 50) + Q(1, 1000), True)
    powered_tie = adjusted_gap(Q(1, 5), False)
    if below["status"] != "MISSES":
        raise RuntimeError("below target")
    if tie["status"] != "TIES_NO_TRIGGER":
        raise RuntimeError("hybrid equality")
    if above["status"] != "STRICTLY_TRIGGERS":
        raise RuntimeError("strict hybrid surplus")
    if powered_tie["status"] != "TIES_NO_TRIGGER":
        raise RuntimeError("powered equality")
    if PENULTIMATE_GAP_WITH_Q + Q_SAVING != PENULTIMATE_GAP_WITHOUT_Q:
        raise RuntimeError("gap reconciliation")
    return {
        "below": below,
        "tie": tie,
        "strict_surplus_example": above,
        "powered_tie": powered_tie,
        "corrected_hybrid_target": "gamma>3/50 or gamma=3/50 plus an explicit non-exponent strict margin",
        "corrected_powered_target": "gamma_q>1/5 or gamma_q=1/5 plus an explicit non-exponent strict margin",
    }


if __name__ == "__main__":
    print(verify_all())
