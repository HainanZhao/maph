#!/usr/bin/env python3
"""Seal the genuine RQ-007500 reconstruction and compare it to old W2 data."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
OLD = ARTIFACTS / "rq007500-b-closure-w2-v1.json"
TRANSCRIPT = ARTIFACTS / "rq007500-genuine-normal-closure-v1.transcript"
SCRIPT = ROOT / "scripts/rq007500_genuine_normal_closure.gp"
OUTPUT = ARTIFACTS / "rq007500-genuine-recovery-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fields(text: str) -> dict[str, str]:
    ansi = re.compile(r"\x1b\\\[[0-9;]*m")
    result: dict[str, str] = {}
    for raw in text.splitlines():
        line = ansi.sub("", raw)
        if "=" in line and not line.lstrip().startswith("***"):
            key, value = line.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def main() -> None:
    old = json.loads(OLD.read_text(encoding="utf-8"))
    parsed = fields(TRANSCRIPT.read_text(encoding="utf-8"))
    required = {
        "CASE_ID": "RQ-007500",
        "PROVENANCE": "GENUINE",
        "BASE_BNFCERTIFY": "1",
        "FINITE_NORM": "90",
        "ONE_PLACE_RAY_CYC": "[8]",
        "ONE_PLACE_RELATIVE_DEGREE": "8",
        "ONE_PLACE_ABSOLUTE_DEGREE": "16",
        "ACTUAL_NORMAL_CLOSURE_DEGREE": "32",
        "ACTUAL_NORMAL_CLOSURE_GROUP_ID": "[32, 38]",
        "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT": "2",
        "ROUTE2_BASE_1_MATCH": "1",
        "ROUTE2_BASE_2_MATCH": "1",
        "TWO_ROUTE_MATCH_INDICES": "[1, 2]",
        "GENUINE_RECONSTRUCTION_COMPLETE": "1",
    }
    for key, expected in required.items():
        actual = parsed.get(key)
        if actual != expected:
            raise RuntimeError(f"{key}: expected {expected}, got {actual}")
    if (
        parsed["ACTUAL_NORMAL_CLOSURE_POLYNOMIAL"]
        != old["normal_closure_absolute_field"]
    ):
        raise RuntimeError("genuine closure differs from historical closure")

    payload = {
        "schema": "effective-stark-rq007500-genuine-recovery-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "case_identity": {
            "case_id": "RQ-007500",
            "field": "Q(sqrt(185))",
            "modulus": {
                "finite_ideal_hnf": [[30, 6], [0, 3]],
                "finite_norm": 90,
                "infinite_part": "infinity_2",
            },
            "support_orders": [8],
        },
        "contaminated_route": {
            "stage": "GENERIC_ENGINE_B_W2",
            "historical_artifact": str(OLD.relative_to(ROOT)),
            "description": (
                "the generic path treated the full two-place ray field "
                "at the original unstable finite modulus as the normal "
                "closure; that equality had not been reconstructed"
            ),
            "historical_effective_tag": "SUPERSEDED_PROXY_W2",
        },
        "genuine_reconstruction": {
            "method": (
                "construct the one-place degree-8 ray field, take its "
                "absolute degree-16 polynomial, then compute its actual "
                "splitting field with nfsplitting"
            ),
            "predicate_provenance": "GENUINE",
            "base_bnfcertify": 1,
            "one_place_ray_cyc": [8],
            "one_place_absolute_degree": 16,
            "normal_closure_degree": 32,
            "normal_closure_group_id": [32, 38],
            "normal_closure_polynomial": parsed[
                "ACTUAL_NORMAL_CLOSURE_POLYNOMIAL"
            ],
            "identical_to_historical_polynomial": True,
            "abelian_imaginary_bases": [
                "x^2 - x + 1",
                "x^2 - x + 139",
            ],
            "base_interpretations": ["Q(sqrt(-3))", "Q(sqrt(-555))"],
            "independent_ray_reconstruction_matches": [True, True],
        },
        "verdict": {
            "outcome": "RE_PASSES",
            "effective_tag": "VERIFIED_W2_GENUINE_RECOVERY",
            "b_completed_closure_count": 51,
            "w3_state": "PENDING",
            "scope": (
                "W2 field/base reconstruction only; no analytic packet "
                "identity is promoted"
            ),
        },
        "source_hashes": {
            str(OLD.relative_to(ROOT)): sha(OLD),
            str(TRANSCRIPT.relative_to(ROOT)): sha(TRANSCRIPT),
            str(SCRIPT.relative_to(ROOT)): sha(SCRIPT),
            "scripts/certify_rq007500_recovery.py": sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
