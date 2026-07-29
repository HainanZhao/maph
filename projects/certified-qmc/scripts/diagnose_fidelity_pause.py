#!/usr/bin/env python3
"""Preserve and diagnose a fidelity-run throughput pause."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import chunk_records, file_sha256, read_chain


PILOT = ROOT / "build" / "native" / "streaming_pilot"
PILOT_AUDIT = (
    ROOT / "scripts" / "audit_workstream_b_streaming_pilot.py"
)
SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: diagnose_fidelity_pause.py "
            "PARTIAL_DATASET SOURCE OUTPUT RECORDED_AT_UTC"
        )
    dataset = Path(sys.argv[1]).resolve()
    source = Path(sys.argv[2]).resolve()
    output = Path(sys.argv[3]).resolve()
    recorded_at = sys.argv[4]
    if not recorded_at.endswith("Z"):
        raise ValueError("recorded timestamp must be UTC")

    telemetry_path = dataset / "telemetry.jsonl"
    manifest_path = dataset / "manifest.jsonl"
    telemetry = read_chain(telemetry_path)
    manifest = read_chain(manifest_path)
    if not telemetry or telemetry[-1]["event"] != "PAUSE":
        raise ValueError("dataset does not end in a throughput pause")
    chunks = chunk_records(manifest)
    for record in chunks:
        chunk = dataset / record["path"]
        if (
            chunk.stat().st_size != record["bytes"]
            or file_sha256(chunk) != record["sha256"]
        ):
            raise ValueError("partial chunk authentication failed")

    batch_records = [
        record for record in telemetry
        if record["event"] == "BATCH"
    ]
    cumulative_updates = sum(
        int(record["updates"]) for record in batch_records
    )
    cumulative_wall_ns = sum(
        int(record["wall_ns"]) for record in batch_records
    )

    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-pause-diagnostic-"
    ) as temporary:
        tmp = Path(temporary)
        pilot_d256_path = tmp / "pilot-d256.json"
        subprocess.run(
            [
                str(ROOT / ".venv" / "bin" / "python"),
                str(PILOT_AUDIT),
                "--source",
                str(source),
                "--output",
                str(pilot_d256_path),
            ],
            check=True,
        )
        pilot_d256 = json.loads(pilot_d256_path.read_text())

        schedule = json.loads(SCHEDULE.read_text())
        primes = [
            int(row["p"]) for row in schedule["primes"][:153]
        ]
        primes_path = tmp / "primes.txt"
        primes_path.write_text(
            "".join(f"{prime}\n" for prime in primes)
        )
        d3600_runs = []
        for trial in range(3):
            checkpoint = tmp / f"d3600-{trial}.bin"
            completed = subprocess.run(
                [
                    str(PILOT),
                    str(source),
                    str(primes_path),
                    "3600",
                    "4",
                    str(checkpoint),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            row = json.loads(completed.stdout)
            row["work_ns_per_update"] = (
                row["work_ns"] / row["work_updates"]
            )
            row["checkpoint_sha256"] = file_sha256(checkpoint)
            d3600_runs.append(row)

    d256_values = [
        Fraction(run["work_ns"], run["work_updates"])
        for run in pilot_d256["runs"]
    ]
    d3600_values = [
        Fraction(run["work_ns"], run["work_updates"])
        for run in d3600_runs
    ]
    payload = {
        "schema": (
            "certified-qmc-cycles-016-017-throughput-"
            "pause-transcript-v1"
        ),
        "recorded_at_utc": recorded_at,
        "claim_tags": {
            "partial_manifest_and_chunks": "VERIFIED",
            "timings_and_diagnosis": "NUMERICAL",
            "production_disposition": "PAUSED_INVESTIGATE",
            "partial_merit_values": "NOT_PROMOTED",
        },
        "partial_dataset": {
            "path": str(dataset.relative_to(ROOT)),
            "run_manifest_sha256": file_sha256(
                dataset / "run-manifest.json"
            ),
            "table_index_sha256": file_sha256(
                dataset / "table-index.json"
            ),
            "manifest_sha256": file_sha256(manifest_path),
            "manifest_last_line_sha256": (
                manifest[-1]["line_sha256"]
            ),
            "manifest_records": len(manifest),
            "authenticated_chunks": len(chunks),
            "authenticated_payload_bytes": sum(
                int(record["bytes"]) for record in chunks
            ),
            "telemetry_sha256": file_sha256(telemetry_path),
            "telemetry_last_line_sha256": (
                telemetry[-1]["line_sha256"]
            ),
        },
        "frozen_trigger": {
            "pilot_median_ns_per_update": "2.482743143245874",
            "drift_fraction": "0.25",
            "maximum_ns_per_update": "3.10342892905734250",
            "minimum_updates_before_enforcement": 5_000_000_000,
            "observed_cumulative_updates": cumulative_updates,
            "observed_cumulative_wall_ns": cumulative_wall_ns,
            "observed_cumulative_ns_per_update": (
                cumulative_wall_ns / cumulative_updates
            ),
            "driver_exit_code": 76,
            "pause_record": telemetry[-1],
            "triggered": True,
        },
        "investigation": {
            "host": "four-visible-core AMD EPYC 9354P virtual machine",
            "d256_same_host_rerun": {
                "runs_ns_per_update": [
                    float(value) for value in d256_values
                ],
                "median_ns_per_update": float(
                    statistics.median(d256_values)
                ),
                "all_oracles_pass": pilot_d256[
                    "decision"
                ]["correctness_pass"],
            },
            "d3600_same_host_single_process_runs": d3600_runs,
            "d3600_median_ns_per_update": float(
                statistics.median(d3600_values)
            ),
            "finding": (
                "The original single-process four-core evaluator "
                "remains below the frozen ceiling at both d=256 and "
                "d=3600. The production orchestration measurement, "
                "which includes one process launch and vector parse "
                "per prime, exceeded the +25% drift alarm on the VPS. "
                "This localizes the pause outside the frozen modular "
                "reduction kernel; it does not promote a universal "
                "causal performance claim."
            ),
        },
        "preservation": {
            "resume_under_v1_forbidden": True,
            "partial_dataset_retained": True,
            "threshold_changed_in_place": False,
            "required_next_step": (
                "human-authorized versioned preregistration and a "
                "clean output dataset"
            ),
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
