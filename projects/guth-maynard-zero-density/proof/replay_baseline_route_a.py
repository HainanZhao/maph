#!/usr/bin/env python3
"""Exact Route A replay for the frozen Guth--Maynard baseline.

This is a proof-grade *arithmetic implication* replay, not a reproof of the
analytic estimates it uses.  Its hypotheses and source locations are frozen in
``docs/cycle-1-route-a.md``.  All mathematical quantities below are instances
of ``fractions.Fraction``; the script performs no floating-point arithmetic.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any


ROUTE = "A"
ARTIFACT_VERSION = 3
SIGMA_STAR = Fraction(7, 10)
CRITICAL_N_IN_T = Fraction(4, 5)
CRITICAL_V_IN_N = Fraction(3, 4)
PREVIOUS_MATHEMATICAL_CERTIFICATE_SHA256 = (
    "ef6b7ceaec9ca397b260de3554f444266ec80c971f2603e3e25320edd45812e9"
)
BOTTLE_SIGMA = Fraction(7, 10)
BOTTLE_N_IN_T = Fraction(5, 13)
BOTTLE_L_IN_T = Fraction(10, 13)
BOTTLE_U_IN_T = Fraction(12, 13)
BOTTLE_W_IN_U = Fraction(2, 3)
FROZEN_SOURCE = {
    "arxiv_identifier": "2405.20552v2",
    "source_tarball_sha256": "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc",
    "tex_sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    "pdf_sha256": "915392cf7d0ecd108479814a9a1481e23423ef63415776471cec3975ae482cae",
}


def fraction_text(value: Fraction) -> str:
    """Render a Fraction canonically, retaining an explicit denominator."""
    return f"{value.numerator}/{value.denominator}"


def ingham_coefficient(sigma: Fraction) -> Fraction:
    """Coefficient A_I(sigma) in N <= T^(A_I(sigma)(1-sigma)+o(1))."""
    return Fraction(3, 1) / (Fraction(2, 1) - sigma)


def guth_maynard_coefficient(sigma: Fraction) -> Fraction:
    """Coefficient A_GM(sigma) from Guth--Maynard Theorem 1.2."""
    return Fraction(15, 1) / (Fraction(3, 1) + Fraction(5, 1) * sigma)


def coefficient_difference(sigma: Fraction) -> Fraction:
    """Return A_I(sigma) - A_GM(sigma), exactly."""
    return ingham_coefficient(sigma) - guth_maynard_coefficient(sigma)


def monomial_t_exponent(
    t_power: Fraction, n_power: Fraction, v_power: Fraction
) -> Fraction:
    """Return the exponent of T after N=T^(4/5), V=N^(3/4)."""
    v_in_t = CRITICAL_N_IN_T * CRITICAL_V_IN_N
    return t_power + n_power * CRITICAL_N_IN_T + v_power * v_in_t


def critical_large_values_cell() -> dict[str, Any]:
    """Evaluate Theorem 1.1 and classical (1.1) at the frozen cell exactly."""
    zero = Fraction(0, 1)
    one = Fraction(1, 1)
    n_squared_v_minus_two = monomial_t_exponent(
        zero, Fraction(2, 1), Fraction(-2, 1)
    )
    guth_maynard_n_18_over_5 = monomial_t_exponent(
        zero, Fraction(18, 5), Fraction(-4, 1)
    )
    guth_maynard_t_n_12_over_5 = monomial_t_exponent(
        one, Fraction(12, 5), Fraction(-4, 1)
    )
    classical_t_n_v_minus_two = monomial_t_exponent(
        one, one, Fraction(-2, 1)
    )
    classical_t_n_four_v_minus_six = monomial_t_exponent(
        one, Fraction(4, 1), Fraction(-6, 1)
    )

    guth_maynard_maximum = max(
        n_squared_v_minus_two,
        guth_maynard_n_18_over_5,
        guth_maynard_t_n_12_over_5,
    )
    classical_minimum = min(
        classical_t_n_v_minus_two,
        classical_t_n_four_v_minus_six,
    )
    classical_maximum = max(n_squared_v_minus_two, classical_minimum)
    gain = classical_maximum - guth_maynard_maximum

    assert CRITICAL_N_IN_T * CRITICAL_V_IN_N == Fraction(3, 5)
    assert n_squared_v_minus_two == Fraction(2, 5)
    assert guth_maynard_n_18_over_5 == Fraction(12, 25)
    assert guth_maynard_t_n_12_over_5 == Fraction(13, 25)
    assert guth_maynard_maximum == Fraction(13, 25)
    assert classical_t_n_v_minus_two == Fraction(3, 5)
    assert classical_t_n_four_v_minus_six == Fraction(3, 5)
    assert classical_minimum == classical_maximum == Fraction(3, 5)
    assert gain == Fraction(2, 25)

    return {
        "cell": {
            "N_in_terms_of_T": "N = T^(4/5)",
            "V_in_terms_of_N": "V = N^(3/4)",
            "V_in_terms_of_T": "V = T^(3/5)",
        },
        "guth_maynard_theorem_1_1": {
            "terms": {
                "N^2*V^-2": fraction_text(n_squared_v_minus_two),
                "N^(18/5)*V^-4": fraction_text(guth_maynard_n_18_over_5),
                "T*N^(12/5)*V^-4": fraction_text(guth_maynard_t_n_12_over_5),
            },
            "maximum_T_exponent": fraction_text(guth_maynard_maximum),
        },
        "classical_equation_1_1": {
            "terms": {
                "N^2*V^-2": fraction_text(n_squared_v_minus_two),
                "T*N*V^-2": fraction_text(classical_t_n_v_minus_two),
                "T*N^4*V^-6": fraction_text(classical_t_n_four_v_minus_six),
            },
            "minimum_inside_T_times_min": fraction_text(classical_minimum),
            "maximum_T_exponent": fraction_text(classical_maximum),
        },
        "strict_gain_in_T_exponent": fraction_text(gain),
    }


def bottleneck_monomial_u_exponent(
    u_power: Fraction = Fraction(0, 1),
    l_power: Fraction = Fraction(0, 1),
    v_power: Fraction = Fraction(0, 1),
    w_power: Fraction = Fraction(0, 1),
) -> Fraction:
    """Return a U exponent at the §13.1 bottleneck cell, exactly."""
    l_in_u = BOTTLE_L_IN_T / BOTTLE_U_IN_T
    v_in_u = l_in_u * BOTTLE_SIGMA
    return u_power + l_power * l_in_u + v_power * v_in_u + w_power * BOTTLE_W_IN_U


def zero_density_bottleneck_cell() -> dict[str, Any]:
    """Evaluate the §13.1 Remark's Theorem 1.1 and energy-bound cells."""
    zero = Fraction(0, 1)
    one = Fraction(1, 1)
    l_in_u = BOTTLE_L_IN_T / BOTTLE_U_IN_T
    v_in_u = l_in_u * BOTTLE_SIGMA
    local_w_in_t = BOTTLE_U_IN_T * BOTTLE_W_IN_U
    interval_count_in_t = one - BOTTLE_U_IN_T

    # Theorem 1.1, with time parameter U, length L and threshold V=L^sigma.
    large_value_term_1 = bottleneck_monomial_u_exponent(
        l_power=Fraction(2, 1), v_power=Fraction(-2, 1)
    )
    large_value_term_2 = bottleneck_monomial_u_exponent(
        l_power=Fraction(18, 5), v_power=Fraction(-4, 1)
    )
    large_value_term_3 = bottleneck_monomial_u_exponent(
        u_power=one, l_power=Fraction(12, 5), v_power=Fraction(-4, 1)
    )
    large_value_maximum = max(
        large_value_term_1, large_value_term_2, large_value_term_3
    )

    # Proposition 11.1 (label prp:energybound), with time parameter U.
    energy_term_1 = bottleneck_monomial_u_exponent(
        l_power=Fraction(4, 1) - Fraction(4, 1) * BOTTLE_SIGMA,
        w_power=one,
    )
    energy_term_2 = bottleneck_monomial_u_exponent(
        u_power=Fraction(1, 4),
        l_power=one - Fraction(2, 1) * BOTTLE_SIGMA,
        w_power=Fraction(21, 8),
    )
    energy_term_3 = bottleneck_monomial_u_exponent(
        l_power=one - Fraction(2, 1) * BOTTLE_SIGMA,
        w_power=Fraction(3, 1),
    )
    random_energy = Fraction(4, 1) * BOTTLE_W_IN_U - one
    stated_energy = Fraction(5, 2) * BOTTLE_W_IN_U

    total_count_in_t = interval_count_in_t + local_w_in_t
    density_target_in_t = Fraction(30, 13) * (one - BOTTLE_SIGMA)

    assert BOTTLE_L_IN_T == Fraction(2, 1) * BOTTLE_N_IN_T
    assert l_in_u == Fraction(5, 6)
    assert v_in_u == Fraction(7, 12)
    assert Fraction(3, 4) <= l_in_u <= one  # Proposition 11.1 range.
    assert large_value_term_1 == Fraction(1, 2)
    assert large_value_term_2 == large_value_term_3 == Fraction(2, 3)
    assert large_value_maximum == BOTTLE_W_IN_U
    assert energy_term_1 == energy_term_2 == energy_term_3 == Fraction(5, 3)
    assert stated_energy == random_energy == Fraction(5, 3)
    assert local_w_in_t == Fraction(8, 13)
    assert interval_count_in_t == Fraction(1, 13)
    assert total_count_in_t == density_target_in_t == Fraction(9, 13)

    return {
        "claim_boundary": (
            "Exact exponent substitution in the parameter pattern stated "
            "in the final Remark of §13.1; not a proof that an extremizing "
            "set W or a sharpness obstruction exists."
        ),
        "parameters": {
            "sigma": fraction_text(BOTTLE_SIGMA),
            "original_N_in_T": "N = T^(5/13)",
            "squared_polynomial_length": "L = N^2 = T^(10/13)",
            "subinterval_length": "U = T^(12/13)",
            "L_in_U": "L = U^(5/6)",
            "threshold": "V = L^sigma = U^(7/12)",
            "local_large_value_count": "|W| = U^(2/3)",
            "stated_energy": "E(W) = |W|^(5/2) = U^(5/3)",
            "random_energy_scale": "|W|^4/U = U^(5/3)",
        },
        "theorem_1_1_at_U": {
            "terms": {
                "L^2*V^-2": fraction_text(large_value_term_1),
                "L^(18/5)*V^-4": fraction_text(large_value_term_2),
                "U*L^(12/5)*V^-4": fraction_text(large_value_term_3),
            },
            "maximum_U_exponent": fraction_text(large_value_maximum),
            "maximizing_terms": ["L^(18/5)*V^-4", "U*L^(12/5)*V^-4"],
        },
        "proposition_11_1_energy_bound_at_U": {
            "terms": {
                "|W|*L^(4-4*sigma)": fraction_text(energy_term_1),
                "|W|^(21/8)*U^(1/4)*L^(1-2*sigma)": fraction_text(energy_term_2),
                "|W|^3*L^(1-2*sigma)": fraction_text(energy_term_3),
            },
            "common_U_exponent": fraction_text(energy_term_1),
            "tie_pattern": "all three Proposition 11.1 terms tie at U^(5/3)",
        },
        "subinterval_aggregation": {
            "number_of_subintervals": "T/U = T^(1/13)",
            "local_bound": "U^(2/3) = T^(8/13)",
            "total": "T^(1/13)*T^(8/13) = T^(9/13)",
            "density_target": "T^((30/13)*(1-7/10)) = T^(9/13)",
            "total_T_exponent": fraction_text(total_count_in_t),
        },
    }


