#!/usr/bin/env python3
"""Assemble the preregistered 2,704-row H taxonomy and frontier."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPH = ROOT.parents[1]
W1 = ROOT / "artifacts" / "w1-full-census-v1.json"
V5 = ROOT / "artifacts" / "full-census-yield-declaration-v5.json"
QUARTIC = (
    MAPH
    / "projects"
    / "dedekind-stark-phase"
    / "artifacts"
    / "b3-roblot-population-v1.json"
)
SEXTIC = ROOT / "artifacts" / "roblot-sextic-population-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v8.json"
)
RESULTS_PAPER = ROOT / "paper" / "effective-stark-results.tex"

SELECTED_RESULTS = {
    "RQ-000021": "Engine B",
    "RQ-000108": "Engine B",
    "RQ-000129": "Engine C",
    "RQ-000190": "Engine B",
    "RQ-000419": "Engine B",
    "RQ-000458": "Engine B",
    "RQ-001107": "Engine B",
    "RQ-001280": "Engine C",
    "RQ-001569": "Engine C",
    "RQ-001894": "Engine C",
    "RQ-002057": "Engine B",
    "RQ-002955": "Engine B",
    "RQ-007519": "Engine C",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(case_id: str) -> int:
    return int(case_id.removeprefix("RQ-"))


def summarize_kernels(
    records: list[dict], applicable_key: str
) -> dict:
    exact_statuses = {
        "EXACT_SCREEN_COMPLETE",
        "EXACT_LOCAL_NONAPPLICABILITY",
    }
    complete = [
        record
        for record in records
        if record["status"] in exact_statuses
    ]
    applicable = [
        record for record in complete if record[applicable_key]
    ]
    failures = [
        {
            "kernel_index": record["kernel_index"],
            "status": record["status"],
        }
        for record in records
        if record["status"] not in exact_statuses
    ]
    if failures:
        status = "INCOMPLETE_KERNEL_FAILURE"
    elif len(applicable) == len(records):
        status = "COMPLETE_ALL_APPLICABLE"
    else:
        status = "COMPLETE_HYPOTHESIS_FAILURE"
    return {
        "status": status,
        "kernel_count": len(records),
        "exact_screen_complete": len(complete),
        "applicable_kernels": len(applicable),
        "failures": failures,
    }


def main() -> None:
    preregistration = load(PREREGISTRATION)
    path_by_label = {
        "artifacts/w1-full-census-v1.json": W1,
        "artifacts/full-census-yield-declaration-v5.json": V5,
        "../dedekind-stark-phase/artifacts/b3-roblot-population-v1.json": (
            QUARTIC
        ),
    }
    for label, expected in preregistration["source_hashes"].items():
        if label == "artifacts/results-paper-core-manifest-v1.json":
            path = ROOT / label
        else:
            path = path_by_label[label]
        if sha256(path) != expected:
            raise RuntimeError(f"frozen source hash changed: {label}")

    w1 = load(W1)
    v5 = load(V5)
    quartic = load(QUARTIC)
    sextic = load(SEXTIC)
    if sextic["status"] != "COMPLETE_EXACT_POPULATION_SCREEN":
        raise RuntimeError("sextic population is not complete")

    v5_by_id = {
        record["case_id"]: record
        for record in v5["classification_records"]
    }
    frontier_by_id = {
        record["case_id"]: record for record in v5["frontier_records"]
    }
    quartic_by_id = defaultdict(list)
    for record in quartic["records"]:
        quartic_by_id[record["case_id"]].append(record)
    sextic_by_id = defaultdict(list)
    for record in sextic["records"]:
        sextic_by_id[record["case_id"]].append(record)

    h_rows = [
        row
        for row in w1["records"]
        if any(order > 2 for order in row["support_orders"])
    ]
    if len(h_rows) != preregistration["h_universe"]["expected_rows"]:
        raise RuntimeError("H universe count changed")

    records = []
    for row in h_rows:
        case_id = row["case_id"]
        higher_orders = sorted(
            order for order in row["support_orders"] if order > 2
        )
        verdict = v5_by_id[case_id]["verdict"]

        if 4 in higher_orders:
            if not quartic_by_id[case_id]:
                raise RuntimeError(f"{case_id}: missing quartic kernels")
            quartic_status = summarize_kernels(
                quartic_by_id[case_id], "eligible"
            )
        else:
            quartic_status = {
                "status": "NOT_APPLICABLE",
                "kernel_count": 0,
                "exact_screen_complete": 0,
                "applicable_kernels": 0,
                "failures": [],
            }

        if 6 in higher_orders:
            if not sextic_by_id[case_id]:
                raise RuntimeError(f"{case_id}: missing sextic kernels")
            sextic_status = summarize_kernels(
                sextic_by_id[case_id], "applicable"
            )
        else:
            sextic_status = {
                "status": "NOT_APPLICABLE",
                "kernel_count": 0,
                "exact_screen_complete": 0,
                "applicable_kernels": 0,
                "failures": [],
            }

        component_statuses = [
            quartic_status["status"]
            for order in higher_orders
            if order == 4
        ] + [
            sextic_status["status"]
            for order in higher_orders
            if order == 6
        ]
        if any(order not in {4, 6} for order in higher_orders):
            roblot_status = "NOT_COVERED_UNSUPPORTED_ORDER"
        elif any(
            status == "INCOMPLETE_KERNEL_FAILURE"
            for status in component_statuses
        ):
            roblot_status = "INCOMPLETE_KERNEL_FAILURE"
        elif all(
            status == "COMPLETE_ALL_APPLICABLE"
            for status in component_statuses
        ):
            roblot_status = "FULL_ROW_WEAK_COVERAGE"
        else:
            roblot_status = "NOT_COVERED_HYPOTHESIS_FAILURE"

        engine_b = verdict == "ENGINE_B_ELIGIBLE"
        engine_c = verdict == "ENGINE_C_ELIGIBLE"
        exact_resolution = (
            "SELECTED_RESULTS_PAPER_THEOREM"
            if case_id in SELECTED_RESULTS
            else "OPEN_CASE_LEVEL_IDENTIFICATION"
        )
        if roblot_status == "INCOMPLETE_KERNEL_FAILURE":
            all_mechanisms_fail = None
        else:
            all_mechanisms_fail = (
                not engine_b
                and not engine_c
                and roblot_status != "FULL_ROW_WEAK_COVERAGE"
            )

        records.append(
            {
                "case_id": case_id,
                "d": row["d"],
                "finite_norm": row["finite_norm"],
                "finite_ideal_hnf": row["finite_ideal_hnf"],
                "support_orders": row["support_orders"],
                "higher_support_orders": higher_orders,
                "shintani_index": row["shintani_index"],
                "exclusive_v5_route": verdict,
                "engine_b_route_eligible": engine_b,
                "engine_c_route_eligible": engine_c,
                "v5_frontier_obstruction": (
                    frontier_by_id[case_id]["obstruction"]
                    if case_id in frontier_by_id
                    else None
                ),
                "roblot_quartic": quartic_status,
                "roblot_sextic": sextic_status,
                "roblot_full_row_status": roblot_status,
                "exact_resolution_status": exact_resolution,
                "results_paper_route": SELECTED_RESULTS.get(case_id),
                "all_known_mechanisms_fail": all_mechanisms_fail,
            }
        )

    records.sort(key=lambda record: stable_id(record["case_id"]))
    route_counts = Counter(
        record["exclusive_v5_route"] for record in records
    )
    expected_routes = preregistration["required_reconciliations"]
    observed_routes = {
        "engine_b_route_eligible": route_counts["ENGINE_B_ELIGIBLE"],
        "engine_c_route_eligible": route_counts["ENGINE_C_ELIGIBLE"],
        "exclusive_frontier": route_counts["FRONTIER"],
    }
    if observed_routes != expected_routes:
        raise RuntimeError("exclusive mechanism reconciliation changed")

    higher_orders = sorted(
        {
            order
            for record in records
            for order in record["higher_support_orders"]
        }
    )
    minimal_unresolved = {}
    minimal_all_fail = {}
    for order in higher_orders:
        unresolved = [
            record
            for record in records
            if order in record["higher_support_orders"]
            and record["exact_resolution_status"]
            == "OPEN_CASE_LEVEL_IDENTIFICATION"
        ]
        all_fail = [
            record
            for record in unresolved
            if record["all_known_mechanisms_fail"] is True
        ]
        minimal_unresolved[str(order)] = unresolved[0]["case_id"]
        minimal_all_fail[str(order)] = (
            all_fail[0]["case_id"] if all_fail else None
        )

    wall = next(
        record for record in records if record["case_id"] == "RQ-000692"
    )
    if wall["d"] != 21 or 6 not in wall["higher_support_orders"]:
        raise RuntimeError("Q(sqrt(21)) wall identity changed")

    canonical_records = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode()
    payload = {
        "schema": "effective-stark-census-h-taxonomy-v1",
        "claim_tag": "OBSERVED",
        "claim_boundary": {
            "engine_and_roblot_fields": "exact hypothesis eligibility",
            "eligibility_is_not_case_level_packet_proof": True,
            "selected_results_rows": (
                "PROVED in the cited results-paper certificates"
            ),
        },
        "source_hashes": {
            "artifacts/w1-full-census-v1.json": sha256(W1),
            "artifacts/full-census-yield-declaration-v5.json": sha256(V5),
            (
                "../dedekind-stark-phase/artifacts/"
                "b3-roblot-population-v1.json"
            ): sha256(QUARTIC),
            "artifacts/roblot-sextic-population-v1.json": sha256(SEXTIC),
            "data/census-paper-preregistration-amendment-v8.json": (
                sha256(PREREGISTRATION)
            ),
            "paper/effective-stark-results.tex": sha256(RESULTS_PAPER),
        },
        "counts": {
            "H_rows": len(records),
            **observed_routes,
            "selected_results_paper_rows": sum(
                record["exact_resolution_status"]
                == "SELECTED_RESULTS_PAPER_THEOREM"
                for record in records
            ),
            "roblot_full_row_status": dict(
                sorted(
                    Counter(
                        record["roblot_full_row_status"]
                        for record in records
                    ).items()
                )
            ),
            "support_profiles": {
                ",".join(map(str, profile)): count
                for profile, count in sorted(
                    Counter(
                        tuple(record["support_orders"])
                        for record in records
                    ).items()
                )
            },
            "all_known_mechanisms_fail": sum(
                record["all_known_mechanisms_fail"] is True
                for record in records
            ),
            "mechanism_status_incomplete": sum(
                record["all_known_mechanisms_fail"] is None
                for record in records
            ),
        },
        "frontier_tables": {
            "minimum_ordering": "stable numeric RQ id",
            "minimal_unresolved_by_support_order": minimal_unresolved,
            "minimal_all_mechanisms_fail_by_support_order": (
                minimal_all_fail
            ),
            "q_sqrt_21_order_six_wall": wall,
        },
        "records_sha256": hashlib.sha256(canonical_records).hexdigest(),
        "records": records,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
