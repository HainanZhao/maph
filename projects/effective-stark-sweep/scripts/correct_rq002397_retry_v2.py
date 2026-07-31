#!/usr/bin/env python3
"""Versioned correction for GP's zero-exit segmentation-fault diagnostic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "artifacts/rq002397-fresh-segfault-retry-v1.json"
OUTPUT = ROOT / "artifacts/rq002397-fresh-segfault-retry-v2.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned corrected output already exists")
    prior = json.loads(V1.read_text())
    if "Segmentation Fault" not in prior["stderr"]:
        raise RuntimeError("expected PARI segmentation-fault diagnostic")
    if "_C_GEOMETRY_PASS=" in prior["stdout"]:
        raise RuntimeError("unexpected completed geometry verdict")
    payload = dict(prior)
    payload["schema"] = "effective-stark-rq002397-fresh-segfault-retry-v2"
    payload["status"] = "TOOL_FAILURE_REPRODUCED"
    payload["correction"] = {
        "prior_artifact": "artifacts/rq002397-fresh-segfault-retry-v1.json",
        "error": "GP emits exit code zero after this fatal diagnostic",
        "evidence": "stderr contains Segmentation Fault and stdout lacks a geometry verdict",
    }
    payload["source_hashes"] = dict(prior["source_hashes"])
    payload["source_hashes"]["artifacts/rq002397-fresh-segfault-retry-v1.json"] = sha256(V1)
    payload["source_hashes"]["scripts/correct_rq002397_retry_v2.py"] = sha256(Path(__file__))
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    main()
