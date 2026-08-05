#!/usr/bin/env python3
"""Independent direct enumeration for one C81 LEM-triangle witness."""
from __future__ import annotations

from itertools import permutations
import json


PRE = (0, 0, 2, 0, 1, 8, 25, 7, 42)
TRIANGLE = ((0, 3), (3, 1), (1, 0))


def is_extension(pre: tuple[int, ...], order: tuple[int, ...]) -> bool:
    position = [0] * len(pre)
    for index, vertex in enumerate(order):
        position[vertex] = index
    return all(
        not (pre[vertex] & (1 << predecessor))
        or position[predecessor] < position[vertex]
        for vertex in range(len(pre))
        for predecessor in range(len(pre))
    )


def pair_counts(pre: tuple[int, ...]) -> tuple[int, list[list[int]]]:
    counts = [[0] * len(pre) for _ in pre]
    total = 0
    for order in permutations(range(len(pre))):
        if not is_extension(pre, order):
            continue
        total += 1
        position = [0] * len(pre)
        for index, vertex in enumerate(order):
            position[vertex] = index
        for left in range(len(pre)):
            for right in range(len(pre)):
                if left != right and position[left] < position[right]:
                    counts[left][right] += 1
    return total, counts


def split(pre: tuple[int, ...], vertex: int, upper: bool) -> tuple[int, ...]:
    n = len(pre)
    result = list(pre) + [0]
    if upper:
        for target in range(n):
            if pre[target] & (1 << vertex):
                result[target] |= 1 << n
        result[n] = pre[vertex] | (1 << vertex)
    else:
        result[vertex] |= 1 << n
        result[n] = pre[vertex]
    for pivot in range(n + 1):
        for target in range(n + 1):
            if result[target] & (1 << pivot):
                result[target] |= result[pivot]
    return tuple(result)


def has_four_cycle(counts: list[list[int]], pre: tuple[int, ...], incomparable: bool) -> bool:
    n = len(pre)
    def edge(left: int, right: int) -> bool:
        return counts[left][right] > counts[right][left] and (
            not incomparable or not ((pre[left] & (1 << right)) or (pre[right] & (1 << left)))
        )
    return any(
        edge(a, b) and edge(b, c) and edge(c, d) and edge(d, a)
        for a in range(n) for b in range(n) for c in range(n) for d in range(n)
        if len({a, b, c, d}) == 4
    )


def main() -> None:
    total, counts = pair_counts(PRE)
    directed = [[left, right, counts[left][right], counts[right][left]]
                for left, right in TRIANGLE]
    assert total == 1431
    assert all(forward == 720 and reverse == 711
               for _, _, forward, reverse in directed)
    split_checks = []
    for upper in (True, False):
        split_pre = split(PRE, 0, upper)
        split_total, split_counts = pair_counts(split_pre)
        full = has_four_cycle(split_counts, split_pre, False)
        restricted = has_four_cycle(split_counts, split_pre, True)
        assert not (full and not restricted)
        split_checks.append({
            "orientation": "upper" if upper else "lower",
            "extensions": split_total,
            "full_has_4_cycle": full,
            "incomparable_has_4_cycle": restricted,
        })
    print(json.dumps({
        "epistemic_status": "PROVED",
        "extensions": total,
        "predecessor_masks": list(PRE),
        "triangle": directed,
        "scope": "one recovered nine-element witness",
        "split_checks": split_checks,
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
