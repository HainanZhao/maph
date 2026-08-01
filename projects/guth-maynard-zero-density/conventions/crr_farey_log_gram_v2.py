"""Exact bookkeeping for the averaged-jitter actual-Farey extension.

This v2 module preserves the v1 supremum-over-jitter reduction.  It records
the separate averaged-jitter statistic, its RationalMass lower bound, and the
scale supplied by the published raw ``R`` L2 lemma.  It does not prove either
FARI or its averaged variant.
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
    """Return the frozen integral CRR scales for an admissible integer v."""
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
    require(result["R"] == result["Q"] ** 2, "R=Q^2 cardinality mismatch")
    return result


def averaged_farey_geometry(v: int) -> dict[str, Fraction | int | str]:
    """Check the disjoint expanded cells and theta neighborhoods exactly.

    The elementary analytic inequalities used in the accompanying proof are
    ``exp(x)>=1+x`` and, for ``0<=x<=1/2``, ``exp(x)-1<=2x``.
    """
    data = scales(v)
    H = data["H"]
    Q = data["Q"]
    gap = Fraction(1, 4 * Q * Q)
    expanded_radius = (1 + RATIONAL_CELL_RADIUS) / H
    expanded_diameter = 2 * expanded_radius
    theta_neighborhood_radius = Fraction(8, H)
    theta_neighborhood_diameter = 2 * theta_neighborhood_radius
    upper_cover_margin = Fraction(9, 4) - (1 + RATIONAL_CELL_RADIUS)
    lower_cover_margin = Fraction(3, H + JITTER_LOG_RADIUS) - Fraction(101, 75 * H)
    require(expanded_diameter < gap, "expanded actual-Farey cells must be disjoint")
    require(theta_neighborhood_diameter < gap, "theta parameter neighborhoods must be disjoint")
    require(upper_cover_margin > 0, "theta=3 upper endpoint does not cover expanded cells")
    require(lower_cover_margin > 0, "theta=3 lower endpoint does not cover expanded cells")
    require(Fraction(JITTER_LOG_RADIUS, H) <= Fraction(1, 2), "small-exponential bound unavailable")
    require(Fraction(15, 2 * H) < theta_neighborhood_radius, "upper theta neighborhood is too narrow")
    require(Fraction(15, 4 * H) < theta_neighborhood_radius, "lower theta neighborhood is too narrow")
    require(Fraction(5, 4) + expanded_radius < Fraction(4, 3), "expanded cells exceed u=4/3")
    require(Fraction(3, 4) - theta_neighborhood_radius > Fraction(1, 2), "theta neighborhoods leave RL2 range")
    require(Fraction(5, 4) + theta_neighborhood_radius < Fraction(3, 2), "theta neighborhoods leave RL2 range")
    return {
        "H": H,
        "Q": Q,
        "reduced_fraction_gap_lower": gap,
        "expanded_cell_radius": expanded_radius,
        "expanded_cell_diameter": expanded_diameter,
        "theta_neighborhood_radius": theta_neighborhood_radius,
        "theta_neighborhood_diameter": theta_neighborhood_diameter,
        "theta_cover": "J_(r,s)^+ subset {(r/s)*exp(theta/H): |theta|<=3}",
        "upper_theta_cover_margin": upper_cover_margin,
        "lower_theta_cover_margin": lower_cover_margin,
        "raw_cell_u_upper": Fraction(4, 3),
        "rl2_containing_interval": "[1/2,3/2]",
    }


def ray_rows(v: int) -> dict[str, Fraction | int | str]:
    """Return exact lower and upper plateau-ray bounds for every Farey pair."""
    data = scales(v)
    L = data["L"]
    Q = data["Q"]
    lower_width = Fraction(3 * L, 25 * Q)
    lower_count = Fraction(L, 20 * Q)
    upper_count = Fraction(2 * L, Q)
    require(lower_width - 1 >= lower_count, "plateau ray must contain L/(20Q) integers")
    require(Fraction(9 * L, 5 * Q) <= upper_count, "ray upper-count simplification failed")
    return {
        "L": L,
        "Q": Q,
        "plateau": "[6L/5,9L/5]",
        "integer_k_count_lower": lower_count,
        "integer_k_count_upper": upper_count,
        "lower_count_derivation": "width>=3L/(25Q), then subtract one endpoint",
        "upper_count_derivation": "#K<=9L/(5Q)<=2L/Q",
    }


def averaged_lower_constants() -> dict[str, Fraction | str]:
    """Record the exact incidence, Jacobian, and ray constants in v2."""
    smoothing_incidence_upper = 2 * RATIONAL_CELL_RADIUS
    raw_cell_sum_factor = 1 / smoothing_incidence_upper
    theta_jacobian_factor = Fraction(3, 4)
    ray_factor = Fraction(1, 20)
    bundle_prefactor = raw_cell_sum_factor * theta_jacobian_factor * ray_factor
    require(smoothing_incidence_upper == Fraction(1, 50), "smoothing incidence factor mismatch")
    require(raw_cell_sum_factor == 50, "raw actual-Farey L2 factor mismatch")
    require(bundle_prefactor == Fraction(15, 8), "averaged bundle prefactor mismatch")
    return {
        "smoothing_incidence_upper": smoothing_incidence_upper,
        "raw_cell_sum_factor": raw_cell_sum_factor,
        "theta_jacobian_factor": theta_jacobian_factor,
        "ray_factor": ray_factor,
        "averaged_bundle_prefactor": bundle_prefactor,
        "theta_change_of_variables": "du=(u/H)dtheta and u<=4/3 on J_(r,s)^+",
    }


def exponent_rows() -> dict[str, tuple[Fraction, Fraction]]:
    """Pairs encode constant plus delta(v) coefficient for each scale row."""
    rows = {
        "rationalmass_integral_over_cells": (Fraction(8), Fraction(-3)),
        "raw_actual_farey_l2_cell_sum_lower": (Fraction(8), Fraction(-3)),
        "theta_parameter_mass_lower": (Fraction(20), Fraction(-3)),
        "averaged_actual_farey_bundle_lower": (Fraction(26), Fraction(-3)),
        "raw_rl2_global_upper_under_base": (Fraction(26), Fraction(1)),
    }
    require(
        rows["theta_parameter_mass_lower"]
        == (rows["raw_actual_farey_l2_cell_sum_lower"][0] + 12, rows["raw_actual_farey_l2_cell_sum_lower"][1]),
        "theta mass exponent mismatch",
    )
    require(
        rows["averaged_actual_farey_bundle_lower"]
        == (rows["theta_parameter_mass_lower"][0] + 6, rows["theta_parameter_mass_lower"][1]),
        "averaged actual-Farey bundle exponent mismatch",
    )
    require(
        rows["raw_rl2_global_upper_under_base"] == (Fraction(12 + 6 + 8), Fraction(1)),
        "raw RL2 global upper exponent mismatch",
    )
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run every finite exact check used by the v2 replay builder."""
    data = scales(v)
    geometry = averaged_farey_geometry(v)
    rays = ray_rows(v)
    constants = averaged_lower_constants()
    exponents = exponent_rows()
    require(data["Q"] >= 4096, "minimum v must reach the frozen Farey threshold")
    require(rays["integer_k_count_lower"] == Fraction(v**6, 20), "ray lower scale mismatch")
    require(rays["integer_k_count_upper"] == 2 * v**6, "ray upper scale mismatch")
    require(constants["averaged_bundle_prefactor"] == Fraction(15, 8), "bundle constant mismatch")
    return {
        "scales": data,
        "geometry": geometry,
        "rays": rays,
        "constants": constants,
        "exponents": exponents,
    }
