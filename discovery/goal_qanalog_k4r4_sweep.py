#!/usr/bin/env python3
"""Exact bounded falsifier sweep for GOAL.md's Conjecture 5.4 slice."""
from __future__ import annotations

import argparse
import itertools
import json


def convolve_interval(coefficients: list[int], length: int) -> list[int]:
    out = [0] * (len(coefficients) + length - 1)
    running = 0
    for degree in range(len(out)):
        if degree < len(coefficients):
            running += coefficients[degree]
        if degree >= length and degree - length < len(coefficients):
            running -= coefficients[degree - length]
        out[degree] = running
    return out


def multiply_q4_interval(coefficients: list[int], length: int) -> list[int]:
    out = [0] * (len(coefficients) + 4 * (length - 1))
    for residue in range(4):
        running = 0
        for degree in range(residue, len(out), 4):
            if degree < len(coefficients):
                running += coefficients[degree]
            if degree >= 4 * length and degree - 4 * length < len(coefficients):
                running -= coefficients[degree - 4 * length]
            out[degree] = running
    return out


def is_unimodal(coefficients: list[int]) -> bool:
    descending = False
    for left, right in zip(coefficients, coefficients[1:]):
        if right < left:
            descending = True
        elif descending and right > left:
            return False
    return True


def admissible(a: tuple[int, int, int, int], b: int) -> bool:
    return any(value % 4 == 0 for value in a) or b <= 1 + sum(value // 4 for value in a)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--omit-proved-divisible-branch",
        action="store_true",
        help=(
            "skip tuples with an a_i divisible by 4; that universal branch "
            "is already covered by Lemma 4.2/Corollary 4.3 of the source"
        ),
    )
    args = parser.parse_args()
    if args.limit < 1:
        raise SystemExit("--limit must be positive")

    tested = 0
    skipped_proved = 0
    for a in itertools.combinations_with_replacement(range(1, args.limit + 1), 4):
        if args.omit_proved_divisible_branch and any(value % 4 == 0 for value in a):
            skipped_proved += args.limit
            continue
        coefficients = [1]
        for value in a:
            coefficients = convolve_interval(coefficients, value)
        for b in range(1, args.limit + 1):
            if not admissible(a, b):
                continue
            product = multiply_q4_interval(coefficients, b)
            if not is_unimodal(product):
                print(json.dumps({"status": "COUNTEREXAMPLE", "a": a, "b": b}, sort_keys=True))
                raise SystemExit(1)
            tested += 1
    print(json.dumps({
        "status": "NO_COUNTEREXAMPLE",
        "limit": args.limit,
        "tested": tested,
        "skipped_proved_divisible_branch": skipped_proved,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
