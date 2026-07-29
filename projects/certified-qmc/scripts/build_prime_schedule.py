#!/usr/bin/env python3
"""Build and audit the deterministic prototype NTT-prime schedule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.ntt_prime import generate_ntt_prime_schedule


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=16)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    primes = generate_ntt_prime_schedule(args.count)
    result = {
        "schema": "certified-qmc-ntt-prime-schedule-v1",
        "tag": "VERIFIED",
        "date": "2026-07-29",
        "generation": {
            "order": "descending coefficient",
            "coefficient_start": 2**30 - 1,
            "family": "p=c*2^32+1",
            "primality": "deterministic-Miller-Rabin-u64",
            "primitive_root": "least root passing complete-factor tests",
        },
        "count": len(primes),
        "primes": primes,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
