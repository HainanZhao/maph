"""Exact Cycle 74 numerator-cell Huxley--Sargos ledger."""
from __future__ import annotations

from fractions import Fraction as Q


TARGET_BASE = Q(6, 25)


def hs_numerator_cell(theta: Q, kappa: Q, alpha: Q) -> dict[str, object]:
    if min(theta, kappa, alpha) < 0 or alpha > theta or theta + kappa > Q(11, 25):
        raise ValueError("cell outside numerator-resolved atlas")
    derivative = alpha + Q(1, 10) - theta / 2
    tube = alpha - Q(2, 15) - theta / 3 - kappa / 3
    ratio = (-1 + 2 * theta - kappa) / 3
    hs_fixed_q = max(Q(0), derivative, tube, ratio)
    fixed_q = min(alpha, hs_fixed_q)
    total = theta + fixed_q
    target = TARGET_BASE - kappa
    raw_total = theta + alpha
    return {
        "theta": theta,
        "kappa": kappa,
        "alpha": alpha,
        "derivative_term": derivative,
        "tube_term": tube,
        "ratio_term": ratio,
        "constant_term": Q(0),
        "hs_fixed_q_exponent": hs_fixed_q,
        "fixed_q_after_trivial_min": fixed_q,
        "summed_count_exponent": total,
        "target_exponent_open": target,
        "strict_margin": target - total,
        "strictly_closed": total < target,
        "raw_fraction_exponent": raw_total,
        "new_beyond_fraction_budget": raw_total >= target and total < target,
    }


def verify_all() -> dict[str, object]:
    new_cell = hs_numerator_cell(Q(11, 50), Q(0), Q(1, 50))
    endpoint_tie = hs_numerator_cell(Q(6, 25), Q(0), Q(1, 100))
    old_region = hs_numerator_cell(Q(1, 5), Q(0), Q(1, 100))
    if not new_cell["new_beyond_fraction_budget"]:
        raise RuntimeError("new Huxley--Sargos cell")
    if new_cell["summed_count_exponent"] != Q(23, 100):
        raise RuntimeError("new-cell count")
    if new_cell["strict_margin"] != Q(1, 100):
        raise RuntimeError("new-cell margin")
    if endpoint_tie["strictly_closed"] or endpoint_tie["summed_count_exponent"] != Q(6, 25):
        raise RuntimeError("theta endpoint tie")
    if old_region["fixed_q_after_trivial_min"] != old_region["alpha"]:
        raise RuntimeError("theta=1/5 transition")
    return {
        "fixed_q_bound": "w=min(alpha,max(0,alpha+1/10-theta/2))",
        "summed_bound": "theta+w",
        "transition": "theta=1/5",
        "lower_piece_closure": "if alpha<=theta/2-1/10, require theta+kappa<6/25",
        "upper_piece_closure": "if alpha>=theta/2-1/10, require alpha+theta/2+kappa<7/50",
        "new_cell": "(theta,kappa,alpha)=(11/50,0,1/50) ties raw count at 6/25 but HS gives 23/100",
        "gate": "remove the HS numerator wedge; average in q is still required on the residual cells",
    }


if __name__ == "__main__":
    print(verify_all())
