"""Cycle 145 vector-valued moment and autocorrelation conventions."""

from __future__ import annotations

from collections.abc import Sequence
from math import exp, factorial, pi


def vector_moments(
    coefficient_rows: Sequence[Sequence[complex]],
    labels: Sequence[complex],
    order: int,
) -> tuple[tuple[complex, ...], ...]:
    """Return M_m(ell), with outer index m and inner index ell."""
    if order < 0:
        raise ValueError("moment order must be nonnegative")
    if any(len(row) != len(labels) for row in coefficient_rows):
        raise ValueError("every frequency row must match the edge labels")
    return tuple(
        tuple(sum((coefficient * label**m for coefficient, label in zip(row, labels)), 0j) for row in coefficient_rows)
        for m in range(order + 1)
    )


def taylor_remainder_factor(z: float, order: int) -> float:
    if z < 0 or order < 1:
        raise ValueError("need z>=0 and positive truncation order")
    return exp(z) * z**order / factorial(order)


def autocorrelation(sequence: Sequence[complex], difference: int) -> complex:
    """Zero-extended oriented autocorrelation sum_a c_(a+d) conjugate(c_a)."""
    return sum(
        (sequence[a + difference] * sequence[a].conjugate() for a in range(len(sequence)) if 0 <= a + difference < len(sequence)),
        0j,
    )


def selected_autocorrelation(
    sequence: Sequence[complex], difference: int, mask: Sequence[complex]
) -> complex:
    valid = tuple(a for a in range(len(sequence)) if 0 <= a + difference < len(sequence))
    if len(mask) != len(valid):
        raise ValueError("mask must have one entry per oriented edge")
    return sum(
        (weight * sequence[a + difference] * sequence[a].conjugate() for weight, a in zip(mask, valid)),
        0j,
    )


def theorem_record() -> dict[str, object]:
    return {
        "vector_moments": (
            "for C_e(ell), define M_m(ell)=sum_e C_e(ell)x_e^m; the frequency "
            "multiplier D^m acts as (D^m M_m)(ell)=ell^m M_m(ell)"
        ),
        "taylor_compiler": (
            "if |x_e|<=B, |ell|<=L, and z=2pi|kappa|LB, then for every R>=1, "
            "||F||_2 is at most sum_(m<R)(2pi|kappa|)^m/m! ||D^m M_m||_2 "
            "plus exp(z)z^R/R! times ||(sum_e|C_e(ell)|)_ell||_2"
        ),
        "zeroth_autocorrelation": (
            "for a complete difference-d class, M_0(d;ell)=sum_a "
            "c_(a+d)(ell)conjugate(c_a(ell)); its Fourier series in d is "
            "|sum_a c_a(ell)e(-a theta)|^2 and is therefore nonnegative"
        ),
        "selection_mask": (
            "the arithmetic inverse replaces the complete autocorrelation by a "
            "selected one sum_a chi_(a,d,ell)c_(a+d)(ell)conjugate(c_a(ell)); "
            "the positive-definite identity survives only if the mask has a "
            "separately proved Gram or convolution factorization"
        ),
        "fixed_phase_adverse_chart": (
            "on any edge block where c_a has one common phase and nonnegative "
            "magnitude, every unweighted selected zeroth product is nonnegative; "
            "smooth local amplitude alone cannot supply cancellation there"
        ),
        "next_gate": (
            "prove cancellation or a Gram factorization for the actual arithmetic "
            "selection mask in the vector-valued zeroth autocorrelation; otherwise "
            "retain the resulting fixed-phase selected block as inverse data"
        ),
        "boundary": (
            "the compiler is exact but supplies no bound for the selected "
            "autocorrelation, paired norm, endpoint, complete moment, density, or intervals"
        ),
    }
