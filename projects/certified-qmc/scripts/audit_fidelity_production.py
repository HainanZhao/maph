#!/usr/bin/env python3
"""Run the frozen Cycles 016-017 post-production audit."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256, iter_chain
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


def verify_many(
    dataset: Path, entries: list[tuple[dict, int]]
) -> dict[tuple[str, int, int], dict]:
    requests_by_key = {}
    for table, dimension in entries:
        key = (
            table["table_id"],
            int(table["N"]),
            int(dimension),
        )
        requests_by_key[key] = {
            "table": key[0],
            "N": key[1],
            "dimension": key[2],
        }
    with tempfile.NamedTemporaryFile(
        "w",
        prefix="certified-qmc-fidelity-replay-",
        suffix=".json",
    ) as request_file:
        json.dump(list(requests_by_key.values()), request_file)
        request_file.flush()
        completed = subprocess.run(
            [
                str(VERIFIER),
                "--dataset",
                str(dataset),
                "--requests",
                request_file.name,
                "--compact",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    batch = json.loads(completed.stdout)
    if (
        batch["status"] != "VERIFIED"
        or batch["request_count"] != len(requests_by_key)
    ):
        raise ArithmeticError("selected-entry batch replay failed")
    keep = (
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
    return {
        (
            row["table"],
            int(row["N"]),
            int(row["dimension"]),
        ): {key: row[key] for key in keep}
        for row in batch["results"]
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
    final_record = None
    chunk_count = 0
    payload_bytes = 0
    for record in iter_chain(manifest_path):
        final_record = record
        if record["event"] != "CHUNK":
            continue
        chunk_count += 1
        payload_bytes += int(record["bytes"])
        path = dataset / record["path"]
        if (
            path.stat().st_size != record["bytes"]
            or file_sha256(path) != record["sha256"]
        ):
            raise ValueError("full-dataset chunk authentication failed")
    if final_record is None or final_record["event"] != "SEAL":
        raise ValueError("fidelity dataset is not sealed")
    if (
        int(final_record["chunk_count"]) != chunk_count
        or int(final_record["dataset_payload_bytes"]) != payload_bytes
    ):
        raise ValueError("fidelity seal totals do not match manifest")

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
        "manifest_last_line_sha256": final_record["line_sha256"],
        "authenticated_chunk_count": chunk_count,
        "authenticated_payload_bytes": payload_bytes,
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
    table_by_id = {
        table["table_id"]: table for table in spec["tables"]
    }
    oracle_entries = [
        (
            table_by_id[frozen["table_id"]],
            int(frozen["d"]),
        )
        for frozen in prereg[
            "post_run_audit"
        ]["independent_oracle_entries"]
    ]
    replay_by_key = verify_many(
        dataset, [*selected, *oracle_entries]
    )
    replay = [
        replay_by_key[
            (table["table_id"], int(table["N"]), dimension)
        ]
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

    oracles = []
    for frozen in prereg[
        "post_run_audit"
    ]["independent_oracle_entries"]:
        table = table_by_id[frozen["table_id"]]
        dimension = int(frozen["d"])
        replayed = replay_by_key[
            (table["table_id"], int(table["N"]), dimension)
        ]
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

    updates = 0
    wall_ns = 0
    for row in iter_chain(dataset / "telemetry.jsonl"):
        if row["event"] == "BATCH":
            updates += int(row["updates"])
            wall_ns += int(row["wall_ns"])
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
            "seal_line_sha256": final_record["line_sha256"],
            "chunk_count": chunk_count,
            "payload_bytes": dataset_sha[
                "authenticated_payload_bytes"
            ],
        },
        "selected_entry_replay": {
            "seed": prereg["post_run_audit"]["seed"],
            "sample_count": len(replay),
            "verifier_mode": "single authenticated batch",
            "verifier_invocations_including_oracles": 1,
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
