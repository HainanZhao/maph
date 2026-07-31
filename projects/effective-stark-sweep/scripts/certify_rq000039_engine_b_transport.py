#!/usr/bin/env python3
"""Seal the first exact Engine-B member transport, B5-015."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import argparse

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "proof/rq000039_transport_gates_1_2.gp"
SOURCE = ROOT / "scripts/certify_rq000021_packet.py"
ARGUMENT = ROOT / "docs/cycle-108-rq000039-engine-b-transport-proof.md"
OUTPUT = ROOT / "artifacts/rq000039-engine-b-transport-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python-flint", required=True,
                        help="pinned Python 3.12.3 / python-flint 0.9.0 interpreter")
    arguments = parser.parse_args()
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    gates = subprocess.run(
        ["gp", "-q", str(GATES)], cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=600,
    )
    required_gates = (
        "QUOTIENT_NORM=2", "SOURCE_RAY_CYC=[6]", "TARGET_RAY_CYC=[6]",
        "RAY_MAP_MATRIX=Mat(1)", "RAY_MAP_TARGET_IDENTITY=[0]",
        "RAY_MAP_TARGET_GENERATOR=[1]", "RAY_MAP_TARGET_SIGN=[3]",
        "RQ000039_TRANSPORT_GATES_1_2=PASS",
    )
    if not all(item in gates.stdout for item in required_gates):
        raise RuntimeError("exact conductor/ray-map gate failed")
    source = subprocess.run(
        [arguments.python_flint, str(SOURCE)], cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=600,
    )
    if "RQ000021_PACKET_IDENTITY_VERIFIED=1" not in source.stdout:
        raise RuntimeError("source packet replay failed")
    payload = {
        "schema": "effective-stark-rq000039-engine-b-transport-v1",
        "claim_tag": "PROVED_EXACT_MEMBER_TRANSPORT",
        "source_case_id": "RQ-000021",
        "target_case_id": "RQ-000039",
        "closure_id": "B5-015",
        "ray_class_map": "[Mat(1),[6],[6]]",
        "added_prime": {"ideal": "[[2,0],[0,1]]", "norm": 2, "source_ray_log": 1},
        "artin_label_relation": "target label A maps to source label A; A*q^(-1) has generator log one less modulo 6",
        "packet_relation": "X_m98(A) = X_m49(A) / X_m49(A*q^(-1))",
        "orientation": "positive quotient at the same frozen split real embedding",
        "proof_route": "Euler deletion, rank-one vanishing at zero for odd characters, character inversion, exponentiation",
        "claim_boundary": "one transported noncanonical member only; no promotion of other B5-015 or Engine-B members",
        "gate_transcript": gates.stdout + gates.stderr,
        "source_packet_transcript": source.stdout + source.stderr,
        "runtime": {
            "python_flint_executable": arguments.python_flint,
            "python_flint_version": subprocess.run(
                [arguments.python_flint, "-c", "import flint; print(flint.__version__)"],
                text=True, capture_output=True, check=True, timeout=30,
            ).stdout.strip(),
        },
        "source_hashes": {
            "proof/rq000039_transport_gates_1_2.gp": sha256(GATES),
            "scripts/certify_rq000021_packet.py": sha256(SOURCE),
            "docs/cycle-108-rq000039-engine-b-transport-proof.md": sha256(ARGUMENT),
            "scripts/certify_rq000039_engine_b_transport.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("RQ000039_ENGINE_B_TRANSPORT=PASS")


if __name__ == "__main__":
    main()
