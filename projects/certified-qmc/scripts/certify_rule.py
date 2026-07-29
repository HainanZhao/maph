#!/usr/bin/env python3
"""Create a deterministic exact B2-product merit certificate."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from src.certificate import build_certificate


def comma_separated_integers(text: str) -> list[int]:
    try:
        return [int(item.strip()) for item in text.split(",") if item.strip()]
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def comma_separated_fractions(text: str) -> list[Fraction]:
    try:
        return [
            Fraction(item.strip())
            for item in text.split(",")
            if item.strip()
        ]
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modulus", required=True, type=int)
    parser.add_argument("--generator", required=True, type=comma_separated_integers)
    parser.add_argument("--weights", required=True, type=comma_separated_fractions)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    certificate = build_certificate(
        args.modulus,
        args.generator,
        args.weights,
    )
    rendered = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
