#!/usr/bin/env python3
"""Split the frozen Engine-A queue into trivial and quadratic packets."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "w1-full-census-v1.json"
OUTPUT = ROOT / "artifacts" / "engine-a-queue-analysis-v1.json"


def main() -> None:
    source = json.loads(SOURCE.read_text())
    rows = [row for row in source["records"] if row.get("engine") == "A"]
    trivial = [row for row in rows if row["support_count"] == 0]
    quadratic = [row for row in rows if row["support_count"] > 0]
    if any(row["support_orders"] != [2] for row in quadratic):
        raise RuntimeError("nonquadratic support entered Engine A")
    if any(row["sign_log"] != [0] * len(row["one_cyc"]) for row in trivial):
        raise RuntimeError("zero support without trivial sign class")
    if any(row["sign_log"] == [0] * len(row["one_cyc"]) for row in quadratic):
        raise RuntimeError("nonzero support with trivial sign class")

    output = {
        "schema": "effective-stark-engine-a-queue-analysis-v1",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "case_count": len(rows),
        "trivial_packet_count": len(trivial),
        "quadratic_packet_count": len(quadratic),
        "trivial_theorem": {
            "hypothesis": "the exact differencing class R is the identity",
            "certificate": "sign_log is the zero vector",
            "conclusion": "Z'_m(0,A)=0 and X_A=1 for every ray class A",
            "claim_tag": "VERIFIED",
        },
        "trivial_case_ids": [row["case_id"] for row in trivial],
        "quadratic_case_ids": [row["case_id"] for row in quadratic],
        "quadratic_support_count_histogram": {
            str(count): sum(
                row["support_count"] == count for row in quadratic
            )
            for count in sorted({row["support_count"] for row in quadratic})
        },
        "quadratic_bulk_status": (
            "DEFERRED_UNTIL_AFTER_C_AND_B_IDENTIFICATION"
        ),
    }
    if len(rows) != 5459 or len(trivial) != 3899 or len(quadratic) != 1560:
        raise RuntimeError("Engine-A frozen counts changed")
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "case_count": len(rows),
        "trivial_packet_count": len(trivial),
        "quadratic_packet_count": len(quadratic),
        "quadratic_support_count_histogram":
            output["quadratic_support_count_histogram"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
