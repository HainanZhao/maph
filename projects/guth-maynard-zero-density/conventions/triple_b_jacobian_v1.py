"""Cycle 108 triple-B leading Jacobian summability."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import sympy as sp


def symbolic_jacobian_record() -> dict[str, Any]:
    ell, c, c0, H, Delta, m, n, n_prime = sp.symbols(
        "ell c c0 H Delta m n n_prime", positive=True
    )
    amplitudes = (
        sp.sqrt(c * Delta) / m,
        sp.sqrt(c * H) / n,
        sp.sqrt(c * (H - Delta)) / n_prime,
    )
    product = sp.prod(amplitudes)
    expected = c ** sp.Rational(3, 2) * sp.sqrt(Delta * H * (H - Delta)) / (
        m * n * n_prime
    )
    if sp.simplify(product - expected) != 0:
        raise AssertionError("triple-B Jacobian product mismatch")
    scaled = product.subs(
        {H: ell * H, Delta: ell * Delta, m: ell * m, n: ell * n, n_prime: ell * n_prime},
        simultaneous=True,
    )
    if sp.simplify(scaled / product - ell ** sp.Rational(-3, 2)) != 0:
        raise AssertionError("Jacobian scale law mismatch")

    points = (
        c * c0 * Delta / m,
        c * H / n,
        c * (H - Delta) / n_prime,
    )
    scaled_points = tuple(
        point.subs(
            {H: ell * H, Delta: ell * Delta, m: ell * m, n: ell * n, n_prime: ell * n_prime},
            simultaneous=True,
        )
        for point in points
    )
    if any(sp.simplify(left - right) != 0 for left, right in zip(points, scaled_points)):
        raise AssertionError("stationary evaluation point changed with scale")
    return {
        "amplitudes": (
            "sqrt(c*Delta)/m",
            "sqrt(c*H)/n",
            "sqrt(c*(H-Delta))/n'",
        ),
        "product": "c^(3/2)*sqrt(Delta*H*(H-Delta))/(m*n*n')",
        "scale": "J_ell=ell^(-3/2)*J0",
        "stationary_points": (
            "k*=c*c0*Delta/m",
            "r*=c*H/n",
            "r'*=c*(H-Delta)/n'",
        ),
        "points_invariant": True,
    }


def summability_record(length: int) -> dict[str, Any]:
    if length < 1:
        raise ValueError("positive length required")
    x = sp.symbols("x", positive=True)
    integral = sp.integrate(x ** sp.Rational(-3, 2), (x, 1, length))
    integral_bound = sp.simplify(1 + integral)
    if length > 1 and not bool(integral_bound < 3):
        raise AssertionError("integral summability bound failed")
    if length == 1 and integral_bound != 1:
        raise AssertionError("unit summability bound failed")
    endpoint = sp.Rational(1, length) ** sp.Rational(3, 2)
    variation = sum(
        sp.Rational(1, ell) ** sp.Rational(3, 2)
        - sp.Rational(1, ell + 1) ** sp.Rational(3, 2)
        for ell in range(1, length)
    )
    bv = sp.simplify(endpoint + variation)
    if bv != 1:
        raise AssertionError("ell^-3/2 BV norm does not telescope to one")
    return {
        "length": length,
        "integral_upper": integral_bound,
        "strict_uniform_upper": 3,
        "bv_norm": bv,
    }


def residual_envelope_bound(base_jacobian: Fraction, sup_weight: Fraction) -> Fraction:
    if base_jacobian < 0 or sup_weight < 0:
        raise ValueError("nonnegative envelope data required")
    return 3 * base_jacobian * sup_weight


def theorem_record() -> dict[str, object]:
    return {
        "stationary_points": (
            "k*=c*c0*Delta/m, r*=c*H/n, r'*=c*(H-Delta)/n' are scale invariant"
        ),
        "jacobian": (
            "J=c^(3/2)*sqrt(Delta*H*(H-Delta))/(m*n*n') and J_ell=ell^(-3/2)J0"
        ),
        "absolute_sum": "sum_{ell<=L}ell^(-3/2)<3",
        "bv": "L^(-3/2)+sum_{ell<L}(ell^(-3/2)-(ell+1)^(-3/2))=1",
        "weighted": "sum|omega_ell*J_ell|<=3*J0*sup|omega_ell|",
        "implication": (
            "a subpower residual envelope removes the raw Lambda multiplicity from the leading term"
        ),
        "boundary": (
            "arithmetic payload weights, non-invariant cutoff factors, and nonleading B-process remainders are untraced"
        ),
    }
