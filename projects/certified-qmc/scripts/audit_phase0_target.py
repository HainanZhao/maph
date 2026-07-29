#!/usr/bin/env python3
"""Certify a frozen prefix of the first official-table audit target."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from src.certificate import build_audit_wrapper, build_certificate


TARGETS = PROJECT / "data" / "phase0-targets.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    targets = json.loads(TARGETS.read_text(encoding="utf-8"))
    target = targets["targets"][0]
    generator = target["vendored_prefix"]
    if not 1 <= args.dimension <= len(generator):
        raise ValueError(
            f"dimension must be between 1 and {len(generator)}"
        )
    weights = [
        Fraction(1, index * index)
        for index in range(1, args.dimension + 1)
    ]
    core_certificate = build_certificate(
        target["modulus"],
        generator[: args.dimension],
        weights,
    )
    certificate = build_audit_wrapper(
        core_certificate,
        {
            "id": target["id"],
            "dimension": args.dimension,
            "upstream_url": target["url"],
            "upstream_sha256": target["upstream_sha256"],
            "scope": "vendored prefix only",
        },
    )
    rendered = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    destination = args.output
    if destination is None:
        print(rendered, end="")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
