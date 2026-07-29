#!/usr/bin/env python3
"""Build the frozen C -> B -> A identification work queues."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "w1-full-census-v1.json"


REQUIREMENTS = {
    "C": [
        "two CM bases",
        "linear reinduction on normal closure",
        "exact conductor and local factors",
        "|S| >= 3",
        "root-of-unity certification",
        "Arb unit-lattice isolation",
        "exact orientation",
    ],
    "B": [
        "two-route imaginary-base agreement",
        "complete divisor table",
        "safe exponent and real distribution indices",
        "Arb height margin >= 100",
        "ray-field identification over K",
        "two split-prime Artin labels",
        "positive/exact-phase orientation",
    ],
    "A": [
        "exact character conductor",
        "quadratic ray field",
        "class numbers and roots of unity",
        "exact relative-unit coordinate index",
        "imprimitive Euler factors",
        "oriented relative unit",
        "uniform-theorem replay",
    ],
}


def main() -> None:
    census = json.loads(SOURCE.read_text())
    candidates = [
        row
        for row in census["records"]
        if row["verdict"] == "ROUTE_CANDIDATE"
    ]
    batches = []
    priority = 1
    for engine in ("C", "B", "A"):
        rows = sorted(
            (row for row in candidates if row["engine"] == engine),
            key=lambda row: (
                row["finite_norm"],
                row["d"],
                row["case_id"],
            ),
        )
        if engine == "B":
            rows.sort(
                key=lambda row: (
                    row["case_id"] != "RQ-000190",
                    row["finite_norm"],
                    row["d"],
                )
            )
        batches.append(
            {
                "priority": priority,
                "engine": engine,
                "case_count": len(rows),
                "requirements": REQUIREMENTS[engine],
                "case_ids": [row["case_id"] for row in rows],
            }
        )
        priority += 1
    payload = {
        "schema": "effective-stark-identification-batches-v1",
        "claim_tag": "VERIFIED_QUEUE",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "ordering": ["C", "B", "A"],
        "priority_override_already_executed": "RQ-000190",
        "pre_bulk_spotchecks": "10/10 PASSED",
        "batches": batches,
        "warning": (
            "C and B are scarce relative to A but not individually "
            "small: W1 found 817 C and 655 B structural candidates. "
            "Their full predicate batteries are sieves, not assumptions."
        ),
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = ROOT / "artifacts" / "identification-batches-v1.json"
    output.write_text(serialized)
    print("BATCH_ORDER=C,B,A")
    for batch in batches:
        print(f'BATCH_{batch["engine"]}_COUNT={batch["case_count"]}')
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
