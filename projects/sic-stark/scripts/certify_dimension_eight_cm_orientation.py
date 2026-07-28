#!/usr/bin/env python3
"""Rigorous Arb isolation of the two dimension-eight CM Stark units.

Stark's theorem over an imaginary quadratic base supplies an actual unit
whose logarithmic resolvent is the oriented L-derivative.  This script
does not reprove that theorem.  It certifies that, with the exact Artin
labels and normalizations audited by the GP scripts, its anti-unit
coordinates are forced to be the orbit of (0, 2). Thus the unit can be
taken to be the square of PARI's third certified fundamental unit.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import acb, arb, ctx, fmpq, fmpz_poly

from certify_dimension_eight_lower_conductor import overlap_log


def evaluate(coefficients, argument: acb) -> acb:
    value = acb(0)
    for coefficient in reversed(coefficients):
        value = value * argument + coefficient
    return value


def logarithmic_matrix(
    fundamental_units: list[list[fmpq | int]],
    automorphism: list[fmpq | int],
    root: acb,
) -> list[list[arb]]:
    sigma_root = evaluate(automorphism, root)
    return [
        [abs(evaluate(unit, root)).log() for unit in fundamental_units],
        [
            abs(evaluate(unit, sigma_root)).log()
            for unit in fundamental_units
        ],
    ]


def solve_two_by_two(
    matrix: list[list[arb]], target: tuple[arb, arb]
) -> tuple[arb, arb]:
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    first = (
        target[0] * matrix[1][1]
        - target[1] * matrix[0][1]
    ) / determinant
    second = (
        matrix[0][0] * target[1]
        - matrix[1][0] * target[0]
    ) / determinant
    return first, second


def contained_near(value: arb, integer: int, radius: Fraction) -> bool:
    lower = arb(integer) - arb(radius.numerator) / radius.denominator
    upper = arb(integer) + arb(radius.numerator) / radius.denominator
    return value > lower and value < upper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=35)
    parser.add_argument("--tolerance", default="1e-8")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = (7 + 3 * arb(5).sqrt()) / 2

    # Representatives for the quotient by the reciprocal involution
    # h=[2,0,1].  The exact labels are certified independently by
    # dimension_eight_artin_labels.gp.
    characteristics = [
        ((0, 0, 0), (0, 1)),
        ((0, 0, 1), (0, 3)),
        ((0, 1, 0), (4, 5)),
        ((0, 1, 1), (4, 7)),
        ((1, 0, 0), (1, 2)),
        ((1, 0, 1), (3, 6)),
        ((1, 1, 0), (1, 1)),
        ((1, 1, 1), (2, 3)),
    ]
    partial_zeta_differences: dict[tuple[int, int, int], arb] = {}
    total_panels = 0
    for ray_log, characteristic in characteristics:
        logarithm, panels = overlap_log(
            *characteristic, beta, tolerance
        )
        partial_zeta_differences[ray_log] = 2 * logarithm
        total_panels += panels

    # The order-ray characters corresponding to the maximal-order dual
    # labels [1,0,0] and [1,1,0] are (a,b,c)=(1,0,1) and (3,1,1):
    # maximal_dual_character(a,b,c)=[a-2b,b,c-a].  Fourier inversion uses
    # the conjugate order-character value, as in the exact packet
    # reconstruction audit.
    order_characters = [(1, 0), (3, 1)]
    targets: list[tuple[arb, arb]] = []
    for packet, (first_dual, second_dual) in enumerate(order_characters):
        real_part = arb(0)
        imaginary_part = arb(0)
        for (first, second, _third), value in (
            partial_zeta_differences.items()
        ):
            sign = -1 if second_dual * second % 2 else 1
            if first == 0:
                real_part += sign * value
            else:
                # conj(i^first_dual) is -i for first_dual=1 and
                # +i for first_dual=3.
                imaginary_part += (
                    -sign if first_dual == 1 else sign
                ) * value
        targets.append((real_part, imaginary_part))
        print(
            f"PACKET_{packet}_ORIENTED_L_DERIVATIVE="
            f"{real_part} + ({imaginary_part})*I"
        )

    packet_data = [
        {
            "real_polynomial": [
                9, 0, -18, 0, -30, 0, -6, 0, 1
            ],
            "real_unit": [
                1431,
                2531,
                1616,
                fmpq(8581, 3),
                fmpq(866, 3),
                511,
                fmpq(-152, 3),
                fmpq(-809, 9),
            ],
            "polynomial": [
                166, -168, -16, 48, 18, -12, -4, 0, 1
            ],
            "units": [
                [
                    fmpq(113429, 77319),
                    fmpq(-14702, 77319),
                    fmpq(-5494, 25773),
                    fmpq(-1667, 8591),
                    fmpq(701, 8591),
                    fmpq(278, 2343),
                    fmpq(3631, 77319),
                    fmpq(-391, 77319),
                ],
                [
                    fmpq(-86927, 25773),
                    fmpq(50810, 25773),
                    fmpq(16928, 8591),
                    fmpq(1983, 8591),
                    fmpq(-2952, 8591),
                    fmpq(-17, 781),
                    fmpq(1472, 25773),
                    fmpq(892, 25773),
                ],
            ],
            "automorphism": [
                fmpq(37564, 77319),
                fmpq(-140065, 77319),
                fmpq(-2907, 8591),
                fmpq(11500, 25773),
                fmpq(10733, 25773),
                fmpq(-7, 781),
                fmpq(-3373, 77319),
                fmpq(-2114, 77319),
            ],
            # The normalized complex-place absolute value is the square
            # of the ordinary modulus.  With e=2, Stark's formula is
            # therefore -log|g(epsilon)|_ord.  The analytic coordinate
            # target is half the formerly used squared-unit target.
            "log_target": lambda value: (
                value[0] / 2, value[1] / 2
            ),
        },
        {
            "real_polynomial": [
                9, 0, 18, 0, -30, 0, 6, 0, 1
            ],
            "real_unit": [
                -17,
                15,
                -40,
                fmpq(125, 3),
                46,
                fmpq(-103, 3),
                fmpq(16, 3),
                fmpq(-37, 9),
            ],
            "polynomial": [
                24, 96, 144, 96, 28, 8, 0, -4, 1
            ],
            "units": [
                [1, 1, 0, 0, 0, 0, 0, 0],
                [
                    fmpq(-173, 5),
                    fmpq(-493, 5),
                    fmpq(-434, 5),
                    -24,
                    fmpq(-77, 10),
                    fmpq(-13, 5),
                    fmpq(24, 5),
                    fmpq(-21, 20),
                ],
            ],
            "automorphism": [
                fmpq(-178, 5),
                fmpq(-493, 5),
                fmpq(-434, 5),
                -24,
                fmpq(-77, 10),
                fmpq(-13, 5),
                fmpq(24, 5),
                fmpq(-21, 20),
            ],
            "log_target": lambda value: (
                value[0] / 2, value[1] / 2
            ),
        },
    ]

    expected_orbit = {(0, 2), (-2, 0), (0, -2), (2, 0)}
    isolation_radius = Fraction(1, 1000)
    for packet, data in enumerate(packet_data):
        roots = fmpz_poly(data["polynomial"]).complex_roots()
        positive_roots = [
            root for root, multiplicity in roots
            if multiplicity == 1 and root.imag > 0
        ]
        if len(positive_roots) != 4:
            raise RuntimeError("CM field needs four upper-half-plane roots")

        logarithmic_target = data["log_target"](targets[packet])
        isolated_coordinates: set[tuple[int, int]] = set()
        for root_index, root in enumerate(positive_roots):
            matrix = logarithmic_matrix(
                data["units"], data["automorphism"], root
            )
            coordinates = solve_two_by_two(matrix, logarithmic_target)
            matches = [
                candidate for candidate in expected_orbit
                if contained_near(
                    coordinates[0], candidate[0], isolation_radius
                )
                and contained_near(
                    coordinates[1], candidate[1], isolation_radius
                )
            ]
            if len(matches) != 1:
                raise RuntimeError(
                    f"packet {packet}, root {root_index}: "
                    f"coordinate isolation count {len(matches)}"
                )
            isolated_coordinates.add(matches[0])
            print(
                f"PACKET_{packet}_ROOT_{root_index}_"
                f"UNIT_COORDINATES={coordinates} "
                f"ISOLATED_AS={matches[0]}"
            )

        if isolated_coordinates != expected_orbit:
            raise RuntimeError(
                f"packet {packet}: incomplete C4 coordinate orbit"
            )

        # Independently enclose the four real values of the original
        # Roblot unit.  Their logarithms must be exactly the signed real
        # and imaginary coordinates of the oriented derivative.  The
        # subsequent GP bridge proves the corresponding absolute-norm
        # identities exactly in the common normal closure.
        real_roots = [
            root for root, multiplicity in
            fmpz_poly(data["real_polynomial"]).complex_roots()
            if multiplicity == 1 and root.imag.contains(0)
        ]
        if len(real_roots) != 4:
            raise RuntimeError(
                "real-quadratic quartic field needs four real roots"
            )
        real_unit_logs = [
            abs(evaluate(data["real_unit"], root)).log()
            for root in real_roots
        ]
        expected_logs = [
            targets[packet][0],
            -targets[packet][0],
            targets[packet][1],
            -targets[packet][1],
        ]
        for expected in expected_logs:
            match_count = sum(
                (candidate - expected).contains(0)
                for candidate in real_unit_logs
            )
            if match_count != 1:
                raise RuntimeError(
                    f"packet {packet}: real-unit log match count "
                    f"{match_count}"
                )
        print(
            f"PACKET_{packet}_REAL_UNIT_LOG_ORBIT={real_unit_logs} "
            "ORIENTED_TARGET_MATCHED=1"
        )

    print(f"TOTAL_ARBITRARY_PRECISION_PANELS={total_panels}")
    print("CM_STARK_UNIT_COORDINATE_ORBITS_ISOLATED=1")
    print("DIMENSION_EIGHT_ORIENTED_CM_BRIDGE_CERTIFIED=1")


if __name__ == "__main__":
    main()
