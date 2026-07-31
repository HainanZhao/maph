#!/usr/bin/env python3
"""Promote the corrected Cycle-112 B5-025 batch in a successor ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "artifacts/engine-b-transport-ledger-v1.json"
BATCH = ROOT / "artifacts/b5025-euler-deletion-transports-v2.json"
OUTPUT = ROOT / "artifacts/engine-b-transport-ledger-v2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    ledger = json.loads(PREDECESSOR.read_text())
    batch = json.loads(BATCH.read_text())
    if ledger["counts"]["member_transport_completed"] != 1:
        raise RuntimeError("predecessor ledger drifted")
    if batch["claim_tag"] != "PROVED_EXACT_MEMBER_TRANSPORT_BATCH":
        raise RuntimeError("batch is not sealed")
    by_target = {row["case_id"]: row for row in batch["records"]}
    if sorted(by_target) != ["RQ-000195", "RQ-000200", "RQ-000205", "RQ-000213"]:
        raise RuntimeError("unexpected B5-025 promotions")
    members = []
    for row in ledger["members"]:
        successor = dict(row)
        if row["case_id"] in by_target:
            proof = by_target[row["case_id"]]
            successor.update({"transport_status": "PROVED_EXACT_MEMBER_TRANSPORT", "transport_certificate": str(BATCH.relative_to(ROOT)), "source_case_id": proof["source_case_id"], "packet_relation": proof["packet_relation"], "artin_labelled_formula_terms": proof["artin_labelled_formula_terms"]})
        members.append(successor)
    completed = [row for row in members if row["transport_status"] == "PROVED_EXACT_MEMBER_TRANSPORT"]
    if sorted(row["case_id"] for row in completed) != ["RQ-000039", "RQ-000195", "RQ-000200", "RQ-000205", "RQ-000213"]:
        raise RuntimeError("completed transport set drifted")
    payload = {"schema": "effective-stark-engine-b-transport-ledger-v2", "claim_tag": "VERIFIED_ENGINE_B_TRANSPORT_LEDGER", "supersedes": str(PREDECESSOR.relative_to(ROOT)), "counts": {"v5_engine_b_rows": len(members), "member_transport_completed": len(completed), "member_transport_open": len(members)-len(completed)}, "claim_boundary": "only five named members are promoted; every other member is explicit and unpromoted", "members": members, "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (PREDECESSOR, BATCH, Path(__file__))}}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("ENGINE_B_TRANSPORT_LEDGER_V2=PASS")


if __name__ == "__main__":
    main()
