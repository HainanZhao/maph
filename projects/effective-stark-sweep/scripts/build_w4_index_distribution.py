#!/usr/bin/env python3
"""Build the preregistered first W4 slice from the genuine index ledger."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "artifacts/genuine-index-ledger-8200-v3.json"
PREREG = ROOT / "docs/cycle-098-w4-index-distribution-preregistration.md"
OUTPUT = ROOT / "artifacts/w4-genuine-index-distribution-v1.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    ledger = json.loads(LEDGER.read_text())
    records = ledger["records"]
    if len(records) != 8200 or ledger["predicate_provenance"] != "GENUINE":
        raise RuntimeError("genuine 8,200-row ledger gate failed")
    counts = Counter(row["derived_subgroup_order"] for row in records)
    histogram = {str(key): counts[key] for key in sorted(counts)}
    if histogram != ledger["index_histogram"]:
        raise RuntimeError("embedded genuine index histogram disagrees")
    odd_gt_two = [row for row in records
                  if row["derived_subgroup_order"] > 2
                  and row["derived_subgroup_order"] % 2 == 1]
    if len(odd_gt_two) != 446:
        raise RuntimeError("registered odd-index parity population drifted")
    payload = {
        "schema": "effective-stark-w4-genuine-index-distribution-v1",
        "claim_tag": "OBSERVED_EXACT_FINITE_CENSUS",
        "claim_boundary": "frozen 8,200-row range only; no asymptotic or packet claim",
        "population": len(records), "index_histogram": histogram,
        "odd_index_gt_two_count": len(odd_gt_two),
        "odd_index_gt_two_case_ids": [row["case_id"] for row in odd_gt_two],
        "source_hashes": {
            "artifacts/genuine-index-ledger-8200-v3.json": sha256(LEDGER),
            "docs/cycle-098-w4-index-distribution-preregistration.md": sha256(PREREG),
            "scripts/build_w4_index_distribution.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("W4_GENUINE_INDEX_DISTRIBUTION=PASS")

if __name__ == "__main__":
    main()
