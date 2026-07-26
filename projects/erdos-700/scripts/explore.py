#!/usr/bin/env python3
"""Generate an initial table for Erdős Problem 700."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import f_details, factorize, is_composite  # noqa: E402


def format_factorization(factors: dict[int, int]) -> str:
    return "*".join(
        str(p) if exponent == 1 else f"{p}^{exponent}"
        for p, exponent in factors.items()
    )


def rows(limit: int):
    for n in range(4, limit + 1):
        if not is_composite(n):
            continue
        result = f_details(n)
        factors = factorize(n)
        yield {
            "n": n,
            "factorization": format_factorization(factors),
            "omega": len(factors),
            "f": result.value,
            "minimizers": " ".join(map(str, result.minimizers)),
            "above_sqrt": result.value * result.value > n,
            "at_sqrt": result.value * result.value == n,
            "equals_n_over_largest_prime": (
                result.value == n // max(factors)
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()
    if args.limit < 4:
        parser.error("--limit must be at least 4")

    data = list(rows(args.limit))
    strict_hits = [row for row in data if row["above_sqrt"]]
    equality_hits = [row for row in data if row["at_sqrt"]]

    print(f"Composite n checked: {len(data)} (4 <= n <= {args.limit})")
    print(f"Strict f(n) > sqrt(n) hits: {len(strict_hits)}")
    print(f"Equality f(n) = sqrt(n) hits: {len(equality_hits)}")
    if strict_hits:
        print("First strict hits:")
        for row in strict_hits[:20]:
            print(
                f"  n={row['n']:>5}  {row['factorization']:<12}"
                f" f={row['f']:<5} minimizers={row['minimizers']}"
            )

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Wrote {args.csv}")


if __name__ == "__main__":
    main()
