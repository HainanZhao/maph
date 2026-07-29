#!/usr/bin/env python3
"""Run the frozen Cycles 016-017 post-production audit."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import random
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import chunk_records, file_sha256, read_chain
from src.scaled_integer import scaled_squared_error


PREREG = ROOT / "data" / "cycles-016-017-preregistration-v2.json"
SPEC = ROOT / "data" / "cycles-016-017-fidelity-spec-v2.json"
VERIFIER = ROOT / "bin" / "verify-entry"


def parse_generator(path: Path, dimension: int) -> list[int]:
    result = []
    for line in path.read_text().splitlines():
        row, component = map(int, line.split())
        if row != len(result) + 1:
            raise ValueError("generator row sequence mismatch")
        result.append(component)
    if len(result) < dimension:
        raise ValueError("generator is too short")
    return result[:dimension]


def verify_one(dataset: Path, table: dict, dimension: int) -> dict:
    completed = subprocess.run(
        [
            str(VERIFIER),
            "--dataset",
            str(dataset),
            "--table",
            table["table_id"],
            "--N",
            str(table["N"]),
            "--d",
            str(dimension),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    return {
        key: result[key]
        for key in (
            "status",
            "table",
            "N",
            "dimension",
            "weight_power",
            "generator_prefix_sha256",
            "work_prime_count",
            "scaled_numerator",
            "scaled_denominator",
            "reduced_numerator",
            "reduced_denominator",
            "overflow_checks",
            "touched_payload_bytes",
            "touched_payload_fraction",
            "touched_payload_fraction_exact",
        )
    }


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: audit_fidelity_production.py "
            "DATASET OUTPUT RECORDED_AT_UTC"
        )
    dataset = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    recorded_at = sys.argv[3]
    prereg = json.loads(PREREG.read_text())
    spec = json.loads(SPEC.read_text())

    manifest_path = dataset / "manifest.jsonl"
    records = read_chain(manifest_path)
    if not records or records[-1]["event"] != "SEAL":
        raise ValueError("fidelity dataset is not sealed")
    chunks = chunk_records(records)
    for record in chunks:
        path = dataset / record["path"]
        if (
            path.stat().st_size != record["bytes"]
            or file_sha256(path) != record["sha256"]
        ):
            raise ValueError("full-dataset chunk authentication failed")

    dataset_sha = {
        "schema": "certified-qmc-fidelity-dataset-sha256-v1",
        "claim_tag": "VERIFIED_HASH_MANIFEST",
        "run_id": spec["run_id"],
        "files": {
            filename: file_sha256(dataset / filename)
            for filename in (
                "manifest.jsonl",
                "run-manifest.json",
                "table-index.json",
                "telemetry.jsonl",
            )
        },
        "manifest_last_line_sha256": records[-1]["line_sha256"],
        "authenticated_chunk_count": len(chunks),
        "authenticated_payload_bytes": sum(
            int(record["bytes"]) for record in chunks
        ),
    }
    dataset_sha["manifest_sha256"] = canonical_sha256(dataset_sha)
    dataset_sha_path = dataset / "dataset-sha256.json"
    dataset_sha_path.write_text(
        json.dumps(dataset_sha, indent=2, sort_keys=True) + "\n"
    )

    entries = [
        (table, dimension)
        for table in spec["tables"]
        for dimension in range(1, int(table["dimension"]) + 1)
    ]
    randomizer = random.Random(
        int(prereg["post_run_audit"]["seed"])
    )
    selected = randomizer.sample(
        entries, int(prereg["post_run_audit"]["sample_count"])
    )
    replay = [
        verify_one(dataset, table, dimension)
        for table, dimension in selected
    ]
    if (
        len(replay) != 100
        or any(row["status"] != "VERIFIED" for row in replay)
        or any(
            not all(check["equal"] for check in row["overflow_checks"])
            for row in replay
        )
    ):
        raise ArithmeticError("selected-entry replay gate failed")

    table_by_id = {
        table["table_id"]: table for table in spec["tables"]
    }
    oracles = []
    for frozen in prereg[
        "post_run_audit"
    ]["independent_oracle_entries"]:
        table = table_by_id[frozen["table_id"]]
        dimension = int(frozen["d"])
        replayed = verify_one(dataset, table, dimension)
        generator = parse_generator(
            ROOT / table["source_path"], dimension
        )
        weights = [
            f"1/{index ** int(table['weight_power'])}"
            for index in range(1, dimension + 1)
        ]
        direct = scaled_squared_error(
            int(table["N"]), generator, weights
        )
        equal = (
            int(replayed["scaled_numerator"]) == direct.numerator
            and int(replayed["scaled_denominator"]) == direct.denominator
        )
        oracles.append(
            {
                **frozen,
                "replayed_scaled_numerator": replayed[
                    "scaled_numerator"
                ],
                "replayed_scaled_denominator": replayed[
                    "scaled_denominator"
                ],
                "direct_scaled_numerator": str(direct.numerator),
                "direct_scaled_denominator": str(direct.denominator),
                "equal": equal,
            }
        )
    if not all(row["equal"] for row in oracles):
        raise ArithmeticError("independent oracle mismatch")

    telemetry = read_chain(dataset / "telemetry.jsonl")
    batches = [
        row for row in telemetry if row["event"] == "BATCH"
    ]
    updates = sum(int(row["updates"]) for row in batches)
    wall_ns = sum(int(row["wall_ns"]) for row in batches)
    payload = {
        "schema": (
            "certified-qmc-cycles-016-017-production-audit-v1"
        ),
        "recorded_at_utc": recorded_at,
        "claim_tags": {
            "dataset_manifest": "VERIFIED",
            "selected_entry_replay": "VERIFIED",
            "independent_oracles": "VERIFIED",
            "throughput": "NUMERICAL",
        },
        "preregistration": {
            "path": str(PREREG.relative_to(ROOT)),
            "sha256": file_sha256(PREREG),
        },
        "production_spec": {
            "path": str(SPEC.relative_to(ROOT)),
            "sha256": file_sha256(SPEC),
        },
        "dataset": {
            "path": str(dataset.relative_to(ROOT)),
            "sha256_manifest": "dataset-sha256.json",
            "sha256_manifest_file_sha256": file_sha256(
                dataset_sha_path
            ),
            "seal_line_sha256": records[-1]["line_sha256"],
            "chunk_count": len(chunks),
            "payload_bytes": dataset_sha[
                "authenticated_payload_bytes"
            ],
        },
        "selected_entry_replay": {
            "seed": prereg["post_run_audit"]["seed"],
            "sample_count": len(replay),
            "all_verified": True,
            "all_overflow_checks_equal": True,
            "maximum_touched_payload_fraction": max(
                row["touched_payload_fraction"] for row in replay
            ),
            "entries": replay,
        },
        "independent_oracles": oracles,
        "throughput": {
            "updates": updates,
            "wall_ns": wall_ns,
            "aggregate_ns_per_update": wall_ns / updates,
            "frozen_alarm_ns_per_update": float(
                prereg["run_gate"][
                    "maximum_aggregate_ns_per_update"
                ]
            ),
            "alarm_pass": (
                wall_ns / updates
                <= float(
                    prereg["run_gate"][
                        "maximum_aggregate_ns_per_update"
                    ]
                )
            ),
        },
        "gate": {
            "replay_100_of_100": True,
            "oracle_spot_checks_pass": True,
            "manifest_sealed": True,
            "cycles_016_017_exit_gate_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
