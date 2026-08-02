"""Exact Cycle 76 Huxley--Sargos denominator-cell ledger."""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from conventions.denominator_geometry_v1 import exponent_cell


TARGET_BASE = Q(6, 25)


def hs_denominator_cell(theta: Q, kappa: Q, alpha: Q) -> dict[str, object]:
    old = exponent_cell(theta, kappa, alpha)
    derivative = Q(1, 10) + alpha / 6 + theta / 3
    tube = 2 * theta / 3 - Q(2, 15) - kappa / 3
    ratio = (-1 + 3 * theta - alpha - kappa) / 3
    hs_fixed_a = max(Q(0), derivative, tube, ratio)
    fixed_a = min(theta, hs_fixed_a)
    total = alpha + fixed_a
    target = TARGET_BASE - kappa
    return {
        **old,
        "denominator_derivative_term": derivative,
        "denominator_tube_term": tube,
        "denominator_ratio_term": ratio,
        "denominator_constant_term": Q(0),
        "hs_fixed_a_exponent": hs_fixed_a,
        "fixed_a_after_trivial_min": fixed_a,
        "summed_numerator_count_exponent": total,
        "denominator_strict_margin": target - total,
        "denominator_strictly_closed": total < target,
        "new_beyond_cycle75": bool(old["live_residual"] and total < target),
    }


def verify_all() -> dict[str, object]:
    witness = hs_denominator_cell(Q(6, 25), Q(0), Q(0))
    endpoint = hs_denominator_cell(Q(6, 25), Q(0), Q(9, 175))
    no_improvement = hs_denominator_cell(Q(3, 20), Q(0), Q(0))
    if not witness["new_beyond_cycle75"]:
        raise RuntimeError("new denominator wedge witness")
    if witness["summed_numerator_count_exponent"] != Q(9, 50):
        raise RuntimeError("witness count")
    if witness["denominator_strict_margin"] != Q(3, 50):
        raise RuntimeError("witness margin")
    if endpoint["denominator_strictly_closed"] or endpoint["denominator_strict_margin"] != 0:
        raise RuntimeError("denominator endpoint tie")
    if no_improvement["fixed_a_after_trivial_min"] != Q(3, 20):
        raise RuntimeError("theta transition")
    if witness["denominator_derivative_term"] <= witness["denominator_tube_term"]:
        raise RuntimeError("derivative must dominate tube")
    if witness["denominator_derivative_term"] <= witness["denominator_ratio_term"]:
        raise RuntimeError("derivative must dominate ratio")
    return {
        "fixed_a_bound": "u=min(theta,1/10+alpha/6+theta/3)",
        "summed_bound": "alpha+u",
        "improvement_region": "theta>3/20 and alpha<4*theta-3/5",
        "strict_closure": "7*alpha/6+theta/3+kappa<7/50",
        "new_witness": "(theta,kappa,alpha)=(6/25,0,0) ties Cycle 75 at 6/25 but denominator HS gives 9/50",
        "endpoint_tie": "(theta,kappa,alpha)=(6/25,0,9/175)",
        "gate": "remove the denominator HS wedge; E14/E15 remain open on the twice-compressed residual",
    }


if __name__ == "__main__":
    print(verify_all())
