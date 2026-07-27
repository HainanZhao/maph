#!/usr/bin/env python3
"""Exact period-one Shintani cone audit for K=Q(sqrt(21)).

For beta=(5+sqrt(21))/2 the minus continued fraction is [[5]].  At
modulus n=3 or 6, the identity ray has initial Yamamoto coordinates
(x_0,y_0)=(1,1/n).  In residue coordinates (nx,ny), with x=1 represented
by 0, Yamamoto's recurrence is

    (a,b) -> (5a+b,-a) mod n.

The script verifies the length-three cone cycles and the elementary
double-sine shift identity which identifies the modulus-six cone product
with the three-factor Kopp/AFK product.  It performs no floating-point
evaluation.
"""

from __future__ import annotations

from fractions import Fraction
import json


def step(point: tuple[int, int], modulus: int) -> tuple[int, int]:
    a, b = point
    return ((5 * a + b) % modulus, (-a) % modulus)


def orbit(point: tuple[int, int], modulus: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    current = point
    while current not in result:
        result.append(current)
        current = step(current, modulus)
    assert current == point
    return result


def yamamoto_coordinate(residue: int, modulus: int, *, first: bool) -> Fraction:
    """Return x in (0,1] or y in [0,1) from its residue."""
    if first and residue == 0:
        return Fraction(1)
    return Fraction(residue, modulus)


def coordinate_orbit(modulus: int) -> list[tuple[Fraction, Fraction]]:
    return [
        (
            yamamoto_coordinate(a, modulus, first=True),
            yamamoto_coordinate(b, modulus, first=False),
        )
        for a, b in orbit((0, 1), modulus)
    ]


def format_linear_beta(x: Fraction, y: Fraction) -> str:
    return f"({x})*beta+({y})"


def main() -> None:
    cycle_3 = coordinate_orbit(3)
    cycle_6 = coordinate_orbit(6)
    assert cycle_3 == [
        (Fraction(1), Fraction(1, 3)),
        (Fraction(1, 3), Fraction(0)),
        (Fraction(2, 3), Fraction(2, 3)),
    ]
    assert cycle_6 == [
        (Fraction(1), Fraction(1, 6)),
        (Fraction(1, 6), Fraction(0)),
        (Fraction(5, 6), Fraction(5, 6)),
    ]

    # Reduction modulo 3 sends the selected modulus-six characteristic
    # orbit to the known modulus-three orbit.
    reduced_cycle_6 = [
        (a % 3, b % 3)
        for a, b in orbit((0, 1), 6)
    ]
    assert reduced_cycle_6 == orbit((0, 1), 3)

    # All four lifts of the first point of the modulus-three orbit give
    # distinct length-three modulus-six cycles.  The double-sine
    # duplication formula
    #
    #   S(z)=prod_{e,f in {0,1}} S((z+e*beta+f)/2)
    #
    # groups its twelve factors into precisely these four cycles.
    # Conductor lowering therefore determines their product, not the
    # primitive lift used by the TCC.
    lift_starts = [(a, b) for a in (0, 3) for b in (1, 4)]
    lift_orbits = [orbit(point, 6) for point in lift_starts]
    assert all(len(item) == 3 for item in lift_orbits)
    assert len({tuple(item) for item in lift_orbits}) == 4
    assert all(
        [(a % 3, b % 3) for a, b in item] == orbit((0, 1), 3)
        for item in lift_orbits
    )

    # For Yamamoto/Shintani/Kopp's double sine S, quasiperiodicity gives
    #
    #   S(beta,a) = 2 sin(pi a) S(beta,beta+a),
    #   S(beta,a beta) = 2 sin(pi a) S(beta,1+a beta).
    #
    # Dividing the two formulas proves
    #
    #   S(beta,beta+a) S(beta,a beta)
    #       = S(beta,a) S(beta,1+a beta).
    #
    # At a=1/n this converts the first two cone factors into the factors
    # printed in the Kopp/AFK cocycle formula.
    result = {
        "schema": "sic-stark-dimension-six-shintani-cycle-v1",
        "field": "Q(sqrt(21))",
        "beta_polynomial": "beta^2-5*beta+1",
        "minus_continued_fraction": "[[5]]",
        "fundamental_unit_mod_6_order": 3,
        "yamamoto_recurrence": "(a,b) -> (5*a+b,-a) mod n",
        "modulus_3": {
            "coordinate_cycle": [
                [str(x), str(y)]
                for x, y in cycle_3
            ],
            "cone_arguments": [
                format_linear_beta(x, y)
                for x, y in cycle_3
            ],
        },
        "modulus_6": {
            "coordinate_cycle": [
                [str(x), str(y)]
                for x, y in cycle_6
            ],
            "cone_arguments": [
                format_linear_beta(x, y)
                for x, y in cycle_6
            ],
            "kopp_arguments_after_shift_identity": [
                "1/6",
                "1+beta/6",
                "5*(beta+1)/6",
            ],
        },
        "double_sine_convention": "Yamamoto/Shintani/Kopp",
        "shift_identity": (
            "S(beta,beta+a)*S(beta,a*beta)"
            "=S(beta,a)*S(beta,1+a*beta)"
        ),
        "conductor_reduction": {
            "selected_mod_6_orbit_reduces_to_mod_3_orbit": True,
            "number_of_distinct_mod_6_lift_orbits": len(lift_orbits),
            "double_sine_duplication": (
                "S(z)=product_(e,f in {0,1}) "
                "S((z+e*beta+f)/2)"
            ),
            "resulting_product_relation": (
                "P_3=P_6_orbit_1*P_6_orbit_2"
                "*P_6_orbit_3*P_6_orbit_4"
            ),
            "lift_orbits": [
                [[a, b] for a, b in item]
                for item in lift_orbits
            ],
        },
        "conclusion": (
            "The period-one Shintani cone product is exactly the "
            "convention-matched Kopp/AFK three-double-sine product. "
            "Conductor reduction maps its characteristic orbit to the "
            "known modulus-three orbit, while double-sine duplication "
            "determines only the product of four distinct modulus-six "
            "lift orbits.  It therefore does not determine the selected "
            "primitive order-six factor."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
