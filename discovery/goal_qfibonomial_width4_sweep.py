#!/usr/bin/env python3
"""Exact bounded falsifier sweep for width-four q-Fibonomial unimodality."""
from __future__ import annotations

import argparse
import json


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, value in enumerate(left):
        if value:
            for j, other in enumerate(right):
                out[i + j] += value * other
    return out


def multiply_interval(coefficients: list[int], length: int) -> list[int]:
    """Multiply by 1+q+...+q^(length-1) in linear time."""
    out = [0] * (len(coefficients) + length - 1)
    running = 0
    for degree in range(len(out)):
        if degree < len(coefficients):
            running += coefficients[degree]
        if degree >= length and degree - length < len(coefficients):
            running -= coefficients[degree - length]
        out[degree] = running
    return out


def monic_divide(dividend: list[int], divisor: list[int]) -> list[int]:
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    remainder = dividend[:]
    for degree in range(len(quotient) - 1, -1, -1):
        quotient[degree] = remainder[degree + len(divisor) - 1]
        for offset, coefficient in enumerate(divisor):
            remainder[degree + offset] -= quotient[degree] * coefficient
    if any(remainder):
        raise AssertionError("non-polynomial quotient")
    return quotient


def is_unimodal(coefficients: list[int]) -> bool:
    descending = False
    for left, right in zip(coefficients, coefficients[1:]):
        if right < left:
            descending = True
        elif descending and right > left:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be positive")

    fibonacci = [0, 1, 1]
    for _ in range(args.limit + 5):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    denominator = multiply([1, 1], [1, 1, 1])
    for m in range(1, args.limit + 1):
        numerator = [1]
        for index in range(m + 1, m + 5):
            numerator = multiply_interval(numerator, fibonacci[index])
        quotient = monic_divide(numerator, denominator)
        if not is_unimodal(quotient):
            print(json.dumps({"status": "COUNTEREXAMPLE", "m": m}, sort_keys=True))
            raise SystemExit(1)
    print(json.dumps({"status": "NO_COUNTEREXAMPLE", "limit": args.limit}, sort_keys=True))


if __name__ == "__main__":
    main()
