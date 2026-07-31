#!/usr/bin/env python3
"""Versioned correction: replace legacy W1 indices by genuine v5 indices."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "artifacts/census-h-taxonomy-v1.json"
INDEX = ROOT / "artifacts/genuine-index-ledger-8200-v3.json"
OUTPUT = ROOT / "artifacts/census-h-taxonomy-v2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned corrected H taxonomy already exists")
    prior = json.loads(V1.read_text(encoding="utf-8"))
    index = {
        row["case_id"]: row
        for row in json.loads(INDEX.read_text(encoding="utf-8"))["records"]
    }
    records = []
    changed = []
    for old in prior["records"]:
        record = dict(old)
        genuine = index[record["case_id"]]
        if genuine["predicate_provenance"] != "GENUINE":
            raise RuntimeError(f"{record['case_id']}: non-genuine index")
        legacy = record["shintani_index"]
        corrected = genuine["derived_subgroup_order"]
        record["legacy_w1_shintani_index"] = legacy
        record["genuine_derived_subgroup_order"] = corrected
        record["shintani_index"] = corrected
        if legacy != corrected:
            changed.append({
                "case_id": record["case_id"],
                "legacy_w1_shintani_index": legacy,
                "genuine_derived_subgroup_order": corrected,
            })
        records.append(record)
    if len(records) != 2704:
        raise RuntimeError("H population changed")
    target = next(r for r in records if r["case_id"] == "RQ-005298")
    if target["genuine_derived_subgroup_order"] != 4:
        raise RuntimeError("RQ-005298 genuine index changed")
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    payload = {
        "schema": "effective-stark-census-h-taxonomy-v2",
        "claim_tag": "OBSERVED",
        "correction": {
            "prior_artifact": "artifacts/census-h-taxonomy-v1.json",
            "error": "displayed shintani_index copied the legacy W1 proxy field",
            "replacement": "genuine derived subgroup order from the v5 index ledger",
            "affected_record_count": len(changed),
            "affected_records": changed,
            "mathematical_effect": (
                "mechanism counts and eligibility flags are unchanged; "
                "only displayed index provenance is corrected"
            ),
        },
        "claim_boundary": prior["claim_boundary"],
        "source_hashes": {
            "artifacts/census-h-taxonomy-v1.json": sha256(V1),
            "artifacts/genuine-index-ledger-8200-v3.json": sha256(INDEX),
            "scripts/correct_census_h_taxonomy_v2.py": sha256(Path(__file__)),
        },
        "counts": prior["counts"],
        "frontier_tables": prior["frontier_tables"],
        "records_sha256": hashlib.sha256(canonical).hexdigest(),
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
