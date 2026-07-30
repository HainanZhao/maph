#!/usr/bin/env python3
"""Seal the completed 241-row genuine Engine-B recovery."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/genuine-b-recovery-241-v1.json"
OUTPUT = ROOT / "artifacts/genuine-b-recovery-summary-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = source["records"]
    if source["status"] != "COMPLETE" or len(records) != 241:
        raise RuntimeError("genuine B recovery is incomplete")
    if any(row["predicate_provenance"] != "GENUINE" for row in records):
        raise RuntimeError("non-genuine record in recovery")
    former_pass = [
        row for row in records
        if row["former_proxy_classification"] == "TWO_ROUTE_PASS"
    ]
    former_negative = [
        row for row in records
        if row["former_proxy_classification"]
        == "NO_ABELIAN_IMAGINARY_BASE"
    ]
    classification = Counter(row["classification"] for row in records)
    negative_outcomes = Counter(
        row["classification"] for row in former_negative
    )
    derived = Counter(
        row["data"]["derived_subgroup_order"] for row in records
    )
    if len(former_pass) != 64 or len(former_negative) != 177:
        raise RuntimeError("former proxy partition changed")
    if any(
        row["classification"] != "ENGINE_B_GENUINE_PASS"
        for row in former_pass
    ):
        raise RuntimeError("a former proxy pass did not genuinely re-pass")
    if classification["ENGINE_B_GENUINE_PASS"] != 90:
        raise RuntimeError("genuine B pass count changed")
    if any(
        row["classification"].startswith("HALT_")
        or row["failure"] is not None
        for row in records
    ):
        raise RuntimeError("recovery contains a mismatch or tool failure")

    payload = {
        "schema": "effective-stark-genuine-b-recovery-summary-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_GENUINE_B_RECOVERY",
        "predicate_provenance": "GENUINE",
        "recovered_population": 241,
        "classification_counts": dict(sorted(classification.items())),
        "derived_subgroup_order_counts": {
            str(key): value for key, value in sorted(derived.items())
        },
        "former_proxy_passes": {
            "count": 64,
            "genuine_repasses": 64,
            "other_outcomes": 0,
        },
        "former_proxy_negatives": {
            "count": 177,
            "new_genuine_b_passes": 26,
            "genuine_frontiers": 151,
            "outcome_counts": dict(sorted(negative_outcomes.items())),
        },
        "updated_b_occurrence_accounting": {
            "previous_stable_passes": 131,
            "recovered_unstable_passes": 90,
            "total_engine_b_eligible": 221,
            "net_change_from_precontainment_195": 26,
        },
        "mismatches": 0,
        "tool_failures": 0,
        "census_v5_status": (
            "BLOCKED_ON_252_C_CATCHUP_AND_8200_INDEX_LEDGER"
        ),
        "source_hashes": {
            str(SOURCE.relative_to(ROOT)): sha(SOURCE),
            "scripts/summarize_genuine_b_recovery.py": sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
