#!/usr/bin/env python3
"""Exact C104 two-orbit dihedral Cayley/Seidel interface gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def multiply(left: tuple[int, int], right: tuple[int, int], q: int) -> tuple[int, int]:
    # r^a s^b r^c s^d = r^(a + (-1)^b c) s^(b+d).
    a, b = left; c, d = right
    return ((a + (-1 if b else 1) * c) % q, (b + d) % 2)


def inverse(element: tuple[int, int], q: int) -> tuple[int, int]:
    a, b = element
    return ((-a if not b else a) % q, b)


def chi(value: int, q: int) -> int:
    value %= q
    return 0 if value == 0 else (1 if pow(value, (q - 1) // 2, q) == 1 else -1)


def connection(mask: int, q: int) -> set[tuple[int, int]]:
    chosen: set[tuple[int, int]] = set()
    if mask & 1:
        chosen.update((a, 0) for a in range(1, q))
    for a in range(q):
        orbit = 1 if a == 0 else (2 if chi(a, q) == 1 else 3)
        if mask & (1 << orbit):
            chosen.add((a, 1))
    return chosen


def audit(mask: int, q: int) -> dict[str, object]:
    group = [(a, b) for a in range(q) for b in range(2)]
    index = {element: place for place, element in enumerate(group)}
    con = connection(mask, q)
    assert (0, 0) not in con and {inverse(item, q) for item in con} == con
    adjacency = [[0] * len(group) for _ in group]
    for i, left in enumerate(group):
        for right in con:
            adjacency[i][index[multiply(left, right, q)]] = 1
    convolution = {g: sum(multiply(a, b, q) == g for a in con for b in con) for g in group}
    common = [[sum(adjacency[i][k] * adjacency[k][j] for k in range(len(group))) for j in range(len(group))] for i in range(len(group))]
    route_agrees = all(common[i][j] == convolution[multiply(inverse(group[i], q), group[j], q)] for i in range(len(group)) for j in range(len(group)))
    seidel = [[(0 if i == j else 1 - 2 * adjacency[i][j]) for j in range(len(group))] for i in range(len(group))]
    row_ok = all(sum(row) == -1 for row in seidel)
    values = [sum(seidel[i][k] * seidel[k][j] for k in range(len(group))) for i in range(len(group)) for j in range(i + 1, len(group))]
    distribution = {str(value): values.count(value) for value in sorted(set(values))}
    square_ok = all(value in (0, -4) for value in values)
    return {"mask": mask, "degree": len(con), "route_agrees": route_agrees, "row_ok": row_ok, "offdiagonal_square_distribution": distribution, "square_ok": square_ok, "hit": route_agrees and row_ok and square_ok}


def search() -> dict[str, object]:
    q7 = [audit(mask, 7) for mask in range(16)]
    hits = [row["mask"] for row in q7 if row["hit"]]
    q23 = [audit(mask, 23) for mask in hits]
    return {"family": "two-orbit-dihedral-cayley-four-bit", "q7": q7, "q7_hits": hits, "q23": q23}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(search(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
