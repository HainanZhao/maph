#!/usr/bin/env python3
"""Audit the reference DD -> Arb -> exact comparison ladder."""

from __future__ import annotations

from fractions import Fraction
import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

import flint

from src.shadow_decision import compare_candidate_scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cases = [
        {
            "id": "ordinary-separated",
            "weights": [Fraction(1), Fraction(1, 4), Fraction(1, 9)],
            "left": 1,
            "right": 5,
            "expected_layer": "double-double",
        },
        {
            "id": "near-overlap-arb",
            "weights": [
                Fraction(1),
                Fraction(1, 4),
                Fraction(1, 10**29),
            ],
            "left": 1,
            "right": 5,
            "expected_layer": "arb",
        },
        {
            "id": "forced-sign-tie",
            "weights": [Fraction(1), Fraction(1, 4), Fraction(1, 9)],
            "left": 5,
            "right": 27,
            "expected_layer": "exact-crt-reference",
        },
    ]
    records = []
    for case in cases:
        result = compare_candidate_scores(
            32,
            [1, 7],
            case["weights"],
            case["left"],
            case["right"],
            arb_precision=128,
        )
        if result["resolved_by"] != case["expected_layer"]:
            raise ArithmeticError("unexpected escalation layer")
        records.append(
            {
                "id": case["id"],
                "modulus": 32,
                "prefix": [1, 7],
                "weights": [
                    {
                        "numerator": str(weight.numerator),
                        "denominator": str(weight.denominator),
                    }
                    for weight in case["weights"]
                ],
                "left": case["left"],
                "right": case["right"],
                "result": result,
            }
        )
    payload = {
        "schema": "certified-qmc-shadow-decision-preflight-v1",
        "date": "2026-07-29",
        "tag": "VERIFIED_REFERENCE",
        "target_run_started": False,
        "python_flint_version": flint.__version__,
        "flint_version": flint.__FLINT_VERSION__,
        "arb_precision_bits": 128,
        "double_double_radius": (
            "exact rational audit radius around EFT double-double center"
        ),
        "cases": records,
        "claim_boundary": (
            "Reference direct-score comparison ladder only. The compiled "
            "NTT shadow and production-cost radii remain unimplemented."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
