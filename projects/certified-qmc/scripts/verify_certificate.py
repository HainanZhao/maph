#!/usr/bin/env python3
"""Replay one exact B2-product merit certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from src.certificate import (
    AUDIT_SCHEMA,
    canonical_sha256,
    verify_audit_wrapper,
    verify_certificate,
)

REFERENCE_TABLE_SCHEMA = "certified-qmc-workstream-b-reference-table-v1"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument(
        "--dimension",
        type=int,
        help="select one dimension from a reference-table artifact",
    )
    args = parser.parse_args()

    payload = json.loads(args.certificate.read_text(encoding="utf-8"))
    if payload.get("schema") == AUDIT_SCHEMA:
        if args.dimension is not None:
            parser.error("--dimension applies only to a reference table")
        verify_audit_wrapper(payload)
        status = "VERIFIED_AUDIT_REPLAY"
        selected_dimension = None
    elif payload.get("schema") == REFERENCE_TABLE_SCHEMA:
        if args.dimension is None:
            parser.error("--dimension is required for a reference table")
        supplied_hash = payload.pop("table_sha256", None)
        if not isinstance(supplied_hash, str):
            raise ValueError("reference table is missing table_sha256")
        if canonical_sha256(payload) != supplied_hash:
            raise ValueError("reference-table manifest hash mismatch")
        selected = [
            row
            for row in payload["rows"]
            if int(row["dimension"]) == args.dimension
        ]
        if len(selected) != 1:
            raise ValueError("selected dimension is absent or duplicated")
        verify_certificate(selected[0]["core_certificate"])
        status = "VERIFIED_REFERENCE_ENTRY_REPLAY"
        selected_dimension = args.dimension
    else:
        if args.dimension is not None:
            parser.error("--dimension applies only to a reference table")
        verify_certificate(payload)
        status = "VERIFIED_REPLAY"
        selected_dimension = None
    result = {
        "certificate": str(args.certificate),
        "schema": payload["schema"],
        "status": status,
    }
    if selected_dimension is not None:
        result["dimension"] = selected_dimension
    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
