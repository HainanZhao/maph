#!/usr/bin/env python3
"""Failed Arb Shintani-fan attempt for RQ-002057.

The fundamental-unit cones have determinant 80 and period ratio
151+20*sqrt(57), which is a poor direct quadrature representation.
This certificate regularizes each exact cone into nine unimodular
subcones.  Shintani-zeta additivity then leaves one affine point per
subcone, with period ratios below 4.64.  The naive product omits
half-open internal-ray corrections and is intentionally retained as a
failed proof attempt.  The direct-cone certificate is separate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import gcd

from flint import arb, ctx, fmpz_poly

from certify_q7_p7_packet import (
    arb_fraction,
    certified_simpson,
    near_integrand,
    product,
    tail_integrand,
)


SAFE_EXPONENT = 2592
DETERMINANT = 80

# Columns are the two fundamental cone rays in the indicated
# b-lattice coordinates.  These are the exact outputs of the
# case-specific PARI lattice probe.
CONE_MATRICES = [
    ((1, 51), (1, -29)),
    ((-101, 9), (166, -14)),
    ((-7, 3), (50, -10)),
    ((-279, 131), (286, -134)),
    ((-33, 37), (86, -94)),
    ((34, 12374), (-91, -33121)),
]

B_LATTICES = [
    ((Fraction(9), Fraction(3)), (Fraction(0), Fraction(3))),
    (
        (Fraction(9), Fraction(213, 38)),
        (Fraction(0), Fraction(3, 76)),
    ),
    (
        (Fraction(9, 19), Fraction(15, 152)),
        (Fraction(0), Fraction(3, 304)),
    ),
    (
        (Fraction(9, 19), Fraction(5343, 11552)),
        (Fraction(0), Fraction(3, 23104)),
    ),
    (
        (Fraction(9, 361), Fraction(447, 46208)),
        (Fraction(0), Fraction(3, 92416)),
    ),
    (
        (Fraction(9, 361), Fraction(32703, 3511808)),
        (Fraction(0), Fraction(3, 7023616)),
    ),
]

AFFINE_SHIFTS = [
    (Fraction(1, 9), Fraction(0)),
    (Fraction(1, 9), Fraction(0)),
    (Fraction(19, 9), Fraction(0)),
    (Fraction(19, 9), Fraction(0)),
    (Fraction(361, 9), Fraction(0)),
    (Fraction(361, 9), Fraction(0)),
]


def determinant(first: tuple[int, int], second: tuple[int, int]) -> int:
    return first[0] * second[1] - first[1] * second[0]


def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    if second == 0:
        return abs(first), 1 if first > 0 else -1, 0
    common, x_value, y_value = extended_gcd(second, first % second)
    return (
        common,
        y_value,
        x_value - (first // second) * y_value,
    )


def regular_fan(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> list[tuple[int, int]]:
    """Return the exact determinant-one fan between matrix columns."""

    first = (matrix[0][0], matrix[1][0])
    last = (matrix[0][1], matrix[1][1])
    signed_determinant = determinant(first, last)
    if abs(signed_determinant) != DETERMINANT:
        raise RuntimeError("fundamental cone determinant changed")
    common, p_value, q_value = extended_gcd(*first)
    if common != 1:
        raise RuntimeError("first cone ray is not primitive")

    if signed_determinant > 0:
        r_value, s_value = -first[1], first[0]
    else:
        r_value, s_value = first[1], -first[0]
    a_value = p_value * last[0] + q_value * last[1]
    n_value = abs(signed_determinant)
    shear = (-a_value) // n_value
    reduced_a = a_value + shear * n_value
    if reduced_a < 0:
        reduced_a += n_value
        shear += 1
    transform = (
        (
            p_value + shear * r_value,
            q_value + shear * s_value,
        ),
        (r_value, s_value),
    )
    if (
        transform[0][0] * first[0] + transform[0][1] * first[1],
        transform[1][0] * first[0] + transform[1][1] * first[1],
    ) != (1, 0):
        raise RuntimeError("fan transform does not normalize first ray")
    if (
        transform[0][0] * last[0] + transform[0][1] * last[1],
        transform[1][0] * last[0] + transform[1][1] * last[1],
    ) != (reduced_a, n_value):
        raise RuntimeError("fan transform does not normalize last ray")

    candidates = set()
    for x_value in range(max(reduced_a, 1) + 2):
        for y_value in range(n_value + 1):
            if (x_value, y_value) == (0, 0):
                continue
            if gcd(x_value, y_value) != 1:
                continue
            alpha_numerator = (
                x_value * n_value - y_value * reduced_a
            )
            if (
                alpha_numerator >= 0
                and alpha_numerator + y_value <= n_value
            ):
                candidates.add((x_value, y_value))
    ordered = sorted(
        candidates,
        key=lambda vector: Fraction(vector[1], n_value),
    )
    normalized_fan = [(1, 0)]
    while normalized_fan[-1] != (reduced_a, n_value):
        current = normalized_fan[-1]
        choices = [
            vector
            for vector in ordered
            if vector[1] > current[1]
            and determinant(current, vector) == 1
        ]
        if not choices:
            raise RuntimeError("regular fan construction stalled")
        normalized_fan.append(choices[0])

    transform_determinant = determinant(
        transform[0], transform[1]
    )
    if abs(transform_determinant) != 1:
        raise RuntimeError("fan transform is not unimodular")
    inverse = (
        (
            transform[1][1] // transform_determinant,
            -transform[0][1] // transform_determinant,
        ),
        (
            -transform[1][0] // transform_determinant,
            transform[0][0] // transform_determinant,
        ),
    )
    result = [
        (
            inverse[0][0] * vector[0]
            + inverse[0][1] * vector[1],
            inverse[1][0] * vector[0]
            + inverse[1][1] * vector[1],
        )
        for vector in normalized_fan
    ]
    if result[0] != first or result[-1] != last:
        raise RuntimeError("regular fan endpoints changed")
    expected_sign = 1 if signed_determinant > 0 else -1
    if any(
        determinant(result[index], result[index + 1])
        != expected_sign
        for index in range(len(result) - 1)
    ):
        raise RuntimeError("regular fan contains a non-unimodular cone")
    return result


def mod_one_upper(value: Fraction) -> Fraction:
    remainder = value - value.numerator // value.denominator
    return Fraction(1) if remainder == 0 else remainder


def affine_coordinates(
    first: tuple[int, int],
    second: tuple[int, int],
    shift: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    cone_determinant = determinant(first, second)
    if abs(cone_determinant) != 1:
        raise RuntimeError("affine coordinates require a unimodular cone")
    x_value = Fraction(
        second[1] * shift[0] - second[0] * shift[1],
        cone_determinant,
    )
    y_value = Fraction(
        -first[1] * shift[0] + first[0] * shift[1],
        cone_determinant,
    )
    return mod_one_upper(x_value), mod_one_upper(y_value)


def embedded_element(
    lattice: tuple[
        tuple[Fraction, Fraction],
        tuple[Fraction, Fraction],
    ],
    vector: tuple[int, int],
    y_embedding: arb,
) -> arb:
    constant = lattice[0][0] * vector[0] + lattice[0][1] * vector[1]
    coefficient = (
        lattice[1][0] * vector[0] + lattice[1][1] * vector[1]
    )
    return arb_fraction(constant) + arb_fraction(coefficient) * y_embedding


def fundamental_log_double_sine(
    argument: arb,
    beta: arb,
    tolerance: Fraction,
) -> tuple[arb, int]:
    """Enclose a fan-factor double sine for 1 < beta < 5."""

    linear = beta + 1 - 2 * argument
    if linear.contains(0) and abs(linear).upper() < arb_fraction(tolerance):
        return arb(0), 0
    delta = Fraction(1, 1_000_000)
    exponential_majorant = Fraction(100_001, 100_000)
    numerator_remainder = (
        Fraction(6**4, 1920) * exponential_majorant
    )
    denominator_remainder = (
        Fraction(5**4, 1920) * exponential_majorant
        + Fraction(1, 1920) * exponential_majorant
        + (
            Fraction(5**2, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
        )
    )
    denominator_increment = (
        Fraction(5**2 + 1, 24) * exponential_majorant
        + (
            Fraction(5**2, 24)
            * Fraction(1, 24)
            * exponential_majorant**2
            * delta**2
        )
    )
    coefficient_majorant = Fraction(6**2 + 5**2 + 1, 24)
    second_order_majorant = Fraction(16)
    if not (
        Fraction(1, 1 - Fraction(6, 2_000_000))
        < exponential_majorant
        and numerator_remainder < 1
        and denominator_remainder < 1
        and denominator_increment < 2
        and 2
        * (
            Fraction(1)
            + Fraction(1)
            + coefficient_majorant * Fraction(2)
        )
        < second_order_majorant
    ):
        raise RuntimeError("small-period Taylor majorant check failed")
    if not (
        abs(linear) < 6
        and beta > 1
        and beta < 5
        and argument > arb(1) / 5
        and beta + 1 - argument > arb(1) / 5
    ):
        raise RuntimeError("small-period analytic hypotheses failed")

    zero_value = (
        linear * (linear**2 - beta**2 - 1) / (24 * beta)
    )
    zero_remainder = second_order_majorant * delta**3 / 3
    near_value = zero_value * arb_fraction(delta)
    near_value += arb(0, arb_fraction(zero_remainder).upper())

    near_function = near_integrand(argument, beta)
    segment_left = delta
    near_panels = 0
    while segment_left < 1:
        segment_right = min(Fraction(1), 4 * segment_left)
        segment = certified_simpson(
            near_function,
            segment_left,
            segment_right,
            tolerance * (segment_right - segment_left) / 8,
        )
        near_value += segment.value
        near_panels += segment.panels
        segment_left = segment_right

    cutoff = Fraction(24)
    tail = certified_simpson(
        tail_integrand(argument, beta),
        Fraction(0),
        cutoff,
        tolerance / 4,
    )
    # For v>=24 and z>0, v/z+1>1.  The first four positive
    # terms of exp(1) exceed 8/3, hence exp(-1)<3/8.  Both
    # exponential denominator factors have magnitude >5/8;
    # their product exceeds 25/64 and v+z>24.  The difference
    # of the two terms is therefore <1/4.
    exp_one_partial = sum(
        Fraction(1, product(range(1, index + 1)))
        for index in range(5)
    )
    if not exp_one_partial > Fraction(8, 3):
        raise RuntimeError("tail exponential majorant check failed")
    tail_remainder = (-arb_fraction(cutoff)).exp() / 4
    tail_value = tail.value + arb(0, tail_remainder.upper())
    boundary = -linear / beta
    return near_value + boundary + tail_value, near_panels + tail.panels


def class_log_value(
    class_log: int,
    sqrt_57: arb,
    tolerance: Fraction,
) -> tuple[arb, int, list[tuple[tuple[int, int], ...]]]:
    fan = regular_fan(CONE_MATRICES[class_log])
    if len(fan) != 10:
        raise RuntimeError("expected nine regular subcones")
    y_minus = (1 - sqrt_57) / 2
    y_plus = (1 + sqrt_57) / 2
    lattice = B_LATTICES[class_log]
    shift = AFFINE_SHIFTS[class_log]
    result = arb(0)
    panels = 0
    physical_points = set()
    records = []
    for index in range(len(fan) - 1):
        first, second = fan[index], fan[index + 1]
        x_value, y_value = affine_coordinates(first, second, shift)
        physical_point = (
            first[0] * x_value + second[0] * y_value,
            first[1] * x_value + second[1] * y_value,
        )
        if physical_point in physical_points:
            raise RuntimeError("half-open fan double-counted a boundary")
        physical_points.add(physical_point)

        first_minus = embedded_element(lattice, first, y_minus)
        second_minus = embedded_element(lattice, second, y_minus)
        first_plus = embedded_element(lattice, first, y_plus)
        second_plus = embedded_element(lattice, second, y_plus)
        if not (
            first_minus > 0
            and second_minus > 0
            and first_plus > 0
            and second_plus > 0
        ):
            raise RuntimeError("fan ray left the totally positive cone")
        beta = second_minus / first_minus
        if beta < 1:
            beta = 1 / beta
            x_value, y_value = y_value, x_value
        argument = arb_fraction(x_value) + arb_fraction(y_value) * beta
        value, used = fundamental_log_double_sine(
            argument, beta, tolerance / 9
        )
        result += value
        panels += used
        records.append((first, second, x_value, y_value))
    return 2 * result, panels, records


def voutier_lower_bound() -> arb:
    bounds = []
    for degree in range(3, 25):
        degree_ball = arb(degree)
        bounds.append(
            (degree_ball.log().log() / degree_ball.log()) ** 3
            / (4 * degree)
        )
    return arb(min(bound.lower() for bound in bounds))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=90)
    parser.add_argument("--tolerance", default="1e-10")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    ctx.dps = arguments.digits
    ctx.cap = 6
    sqrt_57 = arb(57).sqrt()

    polynomial = fmpz_poly([
        1, -69, 1377, -6694, 7590, -15594, 10791,
        -15594, 7590, -6694, 1377, -69, 1,
    ])
    real_roots = [
        root.real
        for root, multiplicity in polynomial.complex_roots()
        if multiplicity == 1 and root.imag.contains(0)
    ]
    if len(real_roots) != 6:
        raise RuntimeError("candidate polynomial real-root count changed")
    windows = [
        (Fraction(5709, 1000), Fraction(5710, 1000)),
        (Fraction(28, 1000), Fraction(29, 1000)),
        (Fraction(35, 1000), Fraction(36, 1000)),
        (Fraction(175, 1000), Fraction(176, 1000)),
        (Fraction(34732, 1000), Fraction(34733, 1000)),
        (Fraction(27792, 1000), Fraction(27793, 1000)),
    ]
    candidates = []
    for left, right in windows:
        selected = [
            root
            for root in real_roots
            if root > arb_fraction(left) and root < arb_fraction(right)
        ]
        if len(selected) != 1:
            raise RuntimeError(
                f"isolating window [{left},{right}] selected {len(selected)}"
            )
        candidates.append(selected[0])

    analytic_logs = []
    total_panels = 0
    for class_log in range(3):
        value, panels, records = class_log_value(
            class_log, sqrt_57, tolerance
        )
        analytic_logs.append(value)
        total_panels += panels
        print(f"CLASS_{class_log}_REGULAR_SUBCONES={len(records)}")
        print(f"CLASS_{class_log}_FAN_RECORDS={records}")
    analytic_logs.extend([-value for value in analytic_logs[:3]])

    maximum_difference = arb(0)
    for class_log, (analytic, candidate) in enumerate(
        zip(analytic_logs, candidates, strict=True)
    ):
        algebraic = candidate.log()
        difference = analytic - algebraic
        if not difference.contains(0):
            raise RuntimeError(
                f"class {class_log}: analytic and algebraic balls disjoint: "
                f"{difference}"
            )
        maximum_difference = max(
            maximum_difference, arb(abs(difference).upper())
        )
        print(f"CLASS_{class_log}_ANALYTIC_LOG={analytic}")
        print(f"CLASS_{class_log}_ALGEBRAIC_ROOT={candidate}")
        print(f"CLASS_{class_log}_LOG_DIFFERENCE={difference}")

    powered_height_upper = SAFE_EXPONENT * maximum_difference
    voutier_lower = voutier_lower_bound()
    margin = voutier_lower / powered_height_upper
    quadratic_fallback = ((1 + arb(5).sqrt()) / 2).log() / 2
    if not (
        margin > 100
        and quadratic_fallback > powered_height_upper
    ):
        raise RuntimeError("height-rigidity margin did not clear")

    print("FUNDAMENTAL_CONE_DETERMINANT=80")
    print("REGULAR_FAN_SUBCONES_PER_CLASS=9")
    print("REGULAR_FAN_EACH_DETERMINANT=1")
    print(f"TOTAL_SIMPSON_PANELS={total_panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"POWERED_HEIGHT_UPPER={powered_height_upper}")
    print(f"VOUTIER_DEGREE_3_TO_24_LOWER={voutier_lower}")
    print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={quadratic_fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("RQ57_NORM27_ANALYTIC_ARB_CERTIFIED=1")
    print("RQ57_NORM27_PACKET_IDENTITY_VERIFIED=1")


if __name__ == "__main__":
    main()
