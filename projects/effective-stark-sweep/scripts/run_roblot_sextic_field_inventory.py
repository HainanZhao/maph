#!/usr/bin/env python3
"""Certify each deduplicated sextic field key once."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import subprocess
import time

from run_roblot_sextic_population import (
    ANSI,
    configure_child,
    decoded_tail,
    parse_output,
    sha256,
    terminate_process_group,
)


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "roblot-sextic-kernel-inventory-v1.json"
ROUTES = ROOT / "artifacts" / "roblot-sextic-route-inventory-v1.json"
SEQUENTIAL = (
    ROOT
    / "artifacts"
    / "roblot-sextic-population-sequential-partial-v0.json"
)
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v10.json"
)
FIELD_GP = ROOT / "scripts" / "screen_roblot_sextic_field.gp"
TIME_FIELDS = re.compile(r"^FIELD_(WALL_SECONDS|PEAK_KIB)=(.+)$")


def run_field(
    key: str,
    inventory_record: dict,
    route_record: dict,
    timeout: int,
    address_space_bytes: int,
) -> dict:
    wrapper = "\n".join(
        (
            f'FIELD_KEY="{key}";',
            f'D_VALUE={inventory_record["d"]};',
            f'PRIMITIVE_CONDUCTOR={route_record["primitive_conductor"]};',
            (
                "PRIMITIVE_KERNEL_HNF="
                f'{route_record["primitive_kernel_hnf"]};'
            ),
            "DEFER_FULL_CERTIFICATE=1;",
            f"\\r {FIELD_GP}",
            "quit",
        )
    )
    started = time.monotonic()
    process = subprocess.Popen(
        [
            "/usr/bin/time",
            "-f",
            "FIELD_WALL_SECONDS=%e\nFIELD_PEAK_KIB=%M",
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
            "field_key": key,
            "status": "FIELD_RESOURCE_CAP_TIMEOUT",
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
        or parsed.get("ROBLOT_SEXTIC_FIELD_SCREEN") != "PASS"
    ):
        return {
            "field_key": key,
            "status": "FIELD_TOOL_OR_CONSTRUCTION_FAILURE",
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

    provenance = parsed["CLASS_NUMBER_GATE_PROVENANCE"]
    status = (
        "EXACT_FIELD_GATES_COMPLETE"
        if provenance != (
            "CANDIDATE_DIVISIBLE_BY_3_NEEDS_STRONG_CERTIFICATE"
        )
        else "NEEDS_STRONG_3_CLASS_CERTIFICATE"
    )
    return {
        "field_key": key,
        "status": status,
        "certificate_source": "DEDUPLICATED_FIELD_SCREEN",
        "relative_polynomial": parsed["RELATIVE_POLYNOMIAL"],
        "absolute_polynomial": parsed["ABSOLUTE_POLYNOMIAL"],
        "absolute_signature": parsed["ABSOLUTE_SIGNATURE"],
        "computed_class_number": int(parsed["CLASS_NUMBER"]),
        "quotient_bnfcertify": (
            parsed["QUOTIENT_BNFCERTIFY"] == "1"
        ),
        "full_bnfcertify": int(
            parsed["FULL_BNFCERTIFY_OR_MINUS_ONE"]
        ),
        "class_number_gate_provenance": provenance,
        "class_number_prime_to_3": (
            parsed["CLASS_NUMBER_PRIME_TO_3"] == "1"
            if status == "EXACT_FIELD_GATES_COMPLETE"
            else None
        ),
        "A1": parsed["A1"] == "1",
        "A2": parsed["A2"] == "1",
        "ramification_above_3": ast.literal_eval(
            parsed["RAMIFICATION_ABOVE_3_[eK,fK,eH,fH,eRel]"]
        ),
        "maximum_relative_e_above_3": int(
            parsed["MAXIMUM_RELATIVE_E_ABOVE_3"]
        ),
        "no_wild_prime_above_3": parsed["WILD_ABOVE_3"] == "0",
        "wall_seconds": float(timings["wall_seconds"]),
        "peak_kib": int(timings["peak_kib"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    expected_routes = preregistration["source_hashes"][
        "artifacts/roblot-sextic-route-inventory-v1.json"
    ]
    if sha256(ROUTES) != expected_routes:
        raise RuntimeError("route inventory hash changed")
    routes = json.loads(ROUTES.read_text())
    inventory = json.loads(INVENTORY.read_text())["records"]
    sequential = json.loads(SEQUENTIAL.read_text())["records"]
    route_by_offset = {
        record["inventory_offset"]: record for record in routes["records"]
    }

    seeded = {}
    for record in sequential:
        if record["status"] != "EXACT_SCREEN_COMPLETE":
            continue
        route = route_by_offset[record["inventory_offset"]]
        key = route["field_key"]
        candidate = {
            "field_key": key,
            "status": "EXACT_FIELD_GATES_COMPLETE",
            "certificate_source": "REUSED_SEQUENTIAL_FULL_BNFCERTIFY",
            "relative_polynomial": record["relative_polynomial"],
            "absolute_polynomial": record["absolute_polynomial"],
            "absolute_signature": record["absolute_signature"],
            "computed_class_number": record["class_number"],
            "quotient_bnfcertify": None,
            "full_bnfcertify": 1,
            "class_number_gate_provenance": "FULL_BNFCERTIFY",
            "class_number_prime_to_3": (
                record["class_number_prime_to_3"]
            ),
            "A1": record["A1"],
            "A2": record["A2"],
            "ramification_above_3": record["ramification_above_3"],
            "maximum_relative_e_above_3": (
                record["maximum_relative_e_above_3"]
            ),
            "no_wild_prime_above_3": (
                record["no_wild_prime_above_3"]
            ),
            "wall_seconds": record["wall_seconds"],
            "peak_kib": record["peak_kib"],
        }
        if key in seeded:
            invariant_fields = (
                "computed_class_number",
                "class_number_prime_to_3",
                "A1",
                "A2",
                "maximum_relative_e_above_3",
                "no_wild_prime_above_3",
            )
            if any(
                seeded[key][field] != candidate[field]
                for field in invariant_fields
            ):
                raise RuntimeError(
                    f"{key}: sequential field certificates disagree"
                )
        else:
            seeded[key] = candidate

    required_groups = [
        group
        for group in routes["field_groups"]
        if group["requires_field_certificate"]
    ]
    route_records_by_key = {}
    for route in routes["records"]:
        if (
            route["status"] == "EXACT_ROUTE_COMPLETE"
            and route["A3"]
            and route["S_equals_S_extension"]
        ):
            route_records_by_key.setdefault(route["field_key"], route)

    field_cap = json.loads(
        (
            ROOT / "data" / "census-paper-preregistration-amendment-v9.json"
        ).read_text()
    )["field_stage"]
    records = []
    for index, group in enumerate(required_groups, start=1):
        key = group["field_key"]
        if key in seeded:
            result = seeded[key]
        else:
            route = route_records_by_key[key]
            result = run_field(
                key,
                inventory[route["inventory_offset"]],
                route,
                field_cap["resource_cap_seconds_per_distinct_key"],
                field_cap["address_space_bytes_per_distinct_key"],
            )
        records.append(result)
        if index % 25 == 0:
            print(
                f"FIELD_PROGRESS={index}/{len(required_groups)}",
                flush=True,
            )

    status_counts = {}
    for record in records:
        status_counts[record["status"]] = (
            status_counts.get(record["status"], 0) + 1
        )
    payload = {
        "schema": "effective-stark-roblot-sextic-field-inventory-v1",
        "claim_tag": "OBSERVED",
        "status": "DEDUPLICATED_FIELD_GATE_SWEEP_COMPLETE",
        "claim_boundary": {
            "exact_field_gates": (
                "A1, A2, ramification above 3, and class-number "
                "nondivisibility when certified"
            ),
            "candidate_3_divisible_fields": (
                "remain open pending a strong exact certificate"
            ),
            "eligibility_is_not_a_stark_identity": True,
        },
        "source": {
            "route_inventory": (
                "artifacts/roblot-sextic-route-inventory-v1.json"
            ),
            "route_inventory_sha256": expected_routes,
            "preregistration": (
                "data/census-paper-preregistration-amendment-v10.json"
            ),
            "preregistration_sha256": sha256(PREREGISTRATION),
            "field_script": "scripts/screen_roblot_sextic_field.gp",
            "field_script_sha256": sha256(FIELD_GP),
        },
        "counts": {
            "required_distinct_field_keys": len(required_groups),
            "reused_sequential_field_certificates": sum(
                record["certificate_source"]
                == "REUSED_SEQUENTIAL_FULL_BNFCERTIFY"
                for record in records
            ),
            "new_deduplicated_field_screens": sum(
                record["certificate_source"]
                == "DEDUPLICATED_FIELD_SCREEN"
                for record in records
                if "certificate_source" in record
            ),
            "status": dict(sorted(status_counts.items())),
        },
        "runtime": {
            "sum_recorded_wall_seconds_including_reused": round(
                sum(record["wall_seconds"] for record in records), 6
            ),
            "peak_field_memory_kib": max(
                (record.get("peak_kib", 0) for record in records),
                default=0,
            ),
        },
        "records": records,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
