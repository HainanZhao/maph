#!/usr/bin/env python3
"""Independent D001 evaluator; intentionally does not import the enumerator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def character(value: int, prime: int) -> int:
    value %= prime
    return 0 if value == 0 else (1 if pow(value, (prime - 1) // 2, prime) == 1 else -1)


def primitive(prime: int) -> int:
    factors = []
    remaining = prime - 1
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError(prime)


def build(mask: int, prime: int) -> list[list[int]]:
    width = (prime - 1) // 2
    generator = pow(primitive(prime), 2, prime)
    powers = [pow(generator, index, prime) for index in range(width)]
    a = [1 if index == 0 else character(powers[index] - 1, prime) for index in range(width)]
    b = [character(value + 1, prime) for value in powers]
    x = [[a[(column - row) % width] for column in range(width)] for row in range(width)]
    y = [[b[(column - row) % width] for column in range(width)] for row in range(width)]
    bit = lambda index: 1 if mask & (1 << index) else -1
    answer = [[0] * (2 + 4 * width) for _ in range(2 + 4 * width)]
    answer[0][1] = answer[1][0] = bit(0)
    for group in range(4):
        first = 2 + group * width
        for local in range(width):
            answer[0][first + local] = answer[first + local][0] = bit(1 + group)
            answer[1][first + local] = answer[first + local][1] = bit(5 + group)
        for row in range(width):
            for column in range(width):
                if row != column:
                    answer[first + row][first + column] = bit(9 + group) * (1, -1, 1, -1)[group] * y[row][column]
    for offset, (left, right, block, coefficient) in enumerate(((0, 1, y, -1), (0, 2, x, -1), (0, 3, x, 1), (1, 2, x, -1), (1, 3, x, -1), (2, 3, y, 1))):
        for row in range(width):
            for column in range(width):
                value = bit(13 + offset) * coefficient * block[row][column]
                answer[2 + left * width + row][2 + right * width + column] = value
                answer[2 + right * width + column][2 + left * width + row] = value
    return answer


def passes(mask: int, prime: int) -> bool:
    seidel = build(mask, prime)
    order = len(seidel)
    if any(sum(row) != -1 or row[index] != 0 for index, row in enumerate(seidel)):
        return False
    for row in range(order):
        for column in range(row + 1, order):
            square = sum(seidel[row][middle] * seidel[middle][column] for middle in range(order))
            if square not in (0, -4):
                return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    recorded = json.loads(args.result.read_text(encoding="utf-8"))
    if recorded.get("assignments") != 1 << 19:
        raise SystemExit("unexpected assignment cap")
    q7 = [mask for mask in range(1 << 19) if passes(mask, 7)]
    q23 = [mask for mask in q7 if passes(mask, 23)]
    if recorded.get("q7_masks") != q7 or recorded.get("q7_q23_masks") != q23:
        raise SystemExit("enumeration disagreement")
    print(json.dumps({"q7_masks": q7, "q7_q23_masks": q23, "checked": 1 << 19}, sort_keys=True))


if __name__ == "__main__":
    main()
