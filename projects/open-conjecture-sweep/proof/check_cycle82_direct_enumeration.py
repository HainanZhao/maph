#!/usr/bin/env python3
"""Independent exhaustive C82 replay by direct linear-extension enumeration."""
from __future__ import annotations

import json

BASE = (0, 0, 2, 0, 1, 8, 25, 7, 42)
TRIPLE = {0, 1, 3}


def substitution() -> list[int]:
    blocks: list[list[int]] = []
    size = 0
    for vertex in range(len(BASE)):
        width = 3 if vertex in TRIPLE else 1
        blocks.append(list(range(size, size + width)))
        size += width
    pre = [0] * size
    for vertex, members in enumerate(blocks):
        for index, member in enumerate(members):
            if index:
                pre[member] |= 1 << members[index - 1]
            for parent in range(len(BASE)):
                if BASE[vertex] & (1 << parent):
                    for ancestor in blocks[parent]:
                        pre[member] |= 1 << ancestor
    return pre


def closure(pre: list[int]) -> list[int]:
    result = pre[:]
    for _ in result:
        for vertex in range(len(result)):
            inherited = result[vertex]
            for parent in range(len(result)):
                if inherited & (1 << parent):
                    result[vertex] |= result[parent]
    return result


def main() -> None:
    pre = substitution()
    closed = closure(pre)
    n = len(pre)
    pair = [[0] * n for _ in range(n)]
    total = 0

    def visit(used: int, prefix: list[int]) -> None:
        nonlocal total
        if len(prefix) == n:
            total += 1
            for right_index, right in enumerate(prefix):
                for left in prefix[:right_index]:
                    pair[left][right] += 1
            return
        for vertex in range(n):
            if not (used & (1 << vertex)) and not (pre[vertex] & ~used):
                prefix.append(vertex)
                visit(used | (1 << vertex), prefix)
                prefix.pop()

    visit(0, [])

    def edge(left: int, right: int, restricted: bool) -> bool:
        if pair[left][right] <= pair[right][left]:
            return False
        return not restricted or not ((closed[left] | closed[right]) & ((1 << left) | (1 << right)))

    def cycle4(restricted: bool) -> bool:
        return any(
            edge(a, b, restricted) and edge(b, c, restricted)
            and edge(c, d, restricted) and edge(d, a, restricted)
            for a in range(n) for b in range(n) for c in range(n) for d in range(n)
            if len({a, b, c, d}) == 4
        )

    assert total == 571_725
    print(json.dumps({
        "epistemic_status": "PROVED",
        "vertices": n,
        "extensions": total,
        "transitive_closure_added_relations": sum(
            (closed[v] & ~pre[v]).bit_count() for v in range(n)
        ),
        "full_has_4_cycle": cycle4(False),
        "restricted_has_4_cycle": cycle4(True),
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
