#!/usr/bin/env python3
"""Freeze every supported order-six character kernel in the H stratum."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "w1-full-census-v1.json"
EXPECTED_SHA256 = (
    "b656a587bea705e8efe817e2870a0ea86cbf2c10fa37c7d9aa03d3868dfa76f1"
)


def character_order(character: tuple[int, ...], cyc: tuple[int, ...]) -> int:
    order = 1
    for value, modulus in zip(character, cyc, strict=True):
        order = math.lcm(order, modulus // math.gcd(value, modulus))
    return order


def is_supported(
    character: tuple[int, ...],
    cyc: tuple[int, ...],
    sign_log: tuple[int, ...],
) -> bool:
    pairing = sum(
        (
            Fraction(value * sign, modulus)
            for value, sign, modulus in zip(
                character, sign_log, cyc, strict=True
            )
        ),
        Fraction(),
    )
    return pairing.denominator != 1


def inverse(
    character: tuple[int, ...], cyc: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(
        (-value) % modulus
        for value, modulus in zip(character, cyc, strict=True)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SHA256:
        raise RuntimeError("W1 census hash changed")
    source = json.loads(SOURCE.read_text())
    records = []
    relevant_rows = 0
    supported_characters = 0
    for row in source["records"]:
        if 6 not in row["support_orders"]:
            continue
        relevant_rows += 1
        cyc = tuple(row["one_cyc"])
        sign_log = tuple(row["sign_log"])
        characters = [
            character
            for character in itertools.product(
                *(range(modulus) for modulus in cyc)
            )
            if character_order(character, cyc) == 6
            and is_supported(character, cyc, sign_log)
        ]
        representatives = sorted(
            {min(character, inverse(character, cyc)) for character in characters}
        )
        if 2 * len(representatives) != len(characters):
            raise RuntimeError(
                f"{row['case_id']}: inverse pairing failed"
            )
        supported_characters += len(characters)
        for index, character in enumerate(representatives, start=1):
            records.append(
                {
                    "case_id": row["case_id"],
                    "kernel_index": index,
                    "d": row["d"],
                    "finite_ideal_hnf": row["finite_ideal_hnf"],
                    "one_cyc": row["one_cyc"],
                    "sign_log": row["sign_log"],
                    "source_character": list(character),
                    "inverse_character": list(inverse(character, cyc)),
                }
            )
    result = {
        "schema": "effective-stark-roblot-sextic-kernel-inventory-v1",
        "status": "FROZEN_BEFORE_SEXTIC_FIELD_EXTRACTION",
        "claim_tag": "OBSERVED",
        "selection": {
            "row_rule": "6 in support_orders",
            "character_rule": (
                "exact order 6 and nonintegral pairing with sign_log"
            ),
            "kernel_equivalence": "character and inverse character only",
        },
        "counts": {
            "source_rows": len(source["records"]),
            "relevant_rows": relevant_rows,
            "supported_order_six_characters": supported_characters,
            "inverse_pair_kernels": len(records),
        },
        "records": records,
        "source": {
            "path": "artifacts/w1-full-census-v1.json",
            "sha256": EXPECTED_SHA256,
        },
        "primary_reference_boundary": {
            "theorem": "Roblot 2013, Theorem 7.1",
            "requires_S_equal_S_of_extension": True,
            "requires_class_number_prime_to_3": True,
            "requires_no_wild_prime_above_3": True,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
