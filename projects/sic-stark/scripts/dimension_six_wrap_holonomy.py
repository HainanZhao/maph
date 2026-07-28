#!/usr/bin/env python3
"""AFK even-wrap holonomy for the d=6 primitive quotient.

AFK quasiperiodicity says, for nonzero characteristics p'=p+dq,

    nu(p') = tau_d^{<p',p>} nu(p),

where <p,q>=p_2 q_1-p_1 q_2 and tau_d^d=-1 for even d.  At d=6 the
vertical wrap (a,b)->(a,b+6) therefore gives

    nu(a,b+6)=(-1)^a nu(a,b).

Consequently R(a,b)=nu(a,b)/nu(a-1,b) has holonomy -1.  Its *primal*
helical periodization carries the weight (-1)^k.  Under Poisson/Zak
duality this shifts the dual lattice to half-integral characters; it
does not put an alternating weight on the dual alias index.  Thus this
calculation fixes the line-bundle convention but does not by itself
move the raw 2-psi-2 alias series onto Bailey's summable locus.
"""

from __future__ import annotations

import json
import math


DIMENSION = 6


def symplectic(pair_one: tuple[int, int], pair_two: tuple[int, int]) -> int:
    return pair_one[1] * pair_two[0] - pair_one[0] * pair_two[1]


def vertical_wrap_exponent(first_coordinate: int, second_coordinate: int) -> int:
    original = (first_coordinate, second_coordinate)
    wrapped = (first_coordinate, second_coordinate + DIMENSION)
    value = symplectic(wrapped, original)
    assert value == DIMENSION * first_coordinate
    return first_coordinate % 2


def primitive(pair: tuple[int, int]) -> bool:
    return math.gcd(pair[0], pair[1], DIMENSION) == 1


def symplectic_transporter(
    primitive_pair: tuple[int, int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return an SL(2,Z/6) matrix whose first column is primitive_pair."""

    first, second = primitive_pair
    for upper_right in range(DIMENSION):
        for lower_right in range(DIMENSION):
            determinant = (
                first * lower_right - upper_right * second
            ) % DIMENSION
            if determinant == 1:
                return (
                    (first % DIMENSION, upper_right),
                    (second % DIMENSION, lower_right),
                )
    raise AssertionError("primitive pair has no symplectic transporter")


def main() -> None:
    overlap_wrap_records = []
    quotient_wrap_records = []
    for first_coordinate in range(DIMENSION):
        for second_coordinate in range(DIMENSION):
            numerator_exponent = vertical_wrap_exponent(
                first_coordinate,
                second_coordinate,
            )
            denominator_exponent = vertical_wrap_exponent(
                first_coordinate - 1,
                second_coordinate,
            )
            quotient_exponent = (
                numerator_exponent - denominator_exponent
            ) % 2
            assert quotient_exponent == 1
            overlap_wrap_records.append(
                {
                    "a": first_coordinate,
                    "b": second_coordinate,
                    "nu_wrap_sign": (
                        "-1" if numerator_exponent else "+1"
                    ),
                }
            )
            quotient_wrap_records.append(
                {
                    "a": first_coordinate,
                    "b": second_coordinate,
                    "primitive_quotient_wrap_sign": "-1",
                }
            )

    primitive_pairs = [
        (first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
        if primitive((first, second))
    ]
    assert len(primitive_pairs) == 24
    transporters = []
    for pair in primitive_pairs:
        matrix = symplectic_transporter(pair)
        determinant = (
            matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]
        ) % DIMENSION
        assert determinant == 1
        assert (matrix[0][0], matrix[1][0]) == pair
        transporters.append(
            {
                "primitive_pair": list(pair),
                "SL2_transporter": [list(row) for row in matrix],
            }
        )

    result = {
        "schema": "sic-stark-dimension-six-wrap-holonomy-v1",
        "AFK_quasiperiodicity": (
            "nu(p+6q)=tau_6^<p+6q,p>*nu(p)"
        ),
        "vertical_overlap_wrap": "nu(a,b+6)=(-1)^a*nu(a,b)",
        "primitive_quotient": "R(a,b)=nu(a,b)/nu(a-1,b)",
        "primitive_quotient_wrap": "R(a,b+6)=-R(a,b)",
        "primal_helical_periodization_weight": "(-1)^k",
        "dual_effect": (
            "integer helical frequencies shift to Z+1/2; "
            "dual alias coefficients remain unweighted"
        ),
        "overlap_wrap_records": overlap_wrap_records,
        "quotient_wrap_records": quotient_wrap_records,
        "primitive_direction_count": len(primitive_pairs),
        "primitive_transporters": transporters,
        "all_primitive_directions_are_SL2_transports": True,
        "Bailey_alias_sign_gate_closed": False,
        "conclusion": (
            "AFK even-dimensional quasiperiodicity determines the "
            "antiperiodic line bundle exactly.  Fourier duality turns "
            "this into a half-character shift, not an alternating dual "
            "alias weight, so the remaining raw 2-psi-2 value stays at "
            "argument -q."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
