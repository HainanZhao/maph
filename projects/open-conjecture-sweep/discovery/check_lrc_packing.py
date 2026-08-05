#!/usr/bin/env python3
"""Independent exhaustive oracle for the H_11 packing-witness table."""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path


def bad_times(k: int, p: int) -> set[int]:
    h = (p - 1) // 2
    primitive_root = 2
    while any(pow(primitive_root, (p - 1) // q, p) == 1 for q in (2, 5)):
        primitive_root += 1
    result: set[int] = set()
    residue = 1
    for exponent in range(h):
        if (k + 1) * min(residue, p - residue) < p:
            result.add(exponent)
        residue = residue * primitive_root % p
    return result


def brute_has_clique(uncovered: list[int], remaining: int, differences: set[int], h: int) -> bool:
    for candidate in itertools.combinations(uncovered, remaining + 1):
        if all((left - right) % h not in differences for left, right in itertools.combinations(candidate, 2)):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    args = parser.parse_args()

    k, p = 3, 11
    h = (p - 1) // 2
    bad = bad_times(k, p)
    differences = {(left - right) % h for left in bad for right in bad}
    observed: dict[tuple[int, int], bool] = {}
    for line in args.table.read_text().splitlines():
        subset, remaining, value = map(int, line.split())
        observed[(subset, remaining)] = bool(value)

    expected_rows = (1 << h) * 3
    if len(observed) != expected_rows:
        raise SystemExit(f"row-count mismatch: {len(observed)} != {expected_rows}")
    for subset in range(1 << h):
        uncovered = [time for time in range(h) if subset & (1 << time)]
        for remaining in range(1, 4):
            expected = brute_has_clique(uncovered, remaining, differences, h)
            actual = observed[(subset, remaining)]
            if actual != expected:
                raise SystemExit(
                    f"oracle mismatch subset={subset} remaining={remaining}: {actual} != {expected}"
                )
    print(f"packing_oracle=PASS rows={expected_rows} h={h} bad={sorted(bad)}")


if __name__ == "__main__":
    main()
