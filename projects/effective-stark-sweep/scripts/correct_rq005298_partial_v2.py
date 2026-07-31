#!/usr/bin/env python3
"""Versioned correction for the intentionally interrupted 4 GB run."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "artifacts/rq005298-extended-resolvent-v1.json"
OUTPUT = ROOT / "artifacts/rq005298-extended-resolvent-v2.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned corrected output already exists")
    prior = json.loads(V1.read_text())
    if "user interrupt" not in prior["stderr"]:
        raise RuntimeError("expected intentional-interrupt diagnostic")
    if "_C_GEOMETRY_PASS=" in prior["stdout"]:
        raise RuntimeError("unexpected completed geometry verdict")
    payload = dict(prior)
    payload["schema"] = "effective-stark-rq005298-extended-resolvent-v2"
    payload["status"] = "PARTIAL_RESOURCE_CAP_RUN"
    payload["correction"] = {
        "prior_artifact": "artifacts/rq005298-extended-resolvent-v1.json",
        "error": "GP emits zero exit status after an intentional interrupt",
        "evidence": "stderr records user interrupt after reaching the 4 GB cap",
    }
    payload["source_hashes"] = dict(prior["source_hashes"])
    payload["source_hashes"]["artifacts/rq005298-extended-resolvent-v1.json"] = sha256(V1)
    payload["source_hashes"]["scripts/correct_rq005298_partial_v2.py"] = sha256(Path(__file__))
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    main()
