#!/usr/bin/env python3
"""Merge completed W2 tranches and expose theorem-level deduplication."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEMS = [
    "engine-b-two-route-degree24-v1",
    "engine-b-two-route-degree32-v1",
    "engine-b-two-route-degree40-v1",
]
OUTPUT = ROOT / "artifacts" / "engine-b-two-route-analysis-v1.json"
C_ANALYSIS = ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"


def transcript_fields(path: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    blocks = re.split(r"(?m)^===== [^\n]+ =====\n", path.read_text())
    for block in blocks[1:]:
        values: dict[str, list[str]] = collections.defaultdict(list)
        for line in block.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key].append(value)
        case_id = values["CASE_ID"][0]
        result[case_id] = {
            "normal_closure_absolute_field":
                values["NORMAL_CLOSURE_ABSOLUTE_FIELD"][0],
            "commutator_fixed_absolute_field":
                values["COMMUTATOR_FIXED_ABSOLUTE_FIELD"][0],
            "abelian_imaginary_bases":
                values.get("ROUTE1_ABELIAN_IMAGINARY_BASES", ["[]"])[0],
        }
    return result


def main() -> None:
    c_analysis = json.loads(C_ANALYSIS.read_text())
    rerouted = set(c_analysis["reroute_b_case_ids"])
    records: list[dict] = []
    source_hashes = {}
    for stem in STEMS:
        json_path = ROOT / "artifacts" / f"{stem}.json"
        transcript_path = ROOT / "artifacts" / f"{stem}.transcript"
        source_hashes[json_path.name] = hashlib.sha256(
            json_path.read_bytes()
        ).hexdigest()
        source_hashes[transcript_path.name] = hashlib.sha256(
            transcript_path.read_bytes()
        ).hexdigest()
        fields = transcript_fields(transcript_path)
        data = json.loads(json_path.read_text())
        for row in data["records"]:
            enriched = dict(row)
            enriched.update(fields[row["case_id"]])
            enriched["queue_origin"] = (
                "C_GEOMETRY_REROUTE"
                if row["case_id"] in rerouted else "ORIGINAL_B"
            )
            records.append(enriched)

    classification_counts = collections.Counter(
        row["classification"] for row in records
    )
    by_degree: dict[str, dict[str, int]] = {}
    for degree in sorted({row["normal_closure_degree"] for row in records}):
        selected = [
            row for row in records
            if row["normal_closure_degree"] == degree
        ]
        by_degree[str(degree)] = dict(sorted(collections.Counter(
            row["classification"] for row in selected
        ).items()))

    pass_records = [
        row for row in records
        if row["classification"] == "TWO_ROUTE_PASS"
    ]
    normal_multiplicity = collections.Counter(
        row["normal_closure_absolute_field"] for row in pass_records
    )
    base_pair_multiplicity = collections.Counter(
        row["abelian_imaginary_bases"] for row in pass_records
    )
    payload = {
        "schema": "effective-stark-engine-b-two-route-analysis-v1",
        "claim_tag": "VERIFIED_W2_SCREEN",
        "scope": (
            "all 372 queued cases of normal-closure degree <= 40"
        ),
        "source_hashes": source_hashes,
        "case_count": len(records),
        "classification_counts": dict(sorted(classification_counts.items())),
        "classification_by_degree": by_degree,
        "original_b_count": sum(
            row["queue_origin"] == "ORIGINAL_B" for row in records
        ),
        "c_geometry_reroute_count": sum(
            row["queue_origin"] == "C_GEOMETRY_REROUTE"
            for row in records
        ),
        "two_route_pass_case_count": len(pass_records),
        "two_route_pass_distinct_normal_closures": len(normal_multiplicity),
        "deduplication_factor":
            len(pass_records) / len(normal_multiplicity),
        "two_route_pass_distinct_cm_base_sets": len(base_pair_multiplicity),
        "largest_normal_closure_multiplicities": [
            {"polynomial": polynomial, "case_count": count}
            for polynomial, count in normal_multiplicity.most_common(20)
        ],
        "largest_cm_base_set_multiplicities": [
            {"cm_bases": bases, "case_count": count}
            for bases, count in base_pair_multiplicity.most_common(20)
        ],
        "records": records,
        "interpretation": {
            "predicate_correction": (
                "Shintani index two and the real-place split test do not "
                "imply an abelian imaginary quadratic base.  The latter "
                "is a separate Engine-B predicate."
            ),
            "route_consistency": (
                "Every case with an abelian imaginary base reconstructed "
                "the same normal field from the k-side ray subfield."
            ),
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        key: payload[key]
        for key in [
            "case_count",
            "classification_counts",
            "classification_by_degree",
            "two_route_pass_case_count",
            "two_route_pass_distinct_normal_closures",
            "deduplication_factor",
            "two_route_pass_distinct_cm_base_sets",
        ]
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
