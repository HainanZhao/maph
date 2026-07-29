#!/usr/bin/env python3
"""Bank synthetic fast-CBC/direct transcripts without touching external data."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from src.producer_error import (
    certify_p2_cbc_branches,
    direct_product_p2_bound,
    independent_p2_merit,
)


MERIT_PATTERN = re.compile(r"^Merit: ([^\s]+)$", re.MULTILINE)
GENERATOR_PATTERN = re.compile(r"Generating vector = \[([0-9, ]+)\]")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_arb(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def exact_float_arb(value: float) -> arb:
    return fraction_arb(Fraction.from_float(value))


def execute(binary: Path, common: list[str], method: str) -> tuple[str, list[int]]:
    command = [
        str(binary),
        *common,
        "-e",
        method,
        "--merit-digits-displayed",
        "17",
    ]
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True
    )
    merit_match = MERIT_PATTERN.search(completed.stdout)
    generator_match = GENERATOR_PATTERN.search(completed.stdout)
    if merit_match is None or generator_match is None:
        raise RuntimeError("cannot parse LatNet synthetic transcript")
    generator = [
        int(value.strip()) for value in generator_match.group(1).split(",")
    ]
    return merit_match.group(1), generator


def run_case(binary: Path, case: dict[str, object]) -> dict[str, object]:
    dimension = int(case["dimension"])
    weight_decimals = case["weight_decimals"]
    common = [
        "-t",
        "lattice",
        "-c",
        "ordinary",
        "-s",
        str(case["modulus"]),
        "-d",
        str(dimension),
        "-f",
        "CU:P2",
        "-q",
        "2",
        "-w",
        "product:0:" + ",".join(weight_decimals),
    ]
    fast_display, generator = execute(binary, common, "fast-CBC")
    direct_display, direct_generator = execute(
        binary,
        common,
        "evaluation:" + "-".join(str(value) for value in generator),
    )
    if generator != direct_generator:
        raise RuntimeError("direct replay changed the generating vector")

    exact_weights = [Fraction(1, j * j) for j in range(1, dimension + 1)]
    direct_bound = direct_product_p2_bound(
        int(case["modulus"]), generator, exact_weights
    )
    branch_certificate = certify_p2_cbc_branches(
        int(case["modulus"]), generator, exact_weights
    )
    exact = independent_p2_merit(
        int(case["modulus"]), generator, exact_weights
    )
    fast_value = float(fast_display)
    direct_value = float(direct_display)
    fast_error = (exact - exact_float_arb(fast_value)).abs_upper()
    direct_error = (exact - exact_float_arb(direct_value)).abs_upper()
    return {
        "name": case["name"],
        "modulus": case["modulus"],
        "dimension": dimension,
        "generator": generator,
        "fast_displayed_17_digits": fast_display,
        "fast_float_hex": fast_value.hex(),
        "direct_displayed_17_digits": direct_display,
        "direct_float_hex": direct_value.hex(),
        "fast_minus_direct_exact_dyadic": str(
            Fraction.from_float(fast_value) - Fraction.from_float(direct_value)
        ),
        "fast_final_error_enclosure": fast_error.str(40),
        "direct_final_error_enclosure": direct_error.str(40),
        "direct_propagated_bound": direct_bound["forward_error_bound"],
        "direct_midpoint_replayed": (
            direct_value.hex() == direct_bound["float_hex"]
        ),
        "branch_certificate": branch_certificate,
        "seventeen_digits_roundtrip_fast_float": (
            float(fast_display).hex() == fast_value.hex()
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--latnet-binary", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "certificates"
        / "workstream-b-fastcbc-synthetic-transcript.json",
    )
    args = parser.parse_args()
    binary = args.latnet_binary.resolve()
    cases = [
        {
            "name": "n16-d3",
            "modulus": 16,
            "dimension": 3,
            "weight_decimals": ["1", "0.25", "0.11111111111111111"],
        },
        {
            "name": "n32-d4",
            "modulus": 32,
            "dimension": 4,
            "weight_decimals": [
                "1",
                "0.25",
                "0.11111111111111111",
                "0.0625",
            ],
        },
        {
            "name": "n64-d6",
            "modulus": 64,
            "dimension": 6,
            "weight_decimals": [
                "1",
                "0.25",
                "0.11111111111111111",
                "0.0625",
                "0.04",
                "0.027777777777777776",
            ],
        },
    ]
    old_precision = ctx.prec
    ctx.prec = 256
    try:
        results = [run_case(binary, case) for case in cases]
    finally:
        ctx.prec = old_precision
    certificate = {
        "schema": "certified-qmc/workstream-b-fastcbc-synthetic/v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tags": {
            "transcript": "VERIFIED_SYNTHETIC_TRANSCRIPT",
            "final_merit_errors": "ENCLOSED",
            "fast_candidate_decisions": (
                "ENCLOSED_OR_EXACT_TIE_CERTIFIED_SYNTHETIC"
            ),
        },
        "producer": {
            "latnet_builder_commit": "39dd60fceb0c86a6124b701072d91f8e3aed73df",
            "binary": str(binary),
            "binary_sha256": sha256(binary),
            "fftw": "3.3.10-1ubuntu3",
        },
        "cases": results,
        "gate": {
            "all_direct_midpoints_replayed": all(
                case["direct_midpoint_replayed"] for case in results
            ),
            "all_17_digit_fast_values_roundtrip": all(
                case["seventeen_digits_roundtrip_fast_float"]
                for case in results
            ),
            "all_fast_branches_certified": all(
                case["branch_certificate"]["all_branches_certified"]
                for case in results
            ),
            "fft_forward_error_bound_complete": False,
            "external_comparison_authorized": False,
        },
        "boundary": (
            "The final merit of each synthetic vector is independently "
            "enclosed and every selected synthetic branch is separated by "
            "direct Arb enumeration. This certifies these decisions after "
            "the fact; it is not a general FFT forward-error bound."
        ),
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