def compute_certificate() -> dict[str, Any]:
    """Derive every frozen Route A rational endpoint from its stated input."""
    one = Fraction(1, 1)
    ingham_at_star = ingham_coefficient(SIGMA_STAR)
    gm_at_star = guth_maynard_coefficient(SIGMA_STAR)
    global_coefficient = ingham_at_star

    # The exact identity below fixes the direction of the crossover without
    # numerical sampling: A_I-A_GM = 30(sigma-7/10)/((2-sigma)(3+5sigma)).
    difference_numerator_at_star = Fraction(30, 1) * (SIGMA_STAR - SIGMA_STAR)
    difference_denominator_at_star = (
        (Fraction(2, 1) - SIGMA_STAR)
        * (Fraction(3, 1) + Fraction(5, 1) * SIGMA_STAR)
    )

    # In the uniform proof T is x/y up to a subexponential factor and the
    # density input requires T < x^(1/b-epsilon).  Thus theta = 1-1/b.
    uniform_t_exponent = one / global_coefficient
    uniform_theta = one - uniform_t_exponent

    # In the almost-all second-moment proof the corresponding condition is
    # T < X^(2/b-epsilon), while delta X has the threshold interval length.
    almost_all_t_exponent = Fraction(2, 1) / global_coefficient
    delta_exponent = -almost_all_t_exponent
    almost_all_theta = one - almost_all_t_exponent

    assert ingham_at_star == gm_at_star == Fraction(30, 13)
    assert coefficient_difference(SIGMA_STAR) == Fraction(0, 1)
    assert difference_numerator_at_star == Fraction(0, 1)
    assert difference_denominator_at_star > 0
    assert uniform_t_exponent == Fraction(13, 30)
    assert uniform_theta == Fraction(17, 30)
    assert almost_all_t_exponent == Fraction(13, 15)
    assert delta_exponent == Fraction(-13, 15)
    assert almost_all_theta == Fraction(2, 15)

    return {
        "artifact_version": ARTIFACT_VERSION,
        "route": ROUTE,
        "arithmetic": "exact fractions.Fraction only",
        "claim_boundary": (
            "This artifact exactly verifies rational consequences of the "
            "published bounds named in docs/cycle-1-route-a.md; it does not "
            "reprove those analytic bounds or their error estimates."
        ),
        "inputs": {
            "sigma_star": fraction_text(SIGMA_STAR),
            "ingham_coefficient": "3/(2-sigma)",
            "guth_maynard_coefficient": "15/(3+5*sigma)",
        },
        "critical_large_values_cell": critical_large_values_cell(),
        "zero_density_bottleneck_cell": zero_density_bottleneck_cell(),
        "crossover": {
            "sigma": fraction_text(SIGMA_STAR),
            "ingham_at_sigma": fraction_text(ingham_at_star),
            "guth_maynard_at_sigma": fraction_text(gm_at_star),
            "difference_identity": (
                "A_I(sigma)-A_GM(sigma) = "
                "30*(sigma-7/10)/((2-sigma)*(3+5*sigma))"
            ),
            "difference_at_sigma": fraction_text(coefficient_difference(SIGMA_STAR)),
            "positive_denominator_at_sigma": fraction_text(difference_denominator_at_star),
            "global_density_coefficient_b": fraction_text(global_coefficient),
        },
        "uniform_short_interval": {
            "formula": "theta_uniform = 1 - 1/b",
            "one_over_b": fraction_text(uniform_t_exponent),
            "theta": fraction_text(uniform_theta),
            "epsilon_convention": "published conclusion is theta > 17/30, written y >= x^(17/30+epsilon)",
        },
        "almost_all_short_interval": {
            "formula": "theta_almost_all = 1 - 2/b",
            "two_over_b": fraction_text(almost_all_t_exponent),
            "delta_exponent": fraction_text(delta_exponent),
            "theta": fraction_text(almost_all_theta),
            "epsilon_convention": "published conclusion is theta > 2/15, written y >= X^(2/15+epsilon)",
        },
        "assertions": {
            "crossover_equal": True,
            "uniform_endpoint_equal": True,
            "almost_all_endpoint_equal": True,
        },
    }


def source_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    """Hash canonical JSON using only the standard library."""
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    started_ns = time.perf_counter_ns()
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    certificate = compute_certificate()
    certificate["frozen_source"] = FROZEN_SOURCE
    certificate["supersedes"] = {
        "artifact": "artifacts/baseline-route-a-v2.json",
        "mathematical_certificate_sha256": PREVIOUS_MATHEMATICAL_CERTIFICATE_SHA256,
        "change": "adds the exact §13.1 zero-density bottleneck-cell evaluation",
    }
    certificate["mathematical_certificate_sha256"] = canonical_sha256(certificate)
    certificate["replay"] = {
        "script": str(script_path.relative_to(project_root)),
        "script_sha256": source_sha256(script_path),
        "python_implementation": platform.python_implementation(),
        "python_version": sys.version.split()[0],
        "wall_time_ns": time.perf_counter_ns() - started_ns,
    }
    artifact = project_root / "artifacts" / "baseline-route-a-v3.json"
    artifact.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(artifact)


if __name__ == "__main__":
    main()
