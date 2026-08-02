"""Cycle 112 corrected full stationary symbol and anchor absorption."""

from __future__ import annotations

from typing import Any

import sympy as sp


def symbolic_full_symbol() -> dict[str, Any]:
    c, beta, H, Delta, m, n, np, k, r, rp, c0, Q = sp.symbols(
        "c beta H Delta m n np k r rp c0 Q", positive=True
    )
    jacobian = c ** sp.Rational(3, 2) * sp.sqrt(Delta * H * (H - Delta)) / (m * n * np)
    paired = c**2 / (r * rp)
    stationary = {k: c * Delta / m, r: c * H / n, rp: c * (H - Delta) / np}
    full = sp.simplify((paired * jacobian).subs(stationary))
    expected = c ** sp.Rational(3, 2) * sp.sqrt(Delta) / (m * sp.sqrt(H * (H - Delta)))
    if sp.simplify(full - expected) != 0:
        raise AssertionError("full stationary amplitude mismatch")
    chart_form = c**2 * sp.sqrt(k) / sp.sqrt(m * n * np * r * rp)
    if sp.simplify(expected.subs({Delta: k * m / c, H: r * n / c, H - Delta: rp * np / c}) - chart_form) != 0:
        raise AssertionError("chart amplitude mismatch")
    w1 = sp.simplify((r / (k * c0)).subs(stationary))
    w2 = sp.simplify((rp / (k * c0)).subs(stationary))
    v1 = sp.simplify(c * H / (Q * r)).subs(stationary)
    v2 = sp.simplify(c * (H - Delta) / (Q * rp)).subs(stationary)
    return {
        "full_amplitude": "c^(3/2)*sqrt(Delta)/(m*sqrt(H*(H-Delta)))",
        "chart_amplitude": "c^2*sqrt(k/(r*r'))/sqrt(m*n*n')",
        "W_arguments": (
            "beta^(-1)*log(H*m/(n*Delta*c0))",
            "beta^(-1)*log((H-Delta)*m/(n'*Delta*c0))",
        ),
        "V_arguments": ("n/Q", "n'/Q"),
        "anchor_role": "c0 only translates the two logarithmic W arguments; it is not a size prefactor",
    }


def anchor_absorption(*, scale: int, p0: int, q0: int, B0: int, C0: int, Q: int, support_floor_num: int = 1, support_floor_den: int = 2) -> bool:
    if min(scale, p0, q0, B0, C0, Q, support_floor_num, support_floor_den) <= 0:
        raise ValueError("positive data required")
    if B0 > Q or C0 > Q or scale * B0 % p0 or scale * C0 % q0:
        return False
    np_value = scale * B0 // p0
    m_value = scale * C0 // q0
    if min(np_value, m_value) * support_floor_den < support_floor_num * Q:
        return False
    return scale * support_floor_den >= support_floor_num * max(p0, q0)


def theorem_record() -> dict[str, object]:
    return {
        **symbolic_full_symbol(),
        "anchor_absorption": (
            "if B0,C0<=Q and the V-support has n',m>=aQ, then every supported actual scale satisfies lambda>=a*max(p0,q0)"
        ),
        "weighted_core": (
            "the anchor factor p0*sqrt(q0)/lambda^(3/2) is O_a(1), so Cycle 110's normalized split sum applies uniformly"
        ),
        "aggregate": (
            "one injective strong label per signed mode and 4*tau(|w|) split weight give M^(1+o(1)) arithmetic multiplicity, a 1/30 exponent saving over X^(19/30)"
        ),
        "boundary": (
            "the closure is for the registered smooth perfect-power strong branch only; nonsmooth payloads, irrational large degree, weak/simple roots, moments, density, and intervals remain open"
        ),
    }
