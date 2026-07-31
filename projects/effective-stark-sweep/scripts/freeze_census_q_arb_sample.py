#!/usr/bin/env python3
"""Materialize the preregistered deterministic 50-row Q audit sample."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREREGISTRATION = ROOT / "data" / "census-paper-preregistration-v1.json"
HEIGHTS = ROOT / "artifacts" / "census-packet-height-calibration-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    preregistration = json.loads(PREREGISTRATION.read_text())
    policy = preregistration["independent_analytic_spotcheck"]
    heights = json.loads(HEIGHTS.read_text())
    case_ids = [row["case_id"] for row in heights["records"]]
    seed = policy["seed"]
    ranked = sorted(
        (
            hashlib.sha256((seed + case_id).encode("utf-8")).hexdigest(),
            case_id,
        )
        for case_id in case_ids
    )
    selected = [
        {"rank": rank, "sha256": digest, "case_id": case_id}
        for rank, (digest, case_id) in enumerate(
            ranked[: policy["sample_size"]], start=1
        )
    ]
    result = {
        "schema": "effective-stark-census-q-arb-sample-v1",
        "status": "FROZEN_BEFORE_INDEPENDENT_ANALYTIC_VALUES",
        "selection": {
            "seed": seed,
            "concatenation": (
                "UTF-8 bytes of seed immediately followed by case_id"
            ),
            "hash": "SHA-256",
            "ordering": "ascending hexadecimal digest",
            "sample_size": len(selected),
        },
        "selected": selected,
        "source_hashes": {
            "preregistration_sha256": sha256(PREREGISTRATION),
            "height_calibration_sha256": sha256(HEIGHTS),
        },
        "analytic_values_opened": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
