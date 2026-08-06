#!/usr/bin/env python3
"""Exact D001 search in the frozen 19-sign six-block family.

This is deliberately a small symbolic-family search, not a graph search: each
candidate changes only the signs of the public six-block architecture.  The
two prime controls are exact integer evaluations of the same sign vector.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def chi(x: int, q: int) -> int:
    x %= q
    if x == 0:
        return 0
    return 1 if pow(x, (q - 1) // 2, q) == 1 else -1


def primitive_root(q: int) -> int:
    factors = []
    remaining = q - 1
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for {q}")


def circulants(q: int) -> tuple[list[list[int]], list[list[int]]]:
    if q % 8 != 7:
        raise ValueError("D001 controls require q = 7 (mod 8)")
    size = (q - 1) // 2
    g = pow(primitive_root(q), 2, q)
    powers = [1]
    for _ in range(1, size):
        powers.append(powers[-1] * g % q)
    a = [1] + [chi(powers[t] - 1, q) for t in range(1, size)]
    b = [chi(value + 1, q) for value in powers]
    return (
        [[a[(column - row) % size] for column in range(size)] for row in range(size)],
        [[b[(column - row) % size] for column in range(size)] for row in range(size)],
    )


def signs(mask: int) -> list[int]:
    return [1 if mask & (1 << index) else -1 for index in range(19)]


def row_sum_ok(mask: int, q: int) -> bool:
    s = signs(mask)
    _, y = circulants(q)
    size = len(y)
    y_sum = sum(y[0])
    if y_sum != -1:
        raise AssertionError((q, y_sum))
    uv, u, v, diagonal, inter = s[0], s[1:5], s[5:9], s[9:13], s[13:19]
    if uv + size * sum(u) != -1 or uv + size * sum(v) != -1:
        return False
    base_diag = (1, -1, 1, -1)
    base_inter = (("Y", -1), ("X", -1), ("X", 1), ("X", -1), ("X", -1), ("Y", 1))
    rows = []
    for group in range(4):
        total = u[group] + v[group] + diagonal[group] * base_diag[group] * (y_sum - 1)
        for index, (kind, base) in enumerate(base_inter):
            left, right = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))[index]
            if group == left or group == right:
                total += inter[index] * base * (1 if kind == "X" else y_sum)
        rows.append(total)
    return rows == [-1, -1, -1, -1]


def matrix(mask: int, q: int) -> list[list[int]]:
    x, y = circulants(q)
    size = len(x)
    order = 2 + 4 * size
    result = [[0 for _ in range(order)] for _ in range(order)]
    s = signs(mask)
    result[0][1] = result[1][0] = s[0]
    for group in range(4):
        start = 2 + group * size
        for local in range(size):
            result[0][start + local] = result[start + local][0] = s[1 + group]
            result[1][start + local] = result[start + local][1] = s[5 + group]
    diagonal = (1, -1, 1, -1)
    for group in range(4):
        start = 2 + group * size
        factor = s[9 + group] * diagonal[group]
        for row in range(size):
            for column in range(size):
                if row != column:
                    result[start + row][start + column] = factor * y[row][column]
    bases = ((0, 1, y, -1), (0, 2, x, -1), (0, 3, x, 1),
             (1, 2, x, -1), (1, 3, x, -1), (2, 3, y, 1))
    for sign_index, (left, right, block, factor) in enumerate(bases, start=13):
        left_start, right_start = 2 + left * size, 2 + right * size
        for row in range(size):
            for column in range(size):
                value = s[sign_index] * factor * block[row][column]
                result[left_start + row][right_start + column] = value
                result[right_start + column][left_start + row] = value
    return result


def valid(mask: int, q: int) -> bool:
    seidel = matrix(mask, q)
    order = len(seidel)
    if any(seidel[row][row] != 0 or sum(seidel[row]) != -1 for row in range(order)):
        return False
    for row in range(order):
        for column in range(row + 1, order):
            value = sum(seidel[row][mid] * seidel[mid][column] for mid in range(order))
            if value not in (0, -4):
                return False
    return True


def search() -> dict[str, object]:
    row_sum_masks = [mask for mask in range(1 << 19) if row_sum_ok(mask, 7)]
    q7 = [mask for mask in row_sum_masks if valid(mask, 7)]
    q23 = [mask for mask in q7 if valid(mask, 23)]
    return {"family": "fixed-six-block-19-sign", "assignments": 1 << 19,
            "row_sum_masks": row_sum_masks, "q7_masks": q7, "q7_q23_masks": q23}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = search()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
