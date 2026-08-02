"""Cycle 115 local Newton/critical-point turnover atlas."""

from __future__ import annotations

from math import exp, pi
from typing import Any


def local_constants(*, S2: float, M: float, x: float) -> tuple[float, float]:
    if min(S2, M, x) <= 0:
        raise ValueError("positive local data required")
    return S2 * exp(1.5 * M * x), S2 * exp(-1.5 * M * x)


def transition_floor(*, S2: float, M: float, x: float) -> float:
    upper, lower = local_constants(S2=S2, M=M, x=x)
    return lower * lower * x * x / (16 * upper)


def classify(*, delta: float, eta: float, S2: float, M: float, x: float) -> str:
    if min(delta, eta) < 0:
        raise ValueError("nonnegative residual data required")
    upper, lower = local_constants(S2=S2, M=M, x=x)
    newton = max(4 * delta / x, 2 * (upper * delta) ** 0.5)
    critical = lower * x / 2
    if eta >= newton:
        return "LOCAL_SIMPLE_ROOT"
    if eta <= critical:
        return "LOCAL_CRITICAL_POINT"
    if delta > lower * lower * x * x / (16 * upper):
        return "RESIDUAL_FLOOR"
    raise AssertionError("local trichotomy gap")


def theorem_record() -> dict[str, object]:
    return {
        "local_interval": "I=[x/2,3x/2]",
        "curvature": "ell_x=S2*exp(-3Mx/2)<=|f''|<=L_x=S2*exp(3Mx/2)",
        "simple": (
            "eta>=max(4delta/x,2sqrt(L_x delta)) gives a real root within 2delta/eta"
        ),
        "critical": (
            "eta<=ell_x*x/2 excludes same-sign modes and gives the unique critical point within eta/ell_x"
        ),
        "transition_floor": (
            "the remaining transition implies delta>ell_x^2*x^2/(16L_x)"
        ),
        "entropy_specialization": (
            "for x=2pi/D and M<=D, the floor is at least c_abs*S2/D^2 with c_abs=pi^2*exp(-9pi)/4"
        ),
        "boundary": (
            "the actual stationary tolerance has not yet been checked against c_abs*S2/D^2; simple-root averages and moment closure remain open"
        ),
    }
