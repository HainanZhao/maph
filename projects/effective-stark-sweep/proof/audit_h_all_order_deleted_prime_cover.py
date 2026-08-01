#!/usr/bin/env python3
"""Seal the all-order deleted-prime cover screen for the frozen H stratum.

The mathematical implication is stated in the accompanying theorem note.
This program audits only its finite, exact local input: a phase denominator
of one is an exact equality of a finite-order character value with one.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts/w1-full-census-v1.json"
FEATURES = ROOT / "discovery/h-euler-local-features-v1.json"
PREREG = ROOT / "docs/cycle-131-all-order-deleted-prime-cover-preregistration.md"
THEOREM_NOTE = ROOT / "docs/cycle-131-all-order-deleted-prime-cover-theorem.md"
OUT = ROOT / "artifacts/h-all-order-deleted-prime-cover-audit-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def verify_recorded_hashes(payload: dict) -> None:
    for relative, expected in payload["source_hashes"].items():
        path = ROOT / relative
        if sha256(path) != expected:
            raise RuntimeError(f"source hash changed: {relative}")
    transcript = payload["transcript"]
    if sha256(ROOT / transcript["path"]) != transcript["sha256"]:
        raise RuntimeError("feature-export transcript hash changed")


def compute_certificate() -> dict:
    census = load(CENSUS)
    features = load(FEATURES)
    verify_recorded_hashes(features)
    frozen = {
        row["case_id"]: row
        for row in census["records"]
        if max(row["support_orders"], default=0) > 2
    }
    records = features["records"]
    if len(frozen) != 2704 or len(records) != 2704:
        raise RuntimeError("frozen H population changed")
    if {row["case_id"] for row in records} != set(frozen):
        raise RuntimeError("feature export does not cover exactly the H population")

    character_count = 0
    covered_character_count = 0
    no_deleted_prime_count = 0
    deleted_but_uncovered_count = 0
    fully_covered_ids = []
    order_histogram: Counter[int] = Counter()
    row_shape_histogram: Counter[str] = Counter()
    errors = []
    for row in records:
        original = frozen[row["case_id"]]
        for key in ("base_radicand", "finite_norm", "finite_ideal_hnf", "support_count"):
            if row[key] != original[{"base_radicand": "d"}.get(key, key)]:
                errors.append(f"{row['case_id']}:{key}")
        if row["ray_cyc"] != original["one_cyc"] or row["sign_log"] != original["sign_log"]:
            errors.append(f"{row['case_id']}:ray-data")
        if row["support_orders"] != original["support_orders"]:
            errors.append(f"{row['case_id']}:support-orders")

        local_cover = True
        for character in row["characters"]:
            character_count += 1
            order_histogram[character["order"]] += 1
            deleted = character["deleted_primes"]
            exact_cover = any(
                prime["primitive_phase_denominator"] == 1 for prime in deleted
            )
            if exact_cover != character["covered_by_value_one"]:
                errors.append(f"{row['case_id']}:character-cover")
            for prime in deleted:
                if prime["primitive_phase_denominator"] < 1:
                    errors.append(f"{row['case_id']}:invalid-phase")
            covered_character_count += exact_cover
            no_deleted_prime_count += not deleted
            deleted_but_uncovered_count += bool(deleted) and not exact_cover
            local_cover = local_cover and exact_cover
        if local_cover != row["all_supported_characters_covered"]:
            errors.append(f"{row['case_id']}:row-cover")
        if local_cover:
            fully_covered_ids.append(row["case_id"])
        row_shape_histogram[",".join(map(str, row["support_orders"]))] += local_cover

    if errors:
        raise RuntimeError(f"feature audit errors: {errors[:5]}")
    if (character_count, covered_character_count, len(fully_covered_ids)) != (18865, 1040, 64):
        raise RuntimeError("frozen all-order headline counts changed")
    wall = next(row for row in records if row["case_id"] == "RQ-000692")
    if wall["all_supported_characters_covered"]:
        raise RuntimeError("RQ-000692 unexpectedly covered")
    if [char["order"] for char in wall["characters"]] != [6, 2, 6]:
        raise RuntimeError("RQ-000692 support changed")

    return {
        "schema": "effective-stark-h-all-order-deleted-prime-cover-audit-v1",
        "status": "PASS_EXACT_LOCAL_SCREEN",
        "claim_boundary": (
            "The symbolic one-way implication is PROVED in the theorem note; "
            "the finite counts are OBSERVED exact local feature results and do "
            "not assert a converse or resolve an uncovered packet."
        ),
        "theorem_reference": {
            "path": str(THEOREM_NOTE.relative_to(ROOT)),
            "claim_tag": "PROVED",
            "direction": "cover of every supported character implies packet one",
        },
        "finite_H_screen": {
            "claim_tag": "OBSERVED",
            "rows": len(records),
            "supported_character_occurrences": character_count,
            "covered_character_occurrences": covered_character_count,
            "fully_covered_rows": len(fully_covered_ids),
            "fully_covered_case_ids": fully_covered_ids,
            "characters_with_no_deleted_prime": no_deleted_prime_count,
            "characters_with_deleted_primes_but_no_value_one": deleted_but_uncovered_count,
            "support_character_order_histogram": {
                str(key): value for key, value in sorted(order_histogram.items())
            },
            "fully_covered_row_support_order_histogram": {
                key: value for key, value in sorted(row_shape_histogram.items()) if value
            },
        },
        "rq_000692_control": {
            "claim_tag": "OBSERVED",
            "covered": False,
            "support_orders": wall["support_orders"],
            "support_count": wall["support_count"],
            "conclusion": (
                "The all-order deleted-prime cover criterion does not settle "
                "this wild-3 wall; this is not evidence either way for any "
                "other sextic Stark mechanism."
            ),
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (CENSUS, FEATURES, PREREG, THEOREM_NOTE, Path(__file__))
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-artifact", action="store_true")
    args = parser.parse_args()
    computed = compute_certificate()
    if args.write_artifact:
        OUT.write_text(json.dumps(computed, indent=2, sort_keys=True) + "\n")
    else:
        if not OUT.exists() or load(OUT) != computed:
            raise RuntimeError("sealed all-order audit differs from replay")
    print("H_ALL_ORDER_DELETED_PRIME_COVER_AUDIT=PASS")
    print("H_ALL_ORDER_DELETED_PRIME_COVERED_ROWS=64")
    print("RQ_000692_ALL_ORDER_COVER=NO")


if __name__ == "__main__":
    main()
