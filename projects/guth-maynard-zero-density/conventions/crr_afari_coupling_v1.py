"""Exact bookkeeping for the CRR coefficient--Farey coupling reduction.

This module records only the actual-Farey geometry, the Cauchy/exponent
bookkeeping, and the coefficient-phase consequence of the frozen Base(v)
predicate.  It does not prove AFARI, CFARI, CRR-U, or the realizability of
the scalar extremizer used to calibrate the moment argument.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
THETA_RADIUS = 3

SCALE_EXPONENTS = {
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "rational_height_Q": 4,
    "cardinality_R": 8,
    "large_value_V": 7,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return the frozen integral CRR scales."""
    require(isinstance(v, int) and v >= MIN_V, f"v must be an integer at least {MIN_V}")
    data = {
        "v": v,
        "H": v**SCALE_EXPONENTS["local_height_H"],
        "L": v**SCALE_EXPONENTS["polynomial_length_L"],
        "Q": v**SCALE_EXPONENTS["rational_height_Q"],
        "R": v**SCALE_EXPONENTS["cardinality_R"],
        "V": v**SCALE_EXPONENTS["large_value_V"],
    }
    require(data["H"] == data["Q"] ** 3, "the actual-Farey reduction needs H=Q^3")
    require(data["L"] == data["Q"] * v**6, "the ray comparison needs L/Q=v^6")
    require(data["R"] == data["Q"] ** 2, "the critical cardinality needs R=Q^2")
    return data


def farey_window_rows(v: int) -> dict[str, Fraction | int | str]:
    """Return conservative exact measure bounds for the true theta windows.

    The lower bound combines the v1 count ``#F_Q >= Q^2/200`` with
    ``a(exp(3/H)-exp(-3/H)) >= 4/H``.  The upper bound uses the v2
    containment in ``[a-8/H,a+8/H]`` and the elementary ``#F_Q<=Q^2``.
    """
    data = scales(v)
    H = data["H"]
    Q = data["Q"]
    lower = Fraction(Q * Q, 50 * H)
    upper = Fraction(16 * Q * Q, H)
    require(lower > 0, "Farey theta-window lower measure must be positive")
    require(lower <= upper, "Farey theta-window bounds are inconsistent")
    require(upper == Fraction(16, Q), "critical Farey-window upper scale mismatch")
    require(lower == Fraction(1, 50 * Q), "critical Farey-window lower scale mismatch")
    return {
        "H": H,
        "Q": Q,
        "theta_radius": THETA_RADIUS,
        "farey_pair_count_lower": Fraction(Q * Q, 200),
        "farey_pair_count_upper": Q * Q,
        "one_window_length_lower": Fraction(4, H),
        "one_window_length_upper": Fraction(16, H),
        "union_measure_lower": lower,
        "union_measure_upper": upper,
        "actual_label_rule": "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4",
        "disjointness_source": "v2 theta neighborhoods lie in disjoint [r/s-8/H,r/s+8/H]",
    }


def ray_comparison_rows(v: int) -> dict[str, Fraction | int | str]:
    """Return the PSD comparison factors from the labeled ray multiplicities."""
    data = scales(v)
    L = data["L"]
    Q = data["Q"]
    lower = Fraction(L, 20 * Q)
    upper = Fraction(2 * L, Q)
    require(lower == Fraction(v**6, 20), "ray lower scale mismatch")
    require(upper == 2 * v**6, "ray upper scale mismatch")
    return {
        "L": L,
        "Q": Q,
        "ray_weight_lower": lower,
        "ray_weight_upper": upper,
        "loewner_comparison": "(L/(20Q))*K_F <= K_F^ray <= (2L/Q)*K_F",
    }


def affine_text(row: tuple[Fraction, Fraction]) -> str:
    """Render an affine-in-delta exponent row deterministically."""
    constant, slack = row

    def render(value: Fraction) -> str:
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"

    if slack == 0:
        return render(constant)
    sign = "+" if slack > 0 else "-"
    return f"{render(constant)}{sign}{render(abs(slack))}*delta"


def exponent_rows() -> dict[str, tuple[Fraction, Fraction]]:
    """Return all exact frozen exponent arithmetic used by the reduction.

    Rows marked ``source_o`` in the document still carry the published
    subpower loss.  The affine row records only the explicit Base(v) slack.
    """
    rows = {
        "base_energy_upper": (Fraction(20), Fraction(1)),
        "energy_cauchy_theta_mass_upper_base_slack_only": (Fraction(20), Fraction(1, 2)),
        "energy_cauchy_ray_bundle_upper_base_slack_only": (Fraction(26), Fraction(1, 2)),
        "rationalmass_theta_mass_lower": (Fraction(20), Fraction(-3)),
        "rationalmass_local_l2_lower": (Fraction(8), Fraction(-3)),
        "rationalmass_local_l4_lower": (Fraction(20), Fraction(-6)),
        "base_phase_rayleigh_lower": (Fraction(20), Fraction(-4)),
        "base_rationalmass_phase_farey_product_lower": (Fraction(40), Fraction(-7)),
        "scalar_envelope_local_l4": (Fraction(20), Fraction(0)),
        "scalar_envelope_theta_mass": (Fraction(20), Fraction(0)),
        "scalar_envelope_ray_bundle": (Fraction(26), Fraction(0)),
    }
    require(
        rows["energy_cauchy_theta_mass_upper_base_slack_only"]
        == (Fraction(4 + 6 + 10), Fraction(1, 2)),
        "energy-Cauchy theta-mass scale mismatch",
    )
    require(
        rows["energy_cauchy_ray_bundle_upper_base_slack_only"]
        == (
            rows["energy_cauchy_theta_mass_upper_base_slack_only"][0] + 6,
            rows["energy_cauchy_theta_mass_upper_base_slack_only"][1],
        ),
        "energy-Cauchy ray-bundle scale mismatch",
    )
    require(
        rows["rationalmass_local_l4_lower"]
        == (
            2 * rows["rationalmass_local_l2_lower"][0] + 4,
            2 * rows["rationalmass_local_l2_lower"][1],
        ),
        "RationalMass local fourth-moment scale mismatch",
    )
    require(
        rows["base_rationalmass_phase_farey_product_lower"]
        == (
            rows["base_phase_rayleigh_lower"][0] + rows["rationalmass_theta_mass_lower"][0],
            rows["base_phase_rayleigh_lower"][1] + rows["rationalmass_theta_mass_lower"][1],
        ),
        "coefficient-phase/Farey product scale mismatch",
    )
    return rows


