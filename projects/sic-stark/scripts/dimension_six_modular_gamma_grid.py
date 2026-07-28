#!/usr/bin/env python3
"""Exact lattice geometry of the 36 d=6 modular-gamma samples.

For d=6, write omega_2=1 and omega_1=beta^3.  The general modular
gamma dictionary gives

    (mu,h) = (1,-1) + a*(0,-4) + b*(D,1),
    D = 4*beta-1 = (omega_1-omega_2)/6.

Thus the AFK characteristic grid is not merely a sparse set of points:
it is an affine (Z/6)^2 quotient inside R x Z/24.  Its two closure
relations are exactly

    6*(0,-4) = (0,-24),
    6*(D,1)  = (omega_1-omega_2,6)
               = (omega_1,5) - (omega_2,-1),

where the vectors on the right are the two functional-equation shifts
of the general modular gamma function.

The reflection (mu,h)->(omega_1+omega_2-mu,-h), used in the primitive
two-gamma kernel, acts on characteristics by (a,b)->(1-a,-b).
"""

from __future__ import annotations

from fractions import Fraction
import json


DIMENSION = 6
DISCRETE_LEVEL = 24

# Continuous coordinates are coefficients in the basis (omega_1,omega_2).
Continuous = tuple[Fraction, Fraction]
CylinderPoint = tuple[Continuous, int]

ORIGIN: CylinderPoint = ((Fraction(0), Fraction(1)), -1)
A_STEP: CylinderPoint = ((Fraction(0), Fraction(0)), -4)
B_STEP: CylinderPoint = (
    (Fraction(1, 6), Fraction(-1, 6)),
    1,
)
OMEGA_ONE_SHIFT: CylinderPoint = (
    (Fraction(1), Fraction(0)),
    5,
)
OMEGA_TWO_SHIFT: CylinderPoint = (
    (Fraction(0), Fraction(1)),
    -1,
)


def point_add(left: CylinderPoint, right: CylinderPoint) -> CylinderPoint:
    return (
        (
            left[0][0] + right[0][0],
            left[0][1] + right[0][1],
        ),
        left[1] + right[1],
    )


def point_scale(scalar: int, point: CylinderPoint) -> CylinderPoint:
    return (
        (scalar * point[0][0], scalar * point[0][1]),
        scalar * point[1],
    )


def point_subtract(
    left: CylinderPoint,
    right: CylinderPoint,
) -> CylinderPoint:
    return point_add(left, point_scale(-1, right))


def characteristic_point(first: int, second: int) -> CylinderPoint:
    return point_add(
        ORIGIN,
        point_add(
            point_scale(first, A_STEP),
            point_scale(second, B_STEP),
        ),
    )


def reduce_characteristic(first: int, second: int) -> tuple[int, int]:
    return first % DIMENSION, second % DIMENSION


def reflection(point: CylinderPoint) -> CylinderPoint:
    # Q=omega_1+omega_2; the discrete reflection in the primitive
    # quotient is h -> -h.
    return (
        (
            Fraction(1) - point[0][0],
            Fraction(1) - point[0][1],
        ),
        -point[1],
    )


def equivalent_mod_functional_lattice(
    left: CylinderPoint,
    right: CylinderPoint,
) -> dict[str, int] | None:
    """Solve left-right=x*(omega1,5)+y*(omega2,-1)+(0,24z)."""

    difference = point_subtract(left, right)
    x = difference[0][0]
    y = difference[0][1]
    if x.denominator != 1 or y.denominator != 1:
        return None
    x_int = x.numerator
    y_int = y.numerator
    residual_h = difference[1] - (5 * x_int - y_int)
    if residual_h % DISCRETE_LEVEL:
        return None
    return {
        "omega_one_shift_count": x_int,
        "omega_two_shift_count": y_int,
        "pure_period_count": residual_h // DISCRETE_LEVEL,
    }


def serialize_point(point: CylinderPoint) -> dict[str, object]:
    return {
        "continuous_coefficients_omega1_omega2": [
            str(point[0][0]),
            str(point[0][1]),
        ],
        "discrete_coordinate": point[1],
        "discrete_coordinate_mod_24": point[1] % DISCRETE_LEVEL,
    }


def main() -> None:
    six_a = point_scale(DIMENSION, A_STEP)
    six_b = point_scale(DIMENSION, B_STEP)
    assert six_a == ((Fraction(0), Fraction(0)), -24)
    assert six_b == point_subtract(OMEGA_ONE_SHIFT, OMEGA_TWO_SHIFT)

    records = []
    reduced_points: set[tuple[Fraction, Fraction, int]] = set()
    reflection_records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            point = characteristic_point(first, second)
            # In the fundamental b-range, the continuous coordinate is
            # injective in b and h then recovers a.
            key = (point[0][0], point[0][1], point[1] % DISCRETE_LEVEL)
            assert key not in reduced_points
            reduced_points.add(key)
            records.append(
                {
                    "characteristic": [first, second],
                    "point": serialize_point(point),
                }
            )

            reflected = reflection(point)
            target_characteristic = reduce_characteristic(
                1 - first,
                -second,
            )
            target = characteristic_point(*target_characteristic)
            equivalence = equivalent_mod_functional_lattice(
                reflected,
                target,
            )
            assert equivalence is not None
            reflection_records.append(
                {
                    "source": [first, second],
                    "target": list(target_characteristic),
                    "functional_lattice_correction": equivalence,
                }
            )
    assert len(reduced_points) == DIMENSION * DIMENSION

    # The primitive quotient changes a to a-1 at fixed b.  Its reflected
    # second factor consequently has the label (1-a,-b), explaining the
    # affine shift in the two-gamma kernel rather than plain negation.
    assert all(
        tuple(record["target"])
        == reduce_characteristic(
            1 - record["source"][0],
            -record["source"][1],
        )
        for record in reflection_records
    )

    result = {
        "schema": "sic-stark-dimension-six-modular-gamma-grid-v1",
        "period_basis": ["omega_1=beta^3", "omega_2=1"],
        "D_identity": "D=4*beta-1=(omega_1-omega_2)/6",
        "affine_origin": serialize_point(ORIGIN),
        "a_step": serialize_point(A_STEP),
        "b_step": serialize_point(B_STEP),
        "closure_relations": {
            "six_a_steps": serialize_point(six_a),
            "six_b_steps": serialize_point(six_b),
            "six_b_steps_equal_functional_shift_difference": True,
        },
        "sample_count": len(records),
        "sample_records": records,
        "reflection_on_characteristics": "(a,b)->(1-a,-b) mod 6",
        "reflection_records": reflection_records,
        "primitive_two_gamma_kernel_lives_on_same_affine_grid": True,
        "conclusion": (
            "The 36 AFK samples form an exact affine (Z/6)^2 quotient "
            "of the modular-gamma cylinder by its functional-equation "
            "lattice.  The reflection used in the primitive quotient "
            "closes on this grid as (a,b)->(1-a,-b).  This supplies the "
            "missing geometric reason a finite Zak transform of the "
            "published general-modular beta convolution could produce "
            "the TCC sum."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
