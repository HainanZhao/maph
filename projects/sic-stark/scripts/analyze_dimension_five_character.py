#!/usr/bin/env python3
"""Audit the character support of the d=5 Kopp partial-zeta difference."""

from __future__ import annotations

import json
from math import gcd


def main() -> None:
    group_order = 8
    sign_class_log = 4
    characters = []
    for exponent in range(group_order):
        character_order = (
            1 if exponent == 0 else group_order // gcd(exponent, group_order)
        )
        value_on_sign_class = 1 if exponent % 2 == 0 else -1
        fourier_coefficient_at_identity_class = 1 - value_on_sign_class
        characters.append(
            {
                "character_exponent": exponent,
                "character_order": character_order,
                "value_on_sign_class": value_on_sign_class,
                "fourier_coefficient_for_1_minus_R": (
                    fourier_coefficient_at_identity_class
                ),
                "occurs_in_kopp_difference": (
                    fourier_coefficient_at_identity_class != 0
                ),
            }
        )

    support = [
        entry["character_exponent"]
        for entry in characters
        if entry["occurs_in_kopp_difference"]
    ]
    orders_on_support = [
        entry["character_order"]
        for entry in characters
        if entry["occurs_in_kopp_difference"]
    ]
    quadratic = next(
        entry for entry in characters if entry["character_order"] == 2
    )
    result = {
        "schema": "sic-stark-dimension-five-character-support-v1",
        "ray_group": "C8",
        "generator_symbol": "g",
        "sign_class": "R=g^4",
        "kopp_group_ring_element": "(1-R)[A]",
        "character_convention": "chi_k(g)=exp(2*pi*i*k/8)",
        "characters": characters,
        "support_exponents": support,
        "orders_on_support": orders_on_support,
        "unique_quadratic_character_exponent": 4,
        "unique_quadratic_character_coefficient": quadratic[
            "fourier_coefficient_for_1_minus_R"
        ],
        "factors_through_quadratic_quotient": False,
        "all_supporting_characters_have_order_eight": (
            set(orders_on_support) == {8}
        ),
        "conclusion": (
            "The Kopp difference is supported on k=1,3,5,7, all of "
            "order 8. The unique quadratic character k=4 is killed by "
            "1-R, so the d=4 quadratic-L-function shortcut cannot apply."
        ),
    }
    assert support == [1, 3, 5, 7]
    assert set(orders_on_support) == {8}
    assert quadratic["fourier_coefficient_for_1_minus_R"] == 0
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
