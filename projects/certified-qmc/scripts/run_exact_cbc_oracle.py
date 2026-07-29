#!/usr/bin/env python3
"""Run the small exact CBC ground-truth oracle."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from src.cbc import exact_cbc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modulus", type=int, default=31)
    parser.add_argument("--dimension", type=int, default=5)
    args = parser.parse_args()
    weights = [
        Fraction(1, index * index)
        for index in range(1, args.dimension + 1)
    ]
    print(
        json.dumps(
            exact_cbc(args.modulus, weights),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