def rationalmass_localization_constants() -> dict[str, Fraction | str]:
    """Return exact constants converting the v2 bundle lower bound to L4 mass."""
    theta_mass_lower = Fraction(15, 16)
    local_l2_lower = theta_mass_lower / 2
    local_l4_lower = local_l2_lower * local_l2_lower / 16
    require(theta_mass_lower == Fraction(15, 16), "theta-mass lower constant mismatch")
    require(local_l2_lower == Fraction(15, 32), "local L2 lower constant mismatch")
    require(local_l4_lower == Fraction(225, 16384), "local L4 lower constant mismatch")
    return {
        "theta_mass_lower_from_averaged_bundle": theta_mass_lower,
        "local_l2_lower_from_theta_mass": local_l2_lower,
        "local_l4_lower_from_cauchy": local_l4_lower,
        "derivation": "A>=(15/8)v^(26-3delta), A<=(2L/Q)*M, M<=2H*I2, I4>=I2^2/|U|, |U|<=16v^-4",
    }


def scalar_envelope_rows(v: int) -> dict[str, Fraction | int | str]:
    """Calibrate the scalar Cauchy envelope on the actual Farey union.

    ``f_star`` is a nonnegative scalar function, not an asserted ``|R_W|^2``.
    It has integral-square exactly ``v^20`` and saturates the Cauchy scale on
    the same actual labeled union of theta windows.
    """
    data = scales(v)
    measure = farey_window_rows(v)
    # Fractions do not have square roots.  Store squared endpoint constants,
    # which is sufficient for exact exponent and constant verification.
    lower_integral_squared = Fraction(v**20, 50 * data["Q"])
    upper_integral_squared = Fraction(16 * v**20, data["Q"])
    require(lower_integral_squared == Fraction(v**16, 50), "scalar lower integral square mismatch")
    require(upper_integral_squared == 16 * v**16, "scalar upper integral square mismatch")
    return {
        "H": data["H"],
        "Q": data["Q"],
        "f_star": "v^10*|U_v|^(-1/2)*1_(U_v)",
        "integral_f_star_squared": v**20,
        "integral_f_star_squared_scope": "exact: integral_U f_star^2 = v^20",
        "integral_f_star_squared_lower_bound": lower_integral_squared,
        "integral_f_star_squared_upper_bound": upper_integral_squared,
        "measure_lower": measure["union_measure_lower"],
        "measure_upper": measure["union_measure_upper"],
        "scope": "scalar Cauchy-envelope calibration only; f_star is not claimed to be |R_W|^2",
    }


def coefficient_phase_rows(v: int) -> dict[str, Fraction | int | str]:
    """Return the exact Base(v) phase-Rayleigh lower bound."""
    data = scales(v)
    numerator_exponent = 2 * (8 + 7) - 10
    require(numerator_exponent == 20, "Base phase-Rayleigh central exponent mismatch")
    return {
        "L": data["L"],
        "base_cardinality_lower": "v^(8-delta(v))",
        "base_pointwise_lower": "v^(7-delta(v))",
        "phase_definition": "a_t=D_v(t)/|D_v(t)|",
        "identity": "sum_t conjugate(a_t)D_v(t)=sum_t |D_v(t)|",
        "rayleigh_lower": "a^*(M_W M_W^*)a>=v^(20-4*delta(v))",
        "derivation": "|<a,M_W b>|^2<=||M_W^*a||_2^2||b||_2^2 and ||b||_2^2<=L",
    }


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run every finite exact check used by the sealed replay."""
    data = scales(v)
    windows = farey_window_rows(v)
    rays = ray_comparison_rows(v)
    exponents = exponent_rows()
    localization = rationalmass_localization_constants()
    scalar = scalar_envelope_rows(v)
    phase = coefficient_phase_rows(v)
    require(data["Q"] >= 4096, "minimum v must reach the frozen Farey threshold")
    require(windows["union_measure_lower"] < windows["union_measure_upper"], "Farey union scale degeneracy")
    require(rays["ray_weight_lower"] < rays["ray_weight_upper"], "ray comparison degeneracy")
    require(localization["local_l4_lower_from_cauchy"] > 0, "local L4 lower constant must be positive")
    require(phase["rayleigh_lower"] == "a^*(M_W M_W^*)a>=v^(20-4*delta(v))", "phase convention mismatch")
    return {
        "scales": data,
        "farey_windows": windows,
        "rays": rays,
        "exponents": exponents,
        "rationalmass_localization": localization,
        "scalar_envelope": scalar,
        "coefficient_phase": phase,
    }
