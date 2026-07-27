#!/usr/bin/env python3
"""Audit character support for the d=6 Kopp partial-zeta difference."""

from __future__ import annotations

import json
from math import gcd


def main() -> None:
    group_order = 6
    sign_class_log = 3
    characters = []
    for exponent in range(group_order):
        character_order = (
            1 if exponent == 0 else group_order // gcd(exponent, group_order)
        )
        value_on_sign_class = 1 if exponent % 2 == 0 else -1
        coefficient = 1 - value_on_sign_class
        characters.append(
            {
                "character_exponent": exponent,
                "character_order": character_order,
                "value_on_sign_class": value_on_sign_class,
                "fourier_coefficient_for_1_minus_R": coefficient,
                "occurs_in_kopp_difference": coefficient != 0,
            }
        )

    support = [
        entry["character_exponent"]
        for entry in characters
        if entry["occurs_in_kopp_difference"]
    ]
    orders = [
        entry["character_order"]
        for entry in characters
        if entry["occurs_in_kopp_difference"]
    ]
    quadratic = next(
        entry for entry in characters if entry["character_order"] == 2
    )
    result = {
        "schema": "sic-stark-dimension-six-character-support-v1",
        "ray_group": "C6",
        "generator_symbol": "g",
        "sign_class": f"R=g^{sign_class_log}",
        "kopp_group_ring_element": "(1-R)[A]",
        "character_convention": "chi_k(g)=exp(2*pi*i*k/6)",
        "characters": characters,
        "support_exponents": support,
        "orders_on_support": orders,
        "unique_quadratic_character_exponent": 3,
        "unique_quadratic_character_coefficient": quadratic[
            "fourier_coefficient_for_1_minus_R"
        ],
        "quadratic_component_occurs": True,
        "nonquadratic_component_occurs": True,
        "conclusion": (
            "The d=6 Kopp difference has a mixed packet: k=3 is "
            "quadratic, while k=1 and k=5 have order 6. The quadratic "
            "class-number route can evaluate only one component; it "
            "cannot determine the two primitive order-6 components."
        ),
    }
    assert support == [1, 3, 5]
    assert orders == [6, 2, 6]
    assert quadratic["fourier_coefficient_for_1_minus_R"] == 2
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
