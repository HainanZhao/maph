#!/usr/bin/env python3
"""Exact universal-cover cochain audit for Cycle 231/B068."""
from __future__ import annotations

import json
from fractions import Fraction


def audit() -> dict[str, object]:
    """Solve the frozen ansatz and test its full deck multiplier.

    Write L=log(576), P(w)=A*w^2+B*w+C, and H=exp(P).  The
    scaling equation exp(P(w+L)-P(w))=exp(-4*w) forces, for some
    n in Z, 2*A*L=-4 and A*L^2+B*L=2*pi*i*n.  The deck multiplier has
    w coefficient 4*pi*i*A, which is nonzero for every such solution.
    """
    L = "log(576)"
    # Keep all forced coefficients exact.  `a_times_l` is A*L, so no
    # floating-point approximation to log(576) enters the proof.
    a_times_l = Fraction(-2)
    scaling_w = 2 * a_times_l
    deck_w_in_pi_i_over_l = 4 * a_times_l
    assert scaling_w == -4
    assert deck_w_in_pi_i_over_l == -8
    assert deck_w_in_pi_i_over_l != 0
    a = "-2/log(576)"
    b = "2 + 2*pi*i*n/log(576), n in Z"
    scaling_w_coefficient = "2*A*log(576) = -4"
    scaling_constant = "A*log(576)^2 + B*log(576) = 2*pi*i*n"
    deck_w_coefficient = "4*pi*i*A = -8*pi*i/log(576)"
    return {
        "epistemic_status": "PROVED",
        "cover": {"coordinate": "mu=exp(w)", "scaling": f"w -> w + {L}", "deck": "w -> w + 2*pi*i"},
        "frozen_equation": "H(w+log(576))/H(w)=exp(-4*w)",
        "ansatz": "H(w)=exp(A*w^2+B*w+C)",
        "solution_family": {"A": a, "B": b, "C": "arbitrary complex constant"},
        "coefficient_comparison": {
            "a_times_log_576": str(a_times_l),
            "exact_scaling_w_coefficient": str(scaling_w),
            "exact_deck_w_coefficient_in_units_pi_i_over_log_576": str(deck_w_in_pi_i_over_l),
            "scaling_w_coefficient": scaling_w_coefficient,
            "scaling_constant_mod_2pi_i": scaling_constant,
            "deck_w_coefficient": deck_w_coefficient,
        },
        "descent": {
            "deck_multiplier_is_constant": False,
            "descends_single_valuedly": False,
            "reason": "The nonzero deck w coefficient is forced by the order-four residual term for every integer n.",
        },
        "reflection": {
            "source_reflection_test": "UNAVAILABLE_AFTER_DESCENT_FAILURE",
            "reason": "The freeze permits source reflection only for a single-valued descended cochain; it supplies no alternative lifted reflection.",
        },
        "conclusion": "The frozen quadratic-exponential cover ansatz solves the formal scaling equation but cannot descend to a single-valued cochain. This obstructs only that ansatz, not other cover, essential, periodic-corrected, enlarged-action, AFK, fusion, Stark, or TCC constructions.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
