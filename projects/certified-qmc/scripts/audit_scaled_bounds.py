#!/usr/bin/env python3
"""Freeze proved signed bounds at the proposal and audit scales."""

from __future__ import annotations

from fractions import Fraction
import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.scaled_integer import (
    balanced_crt_bits,
    candidate_difference_bound,
    error_numerator_bound,
)


def record(modulus: int, weights: list[Fraction]) -> dict[str, object]:
    error_bound = error_numerator_bound(modulus, weights)
    branch_bound = candidate_difference_bound(
        modulus, weights[:-1], weights[-1]
    )
    return {
        "modulus": modulus,
        "dimension": len(weights),
        "weight_model": (
            "integral gamma_j=1"
            if len(set(weights)) == 1
            else "gamma_j=1/j^2"
        ),
        "error_numerator_bound": str(error_bound),
        "error_bound_bit_length": error_bound.bit_length(),
        "error_crt_product_required_bits": balanced_crt_bits(error_bound),
        "last_stage_difference_bound": str(branch_bound),
        "last_stage_difference_bound_bit_length": branch_bound.bit_length(),
        "last_stage_crt_product_required_bits": balanced_crt_bits(branch_bound),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "schema": "certified-qmc-scaled-bound-audit-v1",
        "tag": "VERIFIED",
        "date": "2026-07-29",
        "formula": {
            "error": "N*(product_j(N^2*(6*b_j+a_j))+product_j(6*b_j*N^2))",
            "candidate_difference": "N*a_s*B2_numerator_span(N)*product_j<s(N^2*(6*b_j+a_j))",
            "crt_uniqueness": "product(primes)>2*bound",
        },
        "cases": [
            record(2**20, [Fraction(1)] * 100),
            record(1024, [Fraction(1, j * j) for j in range(1, 17)]),
        ],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
