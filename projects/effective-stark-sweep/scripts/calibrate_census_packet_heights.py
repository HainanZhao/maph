#!/usr/bin/env python3
"""Calibrate the preregistered packet coefficient-height predictor."""

from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_CEILING, getcontext
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
EULER = ROOT / "artifacts" / "engine-a-euler-degeneracy-v1.json"
THEOREM = ROOT / "data" / "engine-a-uniform-theorem-v1.json"
CONVENTIONS = ROOT / "scripts" / "census_packet_conventions.gp"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v4.json"
)
GP_SCRIPT = ROOT / "scripts" / "calibrate_engine_a_height.gp"

getcontext().prec = 100


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(output: str, key: str) -> str:
    prefix = f"{key}="
    values = [
        line[len(prefix) :]
        for line in output.splitlines()
        if line.startswith(prefix)
    ]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {values}")
    return values[0]


def parse_decimal_vector(value: str) -> list[Decimal]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [Decimal(item.strip().replace(" E", "E")) for item in inner.split(",")]


def parse_integer_vector(value: str) -> list[int]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [int(item.strip()) for item in inner.split(",")]


def predicted_digits(height: Decimal, degree: int) -> int:
    maximum = Decimal(0)
    for index in range(degree + 1):
        candidate = (
            Decimal(math.comb(degree, index)).ln()
            + Decimal(min(index, degree - index)) * height
        )
        maximum = max(maximum, candidate)
    return int((maximum / Decimal(10).ln()).to_integral_value(
        rounding=ROUND_CEILING
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    for relative, expected in preregistration["frozen_inputs"].items():
        actual = sha256(ROOT / relative)
        if actual != expected:
            raise RuntimeError(f"{relative}: expected {expected}, got {actual}")

    census = json.loads(CENSUS.read_text())
    euler = json.loads(EULER.read_text())
    q_ids = [
        row["case_id"]
        for row in euler["records"]
    ]
    by_id = {row["case_id"]: row for row in census["records"]}
    if len(q_ids) != 1560 or q_ids != sorted(q_ids):
        raise RuntimeError("frozen Q population or ordering changed")

    gp_source = GP_SCRIPT.read_text()
    records = []
    stdout_hash = hashlib.sha256()
    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    for index, case_id in enumerate(q_ids, start=1):
        row = by_id[case_id]
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{case_id}";\n'
            f'D_VALUE={row["d"]};\n'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + gp_source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
            timeout=300,
        )
        if (
            completed.returncode
            or "HEIGHT_CALIBRATION=PASS" not in completed.stdout
            or "PACKET_POLYNOMIAL_CONSTRUCTED=0" not in completed.stdout
            or "ANALYTIC_PACKET_TARGET_OPENED=0" not in completed.stdout
        ):
            raise RuntimeError(
                f"{case_id} failed\n{completed.stdout}{completed.stderr}"
            )
        stdout_hash.update(completed.stdout.encode())
        components = parse_decimal_vector(
            scalar(completed.stdout, "LPRIME_ABS_COMPONENTS")
        )
        group_order = int(scalar(completed.stdout, "GROUP_ORDER"))
        image_size = int(
            scalar(completed.stdout, "EFFECTIVE_ARTIN_IMAGE_SIZE")
        )
        height = Decimal(2) / Decimal(group_order) * sum(
            components, Decimal(0)
        )
        digits = predicted_digits(height, image_size)
        records.append(
            {
                "case_id": case_id,
                "group_order": group_order,
                "supported_character_count": int(
                    scalar(completed.stdout, "SUPPORTED_CHARACTER_COUNT")
                ),
                "effective_character_count": int(
                    scalar(completed.stdout, "EFFECTIVE_CHARACTER_COUNT")
                ),
                "effective_artin_image_size": image_size,
                "packet_exponent_denominators": parse_integer_vector(
                    scalar(
                        completed.stdout,
                        "PACKET_EXPONENT_DENOMINATORS",
                    )
                ),
                "height_predictor": str(height),
                "coefficient_decimal_digit_predictor": digits,
            }
        )
        if index % 100 == 0 or index == len(q_ids):
            print(f"HEIGHT_CALIBRATION_PROGRESS={index}/{len(q_ids)}",
                  flush=True)

    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall_seconds = time.monotonic() - started
    maximum_digits = max(
        row["coefficient_decimal_digit_predictor"] for row in records
    )
    cap = 1
    while cap < max(256, 2 * maximum_digits):
        cap *= 2
    hard_ceiling = preregistration["cap_rule"][
        "hard_ceiling_decimal_digits"
    ]
    status = (
        "PASS_HEIGHT_CALIBRATION_CAP_RULE"
        if cap <= hard_ceiling
        else "FAIL_HEIGHT_CALIBRATION_HARD_CEILING"
    )
    result = {
        "schema": "effective-stark-census-height-calibration-v1",
        "status": status,
        "claim_tag": "OBSERVED",
        "claim_boundary": {
            "packet_polynomials_constructed": False,
            "analytic_packet_targets_opened": False,
            "height_values_are_rigorous_enclosures": False,
            "exact_runtime_digit_gate_still_required": True,
        },
        "population": {
            "q_rows": len(records),
            "supported_characters": sum(
                row["supported_character_count"] for row in records
            ),
            "effective_characters": sum(
                row["effective_character_count"] for row in records
            ),
        },
        "distribution": {
            "maximum_height_predictor": max(
                records, key=lambda row: Decimal(row["height_predictor"])
            ),
            "maximum_coefficient_digit_predictor": max(
                records,
                key=lambda row: row[
                    "coefficient_decimal_digit_predictor"
                ],
            ),
            "maximum_common_denominator": max(
                (
                    max(row["packet_exponent_denominators"], default=1)
                    for row in records
                ),
                default=1,
            ),
            "effective_artin_image_size_counts": {
                str(size): sum(
                    row["effective_artin_image_size"] == size
                    for row in records
                )
                for size in sorted(
                    {row["effective_artin_image_size"] for row in records}
                )
            },
        },
        "cap_rule_result": {
            "maximum_observed_B": maximum_digits,
            "frozen_rule_output_decimal_digits": cap,
            "hard_ceiling_decimal_digits": hard_ceiling,
            "full_polynomial_run_can_be_preregistered": cap <= hard_ceiling,
        },
        "records": records,
        "runtime": {
            "python": platform.python_version(),
            "wall_seconds": round(wall_seconds, 6),
            "peak_child_memory_kib": max(
                0, after.ru_maxrss - before.ru_maxrss
            ),
        },
        "source_hashes": {
            "gp_script_sha256": sha256(GP_SCRIPT),
            "preregistration_sha256": sha256(PREREGISTRATION),
            "aggregate_gp_stdout_sha256": stdout_hash.hexdigest(),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if cap > hard_ceiling:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
