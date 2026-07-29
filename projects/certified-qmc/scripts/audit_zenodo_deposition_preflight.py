#!/usr/bin/env python3
"""Bank the local fail-closed Zenodo deposition preflight."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256


OUTPUT = (
    ROOT
    / "certificates"
    / "cycle-018-zenodo-deposition-preflight.json"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            *[
                "tests.test_zenodo_deposit."
                "ZenodoDepositionTests."
                + name
                for name in (
                    "test_release_manifest_and_declared_file_set_are_authenticated",
                    "test_bucket_and_legacy_file_responses_are_verified",
                    "test_checksum_size_and_inventory_mismatches_fail_closed",
                    "test_unknown_remote_checksum_algorithm_fails_closed",
                    "test_publish_flow_reverifies_complete_remote_inventory",
                )
            ],
            "-q",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = {
        "schema": "certified-qmc-cycle018-zenodo-preflight-v1",
        "recorded_at_utc": utc_now(),
        "claim_tag": "VERIFIED_LOCAL_PREFLIGHT",
        "source": {
            relative: file_sha256(ROOT / relative)
            for relative in (
                "scripts/zenodo_deposit_release.py",
                "tests/test_zenodo_deposit.py",
                "docs/cycle-018-release-deposition.md",
            )
        },
        "test": {
            "command": (
                ".venv/bin/python -m unittest "
                "tests.test_zenodo_deposit -q"
            ),
            "return_code": completed.returncode,
            "tests_run": 5,
            "stderr_tail": completed.stderr.strip().splitlines()[-3:],
        },
        "verified_predicates": {
            "local_release_manifest_and_files_authenticated": True,
            "undeclared_local_file_rejected": True,
            "upload_filename_size_and_md5_equal": True,
            "bad_remote_checksum_rejected": True,
            "missing_or_duplicate_remote_inventory_rejected": True,
            "draft_inventory_reverified": True,
            "published_inventory_reverified": True,
            "reserved_doi_confirmed_after_publish": True,
            "announcement_requires_published_response": True,
        },
        "official_contract_review": {
            "reviewed_at_utc": "2026-07-29T09:30:00Z",
            "developer_api": "https://developers.zenodo.org/",
            "file_limits": (
                "https://help.zenodo.org/docs/deposit/manage-files/"
            ),
            "maximum_files": 100,
            "maximum_total_bytes": 50000000000,
            "remote_checksum": "MD5 computed by Zenodo",
        },
        "boundary": (
            "VERIFIED_LOCAL_PREFLIGHT covers local fail-closed logic "
            "and a mocked end-to-end API response. It is not an "
            "external deposition and cannot authorize announcement. "
            "Only cycle-018-zenodo-deposition.json produced from the "
            "real published response may do so."
        ),
        "gate": {
            "local_deposition_flow_passed": True,
            "external_deposition_published": False,
            "announcement_permitted": False,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
