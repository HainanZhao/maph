#!/usr/bin/env python3
"""Seal exact coverage of the 51-closure Engine-B W2 campaign."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "artifacts" / "post-theorem-bulk-plan-v1.json"
OUTPUT = ROOT / "artifacts" / "engine-b-closure-w2-coverage-v1.json"
TRANCHES = [
    ROOT / "artifacts" / f"engine-b-closure-tranche-{index:02d}-v1.json"
    for index in range(1, 12)
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_strings(values: list[str]) -> str:
    encoded = json.dumps(
        values, ensure_ascii=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    plan = json.loads(PLAN.read_text())
    expected = {
        row["canonical_representative"]: row
        for row in plan["engine_b"]["remaining_closures"]
    }
    records = []
    for path in TRANCHES:
        tranche = json.loads(path.read_text())
        if tranche["claim_tag"] != "VERIFIED_W2_TRANCHE":
            raise RuntimeError(f"{path.name}: wrong claim tag")
        if tranche["w3_verified_count"] or (
            tranche["w3_pending_count"] != tranche["closure_count"]
        ):
            raise RuntimeError(f"{path.name}: invalid W3 accounting")
        records.extend(tranche["records"])
    by_case = {row["case_id"]: row for row in records}
    if len(by_case) != len(records):
        raise RuntimeError("a canonical representative occurs twice")
    if set(by_case) != set(expected):
        missing = sorted(set(expected) - set(by_case))
        extra = sorted(set(by_case) - set(expected))
        raise RuntimeError(f"coverage mismatch; missing={missing}, extra={extra}")

    closure_records = []
    all_member_ids = []
    normal_fields = set()
    for case_id, planned in sorted(
        expected.items(), key=lambda item: item[1]["closure_index"]
    ):
        measured = by_case[case_id]
        certificate_path = ROOT / measured["certificate_path"]
        certificate = json.loads(certificate_path.read_text())
        if sha256(certificate_path) != measured["certificate_sha256"]:
            raise RuntimeError(f"{case_id}: certificate hash mismatch")
        if certificate["claim_tag"] != "VERIFIED_W2":
            raise RuntimeError(f"{case_id}: W2 is not verified")
        normal_field = certificate["normal_closure_absolute_field"]
        if normal_field != planned["normal_closure_absolute_field"]:
            raise RuntimeError(f"{case_id}: frozen closure changed")
        if normal_field in normal_fields:
            raise RuntimeError(f"{case_id}: duplicate normal closure")
        normal_fields.add(normal_field)
        member_ids = sorted(planned["case_ids"])
        if len(member_ids) != planned["occurrence_count"]:
            raise RuntimeError(f"{case_id}: member count mismatch")
        all_member_ids.extend(member_ids)
        closure_records.append(
            {
                "closure_index": planned["closure_index"],
                "canonical_representative": case_id,
                "normal_closure_degree": planned["normal_closure_degree"],
                "member_occurrence_count": len(member_ids),
                "member_case_ids": member_ids,
                "member_case_ids_sha256": digest_strings(member_ids),
                "selected_imaginary_base":
                    measured["selected_base"],
                "divisor_count": measured["divisor_count"],
                "safe_exponent": measured["safe_exponent"],
                "w2_certificate": measured["certificate_path"],
                "w2_certificate_sha256":
                    measured["certificate_sha256"],
                "w3_state": "PENDING",
                "member_transport_state": "PENDING",
            }
        )
    all_member_ids.sort()
    if len(all_member_ids) != len(set(all_member_ids)):
        raise RuntimeError("member identity occurs in two closures")

    b_plan = plan["engine_b"]
    if len(closure_records) != b_plan["remaining_closure_count"]:
        raise RuntimeError("remaining closure count changed")
    if len(all_member_ids) != b_plan["remaining_closure_occurrence_count"]:
        raise RuntimeError("remaining occurrence count changed")
    unresolved_transport = (
        len(all_member_ids)
        + b_plan["unverified_members_of_banked_closures"]
    )
    if unresolved_transport != b_plan["remaining_occurrence_identities"]:
        raise RuntimeError("transport decomposition changed")

    safe_exponents = [row["safe_exponent"] for row in closure_records]
    output = {
        "schema": "effective-stark-engine-b-closure-w2-coverage-v1",
        "claim_tag": "VERIFIED_W2_CLOSURE_COVERAGE",
        "claim_boundary": (
            "All 51 previously unbanked normal closures have fresh exact "
            "two-route and divisor-table W2 certificates. Closure coverage "
            "does not identify or orient any member occurrence and is not "
            "a W3 packet claim."
        ),
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in [PLAN, *TRANCHES]
        },
        "closure_coverage": {
            "required": b_plan["remaining_closure_count"],
            "verified_w2": len(closure_records),
            "two_route_disagreements": 0,
            "divisor_audit_failures": 0,
            "w3_promotions_in_campaign": 0,
            "w3_pending": len(closure_records),
        },
        "occurrence_identity_coverage": {
            "eligible_b_occurrences_total":
                b_plan["eligible_occurrences"],
            "member_identities_under_the_51_audited_closures":
                len(all_member_ids),
            "member_identities_sha256":
                digest_strings(all_member_ids),
            "member_case_ids": all_member_ids,
            "occurrence_transport_completed_by_w2_campaign": 0,
            "occurrence_transport_pending_in_51_closures":
                len(all_member_ids),
            "extra_transport_pending_in_8_banked_closures":
                b_plan["unverified_members_of_banked_closures"],
            "occurrence_transport_pending_total":
                unresolved_transport,
        },
        "safe_exponent_range": {
            "minimum": min(safe_exponents),
            "maximum": max(safe_exponents),
        },
        "closures": closure_records,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "claim_tag": output["claim_tag"],
                "closure_coverage":
                    output["closure_coverage"],
                "occurrence_identity_coverage": {
                    key: value
                    for key, value in output[
                        "occurrence_identity_coverage"
                    ].items()
                    if key != "member_case_ids"
                },
                "safe_exponent_range": output["safe_exponent_range"],
                "output": str(OUTPUT.relative_to(ROOT)),
                "output_sha256": sha256(OUTPUT),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
