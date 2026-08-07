#!/usr/bin/env python3
"""Exact recursive checks for the multi-spacer allocation theorem."""

from __future__ import annotations

import json
import random


def qint(length: int, step: int = 1) -> list[int]:
    out = [0] * (step * (length - 1) + 1)
    for exponent in range(0, len(out), step):
        out[exponent] = 1
    return out


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        if x:
            for j, y in enumerate(right):
                if y:
                    out[i + j] += x * y
    return out


def product(factors: list[list[int]]) -> list[int]:
    out = [1]
    for factor in factors:
        out = multiply(out, factor)
    return out


def add(left: list[int], right: list[int]) -> list[int]:
    out = [0] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
    return out


def symmetric_unimodal(poly: list[int]) -> bool:
    if poly != poly[::-1]:
        return False
    middle = (len(poly) - 1) // 2
    return all(poly[i] <= poly[i + 1] for i in range(middle))


def direct(lengths: list[int], b: list[int], r: list[int]) -> list[int]:
    return product(
        [*(qint(length) for length in lengths), *(qint(x, step) for x, step in zip(b, r))]
    )


def construct(
    lengths: list[int], b: list[int], r: list[int], allocation: list[list[int]]
) -> tuple[list[int], int]:
    if not b:
        result = product([qint(length) for length in lengths])
        assert symmetric_unimodal(result)
        return result, 0

    base_lengths = [
        length - r[0] * count for length, count in zip(lengths, allocation[0])
    ]
    assert min(base_lengths) >= 1
    current, steps = construct(base_lengths, b[1:], r[1:], allocation[1:])
    current_lengths = base_lengths[:]
    spacer = 1
    word = [i for i, count in enumerate(allocation[0]) for _ in range(count)]
    for selected in word:
        x = current_lengths[selected]
        correction_lengths = current_lengths[:]
        correction_lengths[selected] = x + r[0] * (spacer + 1)
        correction, nested_steps = construct(
            correction_lengths, b[1:], r[1:], allocation[1:]
        )
        translated = [0] * r[0] + current
        new_degree = len(current) - 1 + 2 * r[0]
        assert len(correction) - 1 == new_degree
        assert symmetric_unimodal(translated + [0] * r[0])
        assert symmetric_unimodal(correction)
        current = add(translated, correction)
        assert symmetric_unimodal(current)
        current_lengths[selected] += r[0]
        spacer += 1
        steps += nested_steps + 1
    assert current == direct(lengths, b, r)
    return current, steps


def main() -> None:
    rng = random.Random(20260807)
    rows = 0
    recursion_steps = 0
    for _ in range(400):
        k = rng.randint(1, 4)
        spacer_count = rng.randint(2, 4)
        r = [rng.randint(1, 6) for _ in range(spacer_count)]
        allocation = [
            [rng.randint(0, 2) for _ in range(k)] for _ in range(spacer_count)
        ]
        b = [1 + sum(row) for row in allocation]
        alpha = [rng.randint(1, 5) for _ in range(k)]
        lengths = [
            alpha[i] + sum(r[j] * allocation[j][i] for j in range(spacer_count))
            for i in range(k)
        ]
        recursive, steps = construct(lengths, b, r, allocation)
        assert recursive == direct(lengths, b, r)
        assert symmetric_unimodal(recursive)
        recursion_steps += steps
        rows += 1
    print(
        json.dumps(
            {
                "random_rows": rows,
                "recursion_steps": recursion_steps,
                "seed": 20260807,
                "spacers_max": 4,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
