#!/usr/bin/env python3
"""Enumerate and Galois-deduplicate the frozen finite ideal range."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def matrix(text: str) -> tuple[int, int, int, int]:
    values = tuple(int(value) for value in text.split(","))
    if len(values) != 4:
        raise ValueError(f"not a 2x2 matrix: {text}")
    return values


def matrix_rows(values: tuple[int, int, int, int]) -> list[list[int]]:
    return [[values[0], values[1]], [values[2], values[3]]]


def run_gp(d_min: int, d_max: int, norm_max: int) -> str:
    source = (ROOT / "scripts" / "enumerate_frozen_ideals.gp").read_text()
    program = f"D_MIN={d_min};D_MAX={d_max};NORM_MAX={norm_max};\n{source}\n"
    completed = subprocess.run(
        ["gp", "-q"],
        cwd=ROOT,
        input=program,
        text=True,
        capture_output=True,
        check=False,
    )
    fatal_stderr = "\n".join(
        line for line in completed.stderr.splitlines() if "Warning:" not in line
    )
    if completed.returncode or "***" in fatal_stderr:
        raise RuntimeError(completed.stdout + completed.stderr)
    return completed.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d-min", type=int, default=2)
    parser.add_argument("--d-max", type=int, default=200)
    parser.add_argument("--norm-max", type=int, default=100)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "artifacts" / "frozen-ideal-census-v1.json",
    )
    args = parser.parse_args()

    stdout = run_gp(args.d_min, args.d_max, args.norm_max)
    fields: dict[int, dict[str, int]] = {}
    representatives: dict[tuple[int, tuple[int, ...]], dict[str, object]] = {}
    raw_count = 0
    conjugate_pairs = 0
    self_conjugate = 0

    for line in stdout.splitlines():
        parts = line.split("|")
        if parts[0] == "FIELD":
            d = int(parts[1])
            fields[d] = {
                "field_discriminant": int(parts[2]),
                "bnfcertify": int(parts[3]),
            }
        elif parts[0] == "IDEAL":
            raw_count += 1
            d = int(parts[1])
            norm = int(parts[2])
            ideal = matrix(parts[3])
            conjugate = matrix(parts[4])
            canonical = min(ideal, conjugate)
            if ideal == conjugate:
                self_conjugate += 1
            else:
                conjugate_pairs += 1
            key = (d, canonical)
            representatives.setdefault(
                key,
                {
                    "D": d,
                    "field_discriminant": fields[d]["field_discriminant"],
                    "finite_norm": norm,
                    "finite_ideal_hnf": matrix_rows(canonical),
                    "galois_orbit_size": 1 if ideal == conjugate else 2,
                },
            )
    if not fields or not representatives:
        raise RuntimeError("GP enumeration returned no fields or ideals")
    if any(record["bnfcertify"] != 1 for record in fields.values()):
        raise RuntimeError("at least one real quadratic bnf failed certification")

    cases = sorted(
        representatives.values(),
        key=lambda row: (
            row["D"],
            row["finite_norm"],
            row["finite_ideal_hnf"],
        ),
    )
    for index, row in enumerate(cases):
        row["case_id"] = f"RQ-{index + 1:06d}"

    payload = {
        "schema": "effective-stark-frozen-ideal-census-v1",
        "claim_tag": "VERIFIED",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "range": {
            "D_min": args.d_min,
            "D_max": args.d_max,
            "norm_max": args.norm_max,
            "archimedean_places_per_orbit": 1,
        },
        "field_count": len(fields),
        "raw_ideal_count": raw_count,
        "deduplicated_case_count": len(cases),
        "self_conjugate_raw_count": self_conjugate,
        "nonself_conjugate_raw_count": conjugate_pairs,
        "all_bnfcertify": True,
        "cases": cases,
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized)
    digest = hashlib.sha256(serialized.encode()).hexdigest()
    print(f"FIELD_COUNT={len(fields)}")
    print(f"RAW_IDEAL_COUNT={raw_count}")
    print(f"DEDUPLICATED_CASE_COUNT={len(cases)}")
    print("ALL_BNFCERTIFY=1")
    print(f"OUTPUT_SHA256={digest}")
    print(f"OUTPUT={args.output}")


if __name__ == "__main__":
    main()
