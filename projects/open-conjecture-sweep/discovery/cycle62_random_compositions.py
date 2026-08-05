#!/usr/bin/env python3
"""Write deterministic PCG64 S3 simplex compositions for C62."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--denominator", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rng = np.random.Generator(np.random.PCG64(args.seed))
    rows = rng.multinomial(args.denominator, [1 / 6] * 6, size=args.count)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.output, rows, fmt="%d", delimiter="\t")
    args.output.with_suffix(".json").write_text(json.dumps({
        "bit_generator": "PCG64", "numpy_version": np.__version__,
        "seed": args.seed, "count": args.count, "denominator": args.denominator,
    }, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
