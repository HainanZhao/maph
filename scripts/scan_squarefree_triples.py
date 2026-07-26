#!/usr/bin/env python3
"""Scan the squarefree three-prime reduction of Erdős Problem 700."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import f_squarefree_triple  # noqa: E402


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [n for n, is_prime in enumerate(sieve) if is_prime]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime-limit", type=int, default=200)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()
    primes = primes_through(args.prime_limit)

    rows = []
    eligible = 0
    strict = 0
    for i, p in enumerate(primes):
        for j in range(i + 1, len(primes)):
            q = primes[j]
            for r in primes[j + 1 :]:
                # Proposition 7: r < p*q is necessary for a strict hit.
                if r >= p * q:
                    break
                eligible += 1
                value = f_squarefree_triple(p, q, r)
                is_strict = value == p * q
                strict += is_strict
                rows.append(
                    {
                        "p": p,
                        "q": q,
                        "r": r,
                        "n": p * q * r,
                        "f": value,
                        "strict_hit": is_strict,
                    }
                )

    print(f"Primes through {args.prime_limit}: {len(primes)}")
    print(f"Eligible triples p < q < r < p*q: {eligible}")
    print(f"Strict square-root hits: {strict}")
    if eligible:
        print(f"Hit proportion among eligible triples: {strict / eligible:.6f}")
    print("First 20 hits:")
    hits = [row for row in rows if row["strict_hit"]]
    for row in hits[:20]:
        print(
            f"  ({row['p']}, {row['q']}, {row['r']})"
            f"  n={row['n']}  f={row['f']}"
        )

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=("p", "q", "r", "n", "f", "strict_hit")
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {args.csv}")


if __name__ == "__main__":
    main()
