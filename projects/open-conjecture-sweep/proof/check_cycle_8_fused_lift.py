#!/usr/bin/env python3
"""Independent exact recheck for the Cycle-8 fused first-lift controls."""

from __future__ import annotations

import itertools
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def masks(k: int, q: int) -> list[int]:
    result: list[int] = []
    for speed in range(q):
        result.append(sum(
            1 << time
            for time in range(q)
            if (k + 1) * min((time * speed) % q, q - ((time * speed) % q)) < q
        ))
    return result


def improper(speed: tuple[int, ...], k: int, c: int, bad: list[int], full: int) -> bool:
    for omitted in range(k):
        divisor = c
        for index, value in enumerate(speed):
            if index != omitted:
                divisor = math.gcd(divisor, value)
        if divisor > 1:
            return False
    covered = 0
    for value in speed:
        covered |= bad[value]
    return covered == full


def h11_check() -> int:
    base_bad = masks(3, 11)
    lifted_bad = masks(3, 44)
    base_full = (1 << 11) - 1
    lifted_full = (1 << 44) - 1
    retained: set[tuple[int, int, int]] = set()
    for base in itertools.product(range(1, 11), repeat=3):
        if not improper(base, 3, 1, base_bad, base_full):
            continue
        for digits in itertools.product(range(4), repeat=3):
            lift = tuple(value + 11 * digit for value, digit in zip(base, digits, strict=True))
            if improper(lift, 3, 4, lifted_bad, lifted_full):
                retained.add(base)
    return len(retained)


def p47_check() -> int:
    rows = [tuple(map(int, line.split())) for line in (ROOT / "discovery/out/partitioned-k6.txt").read_text().splitlines()]
    if len(rows) != 53 or any(len(row) != 6 for row in rows):
        raise AssertionError("frozen p47 representative input mismatch")
    base_bad = masks(6, 47)
    lifted_bad = masks(6, 329)
    base_full = (1 << 47) - 1
    lifted_full = (1 << 329) - 1
    retained = 0
    for base in rows:
        if not improper(base, 6, 1, base_bad, base_full):
            raise AssertionError(f"non-improper frozen base: {base}")
        has_bad_lift = False
        for digits in itertools.product(range(7), repeat=6):
            lift = tuple(value + 47 * digit for value, digit in zip(base, digits, strict=True))
            if improper(lift, 6, 7, lifted_bad, lifted_full):
                has_bad_lift = True
                break
        retained += has_bad_lift
    return retained


def metric(name: str) -> int:
    for line in (ROOT / "discovery/out/cycle8-fused.result").read_text().splitlines():
        if line.startswith(name + "="):
            return int(line.split("=", 1)[1])
    raise AssertionError(f"missing metric {name}")


def main() -> None:
    h11_retained = h11_check()
    p47_retained = p47_check()
    if h11_retained != metric("h11_retained_raw_bases"):
        raise AssertionError("H11 independent retained count mismatch")
    if p47_retained != metric("p47_retained_orbits"):
        raise AssertionError("p47 independent retained count mismatch")
    if (ROOT / "discovery/out/cycle8-p47-retained.txt").read_text() != "":
        raise AssertionError("p47 retained certificate output must be empty")
    print(f"PASS h11_retained={h11_retained} p47_retained={p47_retained} p47_eliminated={53-p47_retained}")


if __name__ == "__main__":
    main()
