#!/usr/bin/env python3
"""Assemble the bounded remaining W4 slices from certified inputs."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W2 = ROOT / "artifacts/engine-b-closure-w2-coverage-v1.json"
Q = ROOT / "artifacts/census-q-packet-corpus-audit-v1.json"
TRANSPORT = ROOT / "artifacts/engine-b-transport-manifest-v5.json"
PREREG = ROOT / "docs/cycle-100-w4-completion-scope.md"
OUTPUT = ROOT / "artifacts/w4-completion-v1.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def median(values: list[int]) -> str:
    values = sorted(values)
    middle = len(values) // 2
    if len(values) % 2:
        return str(values[middle])
    return str(Fraction(values[middle - 1] + values[middle], 2))

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    w2 = json.loads(W2.read_text())
    q = json.loads(Q.read_text())
    transport = json.loads(TRANSPORT.read_text())
    closures = w2["closures"]
    if w2["closure_coverage"]["verified_w2"] != 51 or len(closures) != 51:
        raise RuntimeError("safe-exponent W2 scope drifted")
    by_degree: dict[int, list[int]] = defaultdict(list)
    for row in closures:
        by_degree[row["normal_closure_degree"]].append(row["safe_exponent"])
    safe_by_degree = {
        str(degree): {
            "closure_count": len(values), "minimum": min(values),
            "median": median(values), "maximum": max(values),
        }
        for degree, values in sorted(by_degree.items())
    }
    safe_values = [row["safe_exponent"] for row in closures]
    if (min(safe_values), max(safe_values)) != (
            w2["safe_exponent_range"]["minimum"],
            w2["safe_exponent_range"]["maximum"]):
        raise RuntimeError("safe-exponent range drifted")
    degrees = q["exact_distributions"]["packet_degree_over_K"]
    if sum(degrees.values()) != q["chain"]["row_count"] or q["chain"]["row_count"] != 1560:
        raise RuntimeError("Q packet-family distribution drifted")
    completed = transport["counts"]["member_transport_completed"]
    if completed != 0:
        raise RuntimeError("tower slice preregistration no longer applies")
    payload = {
        "schema": "effective-stark-w4-completion-v1",
        "claim_tag": "OBSERVED_EXACT_FINITE_CENSUS",
        "claim_boundary": {
            "safe_exponent": "51 certified W2 closures only; not all 88 v5 closures",
            "packet_polynomial": "exhaustive 1,560-row Q stratum only",
            "tower_norm_compatibility": "no completed v5 transport; no recurrence inferred",
        },
        "safe_exponent_growth": {
            "closure_scope": 51,
            "by_normal_closure_degree": safe_by_degree,
            "overall_minimum": min(safe_values),
            "overall_maximum": max(safe_values),
        },
        "packet_polynomial_families": {
            "q_rows": 1560, "degree_over_K": degrees,
            "common_denominator": q["exact_distributions"]["common_denominator"],
        },
        "tower_norm_compatibility": {
            "completed_member_transports": completed,
            "status": "NO_DATA_GATE",
            "inference": "none",
        },
        "source_hashes": {
            "artifacts/engine-b-closure-w2-coverage-v1.json": sha256(W2),
            "artifacts/census-q-packet-corpus-audit-v1.json": sha256(Q),
            "artifacts/engine-b-transport-manifest-v5.json": sha256(TRANSPORT),
            "docs/cycle-100-w4-completion-scope.md": sha256(PREREG),
            "scripts/build_w4_completion.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("W4_COMPLETION=PASS")

if __name__ == "__main__":
    main()
