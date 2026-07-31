#!/usr/bin/env python3
"""Record the exact first two Cycle-106 Engine-B transport gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/rq000039_transport_gates_1_2.gp"
PREREG = ROOT / "docs/cycle-106-engine-b-first-transport-preregistration.md"
OUTPUT = ROOT / "artifacts/rq000039-engine-b-transport-gates-1-2-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get(lines: list[str], key: str) -> str:
    values = [line.split("=", 1)[1] for line in lines if line.startswith(key + "=")]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    completed = subprocess.run(
        ["gp", "-q", str(SCRIPT)], cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=600,
    )
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    expected = {
        "SOURCE_FINITE_NORM": "49", "TARGET_FINITE_NORM": "98",
        "QUOTIENT_NORM": "2", "SOURCE_RAY_CYC": "[6]",
        "TARGET_RAY_CYC": "[6]", "RAY_MAP_MATRIX": "Mat(1)",
        "RAY_MAP_TARGET_IDENTITY": "[0]",
        "RAY_MAP_TARGET_GENERATOR": "[1]", "RAY_MAP_TARGET_SIGN": "[3]",
        "RQ000039_TRANSPORT_GATES_1_2": "PASS",
    }
    observed = {key: get(lines, key) for key in expected}
    if observed != expected:
        raise RuntimeError(f"transport gate drift: {observed}")
    payload = {
        "schema": "effective-stark-rq000039-engine-b-transport-gates-1-2-v1",
        "claim_tag": "PROVED_EXACT_TRANSPORT_GATES_1_2",
        "source_case_id": "RQ-000021",
        "target_case_id": "RQ-000039",
        "closure_id": "B5-015",
        "proved_gates": {
            "finite_modulus_relation": "target = source times the unique norm-two prime ideal",
            "ray_class_map": "canonical C6-to-C6 surjection has matrix 1 and preserves identity, generator, and sign log 3",
        },
        "open_gates": [
            "positive_orientation_at_the_split_real_place",
            "Artin-labelled_packet_distribution_or_direct_target_equality",
        ],
        "claim_boundary": "does not identify, transport, or promote the RQ-000039 packet",
        "transcript": completed.stdout + completed.stderr,
        "source_hashes": {
            "proof/rq000039_transport_gates_1_2.gp": sha256(SCRIPT),
            "docs/cycle-106-engine-b-first-transport-preregistration.md": sha256(PREREG),
            "scripts/run_rq000039_transport_gates_1_2.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("RQ000039_TRANSPORT_GATES_1_2=PASS")


if __name__ == "__main__":
    main()
