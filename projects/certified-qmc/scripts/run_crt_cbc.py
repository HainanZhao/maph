#!/usr/bin/env python3
"""Emit the frozen small CRT-CBC branch certificate."""

from __future__ import annotations

from fractions import Fraction
import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.modular_error import certified_crt_cbc
from src.ntt_prime import generate_ntt_prime_schedule


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    weights = [Fraction(1, j * j) for j in range(1, 6)]
    result = certified_crt_cbc(
        31, weights, generate_ntt_prime_schedule(4)
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
