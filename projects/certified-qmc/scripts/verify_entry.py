#!/usr/bin/env python3
"""Verify one or many chunked merit-table entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.entry_replay import DatasetReplay


def main() -> None:
    parser = argparse.ArgumentParser(prog="verify-entry")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--table")
    parser.add_argument("--N", type=int)
    parser.add_argument("--d", type=int)
    parser.add_argument(
        "--requests",
        type=Path,
        help=(
            "JSON array of {table,N,dimension}; mutually exclusive "
            "with --table/--N/--d"
        ),
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="omit selected chunk-path lists",
    )
    args = parser.parse_args()
    single_fields = (args.table, args.N, args.d)
    if args.requests is None:
        if any(value is None for value in single_fields):
            parser.error(
                "--table, --N, and --d are required in single mode"
            )
        requests = [
            {
                "table": args.table,
                "N": args.N,
                "dimension": args.d,
            }
        ]
        batch = False
    else:
        if any(value is not None for value in single_fields):
            parser.error(
                "--requests is mutually exclusive with "
                "--table/--N/--d"
            )
        requests = json.loads(args.requests.read_text())
        if not isinstance(requests, list):
            raise ValueError("batch request file must contain an array")
        batch = True

    replay = DatasetReplay(args.dataset, ROOT)
    results = replay.verify(requests, compact=args.compact)
    payload = (
        {
            "status": "VERIFIED",
            "claim_tag": "VERIFIED_SELECTED_ENTRY_BATCH_REPLAY",
            "request_count": len(results),
            "results": results,
            "boundary": (
                "The dataset manifest is independently authenticated "
                "once; every selected entry retains its own bounded CRT "
                "reconstruction and two overflow-prime checks."
            ),
        }
        if batch
        else results[0]
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
