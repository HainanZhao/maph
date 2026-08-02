"""Cycle 109 uniform complete triple-B kernel contract."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import sympy as sp


def one_dimensional_norm_constant(
    *, curvature_lower: Fraction, sup_norm: Fraction, derivative_l1: Fraction
) -> Fraction:
    """Safe constant from the proved split-and-integration-by-parts lemma."""
    if curvature_lower <= 0 or min(sup_norm, derivative_l1) < 0:
        raise ValueError("positive curvature and nonnegative amplitude norms required")
    # The theorem is (4||w||_infinity+||w'||_1)/sqrt(lambda).
    # Return the squared numerator/denominator contract to stay exact.
    return Fraction((4 * sup_norm + derivative_l1) ** 2, curvature_lower)


def tensor_bound_squared(
    *, curvature_lowers: tuple[Fraction, Fraction, Fraction], symbol_norm: Fraction
) -> Fraction:
    """Square of a safe C_W*(lambda1 lambda2 lambda3)^(-1/2) bound."""
    if min(curvature_lowers) <= 0 or symbol_norm < 0:
        raise ValueError("positive curvatures and nonnegative symbol norm required")
    # 4 per integration and a deliberately safe factor 2 for fixed chart lengths.
    constant = 8**3 * symbol_norm
    product = curvature_lowers[0] * curvature_lowers[1] * curvature_lowers[2]
    return constant * constant / product


def symbolic_log_phase_record() -> dict[str, Any]:
    ell, c, H, Delta, m, n, n_prime, k, r, r_prime = sp.symbols(
        "ell c H Delta m n n_prime k r r_prime", positive=True
    )
    phase_k = ell * (c * Delta * sp.log(k) - m * k)
    phase_r = ell * (-c * H * sp.log(r) + n * r)
    phase_r_prime = ell * (c * (H - Delta) * sp.log(r_prime) - n_prime * r_prime)
    second = (
        sp.simplify(sp.diff(phase_k, k, 2)),
        sp.simplify(sp.diff(phase_r, r, 2)),
        sp.simplify(sp.diff(phase_r_prime, r_prime, 2)),
    )
    expected = (
        -ell * c * Delta / k**2,
        ell * c * H / r**2,
        -ell * c * (H - Delta) / r_prime**2,
    )
    if any(sp.simplify(left - right) != 0 for left, right in zip(second, expected)):
        raise AssertionError("logarithmic phase Hessian mismatch")
    stationary = (
        sp.solve(sp.diff(phase_k, k), k)[0],
        sp.solve(sp.diff(phase_r, r), r)[0],
        sp.solve(sp.diff(phase_r_prime, r_prime), r_prime)[0],
    )
    if any(point.has(ell) for point in stationary):
        raise AssertionError("stationary point depends on ell")
    return {
        "second_derivatives": (
            "-ell*c*Delta/k^2",
            "ell*c*H/r^2",
            "-ell*c*(H-Delta)/r'^2",
        ),
        "fixed_signs": ("negative", "positive", "negative"),
        "stationary_points": (
            "c*Delta/m",
            "c*H/n",
            "c*(H-Delta)/n'",
        ),
        "ell_independent": True,
    }


def summable_kernel_bound(base_constant: Fraction) -> Fraction:
    if base_constant < 0:
        raise ValueError("nonnegative base constant required")
    return 3 * base_constant


def theorem_record() -> dict[str, object]:
    return {
        "one_dimensional_lemma": (
            "if phi'' has fixed sign and abs(phi'')>=lambda, then "
            "|int w e(phi)|<=(4||w||_infinity+||w'||_1)lambda^(-1/2)"
        ),
        "tensor_lemma": (
            "for a separable three-variable phase and joint smooth W, iteration gives "
            "|I|<=C_box N_111(W)(lambda1 lambda2 lambda3)^(-1/2)"
        ),
        "actual_curvature": (
            "the k,r,r' second derivatives are -ell*c*Delta/k^2, "
            "+ell*c*H/r^2, -ell*c*(H-Delta)/r'^2"
        ),
        "complete_kernel": "|I_ell|<=C_W ell^(-3/2)",
        "scale_sum": "sum_{ell<=L}|I_ell|<3C_W uniformly in L",
        "smooth_model": (
            "Cycle 81/87/90 weights are fixed smooth compact symbols; no Mobius weight is inherited"
        ),
        "boundary": (
            "distinct core aggregation, nonsmooth coefficient variants, weak/simple-root rows, moments, density, and intervals remain open"
        ),
    }
