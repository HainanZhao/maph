#!/usr/bin/env python3
"""Extract cheap exact route data and deduplicate sextic field keys."""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

from run_roblot_sextic_population import (
    ANSI,
    configure_child,
    decoded_tail,
    gp_vector,
    parse_output,
    sha256,
    terminate_process_group,
)


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "roblot-sextic-kernel-inventory-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v9.json"
)
SEQUENTIAL = (
    ROOT
    / "artifacts"
    / "roblot-sextic-population-sequential-partial-v0.json"
)
GP = ROOT / "scripts" / "extract_roblot_sextic_route.gp"
TIME_FIELDS = re.compile(r"^ROUTE_(WALL_SECONDS|PEAK_KIB)=(.+)$")


def field_key(record: dict, route: dict) -> str:
    payload = {
        "d": record["d"],
        "primitive_conductor": route["primitive_conductor"],
        "primitive_ray_cyc": route["primitive_ray_cyc"],
        "primitive_kernel_hnf": route["primitive_kernel_hnf"],
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def run_record(
    record: dict, timeout: int, address_space_bytes: int
) -> dict:
    hnf = record["finite_ideal_hnf"]
    wrapper = "\n".join(
        (
            f'CASE_ID="{record["case_id"]}";',
            f'KERNEL_INDEX={record["kernel_index"]};',
            f'D_VALUE={record["d"]};',
            f'H11={hnf[0][0]}; H12={hnf[0][1]};',
            f'H21={hnf[1][0]}; H22={hnf[1][1]};',
            f'SOURCE_CYC={gp_vector(record["one_cyc"])};',
            f'SOURCE_SIGN_LOG={gp_vector(record["sign_log"])};',
            f'SOURCE_CHARACTER={gp_vector(record["source_character"])};',
            f"\\r {GP}",
            "quit",
        )
    )
    started = time.monotonic()
    process = subprocess.Popen(
        [
            "/usr/bin/time",
            "-f",
            "ROUTE_WALL_SECONDS=%e\nROUTE_PEAK_KIB=%M",
            "gp",
            "-q",
        ],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=lambda: configure_child(address_space_bytes),
    )
    try:
        stdout, stderr = process.communicate(
            input=wrapper, timeout=timeout
        )
    except subprocess.TimeoutExpired as error:
        terminate_process_group(process)
        return {
            "case_id": record["case_id"],
            "kernel_index": record["kernel_index"],
            "status": "ROUTE_RESOURCE_CAP_TIMEOUT",
            "wall_seconds": round(time.monotonic() - started, 6),
            "stdout_tail": decoded_tail(error.stdout),
            "stderr_tail": ANSI.sub("", decoded_tail(error.stderr)),
        }
    except BaseException:
        terminate_process_group(process)
        raise

    timings = {}
    fatal_stderr = []
    for line in ANSI.sub("", stderr).splitlines():
        match = TIME_FIELDS.match(line)
        if match:
            timings[match.group(1).lower()] = match.group(2)
        elif line.lstrip().startswith("***") and "Warning:" in line:
            continue
        elif line.strip():
            fatal_stderr.append(line)
    parsed = parse_output(stdout)
    if (
        process.returncode
        or fatal_stderr
        or parsed.get("ROBLOT_SEXTIC_ROUTE_EXTRACTION") != "PASS"
    ):
        return {
            "case_id": record["case_id"],
            "kernel_index": record["kernel_index"],
            "status": "ROUTE_TOOL_OR_CONSTRUCTION_FAILURE",
            "returncode": process.returncode,
            "wall_seconds": float(
                timings.get(
                    "wall_seconds", round(time.monotonic() - started, 6)
                )
            ),
            "peak_kib": int(timings.get("peak_kib", 0)),
            "stdout_tail": stdout[-4000:],
            "stderr_tail": "\n".join(fatal_stderr)[-4000:],
        }

    result = {
        "case_id": record["case_id"],
        "kernel_index": record["kernel_index"],
        "status": "EXACT_ROUTE_COMPLETE",
        "primitive_conductor": parsed["PRIMITIVE_CONDUCTOR"],
        "primitive_ray_cyc": parsed["PRIMITIVE_RAY_CYC"],
        "primitive_character": parsed["PRIMITIVE_CHARACTER"],
        "primitive_kernel_hnf": parsed["PRIMITIVE_KERNEL_HNF"],
        "A3": parsed["A3"] == "1",
        "A3_local_rows": ast.literal_eval(
            parsed["A3_LOCAL_ROWS_[Nq,vS,vcond,frob_order_or_0,pass]"]
        ),
        "extra_finite_S_prime_count": int(
            parsed["EXTRA_FINITE_S_PRIME_COUNT"]
        ),
        "S_equals_S_extension": parsed["S_EQUALS_S_EXTENSION"] == "1",
        "wall_seconds": float(timings["wall_seconds"]),
        "peak_kib": int(timings["peak_kib"]),
    }
    result["field_key"] = field_key(record, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    expected_inventory = preregistration["source_hashes"][
        "data/roblot-sextic-kernel-inventory-v1.json"
    ]
    if sha256(INVENTORY) != expected_inventory:
        raise RuntimeError("frozen sextic inventory hash changed")
    sequential_expected = preregistration["preserved_sequential_run"][
        "sha256"
    ]
    if sha256(SEQUENTIAL) != sequential_expected:
        raise RuntimeError("preserved sequential partial hash changed")

    inventory = json.loads(INVENTORY.read_text())
    source = inventory["records"]
    route_cap = preregistration["route_stage"]
    records = []
    for offset, record in enumerate(source):
        result = run_record(
            record,
            route_cap["resource_cap_seconds_per_kernel"],
            route_cap["address_space_bytes_per_kernel"],
        )
        result["inventory_offset"] = offset
        records.append(result)
        if (offset + 1) % 50 == 0:
            print(f"ROUTE_PROGRESS={offset + 1}/{len(source)}", flush=True)

    sequential = json.loads(SEQUENTIAL.read_text())["records"]
    comparisons = 0
    for old in sequential:
        if old["status"] != "EXACT_SCREEN_COMPLETE":
            continue
        new = records[old["inventory_offset"]]
        if new["status"] != "EXACT_ROUTE_COMPLETE":
            raise RuntimeError("completed sequential route did not replay")
        expected = (
            old["primitive_conductor"],
            old["primitive_kernel_hnf"],
            old["A3"],
            old["S_equals_S_extension"],
        )
        observed = (
            new["primitive_conductor"],
            new["primitive_kernel_hnf"],
            new["A3"],
            new["S_equals_S_extension"],
        )
        if observed != expected:
            raise RuntimeError(
                f"{old['case_id']}: sequential route disagreement"
            )
        comparisons += 1

    complete = [
        record
        for record in records
        if record["status"] == "EXACT_ROUTE_COMPLETE"
    ]
    groups = defaultdict(list)
    for record in complete:
        groups[record["field_key"]].append(record)
    group_records = []
    for key, occurrences in sorted(groups.items()):
        potential = [
            record
            for record in occurrences
            if record["A3"] and record["S_equals_S_extension"]
        ]
        group_records.append(
            {
                "field_key": key,
                "occurrence_count": len(occurrences),
                "potentially_applicable_occurrence_count": len(potential),
                "representative_inventory_offset": occurrences[0][
                    "inventory_offset"
                ],
                "requires_field_certificate": bool(potential),
            }
        )

    payload = {
        "schema": "effective-stark-roblot-sextic-route-inventory-v1",
        "claim_tag": "OBSERVED",
        "status": (
            "COMPLETE_EXACT_ROUTE_INVENTORY"
            if len(complete) == len(records)
            else "INCOMPLETE_ROUTE_INVENTORY"
        ),
        "source": {
            "inventory": "data/roblot-sextic-kernel-inventory-v1.json",
            "inventory_sha256": expected_inventory,
            "preregistration": (
                "data/census-paper-preregistration-amendment-v9.json"
            ),
            "preregistration_sha256": sha256(PREREGISTRATION),
            "route_script": "scripts/extract_roblot_sextic_route.gp",
            "route_script_sha256": sha256(GP),
            "preserved_sequential_partial_sha256": sequential_expected,
        },
        "counts": {
            "inventory_kernels": len(records),
            "exact_route_complete": len(complete),
            "route_failures": len(records) - len(complete),
            "distinct_primitive_field_keys": len(groups),
            "field_keys_requiring_certificate": sum(
                group["requires_field_certificate"]
                for group in group_records
            ),
            "field_keys_short_circuited_by_exact_local_failure": sum(
                not group["requires_field_certificate"]
                for group in group_records
            ),
            "sequential_exact_route_comparisons": comparisons,
        },
        "runtime": {
            "sum_kernel_wall_seconds": round(
                sum(record["wall_seconds"] for record in records), 6
            ),
            "peak_kernel_memory_kib": max(
                (record.get("peak_kib", 0) for record in records),
                default=0,
            ),
        },
        "field_groups": group_records,
        "records": records,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
