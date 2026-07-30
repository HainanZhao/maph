#!/usr/bin/env python3
"""Independently check Engine-B closure-tranche artifact consistency."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "artifacts" / "post-theorem-bulk-plan-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gp_vector(text: str) -> list[int]:
    if not re.fullmatch(r"\[\s*\d+(?:\s*,\s*\d+)*\s*\]", text):
        raise RuntimeError(f"not a positive-integer GP vector: {text}")
    return [int(value) for value in re.findall(r"\d+", text)]


def verify(summary_path: Path) -> dict:
    summary = json.loads(summary_path.read_text())
    if summary["claim_tag"] != "VERIFIED_W2_TRANCHE":
        raise RuntimeError("unexpected tranche claim tag")
    if summary["w3_verified_count"] != 0:
        raise RuntimeError("W3 promotion is outside the W2 tranche contract")
    plan = json.loads(PLAN.read_text())
    frozen = {
        row["canonical_representative"]: row
        for row in plan["engine_b"]["remaining_closures"]
    }
    seen_closures: set[str] = set()
    safe_exponents = {}
    for row in summary["records"]:
        case_id = row["case_id"]
        certificate_path = ROOT / row["certificate_path"]
        transcript_path = ROOT / row["transcript_path"]
        if sha256(certificate_path) != row["certificate_sha256"]:
            raise RuntimeError(f"{case_id}: certificate hash mismatch")
        if sha256(transcript_path) != row["transcript_sha256"]:
            raise RuntimeError(f"{case_id}: transcript hash mismatch")
        certificate = json.loads(certificate_path.read_text())
        expected = frozen[case_id]
        closure = certificate["normal_closure_absolute_field"]
        if closure != expected["normal_closure_absolute_field"]:
            raise RuntimeError(f"{case_id}: closure differs from frozen plan")
        if closure in seen_closures:
            raise RuntimeError(f"{case_id}: repeated closure in tranche")
        seen_closures.add(closure)
        two_route = certificate["two_route"]
        if (
            not two_route["all_routes_reconstruct_identical_closure"]
            or two_route["matching_route_count"]
            != two_route["abelian_imaginary_route_count"]
        ):
            raise RuntimeError(f"{case_id}: two-route gate not closed")
        divisor = certificate["selected_divisor_route"]
        clearing = gp_vector(divisor["clearing_exponents"])
        measured_lcm = math.lcm(*clearing)
        if measured_lcm != divisor["safe_exponent"]:
            raise RuntimeError(f"{case_id}: safe exponent is not the lcm")
        transcript = transcript_path.read_text()
        required = (
            "ENGINE_B_TWO_ROUTE_SCREEN_COMPLETE=1",
            "GENERIC_IMAGINARY_DIVISOR_TABLE_VERIFIED=1",
            f"SHINTANI_SAFE_EXPONENT={measured_lcm}",
        )
        if any(marker not in transcript for marker in required):
            raise RuntimeError(f"{case_id}: transcript marker missing")
        if certificate["w3"]["state"] != "PENDING" or row["w3"] != "PENDING":
            raise RuntimeError(f"{case_id}: invalid W3 state")
        safe_exponents[case_id] = measured_lcm
    if len(summary["records"]) != summary["closure_count"]:
        raise RuntimeError("closure count mismatch")
    if sum(row["member_occurrence_count"] for row in summary["records"]) != (
        summary["member_occurrence_count"]
    ):
        raise RuntimeError("member occurrence count mismatch")
    return {
        "claim_tag": "VERIFIED_ARTIFACT_CHECK",
        "summary": str(summary_path.relative_to(ROOT)),
        "summary_sha256": sha256(summary_path),
        "closure_count": summary["closure_count"],
        "safe_exponents": safe_exponents,
        "w3_promotions": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path, nargs="+")
    arguments = parser.parse_args()
    results = []
    for path in arguments.summary:
        if not path.is_absolute():
            path = ROOT / path
        results.append(verify(path))
    print(json.dumps({"results": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
