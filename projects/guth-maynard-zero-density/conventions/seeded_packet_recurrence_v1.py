"""Exact Cycle 67 seeded packet-recurrence ledger."""
from __future__ import annotations

from fractions import Fraction as Q


H = Q(11, 25)
CRITICAL_DEPTH = Q(6, 25)
DENOMINATOR_THRESHOLD = H - CRITICAL_DEPTH


def recurrence_ledger(theta: Q, kappa: Q) -> dict[str, object]:
    if theta < 0 or kappa < 0:
        raise ValueError("scale exponents must be nonnegative")
    return {
        "theta": theta,
        "kappa": kappa,
        "admissible": theta + kappa <= H,
        "one_sided_progression_count_exponent": kappa,
        "critical_or_deeper": kappa >= CRITICAL_DEPTH,
        "critical_denominator_for_maximal_depth": DENOMINATOR_THRESHOLD,
        "propagated_error": "|j0+ka+beta-(h0+kq)alpha|<=(C0+C1)/X for |k|<=K",
        "boundary_guarantee": "one sign has at least floor(K/2) admissible steps because qK<=H",
    }


def verify_all() -> dict[str, object]:
    critical = recurrence_ledger(Q(1, 5), Q(6, 25))
    if not critical["admissible"] or not critical["critical_or_deeper"]:
        raise RuntimeError("critical packet")
    if critical["critical_denominator_for_maximal_depth"] != Q(1, 5):
        raise RuntimeError("denominator interface")
    return {
        "seeded_identity": critical["propagated_error"],
        "realized_hit_count": "at least 1+floor(K/2) at strip constant C0+C1",
        "critical_interface": "K>=X^(6/25) gives realized AP degree X^(6/25-o(1)); maximal depth then requires q<=X^(1/5+o(1))",
        "scope_correction": "without one genuine transport seed, a beta-free packet supplies allowable differences only",
        "gate": "bound seeded deep packets or feed their realized AP rows to E7/E9/E10 with the enlarged constant tracked",
    }


if __name__ == "__main__":
    print(verify_all())
