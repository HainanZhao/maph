#!/usr/bin/env python3
"""Run the Cycle-104 exact Hilbert/ray containment tranche."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/test_hilbert_ray_containment_tranche.gp"
PREREG = ROOT / "docs/cycle-104-hilbert-ray-containment-tranche-preregistration.md"
OUTPUT = ROOT / "artifacts/hilbert-ray-containment-tranche-v1.json"

CASES = {
    "RQ-001569": {"base_radicand": 42, "hilbert_field_polynomial": "y^4 - 46*y^2 + 361"},
    "RQ-001894": {"base_radicand": 51, "hilbert_field_polynomial": "y^4 - 40*y^2 + 196"},
    "RQ-007519": {"base_radicand": 186, "hilbert_field_polynomial": "y^4 - 190*y^2 + 8281"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fields(stdout: str) -> dict[str, dict[str, str]]:
    parsed: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key == "CASE_ID":
            current = value
            if current in parsed:
                raise RuntimeError(f"duplicate case output: {current}")
            parsed[current] = {}
        elif current is not None:
            parsed[current][key] = value
    return parsed


def require(record: dict[str, str], key: str) -> str:
    if key not in record:
        raise RuntimeError(f"missing {key}")
    return record[key]


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    completed = subprocess.run(
        ["gp", "-q", str(SCRIPT)], cwd=ROOT, text=True,
        capture_output=True, timeout=3 * 3600, check=True,
    )
    parsed = fields(completed.stdout)
    if set(parsed) != set(CASES):
        raise RuntimeError(f"unexpected case set: {sorted(parsed)}")
    records = []
    for case_id, frozen in CASES.items():
        result = parsed[case_id]
        if require(result, "SELECTOR_IRREDUCIBLE") != "1":
            raise RuntimeError(f"{case_id}: selector is reducible")
        if require(result, "HILBERT_FIELD_IRREDUCIBLE") != "1":
            raise RuntimeError(f"{case_id}: Hilbert polynomial is reducible")
        if require(result, "NORMAL_CLOSURE_IRREDUCIBLE") != "1":
            raise RuntimeError(f"{case_id}: normal polynomial is reducible")
        matches = int(require(result, "HILBERT_FIELD_MATCH_COUNT"))
        contained = int(require(result, "HILBERT_FIELD_CONTAINED"))
        if contained != int(matches > 0):
            raise RuntimeError(f"{case_id}: containment consistency failure")
        records.append({
            "case_id": case_id,
            **frozen,
            "normal_closure_degree": int(require(result, "NORMAL_CLOSURE_DEGREE")),
            "degree4_subfield_count": int(require(result, "DEGREE4_SUBFIELD_COUNT")),
            "hilbert_field_match_count": matches,
            "hilbert_field_contained": bool(contained),
            "hilbert_field_isomorphisms": require(result, "HILBERT_FIELD_ISOMORPHISMS"),
        })
    payload = {
        "schema": "effective-stark-hilbert-ray-containment-tranche-v1",
        "claim_tag": "PROVED_EXACT_SUBFIELD_TEST",
        "claim_boundary": "field containment only; no Stark-unit, packet, or theorem-hypothesis comparison",
        "records": records,
        "transcript": completed.stdout + completed.stderr,
        "source_hashes": {
            "scripts/test_hilbert_ray_containment_tranche.gp": sha256(SCRIPT),
            "docs/cycle-104-hilbert-ray-containment-tranche-preregistration.md": sha256(PREREG),
            "scripts/run_hilbert_ray_containment_tranche.py": sha256(Path(__file__)),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("HILBERT_RAY_CONTAINMENT_TRANCHE=PASS")


if __name__ == "__main__":
    main()
