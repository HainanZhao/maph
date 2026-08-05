#!/usr/bin/env python3
"""Independent small-oracle and output-integrity checks for Cycle 6."""

from __future__ import annotations

import itertools
import json
from functools import reduce
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError("no primitive root")


def covers(k: int, p: int) -> list[int]:
    h = (p - 1) // 2
    root = primitive_root(p)
    bad: set[int] = set()
    residue = 1
    for exponent in range(h):
        if (k + 1) * min(residue, p - residue) < p:
            bad.add(exponent)
        residue = residue * root % p
    return [sum(1 << time for time in range(h) if (center + time) % h in bad) for center in range(h)]


def recursive_coverable(uncovered: int, cover_masks: list[int], remaining: int) -> bool:
    memo: dict[tuple[int, int], bool] = {}

    def search(mask: int, depth: int) -> bool:
        if mask == 0:
            return True
        if depth == 0:
            return False
        key = mask, depth
        if key not in memo:
            target = (mask & -mask).bit_length() - 1
            memo[key] = any(search(mask & ~cover, depth - 1) for cover in cover_masks if cover & (1 << target))
        return memo[key]

    return search(uncovered, remaining)


def brute_coverable(uncovered: int, cover_masks: list[int], remaining: int) -> bool:
    h = len(cover_masks)
    return any(
        (uncovered & ~reduce(int.__or__, (cover_masks[center] for center in choices), 0)) == 0
        for width in range(remaining + 1)
        for choices in itertools.product(range(h), repeat=width)
    )


def main() -> None:
    cover_masks = covers(3, 11)
    h = len(cover_masks)
    rows = 0
    for subset in range(1 << h):
        for remaining in range(1, 4):
            if recursive_coverable(subset, cover_masks, remaining) != brute_coverable(subset, cover_masks, remaining):
                raise AssertionError(f"H11 direct-oracle mismatch subset={subset} r={remaining}")
            rows += 1

    sample = ROOT / "discovery/out/triple-sample-p199.txt"
    tuples = [tuple(map(int, line.split())) for line in sample.read_text().splitlines()]
    if len(tuples) != 100_000 or tuples != sorted(tuples) or len(set(tuples)) != len(tuples):
        raise AssertionError("sample is not the required 100000-row sorted unique prefix")
    total = sat = unsat = 0
    for part in range(3):
        lines = (ROOT / f"discovery/out/triple-direct-final-part-{part}.txt").read_text().splitlines()
        result_lines = [line for line in lines if not line.startswith("summary ")]
        total += len(result_lines)
        sat += sum(line.startswith("DIRECT_SAT ") for line in result_lines)
        unsat += sum(line.startswith("DIRECT_UNSAT ") for line in result_lines)
    if (total, sat, unsat) != (100_000, 14_406, 85_594):
        raise AssertionError(f"unexpected direct summary: {(total, sat, unsat)}")
    print(json.dumps({"status": "PASS", "h11_rows": rows, "sample_rows": total,
                      "direct_sat": sat, "direct_unsat": unsat}, sort_keys=True))


if __name__ == "__main__":
    main()
