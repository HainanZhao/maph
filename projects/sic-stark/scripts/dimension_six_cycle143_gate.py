#!/usr/bin/env python3
"""Cycle 143: rigorous enclosure gate for the d=6 connection chain.

This script bisects the proposed chain at its highest-risk link.

Upstream, Arb encloses the four positive double-sine generators, the
algebraic primitive root, all 225 rank-two minors, and AFK's exact
zero-characteristic endpoint ``-4*sqrt(7)``.

At the lens/2-psi-2 link, however, the equal-base specialization needs

    q_tilde = exp(2*pi*i*A_6*tau) = q = exp(2*pi*i*tau).

At the RM point this is true because A_6 fixes beta, but |q|=1 and the
ordinary bilateral convergence annulus has collapsed.  At three exact
points on the A_6 axis in the upper half-plane, Arb excludes
q_tilde=q.  Thus the equal-base 2-psi-2/Slater representation has no
off-boundary neighborhood on that geodesic.  A modular-completion
connection formula is required before the requested end-to-end radial
enclosure can even be defined noncircularly.

The script intentionally prints ``COMPLETE_CHAIN_ENCLOSED=0``.  This is
the Cycle-143 halt outcome required when the broken link is located.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import acb, arb, ctx, fmpz_poly

from certify_dimension_five_double_sine import overlap_log


DIMENSION = 6
A_MATRIX = ((115, -24), (24, -5))


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def acb_exp_pi_i(value: acb) -> acb:
    return (acb(0, arb.pi()) * value).exp()


def algebraic_primitive_root() -> arb:
    polynomial = fmpz_poly(
        [1, 3, -6, -16, 3, 0, 27, 0, 3, -16, -6, 3, 1]
    )
    candidates = []
    for root, multiplicity in polynomial.complex_roots():
        if (
            multiplicity == 1
            and root.imag.contains(0)
            and root.real > arb(2212) / 1000
            and root.real < arb(2213) / 1000
        ):
            candidates.append(root.real)
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one primitive root, found {len(candidates)}"
        )
    return candidates[0]


def structured_table(
    primitive_x: arb,
    lower_y: arb,
    primitive_z: arb,
    primitive_w: arb,
) -> list[list[arb]]:
    return [
        [
            arb(7).sqrt(),
            -primitive_x,
            lower_y,
            arb(-1),
            lower_y**-1,
            -primitive_x**-1,
        ],
        [
            -primitive_x**-1,
            -lower_y**-2,
            -primitive_z,
            -primitive_w,
            -lower_y**-2,
            -primitive_x,
        ],
        [
            lower_y**-1,
            -primitive_w,
            lower_y**-3,
            -primitive_z,
            lower_y,
            lower_y**2,
        ],
        [
            arb(-1),
            -primitive_z,
            -primitive_w,
            arb(-1),
            primitive_w**-1,
            -primitive_z**-1,
        ],
        [
            lower_y,
            -lower_y**-2,
            lower_y**-1,
            primitive_z**-1,
            lower_y**3,
            primitive_w**-1,
        ],
        [
            -primitive_x,
            -primitive_x**-1,
            lower_y**2,
            -primitive_w**-1,
            primitive_z**-1,
            -lower_y**2,
        ],
    ]


def reconstruct(table: list[list[arb]]) -> list[list[acb]]:
    tau_six = -acb_exp_pi_i(acb(arb(1) / DIMENSION))
    omega_six = acb_exp_pi_i(acb(arb(2) / DIMENSION))
    normalizer = arb(DIMENSION) * arb(DIMENSION + 1).sqrt()
    matrix = [
        [acb(0) for _ in range(DIMENSION)]
        for _ in range(DIMENSION)
    ]
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            for column in range(DIMENSION):
                row = (column + first) % DIMENSION
                matrix[row][column] += (
                    acb(table[first][second])
                    * tau_six ** (first * second)
                    * omega_six ** (second * column)
                    / normalizer
                )
    return matrix


def minor_audit(matrix: list[list[acb]]) -> tuple[int, arb]:
    containing_zero = 0
    maximum_radius = arb(0)
    for first_row in range(DIMENSION):
        for second_row in range(first_row + 1, DIMENSION):
            for first_column in range(DIMENSION):
                for second_column in range(first_column + 1, DIMENSION):
                    minor = (
                        matrix[first_row][first_column]
                        * matrix[second_row][second_column]
                        - matrix[first_row][second_column]
                        * matrix[second_row][first_column]
                    )
                    if minor.contains(0):
                        containing_zero += 1
                    radius = abs(minor)
                    if radius.upper() > maximum_radius.upper():
                        maximum_radius = radius
    return containing_zero, maximum_radius


def geodesic_point(parameter: Fraction) -> acb:
    """Rational parametrization of the A_6 axis.

    The axis is the circle

        (Re(tau)-5/2)^2 + Im(tau)^2 = 21/4.

    Parameter zero is the attracting endpoint beta.
    """

    parameter_ball = arb_fraction(parameter)
    radius = arb(21).sqrt() / 2
    denominator = 1 + parameter_ball**2
    real_part = (
        arb(5) / 2
        + radius * (1 - parameter_ball**2) / denominator
    )
    imaginary_part = (
        radius * 2 * parameter_ball / denominator
    )
    return acb(real_part, imaginary_part)


def mobius(matrix: tuple[tuple[int, int], tuple[int, int]], value: acb) -> acb:
    return (
        matrix[0][0] * value + matrix[0][1]
    ) / (
        matrix[1][0] * value + matrix[1][1]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=40)
    parser.add_argument("--tolerance", default="1e-7")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = (5 + arb(21).sqrt()) / 2

    generator_characteristics = {
        "x": (0, 1),
        "y": (0, 2),
        "z": (1, 2),
        "w": (1, 3),
    }
    generators: dict[str, arb] = {}
    total_panels = 0
    for label, (first, second) in generator_characteristics.items():
        logarithm, panels = overlap_log(
            first,
            second,
            beta,
            tolerance,
            dimension=DIMENSION,
        )
        generators[label] = logarithm.exp()
        total_panels += panels
        print(
            f"DOUBLE_SINE_{label.upper()}={generators[label]} "
            f"PANELS={panels}"
        )

    algebraic_x = algebraic_primitive_root()
    x_difference = generators["x"] - algebraic_x
    x_enclosed = x_difference.contains(0)
    print(f"ALGEBRAIC_X={algebraic_x}")
    print(f"DOUBLE_SINE_MINUS_ALGEBRAIC_X={x_difference}")
    print(f"UPSTREAM_X_ALG_ENCLOSED={int(x_enclosed)}")
    if not x_enclosed:
        raise RuntimeError("double-sine x does not enclose algebraic x")

    table = structured_table(
        generators["x"],
        generators["y"],
        generators["z"],
        generators["w"],
    )
    matrix = reconstruct(table)
    zero_minor_count, maximum_minor_ball = minor_audit(matrix)
    print(f"RANK_TWO_MINOR_COUNT={15**2}")
    print(f"MINOR_BALLS_CONTAINING_ZERO={zero_minor_count}")
    print(f"MAXIMUM_MINOR_ABSOLUTE_BALL={maximum_minor_ball}")
    all_minors_enclosed = zero_minor_count == 15**2
    print(
        "ALL_225_ANALYTIC_MINOR_BALLS_CONTAIN_ZERO="
        f"{int(all_minors_enclosed)}"
    )
    if not all_minors_enclosed:
        raise RuntimeError(
            "analytic generator balls do not enclose all minor zeros"
        )

    # AFK Lemma ``nu01overnu0val``: for r=1,d_j=d=6,
    # nu_0+nu_0^{-1}=-(d-2)*sqrt(d+1).
    omega_one = 24 * beta - 5
    auxiliary_zero = -omega_one.rsqrt()
    endpoint = auxiliary_zero + auxiliary_zero**-1
    endpoint_target = -4 * arb(7).sqrt()
    endpoint_difference = endpoint - endpoint_target
    endpoint_verified = endpoint_difference.contains(0)
    print(f"AUXILIARY_ZERO_CHARACTERISTIC={auxiliary_zero}")
    print(f"COLLAPSED_ENDPOINT={endpoint}")
    print(f"ENDPOINT_MINUS_TARGET={endpoint_difference}")
    print(
        "AFK_ENDPOINT_MINUS_4_SQRT7_VERIFIED="
        f"{int(endpoint_verified)}"
    )
    if not endpoint_verified:
        raise RuntimeError("AFK endpoint calibration failed")

    exclusions = 0
    for index, parameter in enumerate(
        (Fraction(20), Fraction(10), Fraction(5)),
        start=1,
    ):
        tau = geodesic_point(parameter)
        transformed_tau = mobius(A_MATRIX, tau)
        q = acb_exp_pi_i(2 * tau)
        q_tilde = acb_exp_pi_i(2 * transformed_tau)
        difference = q_tilde - q
        equal_base_excluded = not difference.contains(0)
        if equal_base_excluded:
            exclusions += 1
        print(f"GEODESIC_RADIUS_{index}={parameter}")
        print(f"GEODESIC_TAU_{index}={tau}")
        print(f"GEODESIC_A_TAU_{index}={transformed_tau}")
        print(f"Q_ABS_{index}={abs(q)}")
        print(f"Q_TILDE_ABS_{index}={abs(q_tilde)}")
        print(f"Q_TILDE_MINUS_Q_{index}={difference}")
        print(
            f"EQUAL_BASE_EXCLUDED_{index}="
            f"{int(equal_base_excluded)}"
        )
    print(f"GEODESIC_EQUAL_BASE_EXCLUSIONS={exclusions}")
    if exclusions != 3:
        raise RuntimeError("failed to exclude equal bases at all radii")

    fixed_tau = acb(beta)
    fixed_difference = mobius(A_MATRIX, fixed_tau) - fixed_tau
    if not fixed_difference.contains(0):
        raise RuntimeError("A_6 does not fix beta")
    fixed_q = acb_exp_pi_i(2 * fixed_tau)
    fixed_q_absolute = abs(fixed_q)
    fixed_modulus_one = fixed_q_absolute.contains(1)
    print(f"FIXED_POINT_A_TAU_MINUS_TAU={fixed_difference}")
    print(f"FIXED_POINT_Q_ABS={fixed_q_absolute}")
    print(f"FIXED_POINT_Q_MODULUS_ONE={int(fixed_modulus_one)}")
    if not fixed_modulus_one:
        raise RuntimeError("fixed-point q is not on the unit circle")

    print(f"TOTAL_ARB_SIMPSON_PANELS={total_panels}")
    print("EQUAL_BASE_OPEN_GEODESIC_NEIGHBORHOOD_EXISTS=0")
    print("BOUNDARY_2PSI2_STANDARD_CONVERGENCE=0")
    print("COMPLETE_CHAIN_ENCLOSED=0")
    print(
        "BROKEN_LINK=equal-base 2psi2/Slater specialization has "
        "no convergent off-boundary A6-geodesic neighborhood"
    )
    print("DOWNSTREAM_CYCLES_AUTHORIZED=0")


if __name__ == "__main__":
    main()
