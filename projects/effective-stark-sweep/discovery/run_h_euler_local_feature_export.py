#!/usr/bin/env python3
"""Export exact all-order deleted-prime cover features for frozen H rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts/w1-full-census-v1.json"
PREREG = ROOT / "docs/cycle-131-all-order-deleted-prime-cover-preregistration.md"
GP = ROOT / "discovery/export_h_euler_local_features.gp"
OUT = ROOT / "discovery/h-euler-local-features-v1.json"
TRANSCRIPT = ROOT / "discovery/h-euler-local-features-v1.transcript"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(output: str, key: str) -> str:
    values = [line[len(key) + 1:].strip() for line in output.splitlines()
              if line.startswith(key + "=")]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {values}")
    return values[0]


def integer(output: str, key: str) -> int:
    return int(scalar(output, key))


def vector(output: str, key: str) -> list[int]:
    text = scalar(output, key)
    if not text.startswith("[") or not text.endswith("]"):
        raise RuntimeError(f"invalid vector for {key}: {text}")
    return [] if not text[1:-1].strip() else [int(x.strip()) for x in text[1:-1].split(",")]


def matrix(output: str, key: str) -> list[list[int]]:
    match = re.fullmatch(r"\[\s*(-?\d+)\s*,\s*(-?\d+)\s*;\s*(-?\d+)\s*,\s*(-?\d+)\s*\]", scalar(output, key))
    if not match:
        raise RuntimeError(f"invalid matrix for {key}")
    return [[int(match.group(1)), int(match.group(2))], [int(match.group(3)), int(match.group(4))]]


def export_row(row: dict, gp_source: str) -> tuple[dict, str]:
    hnf = row["finite_ideal_hnf"]
    prelude = (f'CASE_ID="{row["case_id"]}";\nD_VALUE={row["d"]};\n'
               f"H11={hnf[0][0]};H12={hnf[0][1]};H21={hnf[1][0]};H22={hnf[1][1]};\n")
    completed = subprocess.run(["gp", "-q"], input=prelude + gp_source,
                               text=True, capture_output=True, cwd=ROOT,
                               timeout=120, check=False)
    output = completed.stdout
    if completed.returncode or "H_EULER_LOCAL_FEATURE_EXPORT_VERIFIED=1" not in output:
        raise RuntimeError(f"{row['case_id']} failed\n{output}{completed.stderr}")
    support_count = integer(output, "SUPPORTED_CHARACTER_COUNT")
    characters = []
    for index in range(1, support_count + 1):
        prefix = f"CHARACTER_{index}"
        removed_count = integer(output, f"{prefix}_REMOVED_COUNT")
        removed = []
        for item in range(1, removed_count + 1):
            local = f"{prefix}_REMOVED_{item}"
            phase_denominator = integer(output, f"{local}_PHASE_DENOMINATOR")
            removed.append({
                "rational_prime": integer(output, f"{local}_RATIONAL_PRIME"),
                "ramification_index": integer(output, f"{local}_RAMIFICATION_INDEX"),
                "residue_degree": integer(output, f"{local}_RESIDUE_DEGREE"),
                "absolute_norm": integer(output, f"{local}_ABSOLUTE_NORM"),
                "modulus_exponent": integer(output, f"{local}_MODULUS_EXPONENT"),
                "primitive_phase_numerator": integer(output, f"{local}_PHASE_NUMERATOR"),
                "primitive_phase_denominator": phase_denominator,
                "primitive_value_is_one": phase_denominator == 1,
                "prime_hnf": matrix(output, f"{local}_PRIME_HNF"),
            })
        covered = bool(integer(output, f"{prefix}_COVERED_BY_VALUE_ONE"))
        if covered != any(item["primitive_value_is_one"] for item in removed):
            raise RuntimeError(f"{row['case_id']} character {index}: cover mismatch")
        characters.append({
            "ray_character": vector(output, f"{prefix}_COORDS"),
            "order": integer(output, f"{prefix}_ORDER"),
            "primitive_ray_cyc": vector(output, f"{prefix}_PRIMITIVE_CYC"),
            "primitive_character": vector(output, f"{prefix}_PRIMITIVE_COORDS"),
            "primitive_conductor_hnf": matrix(output, f"{prefix}_PRIMITIVE_CONDUCTOR_HNF"),
            "deleted_primes": removed,
            "covered_by_value_one": covered,
        })
    observed_orders = sorted({item["order"] for item in characters})
    if support_count != row["support_count"] or observed_orders != row["support_orders"]:
        raise RuntimeError(f"{row['case_id']}: frozen support mismatch")
    return ({
        "case_id": row["case_id"], "base_radicand": row["d"],
        "finite_norm": row["finite_norm"], "finite_ideal_hnf": hnf,
        "ray_cyc": vector(output, "RAY_CYC"), "sign_log": vector(output, "SIGN_LOG"),
        "support_count": support_count, "support_orders": observed_orders,
        "all_supported_characters_covered": all(item["covered_by_value_one"] for item in characters),
        "characters": characters,
    }, output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id")
    args = parser.parse_args()
    census = json.loads(CENSUS.read_text())
    selected = [row for row in census["records"] if max(row["support_orders"], default=0) > 2]
    if len(selected) != 2704:
        raise RuntimeError(f"frozen H population changed: {len(selected)}")
    if args.case_id:
        selected = [row for row in selected if row["case_id"] == args.case_id]
        if len(selected) != 1:
            raise RuntimeError("requested H case not found")
    gp_source = GP.read_text()
    started = time.monotonic()
    records, transcript = [], []
    for index, row in enumerate(selected, start=1):
        record, output = export_row(row, gp_source)
        records.append(record)
        transcript.append(f"===== {index}/{len(selected)} {row['case_id']} =====\n{output}")
        print(f"{index}/{len(selected)} {row['case_id']}", flush=True)
    if args.case_id:
        print(json.dumps(records[0], indent=2, sort_keys=True))
        return
    TRANSCRIPT.write_text("\n".join(transcript))
    payload = {
        "schema": "effective-stark-h-euler-local-features-v1",
        "status": "EXPLORATORY_EXACT_FEATURE_EXPORT",
        "claim_tag": "OBSERVED",
        "population": {"rows": len(records), "covered_rows": sum(row["all_supported_characters_covered"] for row in records)},
        "runtime_wall_seconds": time.monotonic() - started,
        "records": records,
        "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (CENSUS, PREREG, GP)},
        "transcript": {"path": str(TRANSCRIPT.relative_to(ROOT)), "sha256": sha256(TRANSCRIPT)},
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"H_EULER_LOCAL_FEATURE_ROWS={len(records)}")
    print("H_EULER_LOCAL_FEATURE_EXPORT=PASS")


if __name__ == "__main__":
    main()
