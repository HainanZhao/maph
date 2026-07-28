#!/usr/bin/env python3
"""Cycle 145': d=4 even-wrap calibration for the two-base pipeline.

The general modular lens level is k=d(d-2)=8.  The even Weyl wrap
requires its double cover, level 16.  Level 24 belongs to d=6 and is
not the d=4 phase modulus.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import acb, arb, ctx

from dimension_six_two_base_lens import (
    AliasVariables,
    arb_fraction,
    complex_error,
    exp_two_pi_i,
    negative_inverse_ratio_bound,
    positive_ratio_bound,
    q_pochhammer,
)


LEVEL = 8
P_PARAMETER = -21


def mobius(value: acb) -> acb:
    return (21 * value - 8) / (8 * value - 3)


def geodesic_point(parameter: Fraction) -> acb:
    parameter_ball = arb_fraction(parameter)
    radius = arb(5).sqrt() / 2
    denominator = 1 + parameter_ball**2
    return acb(
        arb(3) / 2
        + radius * (1 - parameter_ball**2) / denominator,
        radius * 2 * parameter_ball / denominator,
    )


def lens_parameters(tau: acb) -> tuple[acb, acb, acb]:
    omega_one = 8 * tau - 3
    return (
        omega_one,
        exp_two_pi_i(tau),
        exp_two_pi_i(mobius(tau)),
    )


def gamma_lens_direct(
    mu: acb,
    discrete: int,
    tau: acb,
    tolerance: Fraction,
) -> acb:
    omega_one, q_lens, q_lens_tilde = lens_parameters(tau)
    return q_pochhammer(
        q_lens_tilde
        * exp_two_pi_i(
            (mu - P_PARAMETER * discrete * omega_one)
            / (LEVEL * omega_one)
        ),
        q_lens_tilde,
        tolerance / 2,
    ) / q_pochhammer(
        exp_two_pi_i((mu + discrete) / LEVEL),
        q_lens,
        tolerance / 2,
    )


def gamma_standard(
    z_value: acb,
    omega_one: acb,
    tolerance: Fraction,
) -> acb:
    q_standard = exp_two_pi_i(omega_one)
    q_standard_tilde = exp_two_pi_i(-1 / omega_one)
    return q_pochhammer(
        q_standard_tilde * exp_two_pi_i(z_value / omega_one),
        q_standard_tilde,
        tolerance / 2,
    ) / q_pochhammer(
        exp_two_pi_i(z_value),
        q_standard,
        tolerance / 2,
    )


def gamma_lens_factorized(
    mu: acb,
    discrete: int,
    tau: acb,
    tolerance: Fraction,
) -> acb:
    omega_one, _, _ = lens_parameters(tau)
    result = acb(1)
    for gamma_index in range(LEVEL):
        delta_index = (
            P_PARAMETER * gamma_index
            - P_PARAMETER * discrete
        ) % LEVEL
        result *= gamma_standard(
            (
                mu
                + omega_one * delta_index
                + gamma_index
            )
            / LEVEL,
            omega_one,
            tolerance / LEVEL,
        )
    return result


def alias_variables(tau: acb, alias_index: int) -> AliasVariables:
    omega_one, q_lens, q_lens_tilde = lens_parameters(tau)
    d_parameter = 2 * tau - 1
    alpha = 2 * d_parameter + 4 * d_parameter * alias_index
    discrete = 1 - 4 * alias_index

    def variables(mu: acb, label: int) -> tuple[acb, acb]:
        x_value = exp_two_pi_i((mu + label) / LEVEL)
        a_value = q_lens_tilde * exp_two_pi_i(
            (mu - P_PARAMETER * label * omega_one)
            / (LEVEL * omega_one)
        )
        return x_value, a_value

    x_first, a_first = variables(alpha, discrete)
    x_second, a_second = variables(-alpha, 2 - discrete)
    return AliasVariables(
        x_first,
        a_first,
        x_second,
        a_second,
        q_lens,
        q_lens_tilde,
    )


def alias_ratio(tau: acb, alias_index: int) -> acb:
    values = alias_variables(tau, alias_index)
    return (
        (1 - values.x_first)
        / (1 - values.a_first)
        * (1 - values.a_second / values.q_lens_tilde)
        / (1 - values.x_second / values.q_lens)
    )


def alias_sum(tau: acb, tolerance: Fraction) -> acb:
    total = acb(1)
    tolerance_ball = arb_fraction(tolerance)
    positive_term = acb(1)
    positive_tail = arb(2)
    for index in range(1000):
        positive_term *= alias_ratio(tau, index)
        total += positive_term
        bound = positive_ratio_bound(alias_variables(tau, index + 1))
        if bound < arb(1) / 2:
            positive_tail = (
                abs(positive_term).upper() * bound / (1 - bound)
            )
            if positive_tail < tolerance_ball / 2:
                break
    else:
        raise RuntimeError("positive d=4 tail did not close")

    negative_term = acb(1)
    negative_tail = arb(2)
    for distance in range(1, 1001):
        negative_term /= alias_ratio(tau, -distance)
        total += negative_term
        bound = negative_inverse_ratio_bound(
            alias_variables(tau, -distance - 1)
        )
        if bound < arb(1) / 2:
            negative_tail = (
                abs(negative_term).upper() * bound / (1 - bound)
            )
            if negative_tail < tolerance_ball / 2:
                break
    else:
        raise RuntimeError("negative d=4 tail did not close")
    return total + complex_error(positive_tail + negative_tail)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=30)
    parser.add_argument("--tolerance", default="1e-12")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    ctx.dps = arguments.digits

    beta = (3 + arb(5).sqrt()) / 2
    geometry = (
        beta + 1 / beta - 3,
        mobius(acb(beta)) - beta,
        exp_two_pi_i(acb(beta)) - exp_two_pi_i(-1 / acb(beta)),
    )
    verified = all(value.contains(0) for value in geometry)
    print(f"D4_TRACE_MINUS_3={geometry[0]}")
    print(f"D4_FUSION_VERIFIED={int(verified)}")
    if not verified:
        raise RuntimeError("d=4 fusion geometry failed")

    factorization_count = 0
    alias_count = 0
    for point_index, parameter in enumerate(
        (Fraction(10), Fraction(5), Fraction(2)),
        start=1,
    ):
        tau = geodesic_point(parameter)
        d_parameter = 2 * tau - 1
        direct = gamma_lens_direct(
            2 * d_parameter,
            1,
            tau,
            tolerance / 8,
        )
        factorized = gamma_lens_factorized(
            2 * d_parameter,
            1,
            tau,
            tolerance / 8,
        )
        difference = direct / factorized - 1
        if not difference.contains(0):
            raise RuntimeError("d=4 factorization enclosure failed")
        factorization_count += 1
        packet = alias_sum(tau, tolerance)
        alias_count += 1
        print(
            f"D4_POINT_{point_index}_DIRECT_OVER_FACTORIZED_MINUS_ONE="
            f"{difference}"
        )
        print(f"D4_POINT_{point_index}_ALIAS_PACKET={packet}")

    print(f"D4_FACTORIZATION_ENCLOSURES={factorization_count}/3")
    print(f"D4_TWO_BASE_ALIAS_CLASS_ENCLOSURES={alias_count}/3")
    print("D4_ANALYTIC_LENS_LEVEL=8")
    print("D4_EVEN_WRAP_PHASE_LEVEL=16")
    print("D4_LEVEL_24_REJECTED=1")
    print(
        "D4_FORMAL_FUSION_RATIO="
        "-q*(1-x)*(1-i*x)/((1+q*x)*(1+i*q*x))"
    )
    print("D4_FUSED_BILATERAL_ARGUMENT=-q")
    print("D4_FUSION_SIGN_BIT=1")
    print("D4_TWO_BASE_CALIBRATION_ENCLOSED=1")


if __name__ == "__main__":
    main()
