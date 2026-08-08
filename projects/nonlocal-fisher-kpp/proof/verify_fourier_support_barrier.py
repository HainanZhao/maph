#!/usr/bin/env python3
"""Audit the unique highest-mode contribution in the Fourier-barrier proof."""

from __future__ import annotations

import argparse


def audit(maximum: int) -> None:
    for n in range(1, maximum + 1):
        # If a+b=2N and both indices are at most N, then a=N and b=N.
        # Enumerate only a; the former two-dimensional brute-force audit was
        # needlessly cubic across N=1,...,maximum.
        contributors = [(a, 2 * n - a) for a in range(-n, n + 1) if -n <= 2 * n - a <= n]
        if contributors != [(n, n)]:
            raise AssertionError((n, contributors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum", type=int, default=4096)
    args = parser.parse_args()
    if args.maximum < 1:
        raise SystemExit("--maximum must be positive")
    audit(args.maximum)
    print({"status": "PASS", "checked_highest_modes": args.maximum, "unique_pair": "(N,N)"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
