#!/usr/bin/env python3
"""Independent exact checks for the frozen l=1 Lonely Runner ansatz."""

from __future__ import annotations

import argparse
import gzip
import itertools
from pathlib import Path


def bad_mask(speed: int, k: int, p: int) -> int:
    mask = 0
    for time in range(1, (p + 1) // 2):
        residue = speed * time % p
        if residue * (k + 1) < p or (p - residue) * (k + 1) < p:
            mask |= 1 << (time - 1)
    return mask


def canonicalize(values: tuple[int, ...], p: int) -> tuple[int, ...]:
    candidates = []
    for pivot in values:
        inverse = pow(pivot, -1, p)
        normalized = [min(value * inverse % p, p - value * inverse % p) for value in values]
        candidates.append(tuple(sorted(normalized)))
    return min(candidates)


def direct_improper(values: tuple[int, ...], k: int, p: int) -> bool:
    for time in range(1, p):
        if all((k + 1) * min(value * time % p, p - value * time % p) >= p for value in values):
            return False
    return True


def brute_force(k: int, p: int) -> set[tuple[int, ...]]:
    half = (p - 1) // 2
    full = (1 << half) - 1
    masks = [bad_mask(speed, k, p) for speed in range(1, half + 1)]
    result = set()
    for tail in itertools.combinations_with_replacement(range(1, half + 1), k - 1):
        values = (1, *tail)
        cover = 0
        for value in values:
            cover |= masks[value - 1]
        if cover == full:
            result.add(canonicalize(values, p))
    return result


def read_tuples(path: Path, k: int, p: int) -> set[tuple[int, ...]]:
    tuples = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        values = tuple(map(int, line.split()))
        if len(values) != k:
            raise ValueError(f"{path}:{line_number}: expected {k} values")
        if values != canonicalize(values, p):
            raise ValueError(f"{path}:{line_number}: tuple is not canonical")
        if not direct_improper(values, k, p):
            raise ValueError(f"{path}:{line_number}: tuple has a witness")
        tuples.add(values)
    return tuples


def stream_recheck(path: Path, k: int, p: int) -> int:
    """Recheck a large sorted output without materializing it in memory."""
    half = (p - 1) // 2
    full = (1 << half) - 1
    masks = [bad_mask(speed, k, p) for speed in range(1, half + 1)]
    previous: tuple[int, ...] | None = None
    count = 0
    opener = gzip.open if path.suffix == ".gz" else Path.open
    with opener(path, mode="rt", encoding="utf-8") as rows:
        for line_number, line in enumerate(rows, 1):
            values = tuple(map(int, line.split()))
            if len(values) != k:
                raise ValueError(f"{path}:{line_number}: expected {k} values")
            if values[0] != 1 or values != tuple(sorted(values)) or values[-1] > half:
                raise ValueError(f"{path}:{line_number}: invalid representative shape")
            if previous is not None and values <= previous:
                raise ValueError(f"{path}:{line_number}: duplicate or out-of-order tuple")
            cover = 0
            for value in values:
                cover |= masks[value - 1]
            if cover != full:
                raise ValueError(f"{path}:{line_number}: tuple has a witness")
            previous = values
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--p", type=int, required=True)
    parser.add_argument("--tuples", type=Path)
    parser.add_argument(
        "--stream-recheck",
        action="store_true",
        help="stream shape, strict order/uniqueness, and exact modular-cover checks",
    )
    parser.add_argument("--brute-force", action="store_true")
    parser.add_argument("--expected-count", type=int)
    args = parser.parse_args()

    observed = None
    if args.tuples and args.stream_recheck:
        observed_count = stream_recheck(args.tuples, args.k, args.p)
        print(f"stream_rechecked={observed_count}")
        if args.expected_count is not None and observed_count != args.expected_count:
            print(f"expected={args.expected_count} observed={observed_count}")
            return 1
        if args.brute_force:
            parser.error("--stream-recheck and --brute-force are mutually exclusive")
        return 0
    if args.tuples:
        observed = read_tuples(args.tuples, args.k, args.p)
        print(f"direct_rechecked={len(observed)}")
    if args.brute_force:
        brute = brute_force(args.k, args.p)
        print(f"brute_force_canonical={len(brute)}")
        if observed is not None and brute != observed:
            print(f"missing={len(brute - observed)} extra={len(observed - brute)}")
            return 1
        observed = brute
    if args.expected_count is not None:
        if observed is None:
            parser.error("--expected-count requires --tuples or --brute-force")
        if len(observed) != args.expected_count:
            print(f"expected={args.expected_count} observed={len(observed)}")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
