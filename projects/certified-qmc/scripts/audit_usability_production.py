#!/usr/bin/env python3
"""Audit Cycle-018 computation and authenticate j^-2 fidelity reuse."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256, iter_chain


SPEC = ROOT / "data" / "cycle-018-usability-spec.json"
PREREG = (
    ROOT / "data" / "cycle-018-usability-preregistration.json"
)
FIDELITY_SPEC = (
    ROOT / "data" / "cycles-016-017-fidelity-spec-v2.json"
)
FIDELITY_AUDIT = (
    ROOT / "certificates" / "cycles-016-017-production-audit.json"
)
VERIFIER = ROOT / "bin" / "verify-entry"
CONSERVATIVE_PHASE_TOTAL_UPDATES = 54_901_459_582_976


def expected_update_count(spec: dict) -> int:
    return sum(
        (int(table["work_prime_count"]) + 2)
        * int(table["N"])
        * int(table["dimension"])
        for table in spec["tables"]
    )


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def verify_many(
    dataset: Path, requests: list[dict]
) -> dict[tuple[str, int, int], dict]:
    with tempfile.NamedTemporaryFile(
        "w",
        prefix="certified-qmc-usability-replay-",
        suffix=".json",
    ) as request_file:
        json.dump(requests, request_file)
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
        or batch["request_count"] != len(requests)
    ):
        raise ArithmeticError("selected-entry batch replay failed")
    result = {}
    for row in batch["results"]:
        if (
            row["status"] != "VERIFIED"
            or not all(
                check["equal"] for check in row["overflow_checks"]
            )
        ):
            raise ArithmeticError("selected-entry replay failed")
        compact = {
            key: row[key]
            for key in (
                "status",
                "table",
                "N",
                "dimension",
                "weight_power",
                "generator_prefix_sha256",
                "work_prime_count",
                "reduced_numerator",
                "reduced_denominator",
                "touched_payload_fraction",
            )
        }
        compact["overflow_checks_equal"] = True
        compact["entry_replay_sha256"] = canonical_sha256(
            compact
        )
        result[
            (
                row["table"],
                int(row["N"]),
                int(row["dimension"]),
            )
        ] = compact
    return result


def authenticate_dataset(dataset: Path) -> dict:
    final_record = None
    chunk_count = 0
    payload_bytes = 0
    for record in iter_chain(dataset / "manifest.jsonl"):
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
            raise ValueError("chunk authentication failed")
    if final_record is None or final_record["event"] != "SEAL":
        raise ValueError(f"{dataset.name} is not sealed")
    if (
        int(final_record["chunk_count"]) != chunk_count
        or int(final_record["dataset_payload_bytes"]) != payload_bytes
    ):
        raise ValueError("dataset seal totals do not match manifest")
    result = {
        "manifest_sha256": file_sha256(dataset / "manifest.jsonl"),
        "manifest_last_line_sha256": final_record["line_sha256"],
        "run_manifest_sha256": file_sha256(
            dataset / "run-manifest.json"
        ),
        "table_index_sha256": file_sha256(
            dataset / "table-index.json"
        ),
        "chunk_count": chunk_count,
        "payload_bytes": payload_bytes,
    }
    result["dataset_authentication_sha256"] = canonical_sha256(result)
    return result


def main() -> None:
    if len(sys.argv) != 6:
        raise SystemExit(
            "usage: audit_usability_production.py "
            "FIDELITY_DATASET USABILITY_DATASET "
            "LOGICAL_INDEX OUTPUT RECORDED_AT_UTC"
        )
    fidelity_dataset = Path(sys.argv[1]).resolve()
    usability_dataset = Path(sys.argv[2]).resolve()
    logical_index_path = Path(sys.argv[3]).resolve()
    output = Path(sys.argv[4]).resolve()
    recorded_at = sys.argv[5]

    fidelity_audit = json.loads(FIDELITY_AUDIT.read_text())
    if not fidelity_audit["gate"][
        "cycles_016_017_exit_gate_passed"
    ]:
        raise ValueError("fidelity predecessor gate is not passed")
    spec = json.loads(SPEC.read_text())
    prereg = json.loads(PREREG.read_text())
    fidelity_spec = json.loads(FIDELITY_SPEC.read_text())
    usability_auth = authenticate_dataset(usability_dataset)
    fidelity_auth = authenticate_dataset(fidelity_dataset)
    usability_updates = 0
    usability_wall_ns = 0
    for row in iter_chain(usability_dataset / "telemetry.jsonl"):
        if row["event"] == "BATCH":
            usability_updates += int(row["updates"])
            usability_wall_ns += int(row["wall_ns"])
    expected_usability_updates = expected_update_count(spec)
    if usability_updates != expected_usability_updates:
        raise ArithmeticError(
            "usability telemetry does not cover the frozen compute"
        )
    fidelity_updates = int(
        fidelity_audit["throughput"]["expected_updates"]
    )
    combined_updates = fidelity_updates + usability_updates
    if combined_updates > CONSERVATIVE_PHASE_TOTAL_UPDATES:
        raise ArithmeticError(
            "exact scheduled work exceeds the preregistered budget"
        )

    computed_by_key = {
        (
            table["source_id"],
            int(table["N"]),
            int(table["weight_power"]),
        ): table
        for table in spec["tables"]
    }
    fidelity_by_key = {
        (table["source_id"], int(table["N"])): table
        for table in fidelity_spec["tables"]
    }
    computed_requests = []
    reused_requests = []
    for source_id in prereg["grid"]["families"]:
        for modulus in prereg["grid"]["N"]:
            for dimension in prereg["grid"]["dimensions"]:
                fidelity_table = fidelity_by_key[
                    (source_id, modulus)
                ]
                reused_requests.append(
                    {
                        "table": fidelity_table["table_id"],
                        "N": modulus,
                        "dimension": dimension,
                    }
                )
                for power in (1, 3):
                    computed_table = computed_by_key[
                        (source_id, modulus, power)
                    ]
                    computed_requests.append(
                        {
                            "table": computed_table["table_id"],
                            "N": modulus,
                            "dimension": dimension,
                        }
                    )
    computed_by_replay_key = verify_many(
        usability_dataset, computed_requests
    )
    reused_by_replay_key = verify_many(
        fidelity_dataset, reused_requests
    )
    logical_entries = []
    computed_replays = []
    reused_replays = []
    for source_id in prereg["grid"]["families"]:
        for modulus in prereg["grid"]["N"]:
            for dimension in prereg["grid"]["dimensions"]:
                for power in prereg["grid"]["weight_powers"]:
                    if power == 2:
                        table = fidelity_by_key[
                            (source_id, modulus)
                        ]
                        replay = reused_by_replay_key[
                            (
                                table["table_id"],
                                modulus,
                                dimension,
                            )
                        ]
                        reused_replays.append(replay)
                        mode = "HASH_REUSED_FROM_FIDELITY_V2"
                        dataset = "fidelity-v2"
                    else:
                        table = computed_by_key[
                            (source_id, modulus, power)
                        ]
                        replay = computed_by_replay_key[
                            (
                                table["table_id"],
                                modulus,
                                dimension,
                            )
                        ]
                        computed_replays.append(replay)
                        mode = "COMPUTED_CYCLE_018"
                        dataset = "usability-v1"
                    logical_entries.append(
                        {
                            "source_id": source_id,
                            "source_file_sha256": table[
                                "source_file_sha256"
                            ],
                            "N": modulus,
                            "dimension": dimension,
                            "weight_power": power,
                            "mode": mode,
                            "dataset": dataset,
                            "table_id": table["table_id"],
                            "generator_prefix_sha256": replay[
                                "generator_prefix_sha256"
                            ],
                            "reduced_numerator": replay[
                                "reduced_numerator"
                            ],
                            "reduced_denominator": replay[
                                "reduced_denominator"
                            ],
                            "entry_replay_sha256": replay[
                                "entry_replay_sha256"
                            ],
                        }
                    )

    if len(computed_replays) != 36 or len(reused_replays) != 18:
        raise ArithmeticError("usability logical-grid count mismatch")
    logical_index = {
        "schema": "certified-qmc-usability-logical-index-v1",
        "claim_tag": "VERIFIED",
        "frozen_dimensions": [16, 64, 256],
        "entries": logical_entries,
        "computed_entry_count": len(computed_replays),
        "hash_reused_entry_count": len(reused_replays),
        "j2_recomputed": False,
        "fidelity_dataset_authentication_sha256": fidelity_auth[
            "dataset_authentication_sha256"
        ],
        "usability_dataset_authentication_sha256": usability_auth[
            "dataset_authentication_sha256"
        ],
    }
    logical_index["index_sha256"] = canonical_sha256(logical_index)
    logical_index_path.write_text(
        json.dumps(logical_index, indent=2, sort_keys=True) + "\n"
    )

    payload = {
        "schema": "certified-qmc-cycle-018-usability-audit-v1",
        "recorded_at_utc": recorded_at,
        "claim_tags": {
            "computed_entries": "VERIFIED",
            "fidelity_reuse": "VERIFIED",
            "dataset_manifests": "VERIFIED",
            "throughput": "NUMERICAL",
        },
        "preregistration": {
            "path": str(PREREG.relative_to(ROOT)),
            "sha256": digest(PREREG),
        },
        "fidelity_predecessor": {
            "audit_path": str(FIDELITY_AUDIT.relative_to(ROOT)),
            "audit_sha256": digest(FIDELITY_AUDIT),
            "dataset": fidelity_auth,
        },
        "usability_dataset": usability_auth,
        "logical_index": {
            "path": str(logical_index_path.relative_to(ROOT)),
            "sha256": digest(logical_index_path),
            "self_hash": logical_index["index_sha256"],
        },
        "computed_replays": computed_replays,
        "hash_reused_j2_replays": reused_replays,
        "verifier_batching": {
            "computed_dataset_manifest_passes": 1,
            "fidelity_dataset_manifest_passes": 1,
            "total_verify_entry_invocations": 2,
        },
        "throughput": {
            "updates": usability_updates,
            "expected_updates": expected_usability_updates,
            "update_count_exact": True,
            "wall_ns": usability_wall_ns,
            "aggregate_ns_per_update": (
                usability_wall_ns / usability_updates
            ),
        },
        "phase_update_budget_reconciliation": {
            "fidelity_scheduled_updates_including_overflow": (
                fidelity_updates
            ),
            "usability_scheduled_updates_including_overflow": (
                usability_updates
            ),
            "combined_scheduled_updates_including_overflow": (
                combined_updates
            ),
            "preregistered_conservative_updates": (
                CONSERVATIVE_PHASE_TOTAL_UPDATES
            ),
            "within_conservative_budget": True,
            "reason": (
                "The preregistered projection used conservative 61-bit "
                "prime counts. The verified schedule uses larger "
                "admitted primes and therefore shorter exact prefixes."
            ),
        },
        "gate": {
            "computed_36_of_36_verified": True,
            "reused_18_of_18_verified_by_hash": True,
            "j2_recomputed": False,
            "telemetry_exactly_covers_frozen_usability_compute": True,
            "combined_work_within_preregistered_budget": True,
            "cycle_018_data_gate_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
