"""Pinned exact bookkeeping for the CRR actual-Farey/log-Gram reduction.

This module records only finite algebra, geometry, and exponent arithmetic.
It does not assert the proposed Farey restricted inverse inequality (FARI),
does not evaluate a CRR witness, and does not run a numerical search.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
RATIONAL_CELL_RADIUS = Fraction(1, 100)
JITTER_LOG_RADIUS = 3

SCALE_EXPONENTS = {
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "affine_scale_M": 2,
    "rational_height_Q": 4,
    "cardinality_R": 8,
    "large_value_V": 7,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return the frozen integral scales for an admissible finite v."""
    require(isinstance(v, int) and v >= MIN_V, f"v must be an integer at least {MIN_V}")
    result = {
        "v": v,
        "H": v**SCALE_EXPONENTS["local_height_H"],
        "L": v**SCALE_EXPONENTS["polynomial_length_L"],
        "M": v**SCALE_EXPONENTS["affine_scale_M"],
        "Q": v**SCALE_EXPONENTS["rational_height_Q"],
        "R": v**SCALE_EXPONENTS["cardinality_R"],
        "V": v**SCALE_EXPONENTS["large_value_V"],
    }
    require(result["Q"] == result["M"] ** 2, "Q=M^2 critical rational scale mismatch")
    require(result["H"] == result["Q"] ** 3, "H=Q^3 critical cell scale mismatch")
    require(result["L"] == result["Q"] * v**6, "L/Q=v^6 multiplicative-ray mismatch")
    require(result["R"] == result["Q"] ** 2, "R=Q^2 critical cardinality mismatch")
    require(result["V"] == v**6 * v, "V=v^6*v large-value scale mismatch")
    return result


