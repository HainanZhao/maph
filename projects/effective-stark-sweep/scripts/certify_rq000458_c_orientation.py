#!/usr/bin/env python3
"""Independent Arb orientation certificate for RQ-000458 Engine C.

The analytic target is recomputed from immutable cone input during this
run; no Engine-B transcript or enclosure is read.  Stark 1980 supplies
an actual global unit because |S|=3.  Here e=4, so the coefficient for
ordinary complex modulus is 2/e=1/2.  The Arb lattice inversion isolates
the Stark-unit coordinate orbit

    {(-8,4), (0,-4), (8,-4), (0,4)}

in the exact anti-unit basis.  Each coordinate is divisible by four;
the distinguished fourth root has coordinates (-2,1), whose exact
normal-closure norm is audited separately.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import acb, arb, ctx, fmpq, fmpz_poly

# This imports code, not data: class values are recomputed from scratch.
# In particular this script never parses the Engine-B certificate.
from certify_rq000458_b_packet import class_log_value


def evaluate(coefficients, argument: acb) -> acb:
    value = acb(0)
    for coefficient in reversed(coefficients):
        value = value * argument + coefficient
    return value


def logarithmic_matrix(
    units: list[list[fmpq | int]],
    automorphism: list[fmpq | int],
    root: acb,
) -> list[list[arb]]:
    sigma_root = evaluate(automorphism, root)
    return [
        [abs(evaluate(unit, root)).log() for unit in units],
        [abs(evaluate(unit, sigma_root)).log() for unit in units],
    ]


def solve_two_by_two(
    matrix: list[list[arb]],
    target: tuple[arb, arb],
) -> tuple[arb, arb]:
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return (
        (
            target[0] * matrix[1][1]
            - target[1] * matrix[0][1]
        )
        / determinant,
        (
            matrix[0][0] * target[1]
            - matrix[1][0] * target[0]
        )
        / determinant,
    )


def contained_near(
    value: arb,
    integer: int,
    radius: Fraction,
) -> bool:
    width = arb(radius.numerator) / radius.denominator
    return value > arb(integer) - width and value < arb(integer) + width


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=90)
    parser.add_argument("--tolerance", default="1e-10")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    ctx.dps = arguments.digits
    ctx.cap = 16
    beta = 15 + 4 * arb(14).sqrt()

    full_logs = []
    total_panels = 0
    for class_code in range(8):
        value, panels, points = class_log_value(
            class_code, beta, tolerance
        )
        full_logs.append(value)
        total_panels += panels
        print(
            f"C_ORIENTATION_CLASS_{class_code}_"
            f"RECOMPUTED_LOG={value} POINTS={points}"
        )

    projected = [
        (full_logs[first] - full_logs[first + 4]) / 2
        for first in range(4)
    ]
    oriented_l = (
        projected[0] - projected[2],
        projected[1] - projected[3],
    )
    print(
        "ORIENTED_SOURCE_L_DERIVATIVE="
        f"{oriented_l[0]} + ({oriented_l[1]})*I"
    )

    denominator = 957457
    polynomial = [
        58, 184, 152, -152, 106, -28, 20, -4, 1
    ]
    anti_units = [
        [
            fmpq(302693, denominator),
            fmpq(-293908, denominator),
            fmpq(239566, denominator),
            fmpq(-319720, denominator),
            fmpq(7839, denominator),
            fmpq(-55323, denominator),
            fmpq(4141, denominator),
            fmpq(-2541, denominator),
        ],
        [
            fmpq(1792057, denominator),
            fmpq(6168940, denominator),
            fmpq(6324638, denominator),
            fmpq(-3450078, denominator),
            fmpq(734596, denominator),
            fmpq(-776302, denominator),
            fmpq(165149, denominator),
            fmpq(-49778, denominator),
        ],
    ]
    sigma = [
        fmpq(-3246442, denominator),
        fmpq(-5560415, denominator),
        fmpq(4318845, denominator),
        fmpq(-3299196, denominator),
        fmpq(849281, denominator),
        fmpq(-590202, denominator),
        fmpq(113399, denominator),
        fmpq(-28455, denominator),
    ]
    roots = [
        root
        for root, multiplicity in fmpz_poly(polynomial).complex_roots()
        if multiplicity == 1 and root.imag > 0
    ]
    if len(roots) != 4:
        raise RuntimeError("character field needs four upper roots")

    # Stark's coefficient is 2/e=1/2.  Therefore the logarithmic
    # coordinates of epsilon are 2*L in this Artin convention.
    target = (2 * oriented_l[0], 2 * oriented_l[1])
    expected_orbit = {(-8, 4), (0, -4), (8, -4), (0, 4)}
    isolation_radius = Fraction(1, 1000)
    isolated = set()
    for root_index, root in enumerate(roots):
        matrix = logarithmic_matrix(anti_units, sigma, root)
        coordinates = solve_two_by_two(matrix, target)
        matches = [
            candidate
            for candidate in expected_orbit
            if contained_near(
                coordinates[0], candidate[0], isolation_radius
            )
            and contained_near(
                coordinates[1], candidate[1], isolation_radius
            )
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"root {root_index}: coordinate match count {len(matches)} "
                f"for {coordinates}"
            )
        isolated.add(matches[0])
        print(
            f"ROOT_{root_index}_STARK_UNIT_COORDINATES={coordinates} "
            f"ISOLATED_AS={matches[0]}"
        )
    if isolated != expected_orbit:
        raise RuntimeError(f"incomplete coordinate orbit: {isolated}")

    print("CASE_ID=RQ-000458")
    print("ENGINE=C")
    print("CM_BASE=Q(sqrt(-42))")
    print("STARK_S_SIZE=3")
    print("GLOBAL_UNIT_CLAUSE_APPLIES=1")
    print("ROOT_OF_UNITY_COUNT_E=4")
    print("ORDINARY_MODULUS_COEFFICIENT=1/2")
    print("STARK_UNIT_COORDINATE_ORBIT=[(-8,4),(0,-4),(8,-4),(0,4)]")
    print("DISTINGUISHED_FOURTH_ROOT_COORDINATES=(-2,1)")
    print(f"TOTAL_RECOMPUTED_TAYLOR_PANELS={total_panels}")
    print("NO_ENGINE_B_TRANSCRIPT_READ=1")
    print("RQ000458_ENGINE_C_ARB_ORIENTATION_CERTIFIED=1")
    print("CLAIM_TAG=VERIFIED")


if __name__ == "__main__":
    main()
