#!/usr/bin/env python3
"""Certify residual sextic 3-class obstructions by unramified cubics."""

from __future__ import annotations

import argparse
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
FIELDS = ROOT / "artifacts" / "roblot-sextic-field-inventory-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v11.json"
)
GP = ROOT / "scripts" / "certify_roblot_sextic_3class.gp"
TIME_FIELDS = re.compile(r"^THREECLASS_(WALL_SECONDS|PEAK_KIB)=(.+)$")


def run_record(
    record: dict, timeout: int, address_space_bytes: int
) -> dict:
    key = record["field_key"]
    wrapper = "\n".join(
        (
            f'FIELD_KEY="{key}";',
            f'ABSOLUTE_POLYNOMIAL={record["absolute_polynomial"]};',
            f"\\r {GP}",
            "quit",
        )
    )
    started = time.monotonic()
    process = subprocess.Popen(
        [
            "/usr/bin/time",
            "-f",
            "THREECLASS_WALL_SECONDS=%e\nTHREECLASS_PEAK_KIB=%M",
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
            "status": "RESOURCE_CAP_TIMEOUT",
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
        or parsed.get("ROBLOT_SEXTIC_3CLASS_CERTIFICATE") != "PASS"
    ):
        return {
            "field_key": key,
            "status": "TOOL_OR_CERTIFICATE_FAILURE",
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

    return {
        "field_key": key,
        "status": "EXACT_UNRAMIFIED_CYCLIC_CUBIC",
        "computed_class_group_cyc": parsed["COMPUTED_CLASS_GROUP_CYC"],
        "index_three_subgroup_hnf": parsed[
            "INDEX_THREE_SUBGROUP_HNF"
        ],
        "relative_cubic_polynomial": parsed[
            "RELATIVE_CUBIC_POLYNOMIAL"
        ],
        "relative_cubic_root_count_in_H": int(
            parsed["RELATIVE_CUBIC_ROOT_COUNT_IN_H"]
        ),
        "relative_discriminant_ideal": parsed[
            "RELATIVE_DISCRIMINANT_IDEAL"
        ],
        "relative_discriminant_ideal_norm": int(
            parsed["RELATIVE_DISCRIMINANT_IDEAL_NORM"]
        ),
        "cubic_polynomial_discriminant_square": (
            parsed["CUBIC_POLYNOMIAL_DISCRIMINANT_SQUARE"] == "1"
        ),
        "three_divides_class_number_proved": (
            parsed["THREE_DIVIDES_CLASS_NUMBER_PROVED"] == "1"
        ),
        "wall_seconds": float(timings["wall_seconds"]),
        "peak_kib": int(timings["peak_kib"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    if sha256(FIELDS) != preregistration["source"]["sha256"]:
        raise RuntimeError("field inventory hash changed")
    field_inventory = json.loads(FIELDS.read_text())
    by_key = {
        record["field_key"]: record
        for record in field_inventory["records"]
    }
    controls = preregistration["controls"]
    residual = [
        record["field_key"]
        for record in field_inventory["records"]
        if record["status"] == "NEEDS_STRONG_3_CLASS_CERTIFICATE"
    ]
    if len(residual) != preregistration["population"][
        "candidate_3_divisible_field_keys"
    ]:
        raise RuntimeError("residual 3-class population changed")
    selected = controls + residual
    caps = preregistration["resource_caps"]
    records = []
    for index, key in enumerate(selected, start=1):
        result = run_record(
            by_key[key],
            caps["wall_seconds_per_field"],
            caps["address_space_bytes_per_field"],
        )
        result["population"] = (
            "FULL_BNFCERTIFY_CONTROL"
            if key in controls
            else "RESIDUAL_FIELD"
        )
        records.append(result)
        if index % 10 == 0:
            print(
                f"THREECLASS_PROGRESS={index}/{len(selected)}",
                flush=True,
            )

    exact = [
        record
        for record in records
        if record["status"] == "EXACT_UNRAMIFIED_CYCLIC_CUBIC"
    ]
    payload = {
        "schema": "effective-stark-roblot-sextic-3class-v1",
        "claim_tag": "PROVED",
        "status": (
            "COMPLETE_EXACT_3CLASS_OBSTRUCTION_POPULATION"
            if len(exact) == len(records)
            else "INCOMPLETE_3CLASS_OBSTRUCTION_POPULATION"
        ),
        "proof": (
            "An irreducible cyclic cubic extension with relative "
            "discriminant ideal 1 is an unramified cyclic cubic "
            "extension, so class field theory gives 3 | h_H."
        ),
        "source": {
            "field_inventory": (
                "artifacts/roblot-sextic-field-inventory-v1.json"
            ),
            "field_inventory_sha256": preregistration["source"][
                "sha256"
            ],
            "preregistration": (
                "data/census-paper-preregistration-amendment-v11.json"
            ),
            "preregistration_sha256": sha256(PREREGISTRATION),
            "certificate_script": (
                "scripts/certify_roblot_sextic_3class.gp"
            ),
            "certificate_script_sha256": sha256(GP),
        },
        "counts": {
            "full_bnfcertify_controls": len(controls),
            "residual_fields": len(residual),
            "attempted_certificates": len(records),
            "exact_unramified_cyclic_cubics": len(exact),
            "failures": len(records) - len(exact),
        },
        "runtime": {
            "sum_field_wall_seconds": round(
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
