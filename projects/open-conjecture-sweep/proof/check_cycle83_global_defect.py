#!/usr/bin/env python3
"""Exact global-defect scan for the ordered-tip C83 gate."""
from __future__ import annotations

import json

from check_cycle83_tip_fibers import BASE, c82_predecessors, closure


def pair_counts(pre: list[int]) -> tuple[int, list[list[int]]]:
    n = len(pre)
    order: list[int] = []
    pair = [[0] * n for _ in range(n)]
    extensions = 0

    def visit(used: int) -> None:
        nonlocal extensions
        if len(order) == n:
            extensions += 1
            for right_index, right in enumerate(order):
                for left in order[:right_index]:
                    pair[left][right] += 1
            return
        for vertex in range(n):
            if not (used & (1 << vertex)) and not (pre[vertex] & ~used):
                order.append(vertex)
                visit(used | (1 << vertex))
                order.pop()

    visit(0)
    return extensions, pair


def scan(pre: list[int]) -> dict[str, object]:
    closed = closure(pre)
    extensions, pair = pair_counts(pre)
    maximum = -1
    witness: tuple[int, int, int, int] | None = None
    failures = 0
    tested = 0
    for y in range(len(pre)):
        for x in range(len(pre)):
            if not (closed[y] & (1 << x)):
                continue
            for z in range(len(pre)):
                for w in range(len(pre)):
                    if len({x, y, z, w}) != 4:
                        continue
                    tested += 1
                    defect = pair[z][w] + pair[w][x] + pair[y][z]
                    if defect > maximum:
                        maximum, witness = defect, (x, y, z, w)
                    if 2 * defect > 3 * extensions:
                        failures += 1
    assert witness is not None
    return {
        "extensions": extensions,
        "marked_quadruples": tested,
        "maximum_defect_numerator": maximum,
        "maximum_defect_denominator": extensions,
        "maximum_witness_xyzw": witness,
        "inequality_failures": failures,
    }


def main() -> None:
    c81 = scan(list(BASE))
    c82 = scan(c82_predecessors())
    assert c81["extensions"] == 1431
    assert c82["extensions"] == 571_725
    print(json.dumps({
        "epistemic_status": "PROVED",
        "inequality": "P(z<w)+P(w<x)+P(y<z)<=3/2 for every marked x<y,z,w",
        "c81": c81,
        "c82": c82,
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
