#!/usr/bin/env python3
"""Compare a compiled LatNet direct evaluator with the enclosed midpoint replay."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import platform
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from src.producer_error import direct_product_p2_bound


MERIT_PATTERN = re.compile(r"^Merit: ([^\s]+)$", re.MULTILINE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(binary: Path, case: dict[str, object]) -> dict[str, object]:
    weight_text = ",".join(case["weight_decimals"])
    generator_text = "-".join(str(value) for value in case["generator"])
    command = [
        str(binary),
        "-t",
        "lattice",
        "-c",
        "ordinary",
        "-s",
        str(case["modulus"]),
        "-d",
        str(len(case["generator"])),
        "-f",
        "CU:P2",
        "-q",
        "2",
        "-w",
        f"product:0:{weight_text}",
        "-e",
        f"evaluation:{generator_text}",
        "--merit-digits-displayed",
        "17",
    ]
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True
    )
    match = MERIT_PATTERN.search(completed.stdout)
    if match is None:
        raise RuntimeError("LatNet output did not contain a unique Merit field")
    displayed = match.group(1)
    latnet_value = float(displayed)
    bounded = direct_product_p2_bound(
        int(case["modulus"]),
        case["generator"],
        [Fraction(value) for value in case["exact_weights"]],
    )
    return {
        "name": case["name"],
        "command": command,
        "displayed_17_digits": displayed,
        "latnet_float_hex": latnet_value.hex(),
        "replay_float_hex": bounded["float_hex"],
        "bit_identical_midpoint": latnet_value.hex() == bounded["float_hex"],
        "replay_forward_error_bound": bounded["forward_error_bound"],
        "independent_arb_target_contained": bounded[
            "contains_independent_arb_target"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--latnet-binary", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "certificates"
        / "workstream-b-latnet-direct-replay.json",
    )
    args = parser.parse_args()
    binary = args.latnet_binary.resolve()
    if not binary.is_file():
        raise FileNotFoundError(binary)

    cases = [
        {
            "name": "small-balanced",
            "modulus": 8,
            "generator": [1, 3],
            "weight_decimals": ["1", "0.25"],
            "exact_weights": ["1", "1/4"],
        },
        {
            "name": "mixed-scale",
            "modulus": 16,
            "generator": [1, 7, 5],
            "weight_decimals": ["1", "0.001", "0.7777777777777778"],
            "exact_weights": ["1", "1/1000", "7/9"],
        },
        {
            "name": "factorial-denominators",
            "modulus": 64,
            "generator": [1, 31, 15, 7, 25, 11],
            "weight_decimals": [
                "1",
                "0.25",
                "0.11111111111111111",
                "0.0625",
                "0.04",
                "0.027777777777777776",
            ],
            "exact_weights": [
                "1",
                "1/4",
                "1/9",
                "1/16",
                "1/25",
                "1/36",
            ],
        },
    ]
    results = [run_case(binary, case) for case in cases]
    linked = subprocess.check_output(["ldd", str(binary)], text=True)
    certificate = {
        "schema": "certified-qmc/workstream-b-latnet-direct-replay/v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_DIRECT_MIDPOINT_REPLAY",
        "scope": {
            "latnet_builder_commit": "39dd60fceb0c86a6124b701072d91f8e3aed73df",
            "submodule_commit": "825610d092e860638b7c6954ad646fe3c7249855",
            "task": "synthetic direct evaluation; no external merit",
            "precision": "17 significant decimal digits",
        },
        "environment": {
            "platform": platform.platform(),
            "binary": str(binary),
            "binary_sha256": sha256(binary),
            "linked_libraries": linked.splitlines(),
        },
        "cases": results,
        "gate": {
            "all_midpoints_bit_identical": all(
                result["bit_identical_midpoint"] for result in results
            ),
            "all_independent_targets_contained": all(
                result["independent_arb_target_contained"]
                for result in results
            ),
        },
        "boundary": (
            "This validates the direct evaluator midpoint replay on the frozen "
            "synthetic cases. It does not validate fast-CBC FFT scores."
        ),
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
