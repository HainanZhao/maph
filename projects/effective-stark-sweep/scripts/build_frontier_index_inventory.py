#!/usr/bin/env python3
"""Build the exact post-routing FRONTIER predicate ledger.

This does not trust the aggregate counts.  It reconstructs the final
1,818-row population from the W1, complete Engine-C, and corrected
Engine-B records, then records the exact index and real-place predicate
separately.  The separation is essential: historical
``INDEX_GT_2`` meant ``index != 2 OR split predicate fails``.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
C_ANALYSIS = ARTIFACTS / "engine-c-geometry-analysis-v1.json"
B_ANALYSIS = ARTIFACTS / "engine-b-two-route-analysis-v1.json"
QUEUES = ARTIFACTS / "identification-queues-v2.json"
OUTPUT = ARTIFACTS / "frontier-index-inventory-v1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_record(numerator: int, denominator: int) -> dict:
    value = Fraction(numerator, denominator)
    return {
        "numerator": numerator,
        "denominator": denominator,
        "reduced": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def main() -> None:
    w1 = load(W1)
    c_analysis = load(C_ANALYSIS)
    b_analysis = load(B_ANALYSIS)
    queues = load(QUEUES)
    rows = w1["records"]
    by_id = {row["case_id"]: row for row in rows}
    if len(by_id) != 8200:
        raise RuntimeError("W1 case identifiers are not unique")

    final: dict[str, tuple[str, str, dict | None]] = {}

    def add(
        case_id: str,
        obstruction: str,
        source: str,
        detail: dict | None = None,
    ) -> None:
        if case_id in final:
            raise RuntimeError(
                f"duplicate final classification for {case_id}: "
                f"{final[case_id]} versus {(obstruction, source)}"
            )
        final[case_id] = (obstruction, source, detail)

    for row in rows:
        if row["verdict"] == "FRONTIER":
            add(
                row["case_id"],
                row["obstruction"],
                "W1_STRUCTURAL_SCREEN",
            )

    for record in c_analysis["frontier_cases"]:
        add(
            record["case_id"],
            record["obstruction"],
            "COMPLETE_ENGINE_C_GEOMETRY",
            record,
        )
    packet_records = c_analysis["packet_records"]
    for case_id in c_analysis["tool_blocked_case_ids"]:
        statuses = [
            record["status"]
            for record in packet_records
            if record["case_id"] == case_id
        ]
        add(
            case_id,
            "TOOL_BLOCKED",
            "COMPLETE_ENGINE_C_GEOMETRY",
            {"packet_statuses": statuses},
        )

    for record in b_analysis["records"]:
        if record["classification"] == "NO_ABELIAN_IMAGINARY_BASE":
            add(
                record["case_id"],
                "NO_ABELIAN_IMAGINARY_BASE",
                "CORRECTED_ENGINE_B_TWO_ROUTE",
                {
                    "normal_closure_degree":
                        record["normal_closure_degree"],
                    "abelian_imaginary_bases":
                        record["abelian_imaginary_bases"],
                    "route1_abelian_imaginary_base_count":
                        record["route1_abelian_imaginary_base_count"],
                    "two_route_ray_subfield_match_count":
                        record["two_route_ray_subfield_match_count"],
                },
            )

    for case_id in queues["engine_b"]["degree_above_40_pending_case_ids"]:
        add(
            case_id,
            "EXPONENT_CAP",
            "FROZEN_DEGREE_CAP",
            {
                "boundary": (
                    "normal closure degree exceeds the frozen full-"
                    "identification cap 40"
                )
            },
        )

    if len(final) != 1818:
        raise RuntimeError(
            f"expected 1818 final FRONTIER rows, got {len(final)}"
        )

    records = []
    for case_id in sorted(final):
        obstruction, source, detail = final[case_id]
        row = by_id[case_id]
        index = int(row["shintani_index"])
        split = bool(row["exactly_one_real_place_splitting"])
        index_components = []
        if index != 2:
            index_components.append("SHINTANI_INDEX_NOT_2")
        if not split:
            index_components.append("REAL_PLACE_SPLITTING_NOT_EXACTLY_ONE")
        records.append(
            {
                "case_id": case_id,
                "d": row["d"],
                "field_discriminant": row["field_discriminant"],
                "finite_ideal_hnf": row["finite_ideal_hnf"],
                "finite_norm": row["finite_norm"],
                "final_obstruction": obstruction,
                "classification_source": source,
                "shintani_index": index,
                "exactly_one_real_place_splitting": split,
                "index_battery_failure_components": index_components,
                "unit_predicates": {
                    "condition_03":
                        bool(row["b03_positive_not_minus_one"]),
                    "condition_06":
                        bool(row["b06_negative_norm_not_one"]),
                },
                "ray_predicates": {
                    "one_place_cyclic_structure": row["one_cyc"],
                    "two_place_cyclic_structure": row["both_cyc"],
                    "one_place_exponent": row["one_exponent"],
                    "one_place_kernel_size":
                        row["one_place_kernel_size"],
                    "commutator_size": row["commutator_size"],
                },
                "later_screen_detail": detail,
            }
        )

    taxonomy = Counter(record["final_obstruction"] for record in records)
    expected = {
        "EXPONENT_CAP": 502,
        "INDEX_GT_2": 1100,
        "NO_ABELIAN_IMAGINARY_BASE": 177,
        "REAL_PLACE_SPLITTING_FAIL": 2,
        "TOOL_BLOCKED": 4,
        "UNIT_CONGRUENCE_FAIL": 33,
    }
    if dict(sorted(taxonomy.items())) != expected:
        raise RuntimeError(
            f"taxonomy mismatch: {dict(sorted(taxonomy.items()))}"
        )

    index_rows = [
        record
        for record in records
        if record["final_obstruction"] == "INDEX_GT_2"
    ]
    odd = [
        {
            "case_id": record["case_id"],
            "shintani_index": record["shintani_index"],
            "finite_norm": record["finite_norm"],
            "split_predicate":
                record["exactly_one_real_place_splitting"],
        }
        for record in index_rows
        if record["shintani_index"] > 2
        and record["shintani_index"] % 2 == 1
    ]
    predicate_combinations = Counter(
        (
            "INDEX_EQ_2"
            if record["shintani_index"] == 2
            else "INDEX_NE_2",
            "SPLIT_PASS"
            if record["exactly_one_real_place_splitting"]
            else "SPLIT_FAIL",
        )
        for record in index_rows
    )

    by_norm: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    frontier_ids = set(final)
    for row in rows:
        norm = int(row["finite_norm"])
        by_norm[norm][0] += 1
        by_norm[norm][1] += row["case_id"] in frontier_ids
    quartiles = []
    for left, right in ((1, 25), (26, 50), (51, 75), (76, 100)):
        total = sum(by_norm[n][0] for n in range(left, right + 1))
        frontier = sum(by_norm[n][1] for n in range(left, right + 1))
        quartiles.append(
            {
                "norm_interval": [left, right],
                "total": total,
                "frontier": frontier,
                "frontier_share": fraction_record(frontier, total),
            }
        )
    monotone = all(
        Fraction(left["frontier"], left["total"])
        < Fraction(right["frontier"], right["total"])
        for left, right in zip(quartiles, quartiles[1:])
    )

    output = {
        "schema": "effective-stark-frontier-index-inventory-v1",
        "claim_tag": "AUDITED_WITH_ANOMALY",
        "record_count": len(records),
        "taxonomy": expected,
        "historical_label_semantics": (
            "INDEX_GT_2 was emitted when shintani_index != 2 OR the "
            "exactly-one-real-place splitting predicate failed; it is "
            "not a literal assertion that every stored index exceeds 2."
        ),
        "index_obstruction_audit": {
            "row_count": len(index_rows),
            "index_distribution": {
                str(key): value
                for key, value in sorted(
                    Counter(
                        record["shintani_index"] for record in index_rows
                    ).items()
                )
            },
            "predicate_combinations": {
                f"{key[0]}__{key[1]}": value
                for key, value in sorted(predicate_combinations.items())
            },
            "odd_index_above_two_count": len(odd),
            "odd_index_above_two_distribution": {
                str(key): value
                for key, value in sorted(
                    Counter(
                        record["shintani_index"] for record in odd
                    ).items()
                )
            },
            "odd_index_above_two_cases": odd,
            "status": "ESCALATED_DISCOVERY_CANDIDATES",
        },
        "corrected_frontier_norm_trend": {
            "quartiles": quartiles,
            "strictly_increasing": monotone,
        },
        "records": records,
        "sources": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (W1, C_ANALYSIS, B_ANALYSIS, QUEUES)
        },
    }
    serialized = json.dumps(output, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(serialized, encoding="utf-8")
    print(f"FRONTIER_ROWS={len(records)}")
    print(f"ODD_INDEX_ABOVE_TWO={len(odd)}")
    print(f"NORM_TREND_STRICTLY_INCREASING={int(monotone)}")
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
