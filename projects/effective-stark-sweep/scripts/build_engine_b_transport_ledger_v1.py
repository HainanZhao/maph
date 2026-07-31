#!/usr/bin/env python3
"""Create a successor Engine-B occurrence ledger without rewriting v5 scope."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "artifacts/engine-b-transport-manifest-v5.json"
TRANSPORT = ROOT / "artifacts/rq000039-engine-b-transport-v1.json"
OUTPUT = ROOT / "artifacts/engine-b-transport-ledger-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    manifest = json.loads(MANIFEST.read_text())
    transport = json.loads(TRANSPORT.read_text())
    if manifest["counts"]["v5_engine_b_rows"] != 232:
        raise RuntimeError("v5 population drift")
    if transport["claim_tag"] != "PROVED_EXACT_MEMBER_TRANSPORT":
        raise RuntimeError("target transport is not sealed")
    target = transport["target_case_id"]
    members = []
    for row in manifest["members"]:
        successor = dict(row)
        if row["case_id"] == target:
            successor["transport_status"] = "PROVED_EXACT_MEMBER_TRANSPORT"
            successor["transport_certificate"] = str(TRANSPORT.relative_to(ROOT))
            successor["source_case_id"] = transport["source_case_id"]
            successor["packet_relation"] = transport["packet_relation"]
        members.append(successor)
    completed = [row for row in members if row["transport_status"] == "PROVED_EXACT_MEMBER_TRANSPORT"]
    if [row["case_id"] for row in completed] != ["RQ-000039"]:
        raise RuntimeError("unexpected promoted members")
    payload = {
        "schema": "effective-stark-engine-b-transport-ledger-v1",
        "claim_tag": "VERIFIED_ENGINE_B_TRANSPORT_LEDGER",
        "predecessor": str(MANIFEST.relative_to(ROOT)),
        "counts": {
            "v5_engine_b_rows": len(members),
            "member_transport_completed": len(completed),
            "member_transport_open": len(members) - len(completed),
        },
        "claim_boundary": "only RQ-000039 is promoted; all other member states are carried forward explicitly",
        "members": members,
        "source_hashes": {
            str(MANIFEST.relative_to(ROOT)): sha256(MANIFEST),
            str(TRANSPORT.relative_to(ROOT)): sha256(TRANSPORT),
            "scripts/build_engine_b_transport_ledger_v1.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("ENGINE_B_TRANSPORT_LEDGER_V1=PASS")


if __name__ == "__main__":
    main()
