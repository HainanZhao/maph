#!/usr/bin/env python3
"""Exact local-ray screen for the canonical SIC--Stark order family.

For d >= 5, let

    O_d = Z[beta],  beta^2-(d-1)beta+1=0.

The script computes the kernel of the one-place ray group modulo d over
the order class group:

    ((O_d/d O_d)^x x {sign at infinity_2}) / image(O_d^x).

The mathematical certificate recorded in the output proves that its
exponent is greater than two for every d >= 5.  The finite enumeration
for 5 <= d <= 40 is an independent exact audit of the general argument.
"""

from __future__ import annotations

from collections import Counter
from math import gcd
import json


FIRST_DIMENSION = 5
LAST_AUDITED_DIMENSION = 40
SCALAR_EXPONENT_TWO_MODULI = {1, 2, 3, 4, 6, 8, 12, 24}
EXCEPTIONAL_WITNESSES = {
    6: ((1, 3), 1),
    8: ((1, 2), 0),
    12: ((1, 3), 0),
    24: ((1, 3), 0),
}


class LocalRayQuotient:
    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self.one = (1 % dimension, 0)
        self.beta = (0, 1 % dimension)
        self.negative_one = ((-1) % dimension, 0)

    def multiply(
        self,
        left: tuple[int, int],
        right: tuple[int, int],
    ) -> tuple[int, int]:
        d = self.dimension
        a, b = left
        c, e = right
        return (
            (a * c - b * e) % d,
            (a * e + b * c + (d - 1) * b * e) % d,
        )

    def norm(self, value: tuple[int, int]) -> int:
        d = self.dimension
        a, b = value
        return (a * a + (d - 1) * a * b + b * b) % d

    def ring_units(self) -> list[tuple[int, int]]:
        d = self.dimension
        return [
            (a, b)
            for a in range(d)
            for b in range(d)
            if gcd(self.norm((a, b)), d) == 1
        ]

    def product_multiply(
        self,
        left: tuple[tuple[int, int], int],
        right: tuple[tuple[int, int], int],
    ) -> tuple[tuple[int, int], int]:
        return (
            self.multiply(left[0], right[0]),
            (left[1] + right[1]) % 2,
        )

    def product_power(
        self,
        value: tuple[tuple[int, int], int],
        exponent: int,
    ) -> tuple[tuple[int, int], int]:
        result = (self.one, 0)
        while exponent:
            if exponent & 1:
                result = self.product_multiply(result, value)
            value = self.product_multiply(value, value)
            exponent //= 2
        return result

    def global_unit_image(self) -> set[tuple[tuple[int, int], int]]:
        # For d >= 5, O_d^x=<-1,beta>.  The unit beta is totally
        # positive and has exact order three modulo d; -1 is negative at
        # the labeled real place.
        return {
            self.product_multiply(
                self.product_power((self.beta, 0), beta_exponent),
                self.product_power(
                    (self.negative_one, 1),
                    sign_exponent,
                ),
            )
            for beta_exponent in range(3)
            for sign_exponent in range(2)
        }

    def quotient_data(self) -> dict[str, object]:
        units = self.ring_units()
        unit_image = self.global_unit_image()
        assert len(unit_image) == 6
        ambient = [
            (unit, sign)
            for unit in units
            for sign in range(2)
        ]
        seen: set[tuple[tuple[int, int], int]] = set()
        representatives: list[tuple[tuple[int, int], int]] = []
        orders: list[int] = []
        for value in ambient:
            if value in seen:
                continue
            coset = {
                self.product_multiply(value, image)
                for image in unit_image
            }
            seen.update(coset)
            representatives.append(value)
            for exponent in range(1, 4 * self.dimension**2 + 1):
                if self.product_power(value, exponent) in unit_image:
                    orders.append(exponent)
                    break
            else:
                raise AssertionError("quotient order bound exceeded")

        sign_class = (self.negative_one, 0)
        assert sign_class not in unit_image
        assert self.product_power(sign_class, 2) in unit_image

        witness = None
        if self.dimension in EXCEPTIONAL_WITNESSES:
            witness = EXCEPTIONAL_WITNESSES[self.dimension]
        else:
            for scalar in range(2, self.dimension):
                if gcd(scalar, self.dimension) != 1:
                    continue
                value = ((scalar, 0), 0)
                for exponent in range(1, self.dimension + 1):
                    if self.product_power(value, exponent) in unit_image:
                        if exponent > 2:
                            witness = value
                        break
                if witness is not None:
                    break
        assert witness is not None

        witness_order = None
        for exponent in range(1, 4 * self.dimension**2 + 1):
            if self.product_power(witness, exponent) in unit_image:
                witness_order = exponent
                break
        assert witness_order is not None and witness_order > 2

        distribution = Counter(orders)
        return {
            "dimension": self.dimension,
            "residue_unit_group_order": len(units),
            "local_one_place_ray_kernel_order": len(representatives),
            "local_one_place_ray_kernel_exponent": max(orders),
            "element_order_distribution": {
                str(order): count
                for order, count in sorted(distribution.items())
            },
            "nonquadratic_witness": {
                "residue": list(witness[0]),
                "sign": witness[1],
                "quotient_order": witness_order,
            },
            "sign_class_nontrivial": True,
        }


def main() -> None:
    records = [
        LocalRayQuotient(dimension).quotient_data()
        for dimension in range(FIRST_DIMENSION, LAST_AUDITED_DIMENSION + 1)
    ]
    assert all(
        record["local_one_place_ray_kernel_exponent"] > 2
        for record in records
    )

    result = {
        "schema": "sic-stark-canonical-order-character-obstruction-v1",
        "audited_dimension_range": [
            FIRST_DIMENSION,
            LAST_AUDITED_DIMENSION,
        ],
        "order_family": (
            "O_d=Z[beta_d], beta_d^2-(d-1)*beta_d+1=0"
        ),
        "unit_theorem": (
            "For d>=5, O_d^x=<-1,beta_d>; beta_d is the smallest "
            "unit greater than one and is totally positive."
        ),
        "mod_d_relation": "beta_d^2+beta_d+1=0, hence beta_d^3=1",
        "scalar_argument": {
            "statement": (
                "If d is not in {6,8,12,24}, the scalar subgroup "
                "(Z/dZ)^x has exponent greater than two and embeds "
                "with the same element orders in the local ray quotient."
            ),
            "all_moduli_with_scalar_unit_exponent_at_most_two": sorted(
                SCALAR_EXPONENT_TWO_MODULI
            ),
        },
        "exceptional_moduli": {
            str(dimension): {
                "witness_residue": list(witness[0]),
                "witness_sign": witness[1],
            }
            for dimension, witness in EXCEPTIONAL_WITNESSES.items()
        },
        "family_conclusion": (
            "For every canonical dimension d>=5, the local one-place "
            "ray kernel has exponent greater than two.  Since Kopp's "
            "sign class is nontrivial, the Fourier support of 1-R "
            "contains a nonquadratic character.  Thus d=4 is the unique "
            "canonical dimension whose full principal Kopp packet can "
            "be entirely quadratic."
        ),
        "finite_audit": records,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
