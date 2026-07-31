#!/usr/bin/env python3
"""Record the exact degree-four subfield containment control."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/test_b5079_hilbert_containment.gp"
PREREG = ROOT / "docs/cycle-102-hilbert-ray-containment-preregistration.md"
OUTPUT = ROOT / "artifacts/b5079-hilbert-ray-containment-v1.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def field(lines: list[str], key: str) -> str:
    values = [line.split("=", 1)[1] for line in lines
              if line.startswith(key + "=")]
    if len(values) != 1:
        raise RuntimeError(f"expected exactly one {key}")
    return values[0]

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    completed = subprocess.run(
        ["gp", "-q", str(SCRIPT)], cwd=ROOT, text=True,
        capture_output=True, timeout=3600, check=True,
    )
    lines = [line.strip() for line in completed.stdout.splitlines()
             if line.strip()]
    count = int(field(lines, "DEGREE4_SUBFIELD_COUNT"))
    matches = int(field(lines, "HILBERT_FIELD_MATCH_COUNT"))
    contained = int(field(lines, "HILBERT_FIELD_CONTAINED"))
    if count != 11 or contained != int(matches > 0):
        raise RuntimeError("containment-screen consistency failure")
    payload = {
        "schema": "effective-stark-b5079-hilbert-ray-containment-v1",
        "claim_tag": "PROVED_EXACT_SUBFIELD_TEST",
        "case_id": "RQ-001262", "closure_id": "B5-079",
        "hilbert_field_polynomial": "x^4 - 24*x^2 + 4",
        "degree4_subfield_count": count,
        "hilbert_field_match_count": matches,
        "hilbert_field_contained": bool(contained),
        "claim_boundary": "field inclusion only; no Stark-unit or packet comparison",
        "transcript": completed.stdout + completed.stderr,
        "source_hashes": {
            "scripts/test_b5079_hilbert_containment.gp": sha256(SCRIPT),
            "docs/cycle-102-hilbert-ray-containment-preregistration.md": sha256(PREREG),
            "scripts/run_b5079_hilbert_containment.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("B5079_HILBERT_CONTAINMENT=PASS")

if __name__ == "__main__":
    main()
