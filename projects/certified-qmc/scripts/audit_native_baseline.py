#!/usr/bin/env python3
"""Validate and benchmark the compiled direct modular baseline."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter_ns

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.exact_error import RuleSpec
from src.modular_error import error_numerator_residue
from src.native_baseline import (
    build_native_baseline,
    native_error_numerator_residue,
)
from src.ntt_prime import generate_ntt_prime_schedule


GENERATOR = [1, 275, 179, 319, 299, 451, 417, 167,
             289, 109, 395, 81, 215, 115, 143, 361]
WEIGHTS = [Fraction(1, j * j) for j in range(1, 17)]


def timed(function, repeats: int = 5):
    samples = []
    result = None
    for _ in range(repeats):
        start = perf_counter_ns()
        result = function()
        samples.append(perf_counter_ns() - start)
    return result, {
        "tag": "NUMERICAL",
        "repeats": repeats,
        "minimum_ns": min(samples),
        "median_ns": sorted(samples)[len(samples) // 2],
        "samples_ns": samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    binary = build_native_baseline()
    prime_records = generate_ntt_prime_schedule(2)
    primes = [int(row["prime"]) for row in prime_records]

    validations = []
    for dimension in (2, 4, 8, 16):
        spec = RuleSpec.create(
            1024, GENERATOR[:dimension], WEIGHTS[:dimension]
        )
        for prime in primes:
            native = native_error_numerator_residue(
                spec.modulus,
                spec.generator,
                spec.weights,
                prime,
                binary=binary,
            )
            oracle = error_numerator_residue(spec, prime)
            if native != oracle:
                raise ArithmeticError("native/Python residue mismatch")
            validations.append(
                {
                    "modulus": spec.modulus,
                    "dimension": dimension,
                    "prime": str(prime),
                    "residue": str(native),
                    "equal_to_python_oracle": True,
                }
            )

    scaling = []
    prime = primes[0]
    for modulus in (2**10, 2**14, 2**18, 2**20):
        residue, timing = timed(
            lambda modulus=modulus: native_error_numerator_residue(
                modulus,
                GENERATOR,
                WEIGHTS,
                prime,
                binary=binary,
            )
        )
        scaling.append(
            {
                "modulus": modulus,
                "dimension": 16,
                "residue": str(residue),
                "timing": timing,
                "input_kind": (
                    "frozen UNSW prefix"
                    if modulus == 1024
                    else "synthetic modulus-scaling case"
                ),
            }
        )

    compiler = subprocess.run(
        ["cc", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    source = PROJECT / "native" / "direct_modular.c"
    result = {
        "schema": "certified-qmc-native-baseline-v1",
        "date": "2026-07-29",
        "tag": "VERIFIED_IMPLEMENTATION",
        "arithmetic": (
            "signed/unsigned __int128 intermediates; residues modulo "
            "audited 62-bit primes"
        ),
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "binary_sha256": sha256(binary.read_bytes()).hexdigest(),
        "environment": {
            "compiler": compiler,
            "platform": platform.platform(),
        },
        "validation": validations,
        "scaling_benchmark": scaling,
        "claim_boundary": (
            "Residue equalities are VERIFIED. Timings are local NUMERICAL "
            "observations and this direct O(Nd) evaluator is not fast CBC."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
