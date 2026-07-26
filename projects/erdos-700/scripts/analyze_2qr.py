#!/usr/bin/env python3
"""Archive witness types for eligible triples n = 2*q*r."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.scan_squarefree_triples import primes_through  # noqa: E402
from src.erdos700 import eligible_2qr_witnesses  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q-limit", type=int, default=1000)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()

    primes = primes_through(2 * args.q_limit)
    rows = []
    type_counts = {"hit": 0, "q_only": 0, "r_only": 0, "both": 0}

    for q in primes:
        if q == 2 or q > args.q_limit:
            continue
        for r in primes:
            if r <= q:
                continue
            if r >= 2 * q:
                break

            witnesses = eligible_2qr_witnesses(q, r)
            q_multipliers = [w.multiplier for w in witnesses if w.target == q]
            r_multipliers = [w.multiplier for w in witnesses if w.target == r]
            if not witnesses:
                witness_type = "hit"
            elif q_multipliers and r_multipliers:
                witness_type = "both"
            elif q_multipliers:
                witness_type = "q_only"
            else:
                witness_type = "r_only"
            type_counts[witness_type] += 1

            rows.append(
                {
                    "q": q,
                    "r": r,
                    "n": 2 * q * r,
                    "two_q_minus_r": 2 * q - r,
                    "witness_type": witness_type,
                    "q_multipliers": " ".join(map(str, q_multipliers)),
                    "r_multipliers": " ".join(map(str, r_multipliers)),
                }
            )

    print(f"Eligible prime pairs with q <= {args.q_limit}: {len(rows)}")
    for witness_type, count in type_counts.items():
        print(f"{witness_type:>6}: {count}")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {args.csv}")


if __name__ == "__main__":
    main()
