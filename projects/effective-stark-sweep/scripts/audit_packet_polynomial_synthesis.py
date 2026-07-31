#!/usr/bin/env python3
"""Audit the exact trace-descent packet-polynomial synthesis anchor."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
GP_SCRIPT = ROOT / "scripts" / "packet_polynomial_synthesis.gp"
CONVENTIONS = ROOT / "scripts" / "census_packet_conventions.gp"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v1.json"
)


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
    if completed.returncode or completed.stderr.strip():
        raise RuntimeError(completed.stdout + completed.stderr)
    parsed = parse_output(completed.stdout)

    required = {
        "TRACE_DESCENT_SYNTHESIS": "PASS",
        "CLAIM_TAG_ALGEBRAIC_RECURRENCE": "PROVED",
        "CLAIM_TAG_NUMERICAL_ANCHOR": "OBSERVED",
        "CENSUS_TARGET_ARTIFACT_OPENED": "0",
        "BASE_BNFCERTIFY": "1",
        "SOURCE_INFINITY_VECTOR": "[1, 0]",
        "RAMIFIED_REAL_PLACE": "1",
        "SPLIT_REAL_PLACE": "2",
        "POWERED_ORBIT_DEGREE": "4",
        "POWERED_ORBIT_RECIPROCAL": "1",
        "SQUARE_LIFT_FACTOR_COUNT": "2",
        "PACKET_FACTOR_DEGREE": "4",
        "PACKET_FACTOR_RECIPROCAL": "1",
        "PACKET_FACTOR_IRREDUCIBLE_OVER_K": "1",
        "ABSOLUTE_PACKET_IRREDUCIBLE": "1",
        "SPLIT_PACKET_REAL_ROOT_COUNT": "4",
    }
    for key, expected in required.items():
        actual = parsed.get(key)
        if actual != expected:
            raise RuntimeError(f"{key}: expected {expected}, got {actual}")

    result = {
        "schema": "effective-stark-census-packet-synthesis-v1",
        "status": "PASS_TRACE_DESCENT_AND_DENOMINATOR_TWO_ANCHOR",
        "claim_tags": {
            "algebraic_recurrence": "PROVED",
            "dimension_eight_exact_lift": "PROVED",
            "archived_decimal_and_brute_force_checks": "OBSERVED",
        },
        "claim_boundary": {
            "raw_recurrence": (
                "sign-orbit polynomial for denominator-cleared "
                "packet powers"
            ),
            "packet_factor": (
                "requires exact denominator lift, positivity, "
                "reciprocity, irreducibility, and Artin conventions"
            ),
            "full_q_corpus_run": False,
            "linear_bit_complexity_claimed": False,
        },
        "correction_to_proposed_method": {
            "dimension_eight_common_denominator": 2,
            "raw_result_is_for": "X_A^2",
            "lift": "factor P_2(X^2) over K",
            "selection": (
                "unique factor with the exact positive-root "
                "coefficient sign pattern at the frozen split place"
            ),
        },
        "exact_gates": {
            "base_bnfcertify": True,
            "source_infinity_vector": [1, 0],
            "ramified_real_place": 1,
            "selected_split_real_place": 2,
            "oriented_traces": ["2*y", "8*y+6"],
            "powered_orbit_degree": 4,
            "powered_orbit_reciprocal": True,
            "square_lift_factor_count": 2,
            "packet_factor_degree_over_K": 4,
            "packet_factor_reciprocal": True,
            "packet_factor_irreducible_over_K": True,
            "absolute_packet_irreducible": True,
        },
        "polynomials": {
            "base": "y^2-y-1",
            "powered_orbit_over_K": parsed["POWERED_ORBIT_POLYNOMIAL"],
            "positive_packet_factor_over_K": parsed[
                "POSITIVE_PACKET_FACTOR"
            ],
            "absolute_packet": parsed["ABSOLUTE_PACKET_POLYNOMIAL"],
        },
        "quarantined_numerical_validation": {
            "archived_anchor": "7.3889768541",
            "anchor_residual": parsed[
                "QUARANTINED_ANALYTIC_ANCHOR_RESIDUAL"
            ],
            "brute_force_root_residuals": [
                parsed[f"QUARANTINED_BRUTE_FORCE_ROOT_RESIDUAL_{index}"]
                for index in range(1, 5)
            ],
            "used_for_selection": False,
        },
        "independence_wall": {
            "census_lprime_or_phase_target_artifact_opened": False,
            "factor_selected_from_archived_decimal": False,
            "benchmark_claim_promoted_to_theorem": False,
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
            "preregistration_amendment_sha256": sha256(PREREGISTRATION),
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
