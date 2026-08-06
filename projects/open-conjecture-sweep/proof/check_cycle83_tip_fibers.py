#!/usr/bin/env python3
"""Exact marked tip-gap identities on C81/C82 uniform-extension controls."""
from __future__ import annotations

import json

BASE = (0, 0, 2, 0, 1, 8, 25, 7, 42)


def closure(pre: list[int]) -> list[int]:
    result = pre[:]
    for _ in result:
        for vertex in range(len(result)):
            for parent in range(len(result)):
                if result[vertex] & (1 << parent):
                    result[vertex] |= result[parent]
    return result


def c82_predecessors() -> list[int]:
    triple = {0, 1, 3}
    blocks: list[list[int]] = []
    cursor = 0
    for base_vertex in range(9):
        width = 3 if base_vertex in triple else 1
        blocks.append(list(range(cursor, cursor + width)))
        cursor += width
    pre = [0] * cursor
    for base_vertex, members in enumerate(blocks):
        for index, vertex in enumerate(members):
            if index:
                pre[vertex] |= 1 << members[index - 1]
            for parent in range(9):
                if BASE[base_vertex] & (1 << parent):
                    for source in blocks[parent]:
                        pre[vertex] |= 1 << source
    return pre


def check(pre: list[int], pairs: list[tuple[int, int]]) -> dict[str, int]:
    n = len(pre)
    queries = [(x, y, z) for x, y in pairs for z in range(n) if z != x and z != y]
    counts = [[0, 0, 0, 0, 0] for _ in queries]
    order: list[int] = []
    extensions = 0

    def visit(used: int) -> None:
        nonlocal extensions
        if len(order) == n:
            extensions += 1
            pos = [0] * n
            for index, vertex in enumerate(order):
                pos[vertex] = index
            for index, (x, y, z) in enumerate(queries):
                px, py, pz = pos[x], pos[y], pos[z]
                row = counts[index]
                row[0] += px < pz
                row[1] += py < pz
                row[2] += px < pz < py
                row[3] += pz < py
                row[4] += pz < px
            return
        for vertex in range(n):
            if not (used & (1 << vertex)) and not (pre[vertex] & ~used):
                order.append(vertex)
                visit(used | (1 << vertex))
                order.pop()

    visit(0)
    for left, right, interval, reverse_left, reverse_right in counts:
        assert left - right == interval
        assert reverse_left - reverse_right == interval
        assert interval >= 0
    return {"extensions": extensions, "queries": len(queries), "identities": len(counts)}


def main() -> None:
    c81_closed = closure(list(BASE))
    c81_pairs = [(x, y) for y in range(9) for x in range(9) if c81_closed[y] & (1 << x)]
    c82_pairs = [(0, 1), (1, 2), (3, 4), (4, 5), (7, 8), (8, 9)]
    c81 = check(list(BASE), c81_pairs)
    c82 = check(c82_predecessors(), c82_pairs)
    assert c81["extensions"] == 1431
    assert c82["extensions"] == 571_725
    print(json.dumps({
        "epistemic_status": "PROVED",
        "identity": "E[x<z]-E[y<z]=E[x<z<y]=E[z<y]-E[z<x] for x<y",
        "c81": c81,
        "c82": c82,
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
