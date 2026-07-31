#!/usr/bin/env python3
"""Audit the exact RQ-000245 proper-Artin-image synthesis anchor."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import resource
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
GP_SCRIPT = ROOT / "scripts" / "certify_rq000245_packet_synthesis.gp"
CONVENTIONS = ROOT / "scripts" / "census_packet_conventions.gp"
PREREGISTRATIONS = [
    ROOT / "data" / "census-paper-preregistration-amendment-v2.json",
    ROOT / "data" / "census-paper-preregistration-amendment-v3.json",
]
SELECTION_SOURCE = ROOT / "artifacts" / "engine-a-euler-degeneracy-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_output(output: str) -> dict[str, str]:
    parsed = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            parsed[key] = value
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    expected_selection_hash = (
        "f4ead3438d3b305fa42e73e1d979530a"
        "04104ce8d642db0b1c9ac85929bac033"
    )
    if sha256(SELECTION_SOURCE) != expected_selection_hash:
        raise RuntimeError("frozen anchor-selection source hash changed")

    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    completed = subprocess.run(
        ["gp", "-q", str(GP_SCRIPT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=300,
    )
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall_seconds = time.monotonic() - started
    # PARI emits ANSI color codes around its harmless stack-size warning.
    stderr = re.sub(r"\x1b\[[0-9;]*m", "", completed.stderr)
    unexpected_stderr = [
        line
        for line in stderr.splitlines()
        if line.strip()
        and "Warning: new maximum stack size = 2000003072" not in line
    ]
    if completed.returncode or unexpected_stderr:
        raise RuntimeError(completed.stdout + completed.stderr)
    parsed = parse_output(completed.stdout)

    required = {
        "RQ000245_ARTIN_ORBIT_SYNTHESIS": "PASS",
        "CENSUS_ANALYTIC_TARGET_OPENED": "0",
        "CASE_ID": "RQ-000245",
        "BASE_BNFCERTIFY": "1",
        "SUPPORTED_CHARACTER_COUNT": "4",
        "FOUR_CHARACTER_PRODUCT_RELATION": "[0, 0, 0]",
        "ARTIN_SIGN_IMAGE_CARDINALITY": "8",
        "COMMON_DENOMINATOR": "2",
        "POWERED_EXPONENTS": "[1, 1, 1, 1]",
        "AMBIENT_FORMAL_SIGN_DEGREE": "16",
        "AMBIENT_FORMAL_SIGN_RECIPROCAL": "1",
        "FULL_RAY_RELATIVE_DEGREE": "8",
        "FULL_RAY_ABSOLUTE_DEGREE": "16",
        "FULL_RAY_BNFCERTIFY": "1",
        "IDENTITY_POWER_IS_FULL_RAY_UNIT": "1",
        "PACKET_ROOT_TORSION_CANDIDATES_NONEMPTY": "1",
        "IDENTITY_PACKET_MATCHING_FACTOR_COUNT": "1",
        "PACKET_FACTOR_RELATIVE_DEGREE": "8",
        "PACKET_FACTOR_RECIPROCAL": "1",
        "PACKET_FACTOR_POSITIVE_ROOT_SIGN_PATTERN": "1",
        "PACKET_FACTOR_IRREDUCIBLE_OVER_K": "1",
        "PACKET_ABSOLUTE_DEGREE": "16",
    }
    for key, expected in required.items():
        actual = parsed.get(key)
        if actual != expected:
            raise RuntimeError(f"{key}: expected {expected}, got {actual}")
    for index in range(1, 5):
        for suffix in (
            "EULER_NONZERO",
            "FIELD_BNFCERTIFY",
            "NORM_KERNEL_RANK",
            "ORIENTED_ABOVE_ONE",
        ):
            key = f"CHARACTER_{index}_{suffix}"
            if parsed.get(key) != "1":
                raise RuntimeError(f"{key}: expected 1, got {parsed.get(key)}")

    result = {
        "schema": "effective-stark-census-rq000245-synthesis-v1",
        "status": "PASS_PROPER_ARTIN_IMAGE_AND_DENOMINATOR_LIFT",
        "claim_tags": {
            "character_relation_and_artin_image": "PROVED",
            "quartic_and_full_ray_field_certification": "PROVED",
            "exact_packet_factor_for_rq000245": "PROVED",
        },
        "claim_boundary": {
            "case_id": "RQ-000245",
            "full_q_corpus_run": False,
            "analytic_lprime_or_packet_target_opened": False,
            "coefficient_height_cap_frozen": False,
        },
        "preserved_selection_failure": {
            "case_id": "RQ-000089",
            "reason": (
                "one of four supported characters has zero Euler product"
            ),
            "unit_or_polynomial_data_opened_before_failure": False,
        },
        "exact_gates": {
            "supported_characters": json.loads(
                parsed["SUPPORTED_CHARACTERS"]
            ),
            "character_product_relation": [0, 0, 0],
            "formal_sign_orbit_size": 16,
            "artin_sign_image_size": 8,
            "common_denominator": 2,
            "powered_exponents": [1, 1, 1, 1],
            "quartic_bnfcertify": [True] * 4,
            "full_ray_relative_degree": 8,
            "full_ray_absolute_degree": 16,
            "full_ray_bnfcertify": True,
            "matching_packet_factor_count": 1,
            "packet_factor_degree_over_K": 8,
            "packet_factor_reciprocal": True,
            "packet_factor_positive_at_split_place": True,
            "packet_factor_irreducible_over_K": True,
            "packet_absolute_degree": 16,
        },
        "exact_data": {
            "base": "y^2-7",
            "finite_ideal_hnf": [[24, 4], [0, 4]],
            "finite_norm": 96,
            "ray_cyc": [2, 2, 2],
            "sign_log": [1, 0, 1],
            "powered_traces": parsed["POWERED_TRACES"],
            "ambient_formal_sign_polynomial": parsed[
                "AMBIENT_FORMAL_SIGN_POLYNOMIAL"
            ],
            "packet_factor_over_K": parsed["PACKET_FACTOR_OVER_K"],
            "packet_absolute_polynomial": parsed[
                "PACKET_ABSOLUTE_POLYNOMIAL"
            ],
        },
        "height_observation": {
            "status": "OBSERVED",
            "ambient_max_coefficient_decimal_digits": 24,
            "packet_factor_max_coefficient_decimal_digits": 6,
            "purpose": "anchor datum only; no corpus cap inferred",
        },
        "runtime": {
            "python": platform.python_version(),
            "pari": parsed["PARI_VERSION"],
            "wall_seconds": round(wall_seconds, 6),
            "peak_child_memory_kib": max(
                0, after.ru_maxrss - before.ru_maxrss
            ),
        },
        "source_hashes": {
            "gp_script_sha256": sha256(GP_SCRIPT),
            "conventions_sha256": sha256(CONVENTIONS),
            "preregistration_v2_sha256": sha256(PREREGISTRATIONS[0]),
            "preregistration_v3_sha256": sha256(PREREGISTRATIONS[1]),
            "selection_source_sha256": sha256(SELECTION_SOURCE),
            "stdout_sha256": hashlib.sha256(
                completed.stdout.encode("utf-8")
            ).hexdigest(),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
