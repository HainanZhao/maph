#!/usr/bin/env python3
"""Generate the exact primitive characteristic/ray-class table for d=8.

The multiplier order is

    O_3=Z[theta], theta^2=3 theta+9, beta=theta+2,

and the one-place ray group modulo 8 is C4 x C2 x C2.  For a
characteristic q=(a,b), the Kopp element is

    8(r_2 beta-r_1)=b beta-a=(2b-a)+b theta.

It is coprime to 8 exactly when a^2-7ab+b^2 is odd.  The script labels
the resulting principal ray class and verifies that the 48 primitive
characteristics form sixteen Zauner orbits mapping bijectively to the
sixteen ray classes.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json

import analyze_dimension_eight_order_ray as order_ray


MODULUS = 8


def main() -> None:
    quotient = order_ray.ray_quotient(1)
    unit_image = quotient["_unit_image"]
    ambient = quotient["_ambient"]

    def multiply(left, right):
        return order_ray.product_group_multiply(left, right)

    def power(value, exponent):
        return order_ray.product_group_power(value, exponent)

    def coset(value):
        return frozenset(
            multiply(value, image)
            for image in unit_image
        )

    classes = []
    for value in ambient:
        value_coset = coset(value)
        if value_coset not in classes:
            classes.append(value_coset)
    classes.sort(key=min)
    assert len(classes) == 16

    def class_index(value):
        return classes.index(coset(value))

    def quotient_order(value):
        for exponent in range(1, 65):
            if power(value, exponent) in unit_image:
                return exponent
        raise AssertionError("quotient order exceeds bound")

    sign_class = (order_ray.NEGATIVE_ONE, (0,))
    generator_4 = min(
        value for value in ambient
        if quotient_order(value) == 4
    )
    generated_by_4_and_sign = {
        class_index(
            multiply(
                power(generator_4, exponent_4),
                power(sign_class, exponent_sign),
            )
        )
        for exponent_4 in range(4)
        for exponent_sign in range(2)
    }
    generator_2 = min(
        value for value in ambient
        if quotient_order(value) == 2
        and class_index(value) not in generated_by_4_and_sign
    )

    coordinate_by_class = {
        class_index(
            multiply(
                multiply(
                    power(generator_4, exponent_4),
                    power(generator_2, exponent_2),
                ),
                power(sign_class, exponent_sign),
            )
        ): (exponent_4, exponent_2, exponent_sign)
        for exponent_4 in range(4)
        for exponent_2 in range(2)
        for exponent_sign in range(2)
    }
    assert len(coordinate_by_class) == 16

    def zauner(characteristic):
        first, second = characteristic
        return (
            (7 * first - second) % MODULUS,
            first % MODULUS,
        )

    records = []
    primitive_class_counts: Counter[tuple[int, int, int]] = Counter()
    for first, second in product(range(MODULUS), repeat=2):
        norm = (
            first * first
            - 7 * first * second
            + second * second
        )
        primitive = norm % 2 == 1
        record: dict[str, object] = {
            "characteristic": [first, second],
            "norm_of_b_beta_minus_a": norm,
            "denominator_stratum": "(8)" if primitive else "proper divisor of (8)",
            "primitive": primitive,
        }
        if primitive:
            # b beta-a=(2b-a)+b theta.  We choose its representative
            # positive at infinity_2, so the sign coordinate is zero
            # before quotienting by global units.
            residue = (
                (2 * second - first) % MODULUS,
                second,
            )
            coordinates = coordinate_by_class[
                class_index((residue, (0,)))
            ]
            primitive_class_counts[coordinates] += 1
            first_image = zauner((first, second))
            second_image = zauner(first_image)
            record.update(
                {
                    "principal_generator_residue_theta_basis": list(
                        residue
                    ),
                    "ray_coordinates_C4_C2_sign": list(coordinates),
                    "zauner_orbit": [
                        [first, second],
                        list(first_image),
                        list(second_image),
                    ],
                }
            )
        records.append(record)

    primitive_records = [
        record for record in records
        if record["primitive"]
    ]
    assert len(primitive_records) == 48
    assert len(primitive_class_counts) == 16
    assert set(primitive_class_counts.values()) == {3}

    record_by_characteristic = {
        tuple(record["characteristic"]): record
        for record in primitive_records
    }
    for record in primitive_records:
        coordinates = record["ray_coordinates_C4_C2_sign"]
        assert all(
            record_by_characteristic[tuple(characteristic)][
                "ray_coordinates_C4_C2_sign"
            ]
            == coordinates
            for characteristic in record["zauner_orbit"]
        )

    orbit_representatives = sorted(
        {
            min(tuple(point) for point in record["zauner_orbit"])
            for record in primitive_records
        }
    )
    assert len(orbit_representatives) == 16

    result = {
        "schema": "sic-stark-dimension-eight-ray-table-v1",
        "dimension": 8,
        "order": "Z[theta], theta^2=3*theta+9",
        "beta": "theta+2",
        "one_place_ray_group": "C4 x C2 x <R>",
        "coordinate_generators": {
            "C4": [
                list(generator_4[0]),
                list(generator_4[1]),
            ],
            "C2": [
                list(generator_2[0]),
                list(generator_2[1]),
            ],
            "R": [
                list(sign_class[0]),
                list(sign_class[1]),
            ],
        },
        "primitive_characteristic_count": len(primitive_records),
        "primitive_zauner_orbit_count": len(orbit_representatives),
        "ray_class_count": len(primitive_class_counts),
        "multiplicity_per_ray_class": 3,
        "primitive_orbits_biject_with_ray_classes": True,
        "orbit_representatives": [
            list(representative)
            for representative in orbit_representatives
        ],
        "records": records,
        "conclusion": (
            "The 48 full-denominator d=8 characteristics form sixteen "
            "length-three Zauner orbits, and these orbits map "
            "bijectively to all classes of the order ray group "
            "C4 x C2 x C2.  Hence no restriction to the AFK primitive "
            "overlap packet removes the quartic character sector."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
