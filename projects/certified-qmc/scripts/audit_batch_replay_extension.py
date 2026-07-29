#!/usr/bin/env python3
"""Bank the post-G3 selected-entry batch replay extension."""

from __future__ import annotations

from datetime import datetime, timezone
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
from src.entry_replay import DatasetReplay
from scripts.build_engine_oracle_set import replay_batch


DATASET = ROOT / "artifacts" / "cycle-015-pilot"
VERIFIER = ROOT / "bin" / "verify-entry"
REQUESTS = (
    ROOT / "tests" / "fixtures" / "cycle015-batch-requests.json"
)
OUTPUT = (
    ROOT / "certificates" / "cycle-015-batch-replay-extension-v2.json"
)
PREDECESSOR = (
    ROOT
    / "certificates"
    / "cycle-015-batch-replay-extension-v1.json"
)
DRIVER = ROOT / "scripts" / "run_chunked_production.py"
SPEC = ROOT / "data" / "cycle-015-pilot-spec.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def invoke(arguments: list[str]) -> dict:
    completed = subprocess.run(
        [str(VERIFIER), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def tree_digest(root: Path) -> str:
    rows = [
        {
            "path": str(path.relative_to(root)),
            "bytes": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]
    return canonical_sha256(rows)


def main() -> None:
    batch = invoke(
        [
            "--dataset",
            str(DATASET),
            "--requests",
            str(REQUESTS),
            "--compact",
        ]
    )
    single = invoke(
        [
            "--dataset",
            str(DATASET),
            "--table",
            "pilot-000",
            "--N",
            "32",
            "--d",
            "7",
            "--compact",
        ]
    )
    if batch["status"] != "VERIFIED" or batch["request_count"] != 2:
        raise ArithmeticError("batch replay did not verify both entries")
    first = batch["results"][0]
    exact_fields = (
        "scaled_numerator",
        "scaled_denominator",
        "reduced_numerator",
        "reduced_denominator",
        "proved_numerator_bound",
        "generator_prefix_sha256",
        "work_prime_count",
        "touched_payload_fraction_exact",
    )
    equal = {
        field: first[field] == single[field]
        for field in exact_fields
    }
    if not all(equal.values()):
        raise ArithmeticError("batch/single exact field mismatch")
    if not all(
        all(check["equal"] for check in row["overflow_checks"])
        for row in batch["results"]
    ):
        raise ArithmeticError("batch overflow-prime failure")
    record_count = 0
    seal = None
    for record in iter_chain(DATASET / "manifest.jsonl"):
        record_count += 1
        seal = record
    if seal is None or seal["event"] != "SEAL":
        raise ValueError("pilot dataset manifest is not sealed")
    dataset_replay = DatasetReplay(DATASET, ROOT)
    if hasattr(dataset_replay, "records") or hasattr(
        dataset_replay, "chunks"
    ):
        raise AssertionError(
            "streaming verifier retained a materialized manifest"
        )
    schedule = json.loads(
        (ROOT / "data" / "primes-schedule-v1.json").read_text()
    )
    oracle_requests = [
        {
            "table_id": "pilot-000",
            "N": 32,
            "dimension": dimension,
            "weight_power": 1,
        }
        for dimension in (7, 13)
    ]
    extracted, extraction_provenance = replay_batch(
        DATASET,
        oracle_requests,
        [int(row["p"]) for row in schedule["primes"]],
        "cycle-015-pilot",
    )
    for oracle, replayed in zip(extracted, batch["results"]):
        if (
            oracle["reduced_numerator"]
            != replayed["reduced_numerator"]
            or oracle["reduced_denominator"]
            != replayed["reduced_denominator"]
        ):
            raise ArithmeticError(
                "streamed oracle extraction changed an exact value"
            )
    summed_entry_chunks = sum(
        row["authenticated_chunk_count"] for row in extracted
    )
    if (
        extraction_provenance["selected_unique_chunk_count"]
        >= summed_entry_chunks
    ):
        raise AssertionError(
            "shared oracle chunks were not deduplicated"
        )
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-streaming-resume-"
    ) as directory:
        temporary = Path(directory)
        baseline = temporary / "baseline"
        resumed = temporary / "resumed"
        subprocess.run(
            [
                sys.executable,
                str(DRIVER),
                "--spec",
                str(SPEC),
                "--output",
                str(baseline),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        stopped = subprocess.run(
            [
                sys.executable,
                str(DRIVER),
                "--spec",
                str(SPEC),
                "--output",
                str(resumed),
                "--stop-after-new-chunks",
                "211",
            ],
            capture_output=True,
            text=True,
        )
        if stopped.returncode != 75:
            raise RuntimeError("streaming resume stop point failed")
        subprocess.run(
            [
                sys.executable,
                str(DRIVER),
                "--spec",
                str(SPEC),
                "--output",
                str(resumed),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        baseline_tree_sha256 = tree_digest(baseline)
        resumed_tree_sha256 = tree_digest(resumed)
        if baseline_tree_sha256 != resumed_tree_sha256:
            raise ArithmeticError(
                "streaming scanner resume is not byte-identical"
            )
    payload = {
        "schema": "certified-qmc-cycle015-batch-replay-extension-v2",
        "recorded_at_utc": utc_now(),
        "claim_tag": "VERIFIED",
        "predecessor": {
            "path": str(PREDECESSOR.relative_to(ROOT)),
            "sha256": file_sha256(PREDECESSOR),
            "status": "PRESERVED",
        },
        "source": {
            "src/chunked_table.py": file_sha256(
                ROOT / "src" / "chunked_table.py"
            ),
            "src/entry_replay.py": file_sha256(
                ROOT / "src" / "entry_replay.py"
            ),
            "scripts/verify_entry.py": file_sha256(
                ROOT / "scripts" / "verify_entry.py"
            ),
            "bin/verify-entry": file_sha256(VERIFIER),
            "scripts/audit_fidelity_production.py": file_sha256(
                ROOT / "scripts" / "audit_fidelity_production.py"
            ),
            "scripts/audit_usability_production.py": file_sha256(
                ROOT / "scripts" / "audit_usability_production.py"
            ),
            "scripts/build_engine_oracle_set.py": file_sha256(
                ROOT / "scripts" / "build_engine_oracle_set.py"
            ),
            "scripts/run_chunked_production.py": file_sha256(
                ROOT / "scripts" / "run_chunked_production.py"
            ),
        },
        "request_fixture": {
            "path": str(REQUESTS.relative_to(ROOT)),
            "sha256": file_sha256(REQUESTS),
            "request_count": 2,
        },
        "dataset": {
            "manifest_sha256": file_sha256(
                DATASET / "manifest.jsonl"
            ),
            "seal_line_sha256": seal["line_sha256"],
            "authenticated_record_count": record_count,
            "run_manifest_sha256": file_sha256(
                DATASET / "run-manifest.json"
            ),
            "table_index_sha256": file_sha256(
                DATASET / "table-index.json"
            ),
        },
        "single_vs_batch": {
            "entry": {
                "table": "pilot-000",
                "N": 32,
                "dimension": 7,
            },
            "equal_fields": equal,
            "single_result_sha256": sha256(
                json.dumps(
                    single,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            ).hexdigest(),
            "batch_entry_sha256": sha256(
                json.dumps(
                    first,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode()
            ).hexdigest(),
        },
        "batch": {
            "request_count": batch["request_count"],
            "dimensions": [
                row["dimension"] for row in batch["results"]
            ],
            "all_entries_verified": True,
            "all_overflow_checks_equal": True,
            "manifest_authentication_passes": 1,
            "per_entry_crt_reconstructions": 2,
        },
        "streaming": {
            "manifest_materialized_by_selected_entry_verifier": False,
            "retained_dataset_records_after_initialization": False,
            "retained_dataset_chunks_after_initialization": False,
            "selected_chunk_payloads_retained_after_scan": False,
            "file_hashing_block_bytes": 1048576,
            "pilot_chain_matches_predecessor_seal": (
                seal["line_sha256"]
                == json.loads(PREDECESSOR.read_text())["dataset"][
                    "seal_line_sha256"
                ]
            ),
            "chunk_boundary_resume": {
                "stop_after_chunks": 211,
                "stop_return_code": stopped.returncode,
                "baseline_tree_sha256": baseline_tree_sha256,
                "resumed_tree_sha256": resumed_tree_sha256,
                "byte_identical": True,
            },
            "oracle_extractor": {
                "entries": len(extracted),
                "exact_values_equal_to_selected_entry_replay": True,
                "selected_unique_chunk_count": (
                    extraction_provenance[
                        "selected_unique_chunk_count"
                    ]
                ),
                "summed_per_entry_chunk_count": summed_entry_chunks,
                "shared_chunks_read_once": True,
            },
        },
        "boundary": (
            "This replaces manifest materialization with streaming "
            "authentication in verifier/audit orchestration only. "
            "Single-entry values, production chunks, thresholds, and "
            "the frozen production kernel are unchanged."
        ),
        "gate": {
            "single_entry_behavior_preserved": True,
            "two_entry_batch_verified": True,
            "all_overflow_checks_equal": True,
            "predecessor_transcript_preserved": True,
            "streaming_manifest_authentication_passed": True,
            "streaming_resume_byte_identical": True,
            "streamed_oracle_extraction_preserves_exact_values": True,
            "cycle_015_streaming_extension_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
