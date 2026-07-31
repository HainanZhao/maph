#!/usr/bin/env python3
"""Run Roblot's exact Theorem 7.1 screen on the frozen sextic kernels."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "roblot-sextic-kernel-inventory-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v7.json"
)
GP = ROOT / "scripts" / "screen_roblot_sextic_kernel.gp"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
TIME_FIELDS = re.compile(r"^SEXTIC_(WALL_SECONDS|PEAK_KIB)=(.+)$")
EXPECTED_CONTROLS = {
    "RQ-000021": (True, False),
    "RQ-000190": (True, False),
    "RQ-000419": (True, False),
    "RQ-002057": (False, True),
    "RQ-002955": (True, False),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gp_vector(values: list[int]) -> str:
    return "[" + ",".join(str(value) for value in values) + "]"


def parse_output(text: str) -> dict[str, str]:
    result = {}
    for line in text.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def decoded_tail(value: str | bytes | None, limit: int = 4000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    return value[-limit:]


def configure_child(byte_cap: int) -> None:
    os.setsid()
    resource.setrlimit(resource.RLIMIT_AS, (byte_cap, byte_cap))


def terminate_process_group(process: subprocess.Popen) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            return
        process.wait()


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
            "SEXTIC_WALL_SECONDS=%e\nSEXTIC_PEAK_KIB=%M",
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
            "source_character": record["source_character"],
            "status": "RESOURCE_CAP_TIMEOUT",
            "applicable": False,
            "wall_seconds": round(time.monotonic() - started, 6),
            "timeout_seconds": timeout,
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
        or parsed.get("ROBLOT_SEXTIC_KERNEL_SCREEN") != "PASS"
    ):
        return {
            "case_id": record["case_id"],
            "kernel_index": record["kernel_index"],
            "source_character": record["source_character"],
            "status": "TOOL_OR_CONSTRUCTION_FAILURE",
            "applicable": False,
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

    gates = {
        "A1": parsed["A1"] == "1",
        "A2": parsed["A2"] == "1",
        "A3": parsed["A3"] == "1",
        "S_equals_S_extension": parsed["S_EQUALS_S_EXTENSION"] == "1",
        "class_number_prime_to_3": (
            parsed["CLASS_NUMBER_PRIME_TO_3"] == "1"
        ),
        "no_wild_prime_above_3": parsed["WILD_ABOVE_3"] == "0",
    }
    applicable = all(gates.values())
    if applicable != (parsed["ROBLOT_THEOREM_7_1_APPLIES"] == "1"):
        raise RuntimeError(
            f"{record['case_id']}: parsed gate conjunction changed"
        )
    return {
        "case_id": record["case_id"],
        "kernel_index": record["kernel_index"],
        "source_character": record["source_character"],
        "status": "EXACT_SCREEN_COMPLETE",
        "applicable": applicable,
        **gates,
        "primitive_conductor": parsed["PRIMITIVE_CONDUCTOR"],
        "primitive_character": parsed["PRIMITIVE_CHARACTER"],
        "primitive_kernel_hnf": parsed["PRIMITIVE_KERNEL_HNF"],
        "relative_polynomial": parsed["RELATIVE_POLYNOMIAL"],
        "absolute_polynomial": parsed["ABSOLUTE_POLYNOMIAL"],
        "absolute_signature": parsed["ABSOLUTE_SIGNATURE"],
        "class_number": int(parsed["CLASS_NUMBER"]),
        "A3_local_rows": ast.literal_eval(
            parsed["A3_LOCAL_ROWS_[Nq,vS,vcond,frob_order_or_0,pass]"]
        ),
        "extra_finite_S_prime_count": int(
            parsed["EXTRA_FINITE_S_PRIME_COUNT"]
        ),
        "ramification_above_3": ast.literal_eval(
            parsed["RAMIFICATION_ABOVE_3_[eK,fK,eH,fH,eRel]"]
        ),
        "maximum_relative_e_above_3": int(
            parsed["MAXIMUM_RELATIVE_E_ABOVE_3"]
        ),
        "wall_seconds": float(timings["wall_seconds"]),
        "peak_kib": int(timings["peak_kib"]),
    }


def validate_controls(records: list[dict]) -> dict:
    by_case = {
        record["case_id"]: record
        for record in records
        if record["kernel_index"] == 1
    }
    results = {}
    for case_id, (expected_applies, expected_wild) in (
        EXPECTED_CONTROLS.items()
    ):
        if case_id not in by_case:
            continue
        record = by_case[case_id]
        passed = (
            record["status"] == "EXACT_SCREEN_COMPLETE"
            and record["applicable"] == expected_applies
            and record["no_wild_prime_above_3"] != expected_wild
        )
        results[case_id] = {
            "expected_applicable": expected_applies,
            "expected_wild_above_3": expected_wild,
            "passed": passed,
        }
        if not passed:
            raise RuntimeError(f"{case_id}: frozen control disagrees")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    frozen_hash = preregistration["inventory"]["sha256"]
    if sha256(INVENTORY) != frozen_hash:
        raise RuntimeError("sextic kernel inventory hash changed")
    timeout = preregistration["resource_caps"]["wall_seconds_per_kernel"]
    address_space_bytes = preregistration["resource_caps"][
        "address_space_bytes_per_kernel"
    ]
    inventory = json.loads(INVENTORY.read_text())
    source = inventory["records"]
    stop = len(source) if args.limit is None else args.start + args.limit
    selected = source[args.start:stop]
    records = []
    if args.checkpoint and args.checkpoint.exists():
        checkpoint = json.loads(args.checkpoint.read_text())
        if (
            checkpoint["inventory_sha256"] != frozen_hash
            or checkpoint["selection_start"] != args.start
            or checkpoint["selection_count"] != len(selected)
        ):
            raise RuntimeError("checkpoint does not match frozen selection")
        records = checkpoint["records"]
        expected_offsets = list(
            range(args.start, args.start + len(records))
        )
        if [record["inventory_offset"] for record in records] != (
            expected_offsets
        ):
            raise RuntimeError("checkpoint offsets are not contiguous")

    remaining = selected[len(records) :]
    first_offset = args.start + len(records)
    for offset, record in enumerate(remaining, start=first_offset):
        result = run_record(record, timeout, address_space_bytes)
        result["inventory_offset"] = offset
        records.append(result)
        if args.checkpoint:
            checkpoint = {
                "schema": (
                    "effective-stark-roblot-sextic-"
                    "population-checkpoint-v1"
                ),
                "inventory_sha256": frozen_hash,
                "selection_start": args.start,
                "selection_count": len(selected),
                "records": records,
            }
            temporary = args.checkpoint.with_suffix(
                args.checkpoint.suffix + ".tmp"
            )
            temporary.write_text(
                json.dumps(checkpoint, indent=2, sort_keys=True) + "\n"
            )
            temporary.replace(args.checkpoint)
        if (offset + 1) % 25 == 0:
            print(
                f"SEXTIC_PROGRESS={offset + 1}/{len(source)}",
                flush=True,
            )

    complete = args.start == 0 and len(selected) == len(source)
    screened = [
        record
        for record in records
        if record["status"] == "EXACT_SCREEN_COMPLETE"
    ]
    applicable = [record for record in screened if record["applicable"]]
    failures = [
        record
        for record in records
        if record["status"] != "EXACT_SCREEN_COMPLETE"
    ]
    controls = validate_controls(records)
    payload = {
        "schema": "effective-stark-roblot-sextic-population-v1",
        "claim_tag": "OBSERVED",
        "status": (
            "COMPLETE_EXACT_POPULATION_SCREEN"
            if complete
            else "PILOT_OR_PARTIAL_EXACT_POPULATION_SCREEN"
        ),
        "claim_boundary": {
            "screened": "Roblot 2013 Theorem 7.1 hypotheses only",
            "phase_or_lprime_target_opened": False,
            "eligibility_is_not_a_stark_identity": True,
        },
        "source": {
            "inventory": "data/roblot-sextic-kernel-inventory-v1.json",
            "inventory_sha256": frozen_hash,
            "preregistration": (
                "data/census-paper-preregistration-amendment-v7.json"
            ),
            "preregistration_sha256": sha256(PREREGISTRATION),
            "screen_script": "scripts/screen_roblot_sextic_kernel.gp",
            "screen_script_sha256": sha256(GP),
            "selection_start": args.start,
            "selection_count": len(selected),
            "resource_cap_seconds_per_kernel": timeout,
            "address_space_bytes_per_kernel": address_space_bytes,
        },
        "counts": {
            "inventory_kernels": len(source),
            "attempted_kernels": len(records),
            "exact_screen_complete": len(screened),
            "applicable_kernels": len(applicable),
            "applicable_rows": len(
                {record["case_id"] for record in applicable}
            ),
            "nonapplicable_kernels": len(screened) - len(applicable),
            "tool_or_resource_failures": len(failures),
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
        "frozen_control_replay": controls,
        "records": records,
    }
    output = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