def actual_farey_cell_rows(v: int) -> dict[str, Fraction | int]:
    """Exact scale rows for the reduced Q-by-Q Farey cells."""
    data = scales(v)
    Q = data["Q"]
    H = data["H"]
    gap = Fraction(1, 4 * Q * Q)
    diameter = Fraction(2) * RATIONAL_CELL_RADIUS / H
    central_interval_length = Q // 4
    require(central_interval_length >= Q // 5, "central rational interval is too short")
    require(diameter < gap, "actual reduced-Farey cells must be disjoint")
    return {
        "Q": Q,
        "H": H,
        "reduced_fraction_gap_lower": gap,
        "cell_diameter": diameter,
        "central_integer_interval_length": central_interval_length,
        "central_farey_count_lower": Fraction(Q * Q, 200),
        "all_cells_measure_scale": Fraction(Q * Q, H),
    }


def farey_union_bound_certificate() -> dict[str, Fraction | int | str]:
    """Check the elementary constants in the central-coprime-pair count.

    The proof uses ``sum_{n>=2} n^-2 <= 3/4`` and ``log(2)<7/10``.
    For Q>=4096 the residual terms in the union bound occupy at most one
    eighth of the central square, leaving at least Q^2/200 reduced pairs.
    """
    Q0 = 4096
    log_2q0_upper = Fraction(91, 10)  # 13 log(2) < 13*(7/10)
    residual_per_Q_upper = Fraction(1, 2) * (1 + log_2q0_upper) + 2
    margin = Fraction(Q0, 200) - residual_per_Q_upper
    require(margin > 0, "central Farey union-bound threshold failed at Q=4096")
    return {
        "minimum_Q": Q0,
        "prime_square_sum_upper": Fraction(3, 4),
        "harmonic_bound": "sum_(p<=2Q) 1/p <= 1+log(2Q)",
        "log_two_upper": Fraction(7, 10),
        "residual_per_Q_upper_at_Q0": residual_per_Q_upper,
        "residual_margin_at_Q0": margin,
        "conclusion": "#F_Q >= Q^2/200 for Q>=4096",
    }


def ray_rows(v: int) -> dict[str, Fraction | int]:
    """Exact plateau-ray lower bounds valid for every r/s in the CRR net."""
    data = scales(v)
    L = data["L"]
    Q = data["Q"]
    width_lower = Fraction(3 * L, 25 * Q)
    count_lower = Fraction(L, 20 * Q)
    require(width_lower - 1 >= count_lower, "plateau ray must contain L/(20Q) integers")
    return {
        "L": L,
        "Q": Q,
        "plateau": "[6L/5,9L/5]",
        "continuous_k_interval_width_lower": width_lower,
        "integer_k_count_lower": count_lower,
        "ray_count_exponent_in_v": 6,
    }


def jitter_rows() -> dict[str, Fraction | int | str]:
    """Constants for passing from a CRR cell to a raw jittered Farey node."""
    relative_shift_upper = Fraction(101, 75)
    logarithmic_shift_upper = 2 * relative_shift_upper
    require(logarithmic_shift_upper < JITTER_LOG_RADIUS, "jitter log radius must contain the smoothing displacement")
    return {
        "cell_radius_times_H": RATIONAL_CELL_RADIUS,
        "raw_window_radius_times_H": 1,
        "relative_shift_times_H_upper": relative_shift_upper,
        "log_shift_times_H_upper": logarithmic_shift_upper,
        "jitter_log_radius": JITTER_LOG_RADIUS,
        "raw_square_loss": Fraction(1, 2),
        "reason": "0<=psi1,psi2<=1 and supp(psi1) subset [-1,1]",
    }


def exponent_rows() -> dict[str, tuple[Fraction, Fraction]]:
    """Each pair denotes constant + delta_coefficient*delta(v)."""
    rows = {
        "activated_actual_farey_cells": (Fraction(8), Fraction(-1)),
        "jittered_raw_amplitude": (Fraction(6), Fraction(-1)),
        "jittered_raw_square": (Fraction(12), Fraction(-2)),
        "plateau_ray_multiplicity": (Fraction(6), Fraction()),
        "farey_log_gram_bundle_lower": (Fraction(26), Fraction(-3)),
        "base_coefficient_spectral_lambda_lower": (Fraction(12), Fraction(-3)),
    }
    require(
        rows["farey_log_gram_bundle_lower"]
        == (
            rows["activated_actual_farey_cells"][0]
            + rows["jittered_raw_square"][0]
            + rows["plateau_ray_multiplicity"][0],
            rows["activated_actual_farey_cells"][1]
            + rows["jittered_raw_square"][1]
            + rows["plateau_ray_multiplicity"][1],
        ),
        "Farey-log bundle exponent mismatch",
    )
    require(
        rows["base_coefficient_spectral_lambda_lower"]
        == (Fraction(8 + 14 - 10), Fraction(-1 - 2)),
        "Base coefficient spectral exponent mismatch",
    )
    return rows


def affine_factorization_rows(v: int) -> dict[str, int | str]:
    """Bookkeeping for the source rational-map factorization s=d*e."""
    data = scales(v)
    require(data["Q"] == data["M"] ** 2, "affine factorization needs Q=M^2")
    return {
        "M": data["M"],
        "Q": data["Q"],
        "identity": "(d*(r/(d*e))+m2)/m3=(r+e*m2)/(e*m3)",
        "scale": "if d,e,m2,m3 asymp M and r asymp Q, numerator and denominator are asymp Q",
        "scope": "dyadic-scale compatibility only; no exact-shell closure or coprimality preservation is asserted",
    }


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run all finite exact checks used by the replay builder."""
    data = scales(v)
    cells = actual_farey_cell_rows(v)
    rays = ray_rows(v)
    certificate = farey_union_bound_certificate()
    jitter = jitter_rows()
    exponents = exponent_rows()
    affine = affine_factorization_rows(v)
    require(data["Q"] >= certificate["minimum_Q"], "minimum v must reach Farey count threshold")
    require(cells["all_cells_measure_scale"] == Fraction(1, data["Q"]), "actual Farey cover must have Q^-1 measure scale")
    require(rays["integer_k_count_lower"] == Fraction(v**6, 20), "plateau ray scale mismatch")
    return {
        "scales": data,
        "cells": cells,
        "rays": rays,
        "certificate": certificate,
        "jitter": jitter,
        "exponents": exponents,
        "affine": affine,
    }
