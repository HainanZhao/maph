#!/usr/bin/env python3
"""Audit Cycle-018 computation and authenticate j^-2 fidelity reuse."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import chunk_records, file_sha256, read_chain


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


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def verify_one(
    dataset: Path, table_id: str, modulus: int, dimension: int
) -> dict:
    completed = subprocess.run(
        [
            str(VERIFIER),
            "--dataset",
            str(dataset),
            "--table",
            table_id,
            "--N",
            str(modulus),
            "--d",
            str(dimension),
            "--compact",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    if (
        result["status"] != "VERIFIED"
        or not all(
            row["equal"] for row in result["overflow_checks"]
        )
    ):
        raise ArithmeticError("selected-entry replay failed")
    compact = {
        key: result[key]
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
    compact["entry_replay_sha256"] = canonical_sha256(compact)
    return compact


def authenticate_dataset(dataset: Path) -> dict:
    records = read_chain(dataset / "manifest.jsonl")
    if not records or records[-1]["event"] != "SEAL":
        raise ValueError(f"{dataset.name} is not sealed")
    chunks = chunk_records(records)
    for record in chunks:
        path = dataset / record["path"]
        if (
            path.stat().st_size != record["bytes"]
            or file_sha256(path) != record["sha256"]
        ):
            raise ValueError("chunk authentication failed")
    result = {
        "manifest_sha256": file_sha256(dataset / "manifest.jsonl"),
        "manifest_last_line_sha256": records[-1]["line_sha256"],
        "run_manifest_sha256": file_sha256(
            dataset / "run-manifest.json"
        ),
        "table_index_sha256": file_sha256(
            dataset / "table-index.json"
        ),
        "chunk_count": len(chunks),
        "payload_bytes": sum(int(row["bytes"]) for row in chunks),
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
                        replay = verify_one(
                            fidelity_dataset,
                            table["table_id"],
                            modulus,
                            dimension,
                        )
                        reused_replays.append(replay)
                        mode = "HASH_REUSED_FROM_FIDELITY_V2"
                        dataset = "fidelity-v2"
                    else:
                        table = computed_by_key[
                            (source_id, modulus, power)
                        ]
                        replay = verify_one(
                            usability_dataset,
                            table["table_id"],
                            modulus,
                            dimension,
                        )
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
        "gate": {
            "computed_36_of_36_verified": True,
            "reused_18_of_18_verified_by_hash": True,
            "j2_recomputed": False,
            "cycle_018_data_gate_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
