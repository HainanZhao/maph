#!/usr/bin/env python3
"""Classify the genuine odd-index RQ-000172 control correctly."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
W1 = ROOT / "artifacts/w1-full-census-v1.json"
TRANSCRIPT = (
    ROOT / "artifacts/genuine-index-ledger-8200-v2/RQ-000172.txt"
)
OUTPUT = ROOT / "artifacts/rq000172-genuine-odd-index-control-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    row = next(
        row
        for row in json.loads(W1.read_text(encoding="utf-8"))["records"]
        if row["case_id"] == "RQ-000172"
    )
    text = TRANSCRIPT.read_text(encoding="utf-8")
    required = [
        "FINITE_IDEAL=[9, 0; 0, 9]",
        "CONJUGATE_FINITE_IDEAL=[9, 0; 0, 9]",
        "NORMAL_CLOSURE_RELATIVE_DEGREE=9",
        "MAXIMAL_ABELIAN_RELATIVE_DEGREE=3",
        "DERIVED_SUBGROUP_ORDER=3",
        "PREDICATE_PROVENANCE=GENUINE",
    ]
    if any(marker not in text for marker in required):
        raise RuntimeError("genuine odd-index transcript mismatch")
    if (
        row["support_count"] != 0
        or row["shintani_index"] != 3
        or row["commutator_size"] != 3
    ):
        raise RuntimeError("historical stable-modulus control mismatch")
    payload = {
        "schema": "effective-stark-rq000172-odd-index-control-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_GENUINE_INDEX_CONTROL",
        "case_id": "RQ-000172",
        "field": "Q(sqrt(6))",
        "modulus": "(9) infinity_2",
        "finite_modulus_conjugation_stable": True,
        "predicate_provenance": "GENUINE",
        "normal_closure_relative_degree": 9,
        "maximal_abelian_relative_degree": 3,
        "derived_subgroup_order": 3,
        "support_count": 0,
        "classification": "PROVED_TRIVIAL_EMPTY_SUPPORT",
        "escalation_disposition": (
            "NOT_A_FRONTIER_ODD_INDEX: the standing discovery trigger "
            "applies to substantive/FRONTIER rows; this differenced "
            "invariant is identically zero"
        ),
        "independent_agreement": (
            "the historical W1 computation is genuine on this stable "
            "modulus and independently recorded index=commutator_size=3"
        ),
        "source_hashes": {
            str(W1.relative_to(ROOT)): sha(W1),
            str(TRANSCRIPT.relative_to(ROOT)): sha(TRANSCRIPT),
            "scripts/seal_rq000172_odd_index_control.py":
                sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
