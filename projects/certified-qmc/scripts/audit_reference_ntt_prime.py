#!/usr/bin/env python3
"""Verify the proposal's first 62-bit NTT-prime example."""

from __future__ import annotations

import json
import argparse
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from src.ntt_prime import audit_ntt_prime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit_ntt_prime(
        4611685941117976577,
        3,
        {
            2: 33,
            311: 1,
            1726273: 1,
        },
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
