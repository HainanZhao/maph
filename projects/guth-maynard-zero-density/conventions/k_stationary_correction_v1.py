"""Cycle 111 exact k-stationary-point correction."""

from __future__ import annotations

from typing import Any

import sympy as sp


def symbolic_correction() -> dict[str, Any]:
    c, Delta, c0, k, m = sp.symbols("c Delta c0 k m", positive=True)
    phase = c * Delta * sp.log(k * c0) - m * k
    derivative = sp.diff(phase, k)
    stationary = sp.solve(derivative, k)[0]
    second = sp.simplify(sp.diff(phase, k, 2).subs(k, stationary))
    value = sp.expand_log(sp.simplify(phase.subs(k, stationary)), force=True)
    expected_point = c * Delta / m
    expected_second = -(m**2) / (c * Delta)
    expected_value = c * Delta * (sp.log(c * c0 * Delta / m) - 1)
    if sp.simplify(stationary - expected_point) != 0:
        raise AssertionError("correct k stationary point mismatch")
    if sp.simplify(second - expected_second) != 0:
        raise AssertionError("correct k Hessian mismatch")
    if sp.simplify(value - expected_value) != 0:
        raise AssertionError("anchor-bearing stationary value mismatch")
    return {
        "phase": "c*Delta*log(k*c0)-m*k",
        "stationary_point": "k*=c*Delta/m",
        "hessian": "Phi''(k*)=-m^2/(c*Delta)",
        "stationary_value": "c*Delta*(log(c*c0*Delta/m)-1)",
        "anchor_location": "c0 is constant under k differentiation and remains in the stationary value",
    }


def theorem_record() -> dict[str, object]:
    return {
        **symbolic_correction(),
        "corrected_record": (
            "Cycle 108's displayed k*=c*c0*Delta/m is replaced by k*=c*Delta/m"
        ),
        "unaffected": (
            "Cycle 94 entropy and anchor relation, Cycle 108 Hessian amplitude and ell^(-3/2) "
            "scale law, Cycle 109 curvature bound, and Cycle 110 normalized split identity"
        ),
        "reaudit_required": (
            "any smooth cutoff or symbol norm evaluated using the Cycle 108 k-location must be "
            "rederived from the corrected point"
        ),
        "boundary": (
            "this correction does not yet provide the full outer-prefactor and anchor normalization ledger"
        ),
    }
