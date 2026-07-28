#!/usr/bin/env python3
"""Exact character-theoretic audit of the d=6 orientation obstruction.

The one-place ray group is C6=<g>.  Kopp's difference 1-g^3 has
character support k=1,3,5.  Rational character data can separate the
quadratic character k=3 from the primitive orbit {1,5}, but it cannot
distinguish k=1 from its complex conjugate k=5.  Equivalently, it is
invariant under reversing the Artin generator g <-> g^{-1}.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import cos, gcd, pi


GROUP_ORDER = 6
SIGN_CLASS_LOG = 3


def character_order(exponent: int) -> int:
    if exponent == 0:
        return 1
    return GROUP_ORDER // gcd(exponent, GROUP_ORDER)


def main() -> None:
    support = [
        exponent
        for exponent in range(GROUP_ORDER)
        if (1 - (-1) ** exponent) != 0
    ]
    assert support == [1, 3, 5]

    # Gal(Q(zeta_6)/Q) acts on character exponents by k -> -k.
    conjugation_orbits = []
    unseen = set(support)
    while unseen:
        exponent = min(unseen)
        orbit = sorted({exponent, (-exponent) % GROUP_ORDER})
        conjugation_orbits.append(orbit)
        unseen.difference_update(orbit)
    assert conjugation_orbits == [[1, 5], [3]]

    # A labeled logarithm packet ell_a on ray classes g^a decomposes
    # into inversion-even and inversion-odd parts.  The odd part changes
    # sign when the Artin generator is reversed and is killed by every
    # inversion-invariant rational linear functional.
    generic_packet = [Fraction(index + 1) for index in range(GROUP_ORDER)]
    reversed_packet = [
        generic_packet[(-index) % GROUP_ORDER]
        for index in range(GROUP_ORDER)
    ]
    even_part = [
        (generic_packet[index] + generic_packet[-index]) / 2
        for index in range(GROUP_ORDER)
    ]
    odd_part = [
        (generic_packet[index] - generic_packet[-index]) / 2
        for index in range(GROUP_ORDER)
    ]
    reversed_even_part = [
        (reversed_packet[index] + reversed_packet[-index]) / 2
        for index in range(GROUP_ORDER)
    ]
    reversed_odd_part = [
        (reversed_packet[index] - reversed_packet[-index]) / 2
        for index in range(GROUP_ORDER)
    ]
    assert reversed_even_part == even_part
    assert reversed_odd_part == [-value for value in odd_part]
    assert any(value != 0 for value in odd_part)

    # Even after the quadratic component q and the absolute value rho of
    # the primitive regulator are fixed, a full circle of real logarithm
    # packets remains.  Fourier inversion gives
    #
    #   D_j(theta) = (2 rho cos(theta-j*pi/3)+(-1)^j q)/3.
    #
    # It satisfies D_(j+3)=-D_j for every theta.  Exponentiating therefore
    # gives positive reciprocal ray values for every theta, not merely for
    # the six Artin orientations of an algebraic unit.
    rho = 1
    quadratic_component = 2

    def ray_packet(angle: float) -> list[float]:
        return [
            (
                2 * rho * cos(angle - index * pi / 3)
                + (-1) ** index * quadratic_component
            )
            / 3
            for index in range(GROUP_ORDER)
        ]

    packet_zero = ray_packet(0)
    packet_generic = ray_packet(pi / 7)
    for packet in (packet_zero, packet_generic):
        assert all(
            abs(packet[index + 3] + packet[index]) < 1e-12
            for index in range(3)
        )
    assert any(
        abs(left - right) > 1e-6
        for left, right in zip(packet_zero, packet_generic)
    )

    # Subgroup norms and field polynomials depend only on unlabeled
    # Galois orbits, so inversion merely permutes their factors.
    subgroups = {
        "order_1": [0],
        "order_2": [0, 3],
        "order_3": [0, 2, 4],
        "order_6": [0, 1, 2, 3, 4, 5],
    }
    for subgroup in subgroups.values():
        assert sorted((-index) % GROUP_ORDER for index in subgroup) == subgroup

    records = [
        {
            "character_exponent": exponent,
            "character_order": character_order(exponent),
            "complex_conjugate_exponent": (-exponent) % GROUP_ORDER,
            "kopp_coefficient": 1 - (-1) ** exponent,
        }
        for exponent in support
    ]
    result = {
        "schema": "sic-stark-dimension-six-orientation-obstruction-v1",
        "ray_group": "C6=<g>",
        "sign_class": "R=g^3",
        "kopp_difference": "1-R",
        "supported_characters": records,
        "rational_character_orbits": conjugation_orbits,
        "artin_reversal": "g -> g^-1",
        "invariants_preserved_by_artin_reversal": [
            "the unlabeled ray-unit polynomial",
            "reciprocal pairing",
            "all subgroup norms",
            "rational sums of the primitive character pair {chi_1,chi_5}",
        ],
        "datum_changed_by_artin_reversal": (
            "the inversion-odd (or oriented) primitive character component"
        ),
        "continuous_ambiguity": {
            "fixed_data": [
                "quadratic component q",
                "primitive absolute value rho",
                "R-reciprocity D_(j+3)=-D_j",
                "positive reciprocal exponentials exp(D_j)",
            ],
            "remaining_parameter": "theta in R/(2*pi*Z)",
            "fourier_family": (
                "D_j(theta)=(2*rho*cos(theta-j*pi/3)+(-1)^j*q)/3"
            ),
            "consequence": (
                "Roblot-type absolute-value information leaves a continuous "
                "circle, not a finite set of Artin orientations."
            ),
        },
        "conclusion": (
            "Quadratic class-number formulas, Dedekind-zeta quotients, "
            "and subgroup norms cannot select the d=6 Artin orientation. "
            "A non-rational order-6 character invariant, an explicit "
            "reciprocity law, or a direct oriented double-sine evaluation "
            "is logically necessary."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
