#!/usr/bin/env python3
"""Exact first-dip census in the conjectured one-spacer necessity regimes."""

from __future__ import annotations

import itertools
import json
import random


PARAMETER_LIMIT = 15
K_LIMIT = 5
R_LIMIT = 6
EXTENDED_B_LIMIT = 100
EXTENDED_GROUP_SAMPLE = 256


def multiply_by_bracket(coefficients: list[int], length: int) -> list[int]:
    result = []
    running = 0
    for index in range(len(coefficients) + length - 1):
        if index < len(coefficients):
            running += coefficients[index]
        if index >= length:
            running -= coefficients[index - length]
        result.append(running)
    return result


def ordinary_product(lengths: tuple[int, ...]) -> list[int]:
    coefficients = [1]
    for length in lengths:
        coefficients = multiply_by_bracket(coefficients, length)
    return coefficients


def add_spacer(ordinary: list[int], length: int, step: int) -> list[int]:
    result = [0] * (len(ordinary) + step * (length - 1))
    for spacer_index in range(length):
        offset = step * spacer_index
        for index, value in enumerate(ordinary):
            result[offset + index] += value
    return result


def naive_product(lengths: tuple[int, ...], b: int, r: int) -> list[int]:
    result = [1]
    for length, step in [*((length, 1) for length in lengths), (b, r)]:
        factor = [0] * (step * (length - 1) + 1)
        for index in range(length):
            factor[step * index] = 1
        out = [0] * (len(result) + len(factor) - 1)
        for i, x in enumerate(result):
            for j, y in enumerate(factor):
                out[i + j] += x * y
        result = out
    return result


def first_dip(coefficients: list[int]) -> tuple[int, int]:
    midpoint = (len(coefficients) - 1) // 2
    for index in range(1, midpoint + 1):
        if coefficients[index] < coefficients[index - 1]:
            return index, coefficients[index - 1] - coefficients[index]
    raise AssertionError("violating row had no dip")


def main() -> None:
    row_count = 0
    parameter_groups = 0
    first_dip_depth_min = None
    first_dip_depth_max = 0
    samples: list[tuple[tuple[int, ...], int, int, int, list[int]]] = []
    groups: list[tuple[tuple[int, ...], int, int]] = []

    for k in range(1, K_LIMIT + 1):
        for r in range(2, R_LIMIT + 1):
            if not (k <= 3 or r <= 3):
                continue
            for lengths in itertools.combinations_with_replacement(
                range(1, PARAMETER_LIMIT + 1), k
            ):
                if any(length % r == 0 for length in lengths):
                    continue
                threshold = 1 + sum(length // r for length in lengths)
                if threshold >= PARAMETER_LIMIT:
                    continue
                ordinary = ordinary_product(lengths)
                locations = set()
                for b in range(threshold + 1, PARAMETER_LIMIT + 1):
                    coefficients = add_spacer(ordinary, b, r)
                    location, depth = first_dip(coefficients)
                    locations.add(location)
                    first_dip_depth_min = depth if first_dip_depth_min is None else min(first_dip_depth_min, depth)
                    first_dip_depth_max = max(first_dip_depth_max, depth)
                    if len(samples) < 500:
                        samples.append((lengths, b, r, location, coefficients))
                    row_count += 1
                assert len(locations) == 1
                groups.append((lengths, r, next(iter(locations))))
                parameter_groups += 1

    rng = random.Random(20260807)
    crosscheck_rows = 100
    for lengths, b, r, location, coefficients in rng.sample(samples, crosscheck_rows):
        independently_built = naive_product(lengths, b, r)
        assert independently_built == coefficients
        assert first_dip(independently_built)[0] == location

    # Target the shallow-b limitation directly.  For a deterministic sample
    # of parameter groups, compute the endpoint b=100 by both the sliding-
    # window route and separately written direct polynomial multiplication.
    # This tests the position claim well beyond the census box without
    # changing the manuscript's stated box.
    extended_groups = rng.sample(groups, EXTENDED_GROUP_SAMPLE)
    for lengths, r, location in extended_groups:
        ordinary = ordinary_product(lengths)
        coefficients = add_spacer(ordinary, EXTENDED_B_LIMIT, r)
        independently_built = naive_product(lengths, EXTENDED_B_LIMIT, r)
        assert independently_built == coefficients
        assert first_dip(coefficients)[0] == location

    assert row_count == 33728
    assert parameter_groups == 4576
    print(
        json.dumps(
            {
                "crosscheck_rows": crosscheck_rows,
                "extended_b_endpoint": EXTENDED_B_LIMIT,
                "extended_b_groups": len(extended_groups),
                "first_dip_depth_max": first_dip_depth_max,
                "first_dip_depth_min": first_dip_depth_min,
                "first_dip_independent_of_b_groups": parameter_groups,
                "parameter_limit": PARAMETER_LIMIT,
                "regime": "k<=3 or r<=3, with k<=5 and r<=6",
                "status": "ALL_VIOLATING_ROWS_HAVE_B_INDEPENDENT_FIRST_DIP",
                "violating_rows": row_count,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
