#!/usr/bin/env python3
"""Run or resume deterministic per-prime chunk production."""

from __future__ import annotations

import argparse
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


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.chunked_table import (
    ZERO_HASH,
    append_record,
    canonical_bytes,
    chunk_records,
    file_sha256,
    read_chain,
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
    return [
        canonical_sha(generator[:dimension])
        for dimension in range(1, len(generator) + 1)
    ]


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
        "chunking": {
            "prefix_block_size": spec["prefix_block_size"],
            "encoding": "unsigned 64-bit little-endian",
            "manifest": "manifest.jsonl",
            "manifest_chain": (
                "each canonical JSON line contains previous_line_sha256 "
                "and its own line_sha256"
            ),
            "universal_overflow_prime_indices": [3738, 3739],
        },
        "table_index_sha256": index["index_sha256"],
    }
    payload["run_manifest_sha256"] = canonical_sha(payload)
    return payload


def write_exact(path: Path, value: dict) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path.exists():
        if path.read_text() != rendered:
            raise RuntimeError(f"resume metadata mismatch: {path.name}")
    else:
        path.write_text(rendered)


def validate_existing_chunks(output: Path, records: list[dict]) -> None:
    seen = set()
    for record in chunk_records(records):
        key = (
            record["table_id"],
            record["prime_index"],
            record["dimension_start"],
            record["dimension_end"],
        )
        if key in seen:
            raise RuntimeError("duplicate chunk in manifest")
        seen.add(key)
        chunk = output / record["path"]
        if not chunk.is_file():
            raise RuntimeError("manifested chunk is missing")
        if chunk.stat().st_size != record["bytes"]:
            raise RuntimeError("manifested chunk length mismatch")
        if file_sha256(chunk) != record["sha256"]:
            raise RuntimeError("manifested chunk hash mismatch")


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
    records = read_chain(manifest_path)
    validate_existing_chunks(output, records)
    if records and records[-1]["event"] == "SEAL":
        print(output)
        return
    existing = {
        (
            record["table_id"],
            record["prime_index"],
            record["dimension_start"],
            record["dimension_end"],
        )
        for record in chunk_records(records)
    }
    previous = records[-1]["line_sha256"] if records else ZERO_HASH
    sequence = len(records)
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
    for (table_id, prime_index), pending in grouped.items():
        table = table_by_id[table_id]
        source_path = ROOT / table["source_path"]
        with tempfile.NamedTemporaryFile(
            prefix="certified-qmc-prime-",
            suffix=".bin",
            delete=False,
        ) as temporary:
            raw_path = Path(temporary.name)
        try:
            subprocess.run(
                [
                    str(BINARY),
                    str(source_path),
                    str(table["N"]),
                    str(table["dimension"]),
                    str(table["weight_power"]),
                    str(primes[prime_index]),
                    str(raw_path),
                ],
                check=True,
            )
            raw = raw_path.read_bytes()
        finally:
            raw_path.unlink(missing_ok=True)
        if len(raw) != int(table["dimension"]) * 8:
            raise RuntimeError("native prime output length mismatch")

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
                            "status": "INTENTIONAL_CHUNK_BOUNDARY_STOP",
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

    final_records = read_chain(manifest_path)
    validate_existing_chunks(output, final_records)
    chunks = chunk_records(final_records)
    expected_tasks = tasks(spec, primes)
    if len(chunks) != len(expected_tasks):
        raise RuntimeError("chunk count does not cover all tasks")
    seal = append_record(
        manifest_path,
        {
            "sequence": len(final_records),
            "event": "SEAL",
            "chunk_count": len(chunks),
            "dataset_payload_bytes": sum(row["bytes"] for row in chunks),
            "table_index_sha256": index["index_sha256"],
            "run_manifest_sha256": run_manifest["run_manifest_sha256"],
        },
        final_records[-1]["line_sha256"] if final_records else ZERO_HASH,
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "status": "SEALED",
                "chunk_count": len(chunks),
                "dataset_payload_bytes": sum(row["bytes"] for row in chunks),
                "seal_sha256": seal["line_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
