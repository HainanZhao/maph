"""Cycle 149 endpoint occupancy and Hilbert anti-alignment ledger."""

from __future__ import annotations

from fractions import Fraction
from math import sqrt


def occupancy_ratio(*, endpoint_modes: Fraction, all_modes: Fraction, q_over_n: Fraction) -> Fraction:
    if endpoint_modes < 0 or all_modes <= 0 or q_over_n <= 0:
        raise ValueError("invalid occupancy data")
    return endpoint_modes * q_over_n / all_modes


def relative_antialignment(*, full_budget_constant: float, comb_to_budget_ratio: float) -> float:
    if full_budget_constant < 0 or comb_to_budget_ratio <= 0:
        raise ValueError("invalid anti-alignment data")
    return sqrt(full_budget_constant / comb_to_budget_ratio)


def modulus_correlation_average(
    *, comb_norm_squared: float, endpoint_weight: float, relative_error: float
) -> float:
    """Magnitude forced for one normalized modulus correlation."""
    if comb_norm_squared < 0 or endpoint_weight <= 0 or not 0 <= relative_error < 1:
        raise ValueError("invalid modulus-witness data")
    return (1.0 - relative_error) * comb_norm_squared / endpoint_weight


def exponent_ledger(
    *, rho: Fraction, endpoint_mode_exponent: Fraction
) -> dict[str, Fraction]:
    occupancy_threshold = Fraction(3, 5) + rho - Fraction(1, 3)
    ratio = endpoint_mode_exponent - occupancy_threshold
    return {
        "endpoint_mode_exponent": endpoint_mode_exponent,
        "threshold_exponent": occupancy_threshold,
        "comb_to_global_diagonal": ratio,
        "relative_antialignment_exponent": -ratio / 2,
    }


def theorem_record() -> dict[str, object]:
    return {
        "occupancy_threshold": (
            "Cycle 148 gives ||C||_2^2>>KQ^2R_C/N while the global diagonal "
            "budget is B0=KDQ; their ratio is Lambda=(R_C/D)(Q/N), so the "
            "critical endpoint fraction is R_C/D=N/Q"
        ),
        "hilbert_inverse": (
            "if ||F||_2^2<=C_diag B0 and ||C||_2^2>=Lambda B0 for F=C+R, then "
            "||R+C||_2/||C||_2<=sqrt(C_diag/Lambda); for Lambda=X^omega the "
            "complement is X^(-omega/2)-close to the negative comb"
        ),
        "norm_balance": (
            "the same triangle inequality gives | ||R||_2/||C||_2-1 | "
            "<=sqrt(C_diag/Lambda)"
        ),
        "modulus_witness": (
            "for the ideal comb C_comb=Q sum_h A_h 1_(h|k), A_h>=0, near "
            "anti-alignment implies sum_h A_h Re<R,Q1_(h|k)> is at most "
            "-(1-epsilon)||C_comb||_2^2; hence one retained denominator h has "
            "negative correlation of magnitude at least "
            "(1-epsilon)||C_comb||_2^2/sum_h A_h"
        ),
        "coefficient_scope": (
            "the endpoint operator and complement are formed from one fixed "
            "polynomial before norms; the inverse retains the common coefficient "
            "vector, rational anchor, endpoint denominators, and frequency block"
        ),
        "structural_implication": (
            "a supercritical strict-endpoint population can coexist with a "
            "diagonal full moment only through near-perfect cross-endpoint or "
            "core--halo anti-alignment on a specific divisor comb"
        ),
        "boundary": (
            "anti-alignment is not excluded here; no full second moment, "
            "endpoint, complete moment, density, or intervals is proved"
        ),
    }
