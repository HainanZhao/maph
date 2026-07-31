#!/usr/bin/env python3
"""Run the exact hash-chained Q-stratum packet synthesis."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
HEIGHTS = ROOT / "artifacts" / "census-packet-height-calibration-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v5.json"
)
GP_SCRIPT = ROOT / "scripts" / "certify_census_q_packet.gp"
DEFAULT_OUTPUT = ROOT / "artifacts" / "census-q-packets-v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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


def memory_limit() -> None:
    cap = 2 * 1024**3
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))


def run_row(
    row: dict, height_row: dict, gp_source: str, cap: int
) -> tuple[dict, float]:
    hnf = row["finite_ideal_hnf"]
    prelude = (
        f'CASE_ID="{row["case_id"]}";\n'
        f'D_VALUE={row["d"]};\n'
        f"H11={hnf[0][0]};H12={hnf[0][1]};"
        f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
    )
    started = time.monotonic()
    completed = subprocess.run(
        ["gp", "-q"],
        input=prelude + gp_source,
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
        timeout=300,
        preexec_fn=memory_limit,
    )
    wall_seconds = time.monotonic() - started
    if (
        completed.returncode
        or "PACKET_POLYNOMIAL_SYNTHESIS=PASS" not in completed.stdout
        or "ANALYTIC_PACKET_TARGET_OPENED=0" not in completed.stdout
    ):
        raise RuntimeError(completed.stdout + completed.stderr)

    effective = int(scalar(completed.stdout, "EFFECTIVE_ARTIN_IMAGE_SIZE"))
    degree = int(scalar(completed.stdout, "PACKET_FACTOR_DEGREE"))
    digits = int(
        scalar(
            completed.stdout,
            "COEFFICIENT_COORDINATE_DECIMAL_DIGITS",
        )
    )
    if effective != height_row["effective_artin_image_size"]:
        raise RuntimeError("effective Artin image changed after calibration")
    if degree != effective:
        raise RuntimeError("packet degree differs from Artin image")
    if digits > cap:
        raise RuntimeError("frozen coefficient digit cap exceeded")

    record = {
        "schema": "effective-stark-census-q-packet-row-v1",
        "status": "PASS_EXACT_PACKET_POLYNOMIAL",
        "claim_tag": "PROVED",
        "case_id": row["case_id"],
        "base_radicand": row["d"],
        "finite_ideal_hnf": hnf,
        "finite_norm": row["finite_norm"],
        "ray_cyc": scalar(completed.stdout, "RAY_CYC"),
        "sign_log": scalar(completed.stdout, "SIGN_LOG"),
        "supported_characters": scalar(
            completed.stdout, "SUPPORTED_CHARACTERS"
        ),
        "effective_characters": scalar(
            completed.stdout, "EFFECTIVE_CHARACTERS"
        ),
        "character_records": scalar(
            completed.stdout, "CHARACTER_RECORDS"
        ),
        "common_denominator": int(
            scalar(completed.stdout, "COMMON_DENOMINATOR")
        ),
        "powered_exponents": scalar(
            completed.stdout, "POWERED_EXPONENTS"
        ),
        "powered_traces": scalar(completed.stdout, "POWERED_TRACES"),
        "formal_sign_orbit_degree": int(
            scalar(completed.stdout, "FORMAL_SIGN_ORBIT_DEGREE")
        ),
        "effective_artin_image_size": effective,
        "packet_factor_over_K": scalar(
            completed.stdout, "PACKET_FACTOR_OVER_K"
        ),
        "packet_factor_degree_over_K": degree,
        "absolute_packet_resultant": scalar(
            completed.stdout, "ABSOLUTE_PACKET_RESULTANT"
        ),
        "exact_gates": {
            "base_bnfcertify": True,
            "packet_factor_reciprocal": True,
            "packet_factor_squarefree": True,
            "packet_factor_irreducible_over_K": True,
            "packet_factor_positive_root_sign_pattern": True,
            "coefficient_coordinate_decimal_digits": digits,
            "coefficient_coordinate_decimal_digit_cap": cap,
        },
        "independence_wall": {
            "analytic_packet_target_opened": False,
            "height_calibration_used_for_factor_selection": False,
        },
        "source": {
            "pari_version": scalar(completed.stdout, "PARI_VERSION"),
            "gp_stdout_sha256": sha256_bytes(
                completed.stdout.encode("utf-8")
            ),
        },
    }
    return record, wall_seconds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    expected_height_hash = preregistration["calibration"]["sha256"]
    if sha256(HEIGHTS) != expected_height_hash:
        raise RuntimeError("height calibration hash changed")
    cap = preregistration["exact_runtime_gates"][
        "coefficient_coordinate_decimal_digit_cap"
    ]
    census = json.loads(CENSUS.read_text())
    heights = json.loads(HEIGHTS.read_text())
    by_id = {row["case_id"]: row for row in census["records"]}
    height_by_id = {row["case_id"]: row for row in heights["records"]}
    case_ids = list(height_by_id)
    if case_ids != sorted(case_ids) or len(case_ids) != 1560:
        raise RuntimeError("Q population or stable ordering changed")
    if args.case_id:
        if args.case_id not in height_by_id:
            raise RuntimeError("requested case is not in Q")
        case_ids = [args.case_id]

    gp_source = GP_SCRIPT.read_text()
    if args.case_id:
        record, wall_seconds = run_row(
            by_id[args.case_id],
            height_by_id[args.case_id],
            gp_source,
            cap,
        )
        record["diagnostic_wall_seconds"] = round(wall_seconds, 6)
        print(json.dumps(record, indent=2, sort_keys=True))
        return

    output_dir = args.output_dir.resolve()
    rows_dir = output_dir / "rows"
    if output_dir.exists() and any(output_dir.iterdir()):
        raise RuntimeError(f"nonempty output directory: {output_dir}")
    rows_dir.mkdir(parents=True, exist_ok=True)

    previous_hash = "0" * 64
    failures = []
    wall_times = []
    started = time.monotonic()
    for index, case_id in enumerate(case_ids, start=1):
        try:
            record, wall_seconds = run_row(
                by_id[case_id],
                height_by_id[case_id],
                gp_source,
                cap,
            )
            wall_times.append(wall_seconds)
        except Exception as exc:
            record = {
                "schema": "effective-stark-census-q-packet-row-v1",
                "status": "FAIL",
                "claim_tag": "OBSERVED",
                "case_id": case_id,
                "error": str(exc),
            }
            failures.append(case_id)
        record["chain_previous_sha256"] = previous_hash
        rendered = (
            json.dumps(record, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        path = rows_dir / f"{case_id.lower()}.json"
        path.write_bytes(rendered)
        previous_hash = sha256_bytes(rendered)
        if index % 25 == 0 or index == len(case_ids):
            print(
                f"Q_PACKET_PROGRESS={index}/{len(case_ids)} "
                f"FAILURES={len(failures)}",
                flush=True,
            )

    manifest = {
        "schema": "effective-stark-census-q-packet-manifest-v1",
        "status": (
            "PASS_EXHAUSTIVE_Q_PACKET_SYNTHESIS"
            if not failures
            else "FAIL_Q_PACKET_SYNTHESIS"
        ),
        "claim_tag": "PROVED" if not failures else "OBSERVED",
        "population": {
            "attempted_rows": len(case_ids),
            "passed_rows": len(case_ids) - len(failures),
            "failed_rows": len(failures),
            "failed_case_ids": failures,
        },
        "chain": {
            "initial_sha256": "0" * 64,
            "final_sha256": previous_hash,
            "ordering": "stable RQ order",
        },
        "runtime": {
            "wall_seconds": round(time.monotonic() - started, 6),
            "maximum_successful_row_wall_seconds": round(
                max(wall_times, default=0), 6
            ),
        },
        "source_hashes": {
            "gp_script_sha256": sha256(GP_SCRIPT),
            "height_calibration_sha256": sha256(HEIGHTS),
            "preregistration_sha256": sha256(PREREGISTRATION),
        },
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
