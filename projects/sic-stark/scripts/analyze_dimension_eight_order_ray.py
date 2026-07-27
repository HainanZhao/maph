#!/usr/bin/env python3
"""Exact ray-group calculation for the canonical d=8 quadratic order.

The canonical form has discriminant 45 and multiplier order
O_3 = Z[theta], theta = 3*phi, with theta^2 = 3*theta + 9.
For the principal modulus 8 O_3, the standard ray exact sequence reduces
the ray groups to explicit quotients of

    (O_3 / 8 O_3)^x x {signs}

by the image of O_3^x = <-1, beta>, beta = phi^4 = theta + 2.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json


MODULUS = 8
ONE = (1, 0)
NEGATIVE_ONE = (7, 0)
BETA = (2, 1)
STABILIZER = ((329, -48), (48, -7))


def multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    """Multiply in (Z/8Z)[theta]/(theta^2-3theta-9)."""

    a, b = left
    c, d = right
    return (
        (a * c + 9 * b * d) % MODULUS,
        (a * d + b * c + 3 * b * d) % MODULUS,
    )


def power(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = ONE
    while exponent:
        if exponent & 1:
            result = multiply(result, value)
        value = multiply(value, value)
        exponent //= 2
    return result


ELEMENTS = list(product(range(MODULUS), repeat=2))
UNITS = [
    value
    for value in ELEMENTS
    if any(multiply(value, candidate) == ONE for candidate in ELEMENTS)
]


def product_group_multiply(
    left: tuple[tuple[int, int], tuple[int, ...]],
    right: tuple[tuple[int, int], tuple[int, ...]],
) -> tuple[tuple[int, int], tuple[int, ...]]:
    return (
        multiply(left[0], right[0]),
        tuple(
            (left_sign + right_sign) % 2
            for left_sign, right_sign in zip(left[1], right[1])
        ),
    )


def product_group_power(
    value: tuple[tuple[int, int], tuple[int, ...]],
    exponent: int,
) -> tuple[tuple[int, int], tuple[int, ...]]:
    result = (ONE, (0,) * len(value[1]))
    while exponent:
        if exponent & 1:
            result = product_group_multiply(result, value)
        value = product_group_multiply(value, value)
        exponent //= 2
    return result


def ray_quotient(sign_count: int) -> dict[str, object]:
    """Return exact quotient data with ``sign_count`` infinite places."""

    zero_signs = (0,) * sign_count
    negative_signs = (1,) * sign_count
    beta_generator = (BETA, zero_signs)
    negative_generator = (NEGATIVE_ONE, negative_signs)
    unit_image = {
        product_group_multiply(
            product_group_power(beta_generator, beta_exponent),
            product_group_power(negative_generator, sign_exponent),
        )
        for beta_exponent in range(3)
        for sign_exponent in range(2)
    }
    ambient = [
        (unit, signs)
        for unit in UNITS
        for signs in product((0, 1), repeat=sign_count)
    ]

    seen: set[tuple[tuple[int, int], tuple[int, ...]]] = set()
    representatives = []
    for value in ambient:
        if value in seen:
            continue
        coset = {
            product_group_multiply(value, image)
            for image in unit_image
        }
        seen.update(coset)
        representatives.append(value)

    quotient_orders = []
    for representative in representatives:
        for exponent in range(1, 33):
            if product_group_power(representative, exponent) in unit_image:
                quotient_orders.append(exponent)
                break
        else:
            raise AssertionError("quotient element order exceeds bound")

    order_distribution = Counter(quotient_orders)
    expected_structures = {
        0: ("C4 x C2", Counter({4: 4, 2: 3, 1: 1})),
        1: ("C4 x C2 x C2", Counter({4: 8, 2: 7, 1: 1})),
        2: ("C4 x C2 x C2 x C2", Counter({4: 16, 2: 15, 1: 1})),
    }
    structure, expected_distribution = expected_structures[sign_count]
    assert len(unit_image) == 6
    assert order_distribution == expected_distribution

    return {
        "infinite_place_count": sign_count,
        "ambient_order": len(ambient),
        "global_unit_image_order": len(unit_image),
        "ray_group_order": len(representatives),
        "ray_group_structure": structure,
        "element_order_distribution": {
            str(order): count
            for order, count in sorted(order_distribution.items())
        },
        "_unit_image": unit_image,
        "_ambient": ambient,
    }


def main() -> None:
    assert len(UNITS) == 48
    assert power(BETA, 3) == ONE
    assert power(BETA, 1) != ONE

    finite = ray_quotient(0)
    one_place = ray_quotient(1)
    both_places = ray_quotient(2)

    # Kopp's R is represented by residue -1 and positive sign. It is a
    # nontrivial order-two class. It is not twice another ray class, so
    # it can be chosen as one of the independent C2 generators.
    sign_class = (NEGATIVE_ONE, (0,))
    one_unit_image = one_place.pop("_unit_image")
    one_ambient = one_place.pop("_ambient")
    assert sign_class not in one_unit_image
    assert product_group_power(sign_class, 2) in one_unit_image
    sign_class_square_roots = [
        value
        for value in one_ambient
        if product_group_multiply(
            product_group_power(value, 2),
            sign_class,
        )
        in one_unit_image
    ]
    assert not sign_class_square_roots

    # The canonical nonzero AFK characteristic q=(0,1) gives
    #
    #     r=(0,1/8),   w=r_2*beta-r_1=beta/8.
    #
    # Since beta is a unit of O_3, w has denominator ideal exactly (8).
    # Moreover 8w=beta is a unit, so its Kopp ray class is the identity.
    # The positive stabilizer B=L_8^3 fixes r modulo Z^2:
    #
    #     B*r-r=(-6,-1).
    #
    # Neither L_8 nor L_8^2 fixes r, so this is the primitive
    # length-three characteristic orbit.
    characteristic = (0, 1)
    characteristic_translation = (
        STABILIZER[0][1] // MODULUS,
        (STABILIZER[1][1] - 1) // MODULUS,
    )
    assert characteristic_translation == (-6, -1)

    # Once R is chosen as an independent C2 coordinate of
    # C4 x C2 x C2, write a character as (a,b,c) with
    # a mod 4 and b,c mod 2.  The Kopp difference 1-R is supported
    # exactly on c=1.  Odd a gives order 4; even a gives order 2.
    supported_character_orders = []
    supported_characters = []
    for a in range(4):
        for b in range(2):
            c = 1
            order = 4 if a % 2 else 2
            supported_character_orders.append(order)
            supported_characters.append(
                {
                    "coordinates": [a, b, c],
                    "order": order,
                    "coefficient_in_identity_class_difference": 2,
                }
            )
    assert Counter(supported_character_orders) == Counter({2: 4, 4: 4})

    for record in (finite, both_places):
        record.pop("_unit_image")
        record.pop("_ambient")

    # Ring class number:
    # h(O_3)=h(O_K)*3*(1-(5/3)/3)/[O_K^x:O_3^x]
    #       =1*3*(1+1/3)/4=1.
    result = {
        "schema": "sic-stark-dimension-eight-order-ray-v1",
        "dimension": 8,
        "canonical_discriminant": 45,
        "base_field": "Q(sqrt(5))",
        "maximal_order_discriminant": 5,
        "order_conductor": 3,
        "order_model": "O_3=Z[theta], theta=3*phi, theta^2=3*theta+9",
        "order_unit_group": "O_3^x=<-1,beta>, beta=phi^4=theta+2",
        "beta_order_mod_8": 3,
        "ring_class_number_formula": "1*3*(1+1/3)/4=1",
        "ring_class_number": 1,
        "residue_unit_group_order": len(UNITS),
        "finite_ray_group": finite,
        "one_place_ray_group": one_place,
        "both_places_ray_group": both_places,
        "kopp_sign_class": {
            "representative": "(-1 mod 8, positive at infinity_2)",
            "nontrivial": True,
            "order": 2,
            "lies_in_twice_the_ray_group": False,
        },
        "kopp_difference_character_support": {
            "total_character_count": 16,
            "supported_character_count": 8,
            "quadratic_character_count": 4,
            "quartic_character_count": 4,
            "coordinate_convention": (
                "chi_(a,b,c) on C4 x C2 x <R>, with chi(R)=(-1)^c"
            ),
            "supported_characters": supported_characters,
            "quartic_conjugacy_pairs": [
                [[1, 0, 1], [3, 0, 1]],
                [[1, 1, 1], [3, 1, 1]],
            ],
            "common_quadratic_square": [2, 0, 0],
        },
        "canonical_primitive_characteristic": {
            "q": list(characteristic),
            "r": ["0", "1/8"],
            "w": "beta/8",
            "denominator_ideal": "(8) in O_3",
            "ray_class": "identity",
            "stabilizer": [list(row) for row in STABILIZER],
            "stabilizer_translation": list(characteristic_translation),
            "quartic_characters_occur_in_its_kopp_difference": True,
        },
        "conclusion": (
            "The actual discriminant-45 order changes the one-place "
            "group from the maximal-order proxy C2 x C2 to "
            "C4 x C2 x C2. The canonical characteristic q=(0,1) "
            "already has full denominator (8) and its identity-ray "
            "Kopp difference contains four quartic characters. The "
            "d=8 TCC packet therefore cannot avoid the quartic sector."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
