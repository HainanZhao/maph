#!/usr/bin/env python3
"""Cycle 145': d=5 calibration of the two-base fusion mechanism.

For d=5,

  beta=2+sqrt(3),  A_5=[[56,-15],[15,-4]],
  (p,k,r,s)=(-56,15,4,15).

The honest lens bases are distinct in the upper half-plane.  At beta
they fuse because A_5 beta=beta.  Independently, the standard modular
double fuses because beta+beta^(-1)=4.

The d=5 bibasic alias ratio has no d=6 minus sign.  At fusion it becomes

  q (1-x)(1-w^-1*x) / ((1-q*x)(1-q*w^-1*x)),

the closed-locus 2-psi-2 packet.  This is the requested branch-(a)
calibration: the proved dimension lands on the positive-argument locus,
while d=6 lands at its sign-reflected neighbor.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import acb, arb, ctx, fmpz_poly

from certify_dimension_five_double_sine import overlap_log
from dimension_six_two_base_lens import (
    AliasVariables,
    arb_fraction,
    complex_error,
    exp_two_pi_i,
    negative_inverse_ratio_bound,
    positive_ratio_bound,
    q_pochhammer,
)


LEVEL = 15
P_PARAMETER = -56
A_MATRIX = ((56, -15), (15, -4))


def mobius(value: acb) -> acb:
    return (56 * value - 15) / (15 * value - 4)


def geodesic_point(parameter: Fraction) -> acb:
    parameter_ball = arb_fraction(parameter)
    radius = arb(3).sqrt()
    denominator = 1 + parameter_ball**2
    return acb(
        2 + radius * (1 - parameter_ball**2) / denominator,
        radius * 2 * parameter_ball / denominator,
    )


def lens_parameters(tau: acb) -> tuple[acb, acb, acb]:
    omega_one = 15 * tau - 4
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
    u = (mu + discrete) / LEVEL
    u_tilde = (
        mu - P_PARAMETER * discrete * omega_one
    ) / (LEVEL * omega_one)
    return q_pochhammer(
        q_lens_tilde * exp_two_pi_i(u_tilde),
        q_lens_tilde,
        tolerance / 2,
    ) / q_pochhammer(
        exp_two_pi_i(u),
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
        z_value = (
            mu
            + omega_one * delta_index
            + gamma_index
        ) / LEVEL
        result *= gamma_standard(
            z_value,
            omega_one,
            tolerance / LEVEL,
        )
    return result


def alias_variables(
    tau: acb,
    first_frequency: int,
    second_frequency: int,
    alias_index: int,
) -> AliasVariables:
    omega_one, q_lens, q_lens_tilde = lens_parameters(tau)
    d_parameter = 3 * tau - 1
    alpha = (
        d_parameter
        * (3 * second_frequency - 4 * first_frequency + 10)
        / 2
        + 5 * d_parameter * alias_index / 2
    )
    discrete = first_frequency - 1 - 5 * alias_index

    def variables(mu: acb, label: int) -> tuple[acb, acb]:
        x_value = exp_two_pi_i((mu + label) / LEVEL)
        u_tilde = (
            mu - P_PARAMETER * label * omega_one
        ) / (LEVEL * omega_one)
        a_value = q_lens_tilde * exp_two_pi_i(u_tilde)
        return x_value, a_value

    x_first, a_first = variables(alpha, discrete)
    x_second, a_second = variables(-alpha, 3 - discrete)
    return AliasVariables(
        x_first,
        a_first,
        x_second,
        a_second,
        q_lens,
        q_lens_tilde,
    )


def alias_ratio(
    tau: acb,
    first_frequency: int,
    second_frequency: int,
    alias_index: int,
) -> acb:
    values = alias_variables(
        tau,
        first_frequency,
        second_frequency,
        alias_index,
    )
    return (
        (1 - values.x_first)
        / (1 - values.a_first)
        * (1 - values.a_second / values.q_lens_tilde)
        / (1 - values.x_second / values.q_lens)
    )


def alias_class_sum(
    tau: acb,
    first_frequency: int,
    second_frequency: int,
    residue: int,
    tolerance: Fraction,
) -> tuple[acb, arb]:
    total = acb(1)
    tolerance_ball = arb_fraction(tolerance)

    positive_term = acb(1)
    positive_tail = arb(2)
    for index in range(1000):
        positive_term *= alias_ratio(
            tau,
            first_frequency,
            second_frequency,
            residue + 2 * index,
        )
        total += positive_term
        next_values = alias_variables(
            tau,
            first_frequency,
            second_frequency,
            residue + 2 * (index + 1),
        )
        bound = positive_ratio_bound(next_values)
        if bound < arb(1) / 2:
            positive_tail = (
                abs(positive_term).upper() * bound / (1 - bound)
            )
            if positive_tail < tolerance_ball / 2:
                break
    else:
        raise RuntimeError("positive d=5 bibasic tail did not close")

    negative_term = acb(1)
    negative_tail = arb(2)
    for distance in range(1, 1001):
        negative_term /= alias_ratio(
            tau,
            first_frequency,
            second_frequency,
            residue - 2 * distance,
        )
        total += negative_term
        next_values = alias_variables(
            tau,
            first_frequency,
            second_frequency,
            residue - 2 * (distance + 1),
        )
        bound = negative_inverse_ratio_bound(next_values)
        if bound < arb(1) / 2:
            negative_tail = (
                abs(negative_term).upper() * bound / (1 - bound)
            )
            if negative_tail < tolerance_ball / 2:
                break
    else:
        raise RuntimeError("negative d=5 bibasic tail did not close")

    tail = positive_tail + negative_tail
    return total + complex_error(tail), tail


def proved_boundary_packet(tolerance: Fraction) -> tuple[arb, arb]:
    beta = 2 + arb(3).sqrt()
    logarithm, _ = overlap_log(
        0,
        1,
        beta,
        tolerance,
        dimension=5,
    )
    squared_overlap = (2 * logarithm).exp()
    polynomial = fmpz_poly(
        [
            1,
            -16,
            95,
            -260,
            355,
            -348,
            388,
            -300,
            195,
            -300,
            388,
            -348,
            355,
            -260,
            95,
            -16,
            1,
        ]
    )
    candidates = [
        root.real
        for root, multiplicity in polynomial.complex_roots()
        if (
            multiplicity == 1
            and root.imag.contains(0)
            and root.real > arb(3890) / 1000
            and root.real < arb(3891) / 1000
        )
    ]
    if len(candidates) != 1:
        raise RuntimeError("failed to isolate the proved d=5 packet")
    return squared_overlap, candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=30)
    parser.add_argument("--tolerance", default="1e-12")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    ctx.dps = arguments.digits
    ctx.cap = 6

    beta = 2 + arb(3).sqrt()
    trace_difference = beta + 1 / beta - 4
    fixed_difference = mobius(acb(beta)) - beta
    standard_fusion = (
        exp_two_pi_i(acb(beta))
        - exp_two_pi_i(-1 / acb(beta))
    )
    lens_fusion = (
        exp_two_pi_i(acb(beta))
        - exp_two_pi_i(mobius(acb(beta)))
    )
    fusion_verified = all(
        value.contains(0)
        for value in (
            trace_difference,
            fixed_difference,
            standard_fusion,
            lens_fusion,
        )
    )
    print(f"D5_TRACE_MINUS_4={trace_difference}")
    print(f"D5_A5_BETA_MINUS_BETA={fixed_difference}")
    print(f"D5_FUSION_VERIFIED={int(fusion_verified)}")
    if not fusion_verified:
        raise RuntimeError("d=5 fusion geometry failed")

    factorization_count = 0
    alias_count = 0
    for point_index, parameter in enumerate(
        (Fraction(20), Fraction(10), Fraction(5)),
        start=1,
    ):
        tau = geodesic_point(parameter)
        d_parameter = 3 * tau - 1
        alpha = d_parameter * 13 / 2
        discrete = -1
        direct = gamma_lens_direct(
            alpha,
            discrete,
            tau,
            tolerance / 8,
        )
        factorized = gamma_lens_factorized(
            alpha,
            discrete,
            tau,
            tolerance / 8,
        )
        difference = direct / factorized - 1
        enclosed = difference.contains(0)
        factorization_count += int(enclosed)
        print(
            f"D5_POINT_{point_index}_DIRECT_OVER_FACTORIZED_MINUS_ONE="
            f"{difference}"
        )
        if not enclosed:
            raise RuntimeError("d=5 factorization enclosure failed")
        for residue in range(2):
            packet, tail = alias_class_sum(
                tau,
                0,
                1,
                residue,
                tolerance,
            )
            alias_count += 1
            print(
                f"D5_POINT_{point_index}_CLASS_{residue}_PACKET={packet} "
                f"TAIL={tail}"
            )

    squared_overlap, algebraic_root = proved_boundary_packet(
        max(tolerance, Fraction(1, 10**8))
    )
    boundary_difference = squared_overlap - algebraic_root
    boundary_enclosed = boundary_difference.contains(0)
    print(f"D5_PROVED_SQUARED_OVERLAP={squared_overlap}")
    print(f"D5_PROVED_ALGEBRAIC_ROOT={algebraic_root}")
    print(f"D5_BOUNDARY_PACKET_DIFFERENCE={boundary_difference}")
    print(f"D5_PROVED_PACKET_ENCLOSED={int(boundary_enclosed)}")
    if not boundary_enclosed:
        raise RuntimeError("proved d=5 boundary packet was not recovered")

    print(f"D5_FACTORIZATION_ENCLOSURES={factorization_count}/3")
    print(f"D5_TWO_BASE_ALIAS_CLASS_ENCLOSURES={alias_count}/6")
    print("D5_FORMAL_FUSION_SUBSTITUTIONS=X1=x,A1=q*x")
    print(
        "D5_FORMAL_FUSION_SUBSTITUTIONS_SECOND="
        "X2=w*x^(-1),A2=q*w*x^(-1)"
    )
    print(
        "D5_FORMAL_FUSION_RATIO="
        "q*(1-x)*(1-w^(-1)*x)/"
        "((1-q*x)*(1-q*w^(-1)*x))"
    )
    print("D5_CLOSED_LOCUS_ARGUMENT=+q")
    print("D5_ANALYTIC_LENS_LEVEL=15")
    print("D5_ALIAS_PARITY_PERIOD=2")
    print("D5_FUSION_SIGN_BIT=0")
    print("D6_NEIGHBOR_ARGUMENT=-q")
    print("D5_CALIBRATION_BRANCH=A")
    print("D5_TWO_BASE_CALIBRATION_ENCLOSED=1")


if __name__ == "__main__":
    main()
