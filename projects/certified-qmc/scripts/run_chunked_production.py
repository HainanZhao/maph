#!/usr/bin/env python3
"""Run or resume deterministic per-prime chunk production."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import signal
import struct
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.chunked_table import (
    ZERO_HASH,
    append_record,
    canonical_bytes,
    file_sha256,
    iter_chain,
    safe_chunk_path,
)


BINARY = ROOT / "build" / "production" / "production_prime"
SOURCE = ROOT / "native" / "production_prime.c"
PILOT_KERNEL = ROOT / "native" / "streaming_pilot.c"
FROZEN_PILOT_KERNEL_SHA256 = (
    "f21c5cc9ab825ea402258fd5832e7ee0b33ebf5f60c2c3fab9cec7484339dd42"
)


def cpu_model() -> str:
    for line in Path("/proc/cpuinfo").read_text().splitlines():
        if line.lower().startswith("model name"):
            return line.split(":", 1)[1].strip()
    return platform.processor() or "UNKNOWN"


def normalized_ldd(text: str) -> list[str]:
    normalized = []
    for line in text.splitlines():
        content = line.strip()
        if " (" in content:
            content = content.rsplit(" (", 1)[0]
        normalized.append(content)
    return normalized


def canonical_sha(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def parse_generator(path: Path, dimension: int) -> list[int]:
    values = []
    for line in path.read_text().splitlines():
        row, component = map(int, line.split())
        if row != len(values) + 1:
            raise ValueError("vector rows are not sequential")
        values.append(component)
    if len(values) < dimension:
        raise ValueError("vector is shorter than requested dimension")
    return values[:dimension]


def prefix_hashes(generator: list[int]) -> list[str]:
    # Canonical compact JSON for an integer vector is exactly
    # ``[v1,v2,...]``. Copying the incremental SHA state before adding
    # the closing bracket preserves the definition without the
    # quadratic re-serialization cost at d=3600.
    state = sha256()
    state.update(b"[")
    result = []
    for index, value in enumerate(generator):
        if index:
            state.update(b",")
        state.update(str(value).encode("ascii"))
        completed = state.copy()
        completed.update(b"]")
        result.append(completed.hexdigest())
    return result


def load_inputs(spec_path: Path) -> tuple[dict, dict, list[int]]:
    spec = json.loads(spec_path.read_text())
    schedule_path = ROOT / spec["prime_schedule"]
    schedule = json.loads(schedule_path.read_text())
    schedule_manifest = json.loads(
        (ROOT / spec["prime_schedule_manifest"]).read_text()
    )
    if file_sha256(schedule_path) != schedule_manifest["schedule"]["sha256"]:
        raise RuntimeError("prime schedule manifest mismatch")
    if not schedule_manifest["gate"]["cycle_014_exit_gate_passed"]:
        raise RuntimeError("prime schedule gate is not passed")
    primes = [int(row["p"]) for row in schedule["primes"]]
    return spec, schedule_manifest, primes


def table_index(spec: dict) -> dict:
    tables = []
    source_cache: dict[tuple[str, int], list[int]] = {}
    for table in spec["tables"]:
        source_path = ROOT / table["source_path"]
        if file_sha256(source_path) != table["source_file_sha256"]:
            raise RuntimeError("input vector hash mismatch")
        cache_key = (str(source_path), int(table["dimension"]))
        generator = source_cache.setdefault(
            cache_key,
            parse_generator(source_path, int(table["dimension"])),
        )
        public = {
            key: value
            for key, value in table.items()
            if key != "source_path"
        }
        public["generator_prefix_sha256"] = prefix_hashes(generator)
        tables.append(public)
    payload = {
        "schema": "certified-qmc-table-index-v1",
        "run_id": spec["run_id"],
        "vectors_embedded": False,
        "prefix_hash_definition": (
            "SHA-256 of canonical compact JSON integer prefix"
        ),
        "tables": tables,
    }
    payload["index_sha256"] = canonical_sha(payload)
    return payload


def build_manifest(
    spec_path: Path,
    spec: dict,
    schedule_manifest: dict,
    index: dict,
) -> dict:
    if file_sha256(PILOT_KERNEL) != FROZEN_PILOT_KERNEL_SHA256:
        raise RuntimeError("frozen pilot kernel hash changed")
    subprocess.run(
        ["make", "-C", str(ROOT / "production"), "all"],
        check=True,
        capture_output=True,
        text=True,
    )
    linked = subprocess.check_output(["ldd", str(BINARY)], text=True)
    if "fftw" in linked.lower():
        raise RuntimeError("production binary unexpectedly links FFTW")
    compiler = subprocess.check_output(
        ["cc", "--version"], text=True
    ).splitlines()[0]
    chunking = {
        "prefix_block_size": spec["prefix_block_size"],
        "encoding": "unsigned 64-bit little-endian",
        "manifest": "manifest.jsonl",
        "manifest_chain": (
            "each canonical JSON line contains previous_line_sha256 "
            "and its own line_sha256"
        ),
        "universal_overflow_prime_indices": [3738, 3739],
    }
    if "parallel_workers" in spec:
        chunking["parallel_workers"] = int(spec["parallel_workers"])
    payload = {
        "schema": "certified-qmc-run-manifest-v1",
        "run_id": spec["run_id"],
        "production_spec": {
            "path": str(spec_path.relative_to(ROOT)),
            "sha256": file_sha256(spec_path),
        },
        "compiler": {
            "version": compiler,
            "flags": (
                "-O3 -std=c11 -Wall -Wextra -Wpedantic "
                "-D_POSIX_C_SOURCE=200809L"
            ),
            "cpu_model": cpu_model(),
            "platform": platform.platform(),
        },
        "kernel": {
            "representation": "plain __int128 remainder",
            "production_source": str(SOURCE.relative_to(ROOT)),
            "production_source_sha256": file_sha256(SOURCE),
            "pilot_source": str(PILOT_KERNEL.relative_to(ROOT)),
            "pilot_source_sha256": file_sha256(PILOT_KERNEL),
            "binary_sha256": file_sha256(BINARY),
            "linked_libraries": normalized_ldd(linked),
            "optimization_changes": False,
        },
        "prime_schedule": {
            "path": spec["prime_schedule"],
            "sha256": schedule_manifest["schedule"]["sha256"],
            "verification_manifest": spec["prime_schedule_manifest"],
            "verification_manifest_sha256": file_sha256(
                ROOT / spec["prime_schedule_manifest"]
            ),
        },
        "input_tables": [
            {
                key: table[key]
                for key in (
                    "table_id",
                    "source_id",
                    "source_citation",
                    "source_snapshot_sha256",
                    "source_file_sha256",
                    "N",
                    "dimension",
                    "weight_power",
                    "work_prime_count",
                )
            }
            for table in spec["tables"]
        ],
        "preregistrations": {
            path: file_sha256(ROOT / path)
            for path in spec["preregistrations"]
        },
        "chunking": chunking,
        "table_index_sha256": index["index_sha256"],
    }
    if "throughput_monitor" in spec:
        payload["throughput_monitor"] = spec["throughput_monitor"]
    payload["run_manifest_sha256"] = canonical_sha(payload)
    return payload


def write_exact(path: Path, value: dict) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path.exists():
        if path.read_text() != rendered:
            raise RuntimeError(f"resume metadata mismatch: {path.name}")
    else:
        path.write_text(rendered)


def scan_existing_chunks(
    output: Path, manifest_path: Path
) -> tuple[set[tuple[str, int, int, int]], dict | None, int, int]:
    """Authenticate a resumable dataset with bounded manifest memory."""
    seen: set[tuple[str, int, int, int]] = set()
    final_record = None
    chunk_count = 0
    payload_bytes = 0
    for record in iter_chain(manifest_path):
        final_record = record
        if record["event"] != "CHUNK":
            continue
        key = (
            record["table_id"],
            int(record["prime_index"]),
            int(record["dimension_start"]),
            int(record["dimension_end"]),
        )
        if key in seen:
            raise RuntimeError("duplicate chunk in manifest")
        seen.add(key)
        chunk = safe_chunk_path(output, record["path"])
        if not chunk.is_file():
            raise RuntimeError("manifested chunk is missing")
        if chunk.stat().st_size != int(record["bytes"]):
            raise RuntimeError("manifested chunk length mismatch")
        if file_sha256(chunk) != record["sha256"]:
            raise RuntimeError("manifested chunk hash mismatch")
        chunk_count += 1
        payload_bytes += int(record["bytes"])
    return seen, final_record, chunk_count, payload_bytes


def tasks(spec: dict, primes: list[int]) -> list[dict]:
    result = []
    block_size = int(spec["prefix_block_size"])
    for table in spec["tables"]:
        prime_indices = [
            *range(int(table["work_prime_count"])),
            3738,
            3739,
        ]
        for prime_index in prime_indices:
            for start in range(1, int(table["dimension"]) + 1, block_size):
                end = min(start + block_size - 1, int(table["dimension"]))
                result.append(
                    {
                        "table": table,
                        "prime_index": prime_index,
                        "prime": primes[prime_index],
                        "role": (
                            "WORK"
                            if prime_index < table["work_prime_count"]
                            else "OVERFLOW"
                        ),
                        "start": start,
                        "end": end,
                    }
                )
    return result


def evaluate_prime(
    table: dict,
    prime_index: int,
    prime: int,
) -> tuple[bytes, int]:
    source_path = ROOT / table["source_path"]
    with tempfile.NamedTemporaryFile(
        prefix="certified-qmc-prime-",
        suffix=".bin",
        delete=False,
    ) as temporary:
        raw_path = Path(temporary.name)
    started = time.monotonic_ns()
    try:
        subprocess.run(
            [
                str(BINARY),
                str(source_path),
                str(table["N"]),
                str(table["dimension"]),
                str(table["weight_power"]),
                str(prime),
                str(raw_path),
            ],
            check=True,
        )
        raw = raw_path.read_bytes()
    finally:
        raw_path.unlink(missing_ok=True)
    return raw, time.monotonic_ns() - started


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stop-after-new-chunks", type=int)
    parser.add_argument("--pause-after-new-chunks", type=int)
    args = parser.parse_args()
    spec_path = args.spec.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    spec, schedule_manifest, primes = load_inputs(spec_path)
    index = table_index(spec)
    run_manifest = build_manifest(
        spec_path, spec, schedule_manifest, index
    )
    write_exact(output / "table-index.json", index)
    write_exact(output / "run-manifest.json", run_manifest)

    manifest_path = output / "manifest.jsonl"
    existing, final_record, sequence, prior_payload_bytes = (
        scan_existing_chunks(output, manifest_path)
    )
    if final_record and final_record["event"] == "SEAL":
        if (
            int(final_record["chunk_count"]) != sequence
            or int(final_record["dataset_payload_bytes"])
            != prior_payload_bytes
        ):
            raise RuntimeError("sealed dataset totals mismatch")
        print(output)
        return
    previous = (
        final_record["line_sha256"] if final_record else ZERO_HASH
    )
    new_chunks = 0

    grouped: dict[tuple[str, int], list[dict]] = {}
    for task in tasks(spec, primes):
        key = (
            task["table"]["table_id"],
            task["prime_index"],
            task["start"],
            task["end"],
        )
        if key not in existing:
            grouped.setdefault(
                (task["table"]["table_id"], task["prime_index"]), []
            ).append(task)

    table_by_id = {
        table["table_id"]: table for table in spec["tables"]
    }
    group_items = list(grouped.items())
    workers = int(spec.get("parallel_workers", 1))
    if workers < 1:
        raise ValueError("parallel_workers must be positive")
    telemetry_path = output / "telemetry.jsonl"
    telemetry_previous = ZERO_HASH
    telemetry_sequence = 0
    cumulative_wall_ns = 0
    cumulative_updates = 0
    if spec.get("throughput_monitor"):
        for record in iter_chain(telemetry_path):
            telemetry_previous = record["line_sha256"]
            telemetry_sequence += 1
            if record["event"] == "BATCH":
                cumulative_wall_ns += int(record["wall_ns"])
                cumulative_updates += int(record["updates"])

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for batch_start in range(0, len(group_items), workers):
            batch = group_items[batch_start:batch_start + workers]
            batch_started = time.monotonic_ns()
            futures = [
                executor.submit(
                    evaluate_prime,
                    table_by_id[table_id],
                    prime_index,
                    primes[prime_index],
                )
                for (table_id, prime_index), _ in batch
            ]
            evaluated = [future.result() for future in futures]
            batch_wall_ns = time.monotonic_ns() - batch_started
            batch_updates = 0

            for (
                ((table_id, prime_index), pending),
                (raw, _prime_process_ns),
            ) in zip(batch, evaluated):
                table = table_by_id[table_id]
                if len(raw) != int(table["dimension"]) * 8:
                    raise RuntimeError("native prime output length mismatch")
                batch_updates += int(table["N"]) * int(table["dimension"])

                for task in pending:
                    start = task["start"]
                    end = task["end"]
                    content = raw[(start - 1) * 8:end * 8]
                    relative = Path("chunks") / table_id / (
                        f"p{prime_index:04d}-d{start:04d}-{end:04d}.bin"
                    )
                    chunk_path = output / relative
                    chunk_path.parent.mkdir(parents=True, exist_ok=True)
                    temporary_chunk = chunk_path.with_suffix(".tmp")
                    temporary_chunk.write_bytes(content)
                    os.replace(temporary_chunk, chunk_path)
                    payload = {
                        "sequence": sequence,
                        "event": "CHUNK",
                        "table_id": table_id,
                        "N": table["N"],
                        "weight_power": table["weight_power"],
                        "prime_index": prime_index,
                        "prime": str(primes[prime_index]),
                        "role": task["role"],
                        "dimension_start": start,
                        "dimension_end": end,
                        "encoding": "u64le",
                        "path": str(relative),
                        "bytes": len(content),
                        "sha256": file_sha256(chunk_path),
                    }
                    record = append_record(manifest_path, payload, previous)
                    previous = record["line_sha256"]
                    sequence += 1
                    new_chunks += 1
                    if (
                        args.stop_after_new_chunks is not None
                        and new_chunks == args.stop_after_new_chunks
                    ):
                        print(
                            json.dumps(
                                {
                                    "status": (
                                        "INTENTIONAL_CHUNK_BOUNDARY_STOP"
                                    ),
                                    "new_chunks": new_chunks,
                                    "last_line_sha256": previous,
                                },
                                sort_keys=True,
                            )
                        )
                        raise SystemExit(75)
                    if (
                        args.pause_after_new_chunks is not None
                        and new_chunks == args.pause_after_new_chunks
                    ):
                        print(
                            json.dumps(
                                {
                                    "status": "READY_FOR_FORCED_KILL",
                                    "new_chunks": new_chunks,
                                    "last_line_sha256": previous,
                                },
                                sort_keys=True,
                            ),
                            flush=True,
                        )
                        while True:
                            signal.pause()

            monitor = spec.get("throughput_monitor")
            if monitor:
                telemetry = append_record(
                    telemetry_path,
                    {
                        "sequence": telemetry_sequence,
                        "event": "BATCH",
                        "batch_index": telemetry_sequence,
                        "workers": len(batch),
                        "wall_ns": batch_wall_ns,
                        "updates": batch_updates,
                        "aggregate_ns_per_update": (
                            batch_wall_ns / batch_updates
                        ),
                    },
                    telemetry_previous,
                )
                telemetry_previous = telemetry["line_sha256"]
                telemetry_sequence += 1
                cumulative_wall_ns += batch_wall_ns
                cumulative_updates += batch_updates
                if (
                    cumulative_updates
                    >= int(monitor["minimum_updates_before_enforcement"])
                    and cumulative_wall_ns / cumulative_updates
                    > float(monitor["maximum_aggregate_ns_per_update"])
                ):
                    append_record(
                        telemetry_path,
                        {
                            "sequence": telemetry_sequence,
                            "event": "PAUSE",
                            "reason": (
                                "THROUGHPUT_DRIFT_ABOVE_"
                                "FROZEN_CEILING"
                            ),
                            "cumulative_wall_ns": cumulative_wall_ns,
                            "cumulative_updates": cumulative_updates,
                            "cumulative_ns_per_update": (
                                cumulative_wall_ns / cumulative_updates
                            ),
                            "maximum_aggregate_ns_per_update": float(
                                monitor["maximum_aggregate_ns_per_update"]
                            ),
                        },
                        telemetry_previous,
                    )
                    print(
                        json.dumps(
                            {
                                "status": "PAUSED_THROUGHPUT_DRIFT",
                                "cumulative_ns_per_update": (
                                    cumulative_wall_ns / cumulative_updates
                                ),
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
                    raise SystemExit(76)

    _, final_record, chunk_count, payload_bytes = scan_existing_chunks(
        output, manifest_path
    )
    expected_tasks = tasks(spec, primes)
    if chunk_count != len(expected_tasks):
        raise RuntimeError("chunk count does not cover all tasks")
    seal = append_record(
        manifest_path,
        {
            "sequence": chunk_count,
            "event": "SEAL",
            "chunk_count": chunk_count,
            "dataset_payload_bytes": payload_bytes,
            "table_index_sha256": index["index_sha256"],
            "run_manifest_sha256": run_manifest["run_manifest_sha256"],
        },
        final_record["line_sha256"] if final_record else ZERO_HASH,
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "status": "SEALED",
                "chunk_count": chunk_count,
                "dataset_payload_bytes": payload_bytes,
                "seal_sha256": seal["line_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
