#!/usr/bin/env python3
"""Validate the sealed RQ-000190 source certificate for Cycle 112 reuse."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "data/census-paper-preregistration-amendment-v13.json"
OUTPUT = ROOT / "artifacts/b5025-source-certificate-integrity-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    prereg = json.loads(PREREG.read_text())
    if prereg["status"] != "FROZEN_BEFORE_B5025_REUSABLE_SOURCE_TRANSPORT_BATCH":
        raise RuntimeError("preregistration not frozen")
    for relative, expected in prereg["source_hashes"].items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"hash drift: {relative}")
    source = json.loads((ROOT / "data/q7-p7-case-v1.json").read_text())
    if source["w3"]["packet_identity_verdict"] != "VERIFIED":
        raise RuntimeError("source packet is not verified")
    transcript = (ROOT / "artifacts/q7-p7-w3-arb-certificate-v1.txt").read_text()
    for required in ("Q7_P7_ANALYTIC_ARB_CERTIFIED=1", "Q7_P7_PACKET_IDENTITY_VERIFIED=1"):
        if required not in transcript:
            raise RuntimeError("source transcript lacks certificate token")
    payload = {
        "schema": "effective-stark-b5025-source-certificate-integrity-v1",
        "claim_tag": "VERIFIED_SEALED_SOURCE_CERTIFICATE_INTEGRITY",
        "source_case_id": "RQ-000190",
        "claim_boundary": "hash and certificate-token validation only; not a fresh independent Arb replay",
        "source_hashes": prereg["source_hashes"],
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("B5025_SOURCE_CERTIFICATE_INTEGRITY=PASS")


if __name__ == "__main__":
    main()
