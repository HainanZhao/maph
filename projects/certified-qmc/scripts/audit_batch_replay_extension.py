#!/usr/bin/env python3
"""Bank the post-G3 selected-entry batch replay extension."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256, read_chain


DATASET = ROOT / "artifacts" / "cycle-015-pilot"
VERIFIER = ROOT / "bin" / "verify-entry"
REQUESTS = (
    ROOT / "tests" / "fixtures" / "cycle015-batch-requests.json"
)
OUTPUT = (
    ROOT / "certificates" / "cycle-015-batch-replay-extension.json"
)


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
    records = read_chain(DATASET / "manifest.jsonl")
    payload = {
        "schema": "certified-qmc-cycle015-batch-replay-extension-v1",
        "recorded_at_utc": utc_now(),
        "claim_tag": "VERIFIED",
        "source": {
            "src/entry_replay.py": file_sha256(
                ROOT / "src" / "entry_replay.py"
            ),
            "scripts/verify_entry.py": file_sha256(
                ROOT / "scripts" / "verify_entry.py"
            ),
            "bin/verify-entry": file_sha256(VERIFIER),
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
            "seal_line_sha256": records[-1]["line_sha256"],
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
        "boundary": (
            "This extends verifier orchestration only. Single-entry "
            "semantics, production chunks, thresholds, and the frozen "
            "production kernel are unchanged."
        ),
        "gate": {
            "single_entry_behavior_preserved": True,
            "two_entry_batch_verified": True,
            "all_overflow_checks_equal": True,
            "cycle_015_batch_extension_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
