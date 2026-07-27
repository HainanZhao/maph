#!/usr/bin/env python3
"""Generate the convention and ray-label audit for dimension five."""

from __future__ import annotations

import json
from fractions import Fraction


# The raw PARI cyclic basis writes the prime above 3 as g^5.
PARI_CLASS_LOGS = [
    [None, 0, 6, 2, 4],
    [4, 3, 1, 3, 0],
    [2, 1, 1, 6, 7],
    [6, 3, 2, 5, 5],
    [0, 4, 7, 5, 7],
]

# Multiplication by 5 (its own inverse modulo 8) converts those entries
# to coordinates in the generator given by the prime above 3.
CLASS_LOGS = [
    [None if value is None else (5 * value) % 8 for value in row]
    for row in PARI_CLASS_LOGS
]

# A ray log determines the positive square root of its conjectural Stark
# value.  Logs separated by the sign class 4 are reciprocal.
RAY_SQUARE_ROOTS = {
    0: "x",
    1: "w",
    2: "y^-1",
    3: "z",
    4: "x^-1",
    5: "w^-1",
    6: "y",
    7: "z^-1",
}


def text(value: Fraction) -> str:
    value %= 1
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def signed_ray_square_root(ray_log: int, sign: int) -> str:
    value = RAY_SQUARE_ROOTS[ray_log]
    return value if sign == 1 else f"-{value}"


def main() -> None:
    # B=[[a,b],[c,d]], beta'=2-sqrt(3).
    a, b, c, d = 56, -15, 15, -4
    beta_conjugate = 2 - 3**0.5
    records = []
    for first in range(5):
        for second in range(5):
            if first == second == 0:
                records.append(
                    {
                        "characteristic": [0, 0],
                        "identity_weyl_coefficient": "1",
                        "reconstruction_table_entry": "sqrt(6)",
                        "note": (
                            "This is not AFK's auxiliary zero-"
                            "characteristic cocycle value."
                        ),
                    }
                )
                continue

            positive_lift = first
            while second * beta_conjugate - positive_lift <= 0:
                positive_lift -= 5
            r1 = Fraction(positive_lift, 5)
            r2 = Fraction(second, 5)
            theta_exponent = Fraction(
                (c - d + 1) * r1
                + (-a + b + 1) * r2
                - c * d * r1 * r1
                + 2 * (a - 1) * d * r1 * r2
                - (a - 2) * b * r2 * r2,
                2,
            ) % 1
            form_value = (
                first * first - 4 * first * second + second * second
            )
            expected_theta = Fraction(form_value, 5) % 1
            multiplier_exponent = (
                -Fraction(1, 4) - theta_exponent
            ) % 1
            phase_square_exponent = (
                -Fraction(1, 4) - Fraction(form_value, 5)
            ) % 1
            third = (-first - second) % 5
            sign_exponent = (
                5 * (first + second)
                + first * second
                + min(5, first + second)
            )
            overlap_sign = -1 if sign_exponent % 2 else 1
            ray_log = CLASS_LOGS[first][second]
            records.append(
                {
                    "characteristic": [first, second],
                    "positive_kopp_lift": [positive_lift, second],
                    "positive_at_infinity_2": True,
                    "ray_class_log_in_C8": ray_log,
                    "sign_class_partner_log": (
                        ray_log + 4
                    )
                    % 8,
                    "third_residue": third,
                    "triple_double_sine_sign_exponent": sign_exponent,
                    "triple_double_sine_sign": overlap_sign,
                    "double_sine_arguments": [
                        [5 - first, second],
                        [5 - third, first],
                        [5 - second, third],
                    ],
                    "argument_encoding": (
                        "(constant + beta_coefficient*beta)/5"
                    ),
                    "positive_square_root_from_ray_log": (
                        RAY_SQUARE_ROOTS[ray_log]
                    ),
                    "overlap": signed_ray_square_root(
                        ray_log, overlap_sign
                    ),
                    "quadratic_form_mod_5": form_value % 5,
                    "theta_character_exponent_mod_1": text(
                        theta_exponent
                    ),
                    "expected_Q_over_5_mod_1": text(expected_theta),
                    "kopp_multiplier_exponent_mod_1": text(
                        multiplier_exponent
                    ),
                    "afk_phase_square_exponent_mod_1": text(
                        phase_square_exponent
                    ),
                    "multiplier_matches_phase_square": (
                        multiplier_exponent == phase_square_exponent
                    ),
                }
            )

    assert all(
        record.get("multiplier_matches_phase_square", True)
        for record in records
    )
    record_by_characteristic = {
        tuple(record["characteristic"]): record for record in records
    }
    derived_table = []
    for first in range(5):
        row = []
        for second in range(5):
            record = record_by_characteristic[(first, second)]
            row.append(
                record.get(
                    "overlap", record.get("reconstruction_table_entry")
                )
            )
        derived_table.append(row)
    certificate = {
        "schema": "sic-stark-dimension-five-bridge-v2",
        "dimension": 5,
        "base_field": "Q(sqrt(3))",
        "beta": "2+sqrt(3)",
        "modulus": "(5) infinity_2",
        "ray_group": "C8",
        "ray_generator": "prime above 3",
        "raw_pari_prime_above_3_log": 5,
        "raw_pari_to_ray_generator_multiplier": 5,
        "both_infinite_places_ray_group": "C8 x C2",
        "sign_class_log": 4,
        "characteristic_stabilizer": [[56, -15], [15, -4]],
        "rademacher_invariant": 3,
        "eta_character_square": "i",
        "kopp_exponent": 1,
        "ray_log_to_positive_square_root": RAY_SQUARE_ROOTS,
        "derived_reconstruction_table": derived_table,
        "records": records,
        "all_24_nonexceptional_multipliers_match": True,
    }
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
