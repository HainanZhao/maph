#!/usr/bin/env python3
"""Seal the second exact Engine-B member transport, B5-025."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "proof/rq000195_transport_gates.gp"
SOURCE = ROOT / "scripts/certify_q7_p7_packet.py"
PREREG = ROOT / "docs/cycle-110-engine-b-second-transport-preregistration.md"
PROOF = ROOT / "docs/cycle-108-rq000039-engine-b-transport-proof.md"
OUTPUT = ROOT / "artifacts/rq000195-engine-b-transport-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python-flint", required=True)
    args = parser.parse_args()
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    gates = subprocess.run(["gp", "-q", str(GATES)], cwd=ROOT, text=True,
                           capture_output=True, check=True, timeout=600)
    expected = ("SOURCE_FINITE_NORM=7", "TARGET_FINITE_NORM=14",
                "QUOTIENT_NORM=2", "SOURCE_RAY_CYC=[6]", "TARGET_RAY_CYC=[6]",
                "RAY_MAP_MATRIX=Mat(1)", "SOURCE_SIGN_LOG=3", "TARGET_SIGN_LOG=3",
                "RAY_MAP_TARGET_IDENTITY=[0]", "RAY_MAP_TARGET_GENERATOR=[1]",
                "RAY_MAP_TARGET_SIGN=[3]", "ADDED_PRIME_SOURCE_RAY_LOG=1",
                "RQ000195_TRANSPORT_GATES=PASS")
    if not all(value in gates.stdout for value in expected):
        raise RuntimeError("exact transport gates failed")
    source = subprocess.run([args.python_flint, str(SOURCE)], cwd=ROOT, text=True,
                            capture_output=True, check=True, timeout=600)
    if "Q7_P7_PACKET_IDENTITY_VERIFIED=1" not in source.stdout:
        raise RuntimeError("source packet replay failed")
    payload = {
        "schema": "effective-stark-rq000195-engine-b-transport-v1",
        "claim_tag": "PROVED_EXACT_MEMBER_TRANSPORT",
        "source_case_id": "RQ-000190", "target_case_id": "RQ-000195", "closure_id": "B5-025",
        "ray_class_map": "[Mat(1),[6],[6]]",
        "added_prime": {"ideal": "[[2,1],[0,1]]", "norm": 2, "source_ray_log": 1},
        "artin_label_relation": "target label A maps to source label A; A*q^(-1) has generator log one less modulo 6",
        "packet_relation": "X_m14(A) = X_m7(A) / X_m7(A*q^(-1))",
        "orientation": "positive quotient at the same frozen split real embedding",
        "proof_route": "Cycle-108 Euler-deletion/rank-one-vanishing lemma with exact Cycle-110 gates",
        "claim_boundary": "one transported noncanonical member only; no promotion of other B5-025 or Engine-B members",
        "gate_transcript": gates.stdout + gates.stderr,
        "source_packet_transcript": source.stdout + source.stderr,
        "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (GATES, SOURCE, PREREG, PROOF, Path(__file__))},
        "runtime": {"python_flint_executable": args.python_flint,
                    "python_flint_version": subprocess.run([args.python_flint, "-c", "import flint; print(flint.__version__)"], text=True, capture_output=True, check=True).stdout.strip()},
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("RQ000195_ENGINE_B_TRANSPORT=PASS")


if __name__ == "__main__":
    main()
