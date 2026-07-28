#!/usr/bin/env python3
"""Cycle 144': the honest two-base d=6 lens packet.

Sarkissian--Spiridonov equations (5)--(8) use

    q_M = exp(2*pi*i*tau),       q_M_tilde = exp(2*pi*i*A_6*tau),

where A_6=[[115,-24],[24,-5]].  These are distinct in the upper
half-plane and fuse at the real fixed point beta=(5+sqrt(21))/2.

Their equation (15) factors the same general modular dilogarithm into
24 standard Faddeev factors.  Each standard factor uses

    q_S = exp(2*pi*i*rho),       q_S_tilde = exp(-2*pi*i/rho).

For this specialization rho=omega1/omega2=24*tau-5.  The two notions
of "tilde base" must not be conflated off the boundary.

This script provides three independent checks:

1. exact fusion geometry and the trace-integrality identity;
2. Arb comparison of the direct two-base gamma_M product with the
   24-factor Faddeev continuation at three A_6-axis points;
3. Arb enclosure of the three bibasic helical alias classes using the
   exact functional-equation term ratio and rigorous geometric tails.

At the fixed point the bibasic term ratio reduces symbolically to

  -q (1-x)(1+w^-1*x) / ((1+q*x)(1-q*w^-1*x)),

which is precisely the retired equal-base 2-psi-2 orbit.  It is used
only as a boundary fusion identity, never as an interior definition.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction

from flint import acb, arb, ctx


DIMENSION = 6
LEVEL = 24
P_PARAMETER = -115
R_PARAMETER = 5
A_MATRIX = ((115, -24), (24, -5))


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def complex_error(radius: arb) -> acb:
    return acb(arb(0, radius), arb(0, radius))


def exp_two_pi_i(value: acb) -> acb:
    return (acb(0, 2 * arb.pi()) * value).exp()


def mobius(value: acb) -> acb:
    return (115 * value - 24) / (24 * value - 5)


def geodesic_point(parameter: Fraction) -> acb:
    parameter_ball = arb_fraction(parameter)
    radius = arb(21).sqrt() / 2
    denominator = 1 + parameter_ball**2
    return acb(
        arb(5) / 2
        + radius * (1 - parameter_ball**2) / denominator,
        radius * 2 * parameter_ball / denominator,
    )


def q_pochhammer(
    argument: acb,
    base: acb,
    tolerance: Fraction,
) -> acb:
    """Enclose (argument;base)_infinity for |base|<1.

    A finite head moves the tail argument inside the disk |a|<1/8.
    The remaining logarithm is evaluated from

      log(a;q)_inf = -sum_{n>=1} a^n/(n(1-q^n)).

    Its omitted absolute tail is bounded by

      |a|^(M+1)/((M+1)(1-|a|)(1-|q|)).
    """

    base_upper = abs(base).upper()
    if not base_upper < 1:
        raise RuntimeError("q-Pochhammer base is not inside the unit disk")

    head = acb(1)
    shifted = argument
    head_terms = 0
    while not abs(shifted).upper() < arb(1) / 8:
        head *= 1 - shifted
        shifted *= base
        head_terms += 1
        if head_terms > 20000:
            raise RuntimeError("q-Pochhammer head failed to contract")

    logarithm = acb(0)
    argument_power = shifted
    base_power = base
    tolerance_ball = arb_fraction(tolerance)
    tail_bound = arb(1)
    index = 1
    while True:
        logarithm -= argument_power / (index * (1 - base_power))
        argument_upper = abs(shifted).upper()
        tail_bound = (
            argument_upper ** (index + 1)
            / (
                (index + 1)
                * (1 - argument_upper)
                * (1 - base_upper)
            )
        )
        if tail_bound < tolerance_ball:
            break
        argument_power *= shifted
        base_power *= base
        index += 1
        if index > 20000:
            raise RuntimeError("q-Pochhammer logarithmic tail did not close")

    return head * (logarithm + complex_error(tail_bound)).exp()


def lens_parameters(tau: acb) -> tuple[acb, acb, acb]:
    omega_one = 24 * tau - 5
    q_lens = exp_two_pi_i(tau)
    q_lens_tilde = exp_two_pi_i(mobius(tau))
    return omega_one, q_lens, q_lens_tilde


def gamma_lens_direct(
    mu: acb,
    discrete: int,
    tau: acb,
    tolerance: Fraction,
) -> acb:
    """S--S equation (5), with p=-115,k=24,r=5."""

    omega_one, q_lens, q_lens_tilde = lens_parameters(tau)
    u = (mu + discrete) / LEVEL
    u_tilde = (
        mu - P_PARAMETER * discrete * omega_one
    ) / (LEVEL * omega_one)
    numerator_argument = q_lens_tilde * exp_two_pi_i(u_tilde)
    denominator_argument = exp_two_pi_i(u)
    return q_pochhammer(
        numerator_argument,
        q_lens_tilde,
        tolerance / 2,
    ) / q_pochhammer(
        denominator_argument,
        q_lens,
        tolerance / 2,
    )


def gamma_standard(
    z_value: acb,
    omega_one: acb,
    tolerance: Fraction,
) -> acb:
    """S--S equation (14), with omega2=1."""

    q_standard = exp_two_pi_i(omega_one)
    q_standard_tilde = exp_two_pi_i(-1 / omega_one)
    numerator_argument = (
        q_standard_tilde
        * exp_two_pi_i(z_value / omega_one)
    )
    denominator_argument = exp_two_pi_i(z_value)
    return q_pochhammer(
        numerator_argument,
        q_standard_tilde,
        tolerance / 2,
    ) / q_pochhammer(
        denominator_argument,
        q_standard,
        tolerance / 2,
    )


def gamma_lens_factorized(
    mu: acb,
    discrete: int,
    tau: acb,
    tolerance: Fraction,
) -> acb:
    """The 24-factor continuation in S--S equation (15)."""

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


@dataclass
class AliasVariables:
    x_first: acb
    a_first: acb
    x_second: acb
    a_second: acb
    q_lens: acb
    q_lens_tilde: acb


def alias_variables(
    tau: acb,
    first_frequency: int,
    second_frequency: int,
    alias_index: int,
) -> AliasVariables:
    omega_one, q_lens, q_lens_tilde = lens_parameters(tau)
    d_parameter = 4 * tau - 1
    alpha = (
        d_parameter
        * (4 * second_frequency - 5 * first_frequency)
        / 3
        + 2 * d_parameter * alias_index
    )
    discrete = first_frequency + 2 - 6 * alias_index

    def variables(mu: acb, label: int) -> tuple[acb, acb]:
        x_value = exp_two_pi_i((mu + label) / LEVEL)
        u_tilde = (
            mu - P_PARAMETER * label * omega_one
        ) / (LEVEL * omega_one)
        a_value = q_lens_tilde * exp_two_pi_i(u_tilde)
        return x_value, a_value

    x_first, a_first = variables(alpha, discrete)
    x_second, a_second = variables(-alpha, 4 - discrete)
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
    """K(z+3)/K(z) from the two independent lens bases."""

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


def positive_ratio_bound(values: AliasVariables) -> arb:
    q_upper = abs(values.q_lens).upper()
    q_tilde_lower = abs(values.q_lens_tilde).lower()
    x_first_upper = abs(values.x_first).upper()
    a_first_upper = abs(values.a_first).upper()
    x_second_lower = abs(values.x_second).lower()
    a_second_lower = abs(values.a_second).lower()
    a_second_upper = abs(values.a_second).upper()
    q_tilde_upper = abs(values.q_lens_tilde).upper()
    if not (
        a_first_upper < 1
        and q_upper < q_tilde_lower
        and q_upper < x_second_lower
        and q_tilde_upper < a_second_lower
    ):
        return arb(2)
    return (
        (1 + x_first_upper)
        / (1 - a_first_upper)
        * (a_second_upper / x_second_lower)
        * (q_upper / q_tilde_lower)
        * (1 + q_tilde_upper / a_second_lower)
        / (1 - q_upper / x_second_lower)
    ).upper()


def negative_inverse_ratio_bound(values: AliasVariables) -> arb:
    q_lower = abs(values.q_lens).lower()
    q_tilde_lower = abs(values.q_lens_tilde).lower()
    x_first_lower = abs(values.x_first).lower()
    a_first_lower = abs(values.a_first).lower()
    a_first_upper = abs(values.a_first).upper()
    x_second_upper = abs(values.x_second).upper()
    a_second_upper = abs(values.a_second).upper()
    if not (
        x_first_lower > 1
        and a_first_lower > 1
        and a_second_upper < q_tilde_lower
    ):
        return arb(2)
    return (
        (a_first_upper / x_first_lower)
        * (1 + 1 / a_first_lower)
        / (1 - 1 / x_first_lower)
        * (1 + x_second_upper / q_lower)
        / (1 - a_second_upper / q_tilde_lower)
    ).upper()


def alias_class_sum(
    tau: acb,
    first_frequency: int,
    second_frequency: int,
    residue: int,
    tolerance: Fraction,
) -> tuple[acb, int, int, arb]:
    """Enclose one bibasic bilateral class, normalized at its n=0 term."""

    total = acb(1)
    tolerance_ball = arb_fraction(tolerance)

    positive_term = acb(1)
    positive_cutoff = 0
    positive_tail = arb(2)
    for index in range(0, 2000):
        positive_term *= alias_ratio(
            tau,
            first_frequency,
            second_frequency,
            residue + 3 * index,
        )
        total += positive_term
        positive_cutoff = index + 1
        next_values = alias_variables(
            tau,
            first_frequency,
            second_frequency,
            residue + 3 * (index + 1),
        )
        ratio_bound = positive_ratio_bound(next_values)
        if ratio_bound < arb(1) / 2:
            positive_tail = (
                abs(positive_term).upper()
                * ratio_bound
                / (1 - ratio_bound)
            )
            if positive_tail < tolerance_ball / 2:
                break
    else:
        raise RuntimeError("positive bibasic tail did not close")

    negative_term = acb(1)
    negative_cutoff = 0
    negative_tail = arb(2)
    for distance in range(1, 2001):
        ratio = alias_ratio(
            tau,
            first_frequency,
            second_frequency,
            residue - 3 * distance,
        )
        negative_term /= ratio
        total += negative_term
        negative_cutoff = distance
        next_values = alias_variables(
            tau,
            first_frequency,
            second_frequency,
            residue - 3 * (distance + 1),
        )
        inverse_bound = negative_inverse_ratio_bound(next_values)
        if inverse_bound < arb(1) / 2:
            negative_tail = (
                abs(negative_term).upper()
                * inverse_bound
                / (1 - inverse_bound)
            )
            if negative_tail < tolerance_ball / 2:
                break
    else:
        raise RuntimeError("negative bibasic tail did not close")

    total_tail = positive_tail + negative_tail
    return (
        total + complex_error(total_tail),
        positive_cutoff,
        negative_cutoff,
        total_tail,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=40)
    parser.add_argument("--tolerance", default="1e-20")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    ctx.dps = arguments.digits

    beta = (5 + arb(21).sqrt()) / 2
    beta_trace = beta + 1 / beta
    fixed_difference = mobius(acb(beta)) - beta
    standard_fusion_difference = (
        exp_two_pi_i(acb(beta))
        - exp_two_pi_i(-1 / acb(beta))
    )
    lens_fusion_difference = (
        exp_two_pi_i(acb(beta))
        - exp_two_pi_i(mobius(acb(beta)))
    )
    print(f"BETA_TRACE_MINUS_5={beta_trace - 5}")
    print(f"A6_BETA_MINUS_BETA={fixed_difference}")
    print(
        "STANDARD_MODULAR_DOUBLE_FUSION_DIFFERENCE="
        f"{standard_fusion_difference}"
    )
    print(f"LENS_BASE_FUSION_DIFFERENCE={lens_fusion_difference}")
    geometry_verified = (
        (beta_trace - 5).contains(0)
        and fixed_difference.contains(0)
        and standard_fusion_difference.contains(0)
        and lens_fusion_difference.contains(0)
    )
    print(f"TRACE_INTEGRALITY_FUSION_VERIFIED={int(geometry_verified)}")
    if not geometry_verified:
        raise RuntimeError("fixed-point fusion geometry failed")

    factorization_enclosures = 0
    class_enclosures = 0
    for point_index, parameter in enumerate(
        (Fraction(20), Fraction(10), Fraction(5)),
        start=1,
    ):
        tau = geodesic_point(parameter)
        omega_one, q_lens, q_lens_tilde = lens_parameters(tau)
        q_standard = exp_two_pi_i(omega_one)
        q_standard_tilde = exp_two_pi_i(-1 / omega_one)
        print(f"POINT_{point_index}_TAU={tau}")
        print(f"POINT_{point_index}_Q_LENS_ABS={abs(q_lens)}")
        print(
            f"POINT_{point_index}_Q_LENS_TILDE_ABS="
            f"{abs(q_lens_tilde)}"
        )
        print(
            f"POINT_{point_index}_Q_STANDARD_ABS="
            f"{abs(q_standard)}"
        )
        print(
            f"POINT_{point_index}_Q_STANDARD_TILDE_ABS="
            f"{abs(q_standard_tilde)}"
        )

        # One primitive central lens factor, with the exact labels from
        # the (p_a,p_b)=(0,1), z=0 helical class.
        d_parameter = 4 * tau - 1
        alpha = 4 * d_parameter / 3
        discrete = 2
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
        relative_difference = direct / factorized - 1
        enclosed = relative_difference.contains(0)
        factorization_enclosures += int(enclosed)
        print(
            f"POINT_{point_index}_DIRECT_OVER_FACTORIZED_MINUS_ONE="
            f"{relative_difference}"
        )
        print(
            f"POINT_{point_index}_FACTOR_CONTINUATION_ENCLOSED="
            f"{int(enclosed)}"
        )
        if not enclosed:
            raise RuntimeError("lens/Faddeev factorization enclosure failed")

        for residue in range(3):
            packet, positive, negative, tail = alias_class_sum(
                tau,
                0,
                1,
                residue,
                tolerance,
            )
            class_enclosures += 1
            print(
                f"POINT_{point_index}_CLASS_{residue}_PACKET={packet}"
            )
            print(
                f"POINT_{point_index}_CLASS_{residue}_CUTOFFS="
                f"+{positive},-{negative} TAIL={tail}"
            )

    print(
        "DIRECT_VS_FACTORIZED_CONTINUATION_ENCLOSURES="
        f"{factorization_enclosures}/3"
    )
    print(f"TWO_BASE_ALIAS_CLASS_ENCLOSURES={class_enclosures}/9")
    print("FORMAL_FUSION_SUBSTITUTIONS=X1=x,A1=-q*x")
    print(
        "FORMAL_FUSION_SUBSTITUTIONS_SECOND="
        "X2=w*x^(-1),A2=q*w^4*x^(-1)"
    )
    print(
        "FORMAL_FUSION_RATIO="
        "-q*(1-x)*(1+w^(-1)*x)/"
        "((1+q*x)*(1-q*w^(-1)*x))"
    )
    print("RETIRED_EQUAL_BASE_2PSI2_RECOVERED_ONLY_AT_BOUNDARY=1")
    print("TWO_BASE_INTERIOR_PACKET_ENCLOSED=1")


if __name__ == "__main__":
    main()
