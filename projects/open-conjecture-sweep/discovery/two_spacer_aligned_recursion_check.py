#!/usr/bin/env python3
"""Exact checks for the two-spacer aligned-center recursion."""

from __future__ import annotations

import itertools
import json
import random


def qint(length: int, step: int = 1) -> list[int]:
    assert length >= 1 and step >= 1
    out = [0] * (step * (length - 1) + 1)
    for exponent in range(0, len(out), step):
        out[exponent] = 1
    return out


def add(left: list[int], right: list[int]) -> list[int]:
    out = [0] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
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


def shift(poly: list[int], amount: int) -> list[int]:
    return [0] * amount + poly


def symmetric_unimodal(poly: list[int]) -> bool:
    if poly != poly[::-1] or any(value < 0 for value in poly):
        return False
    midpoint = (len(poly) - 1) // 2
    return all(poly[i] <= poly[i + 1] for i in range(midpoint))


def allocations(capacities: tuple[int, ...], total: int):
    for candidate in itertools.product(*(range(cap + 1) for cap in capacities)):
        if sum(candidate) == total:
            yield candidate


def recurse(
    alpha: tuple[int, ...], word: tuple[int, ...], c: int, r: int, s: int
) -> tuple[list[int], int]:
    lengths = list(alpha)
    spacer = 1
    current = product([*(qint(x) for x in lengths), qint(c, s)])
    center_checks = 0
    for selected in word:
        x = lengths[selected]
        others = [qint(value) for i, value in enumerate(lengths) if i != selected]
        correction = product([qint(x + r * (spacer + 1)), *others, qint(c, s)])
        translated = shift(current, r)
        translated_at_new_degree = translated + [0] * r
        new_degree = len(current) - 1 + 2 * r
        assert r + (len(current) - 1 + r) == new_degree
        assert len(correction) - 1 == new_degree
        assert symmetric_unimodal(translated_at_new_degree)
        assert symmetric_unimodal(correction)
        current = add(translated, correction)
        assert symmetric_unimodal(current)
        lengths[selected] += r
        spacer += 1
        center_checks += 1
    direct = product(
        [*(qint(value) for value in lengths), qint(spacer, r), qint(c, s)]
    )
    assert current == direct
    return current, center_checks


def eligible(
    lengths: tuple[int, ...], allocation: tuple[int, ...], c: int, r: int, s: int
) -> tuple[bool, tuple[int, ...]]:
    alpha = tuple(a - r * d for a, d in zip(lengths, allocation))
    inequality = c <= 1 + sum(x // s for x in alpha)
    fixed_divisor = any(d == 0 and a % s == 0 for a, d in zip(lengths, allocation))
    return inequality or fixed_divisor, alpha


def check_instance(
    lengths: tuple[int, ...], allocation: tuple[int, ...], c: int, r: int, s: int
) -> int:
    ok, alpha = eligible(lengths, allocation, c, r, s)
    assert ok
    word = tuple(i for i, count in enumerate(allocation) for _ in range(count))
    recursive, centers = recurse(alpha, word, c, r, s)
    b = 1 + sum(allocation)
    direct = product([*(qint(a) for a in lengths), qint(b, r), qint(c, s)])
    assert recursive == direct
    assert symmetric_unimodal(direct)
    return centers


def main() -> None:
    rows = 0
    center_checks = 0
    for k in (1, 2):
        for r in range(2, 5):
            for s in range(2, 5):
                for lengths in itertools.product(range(1, 8), repeat=k):
                    capacities = tuple((a - 1) // r for a in lengths)
                    for b in range(1, 5):
                        for allocation in allocations(capacities, b - 1):
                            for c in range(1, 5):
                                ok, _ = eligible(lengths, allocation, c, r, s)
                                if ok:
                                    center_checks += check_instance(
                                        lengths, allocation, c, r, s
                                    )
                                    rows += 1

    rng = random.Random(20260807)
    random_rows = 0
    while random_rows < 500:
        k = rng.randint(1, 4)
        r = rng.randint(2, 7)
        s = rng.randint(2, 7)
        lengths = tuple(rng.randint(1, 18) for _ in range(k))
        capacities = tuple((a - 1) // r for a in lengths)
        allocation = tuple(rng.randint(0, cap) for cap in capacities)
        c = rng.randint(1, 8)
        ok, _ = eligible(lengths, allocation, c, r, s)
        if not ok:
            continue
        center_checks += check_instance(lengths, allocation, c, r, s)
        random_rows += 1

    print(
        json.dumps(
            {
                "center_steps_checked": center_checks,
                "exhaustive_rows": rows,
                "random_rows": random_rows,
                "seed": 20260807,
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
