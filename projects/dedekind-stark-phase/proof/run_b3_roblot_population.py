#!/usr/bin/env python3
"""Run the exact A1--A3 screen over the frozen B3 kernel inventory."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "artifacts" / "b3-quartic-kernel-inventory-v1.json"
GP = ROOT / "proof" / "screen_b3_roblot_kernel.gp"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
TIME_FIELDS = re.compile(r"^B3_(WALL_SECONDS|PEAK_KIB)=(.+)$")


def gp_vector(values: list[int]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"


def parse_output(text: str) -> dict[str, str]:
    result = {}
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def run_record(record: dict, timeout: int) -> dict:
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
    try:
        completed = subprocess.run(
            [
                "/usr/bin/time",
                "-f",
                "B3_WALL_SECONDS=%e\nB3_PEAK_KIB=%M",
                "gp",
                "-q",
            ],
            cwd=ROOT,
            input=wrapper,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "case_id": record["case_id"],
            "kernel_index": record["kernel_index"],
            "source_character": record["source_character"],
            "status": "RESOURCE_CAP_TIMEOUT",
            "eligible": False,
            "wall_seconds": round(time.monotonic() - started, 6),
            "timeout_seconds": timeout,
            "stdout_tail": (error.stdout or "")[-4000:],
            "stderr_tail": ANSI.sub("", error.stderr or "")[-4000:],
        }

    timings = {}
    fatal_stderr = []
    for line in ANSI.sub("", completed.stderr).splitlines():
        match = TIME_FIELDS.match(line)
        if match:
            timings[match.group(1).lower()] = match.group(2)
        elif line.lstrip().startswith("***") and "Warning:" in line:
            continue
        elif line.strip():
            fatal_stderr.append(line)
    parsed = parse_output(completed.stdout)
    if (
        completed.returncode
        or fatal_stderr
        or parsed.get("B3_ROBLOT_KERNEL_SCREEN") != "PASS"
    ):
        return {
            "case_id": record["case_id"],
            "kernel_index": record["kernel_index"],
            "source_character": record["source_character"],
            "status": "TOOL_OR_CONSTRUCTION_FAILURE",
            "eligible": False,
            "returncode": completed.returncode,
            "wall_seconds": float(
                timings.get(
                    "wall_seconds", round(time.monotonic() - started, 6)
                )
            ),
            "peak_kib": int(timings.get("peak_kib", 0)),
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": "\n".join(fatal_stderr)[-4000:],
        }

    a1 = parsed["A1"] == "1"
    a2 = parsed["A2"] == "1"
    a3 = parsed["A3"] == "1"
    eligible = a1 and a2 and a3 and parsed["ROBLOT_ELIGIBLE"] == "1"
    return {
        "case_id": record["case_id"],
        "kernel_index": record["kernel_index"],
        "source_character": record["source_character"],
        "status": "EXACT_SCREEN_COMPLETE",
        "eligible": eligible,
        "A1": a1,
        "A2": a2,
        "A3": a3,
        "primitive_conductor": parsed["PRIMITIVE_CONDUCTOR"],
        "primitive_ray_cyc": parsed["PRIMITIVE_RAY_CYC"],
        "primitive_character": parsed["PRIMITIVE_CHARACTER"],
        "primitive_kernel_hnf": parsed["PRIMITIVE_KERNEL_HNF"],
        "relative_polynomial": parsed["RELATIVE_POLYNOMIAL"],
        "absolute_polynomial": parsed["ABSOLUTE_POLYNOMIAL"],
        "absolute_signature": parsed["ABSOLUTE_SIGNATURE"],
        "absolute_automorphism_count": int(
            parsed["ABSOLUTE_AUTOMORPHISM_COUNT"]
        ),
        "Kplus_polynomial": parsed["KPLUS_POLYNOMIAL"],
        "A3_local_rows": ast.literal_eval(
            parsed["A3_LOCAL_ROWS_[Nq,vS,vcond,frob_order_or_0,pass]"]
        ),
        "wall_seconds": float(timings["wall_seconds"]),
        "peak_kib": int(timings["peak_kib"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    source = inventory["records"]
    stop = len(source) if args.limit is None else args.start + args.limit
    selected = source[args.start:stop]
    records = []
    for offset, record in enumerate(selected, start=args.start):
        result = run_record(record, args.timeout)
        result["inventory_offset"] = offset
        records.append(result)
        if (offset + 1) % 25 == 0:
            print(
                f"B3_PROGRESS={offset + 1}/{len(source)}",
                flush=True,
            )

    complete = args.start == 0 and len(selected) == len(source)
    screened = [
        record for record in records if record["status"] == "EXACT_SCREEN_COMPLETE"
    ]
    eligible = [record for record in screened if record["eligible"]]
    failures = [
        record for record in records if record["status"] != "EXACT_SCREEN_COMPLETE"
    ]
    payload = {
        "schema": "dedekind-stark-b3-roblot-population-v1",
        "claim_tag": "OBSERVED",
        "status": (
            "COMPLETE_EXACT_POPULATION_SCREEN"
            if complete
            else "PILOT_OR_PARTIAL_EXACT_POPULATION_SCREEN"
        ),
        "claim_boundary": {
            "screened": "Roblot A1--A3 only",
            "phase_or_lprime_target_opened": False,
            "eligibility_is_not_a_stark_identity": True,
        },
        "source": {
            "inventory": "artifacts/b3-quartic-kernel-inventory-v1.json",
            "inventory_status": inventory["status"],
            "selection_start": args.start,
            "selection_count": len(selected),
            "resource_cap_seconds_per_kernel": args.timeout,
        },
        "counts": {
            "inventory_kernels": len(source),
            "attempted_kernels": len(records),
            "exact_screen_complete": len(screened),
            "eligible_kernels": len(eligible),
            "eligible_rows": len({record["case_id"] for record in eligible}),
            "noneligible_kernels": len(screened) - len(eligible),
            "tool_or_resource_failures": len(failures),
        },
        "runtime": {
            "sum_kernel_wall_seconds": round(
                sum(record["wall_seconds"] for record in records), 6
            ),
            "peak_kernel_memory_kib": max(
                (record.get("peak_kib", 0) for record in records), default=0
            ),
        },
        "records": records,
    }
    output = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
