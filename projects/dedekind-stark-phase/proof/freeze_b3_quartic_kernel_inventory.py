#!/usr/bin/env python3
"""Freeze every supported order-four character kernel without phase data."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT.parent
    / "effective-stark-sweep"
    / "artifacts"
    / "w1-full-census-v1.json"
)
EXPECTED_FILE_SHA256 = (
    "b656a587bea705e8efe817e2870a0ea86cbf2c10fa37c7d9aa03d3868dfa76f1"
)
EXPECTED_SOURCE_CENSUS_SHA256 = (
    "9fa0f1880ca0c2d263e0235bd4ed83e8e6001b88bfede0927a7197f46f7d4563"
)
EXPECTED_SCREEN_SOURCE_SHA256 = (
    "4ee9d907c9a3d601c5f0346e8e8f7f2ddec725170e7a061b153cbc69fc9b2683"
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
        start=Fraction(),
    )
    return pairing.denominator != 1


def inverse(
    character: tuple[int, ...], cyc: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(
        (-value) % modulus
        for value, modulus in zip(character, cyc, strict=True)
    )


def kernels_for(row: dict) -> tuple[list[tuple[int, ...]], int]:
    cyc = tuple(row["one_cyc"])
    sign_log = tuple(row["sign_log"])
    supported = []
    for character in itertools.product(*(range(modulus) for modulus in cyc)):
        if character_order(character, cyc) == 4 and is_supported(
            character, cyc, sign_log
        ):
            supported.append(character)
    representatives = sorted(
        {min(character, inverse(character, cyc)) for character in supported}
    )
    if 2 * len(representatives) != len(supported):
        raise RuntimeError(
            f"{row['case_id']}: inverse pairing did not partition characters"
        )
    return representatives, len(supported)


def build_inventory() -> dict:
    source_bytes = SOURCE.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    if source_sha256 != EXPECTED_FILE_SHA256:
        raise RuntimeError(f"source file changed: {source_sha256}")
    source = json.loads(source_bytes)
    if source["source_census_sha256"] != EXPECTED_SOURCE_CENSUS_SHA256:
        raise RuntimeError("source census hash changed")
    if source["screen_source_sha256"] != EXPECTED_SCREEN_SOURCE_SHA256:
        raise RuntimeError("W1 screen hash changed")

    records = []
    relevant_row_count = 0
    supported_character_count = 0
    metadata_crosscheck_count = 0
    for row in source["records"]:
        if 4 not in row["support_orders"]:
            continue
        relevant_row_count += 1
        representatives, character_count = kernels_for(row)
        if not representatives:
            raise RuntimeError(
                f"{row['case_id']}: metadata claims order four without a kernel"
            )
        if row["max_support_order"] == 4:
            metadata_crosscheck_count += 1
            if character_count != row["c_quartic_count"]:
                raise RuntimeError(
                    f"{row['case_id']}: W1 quartic count mismatch"
                )
        supported_character_count += character_count
        for index, representative in enumerate(representatives, start=1):
            records.append(
                {
                    "case_id": row["case_id"],
                    "kernel_index": index,
                    "d": row["d"],
                    "finite_ideal_hnf": row["finite_ideal_hnf"],
                    "one_cyc": row["one_cyc"],
                    "sign_log": row["sign_log"],
                    "source_character": list(representative),
                    "inverse_character": list(
                        inverse(representative, tuple(row["one_cyc"]))
                    ),
                }
            )

    if relevant_row_count != 1512:
        raise RuntimeError(f"relevant row count changed: {relevant_row_count}")
    if supported_character_count != 4490:
        raise RuntimeError(
            f"supported character count changed: {supported_character_count}"
        )
    if len(records) != 2245:
        raise RuntimeError(f"kernel count changed: {len(records)}")

    return {
        "schema": "dedekind-stark-b3-quartic-kernel-inventory-v1",
        "claim_tag": "OBSERVED",
        "status": "FROZEN_BEFORE_FIELD_AND_PHASE_EVALUATION",
        "independence_wall": {
            "selection_uses_only_w1_group_and_sign_metadata": True,
            "engine_c_geometry_read": False,
            "lprime_or_phase_artifact_read": False,
        },
        "source": {
            "path": "../effective-stark-sweep/artifacts/w1-full-census-v1.json",
            "file_sha256": EXPECTED_FILE_SHA256,
            "source_census_sha256": EXPECTED_SOURCE_CENSUS_SHA256,
            "screen_source_sha256": EXPECTED_SCREEN_SOURCE_SHA256,
        },
        "selection": {
            "row_rule": "4 in support_orders",
            "character_rule": (
                "exact order 4 and nonintegral pairing with sign_log"
            ),
            "kernel_equivalence": "character and inverse character only",
        },
        "counts": {
            "source_rows": len(source["records"]),
            "relevant_rows": relevant_row_count,
            "supported_order_four_characters": supported_character_count,
            "inverse_pair_kernels": len(records),
            "w1_quartic_count_crosschecked_rows": metadata_crosscheck_count,
        },
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(build_inventory(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
