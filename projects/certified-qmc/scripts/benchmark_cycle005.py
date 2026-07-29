#!/usr/bin/env python3
"""Benchmark the three exact evaluators on frozen UNSW prefixes."""

from __future__ import annotations

from fractions import Fraction
import argparse
import json
import platform
from pathlib import Path
from time import perf_counter_ns
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.exact_error import exact_squared_error
from src.modular_error import reconstruct_error_numerator
from src.ntt_prime import generate_ntt_prime_schedule
from src.scaled_integer import scaled_squared_error


GENERATOR = [1, 275, 179, 319, 299, 451, 417, 167,
             289, 109, 395, 81, 215, 115, 143, 361]


def timed(callable_, repeats: int = 3):
    durations = []
    value = None
    for _ in range(repeats):
        start = perf_counter_ns()
        value = callable_()
        durations.append(perf_counter_ns() - start)
    return value, {
        "repeats": repeats,
        "minimum_ns": min(durations),
        "median_ns": sorted(durations)[len(durations) // 2],
        "samples_ns": durations,
        "tag": "NUMERICAL",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    schedule = generate_ntt_prime_schedule(16)
    rows = []
    for dimension in (2, 4, 8, 16):
        generator = GENERATOR[:dimension]
        weights = [Fraction(1, j * j) for j in range(1, dimension + 1)]
        fraction_value, fraction_time = timed(
            lambda: exact_squared_error(1024, generator, weights)
        )
        scaled_value, scaled_time = timed(
            lambda: scaled_squared_error(1024, generator, weights)
        )
        crt_value, crt_time = timed(
            lambda: reconstruct_error_numerator(
                1024, generator, weights, schedule
            )
        )
        crt_fraction = Fraction(
            int(crt_value["reduced_numerator"]),
            int(crt_value["reduced_denominator"]),
        )
        if not fraction_value == scaled_value.value == crt_fraction:
            raise ArithmeticError("benchmark evaluators disagree")
        rows.append(
            {
                "dimension": dimension,
                "exact_result": {
                    "numerator": str(fraction_value.numerator),
                    "denominator": str(fraction_value.denominator),
                    "tag": "VERIFIED",
                },
                "all_three_exactly_equal": True,
                "crt_prime_count": len(crt_value["moduli"]),
                "crt_bound_bits": int(crt_value["bound"]).bit_length(),
                "fraction_oracle": fraction_time,
                "scaled_integer": scaled_time,
                "direct_modular_crt": crt_time,
            }
        )
    result = {
        "schema": "certified-qmc-cycle005-benchmark-v1",
        "date": "2026-07-29",
        "claim_boundary": (
            "Timings are local NUMERICAL observations for direct Python "
            "evaluators; they are not NTT or production-scale projections."
        ),
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "input": {
            "source": "frozen UNSW lattice-29102-1024 prefix",
            "modulus": 1024,
            "weight_model": "gamma_j=1/j^2",
        },
        "rows": rows,
        "decision": "CONTINUE_WITH_FAST_MODULAR_ENGINEERING",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
