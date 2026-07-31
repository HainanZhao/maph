#!/usr/bin/env python3
"""Recompute the preregistered v5 frontier/norm finite-range table."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / "artifacts/full-census-yield-declaration-v5.json"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
PREREG = ROOT / "docs/cycle-099-w4-frontier-norm-preregistration.md"
OUTPUT = ROOT / "artifacts/w4-frontier-norm-v1.json"
BINS = ((1, 25), (26, 50), (51, 75), (76, 100))

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    v5 = json.loads(V5.read_text())
    if v5["predicate_provenance"] != "GENUINE":
        raise RuntimeError("v5 provenance gate failed")
    norms = {row["case_id"]: row["finite_norm"]
             for row in json.loads(W1.read_text())["records"]}
    verdicts = {row["case_id"]: row["verdict"]
                for row in v5["classification_records"]}
    if set(norms) != set(verdicts) or len(norms) != 8200:
        raise RuntimeError("case-id join gate failed")
    table = []
    for low, high in BINS:
        members = [case_id for case_id, norm in norms.items()
                   if low <= norm <= high]
        frontier = sum(verdicts[case_id] == "FRONTIER" for case_id in members)
        table.append({
            "norm_interval": [low, high], "total": len(members),
            "frontier": frontier,
            "frontier_share": {"numerator": frontier,
                               "denominator": len(members)},
        })
    expected = v5["frontier_norm_quartiles"]
    actual_pairs = [(r["frontier"], r["total"]) for r in table]
    expected_pairs = [(r["frontier"], r["total"]) for r in expected]
    if actual_pairs != expected_pairs:
        raise RuntimeError("stored v5 frontier/norm fractions disagree")
    payload = {
        "schema": "effective-stark-w4-frontier-norm-v1",
        "claim_tag": "OBSERVED_EXACT_FINITE_CENSUS",
        "claim_boundary": "frozen 8,200-row range only; no asymptotic claim",
        "bins": table,
        "strictly_increasing": all(
            table[i]["frontier"] * table[i - 1]["total"]
            > table[i - 1]["frontier"] * table[i]["total"]
            for i in range(1, len(table))
        ),
        "source_hashes": {
            "artifacts/full-census-yield-declaration-v5.json": sha256(V5),
            "artifacts/w1-full-census-v1.json": sha256(W1),
            "docs/cycle-099-w4-frontier-norm-preregistration.md": sha256(PREREG),
            "scripts/build_w4_frontier_norm.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("W4_FRONTIER_NORM=PASS")

if __name__ == "__main__":
    main()
