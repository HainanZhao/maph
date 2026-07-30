#!/usr/bin/env python3
"""Issue census v5 using only GENUINE predicates."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
INDEX = ARTIFACTS / "genuine-index-ledger-8200-v3.json"
B_DEDUP = ARTIFACTS / "genuine-b-deduplication-v5.json"
C_OLD = ARTIFACTS / "engine-c-geometry-analysis-v1.json"
C_INVENTORY = ARTIFACTS / "engine-c-e-inventory-v1.json"
C_NEW = ARTIFACTS / "engine-c-catchup-252-v1.json"
ID_QUEUES = ARTIFACTS / "identification-queues-v2.json"
B_SUMMARY = ARTIFACTS / "genuine-b-recovery-summary-v1.json"
C_SUMMARY = ARTIFACTS / "engine-c-catchup-summary-v1.json"
R13 = ARTIFACTS / "predicate-provenance-ledger-r13-v1.json"
V4 = ARTIFACTS / "full-census-yield-declaration-v4.json"
OUTPUT = ARTIFACTS / "full-census-yield-declaration-v5.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ratio(numerator: int, denominator: int) -> dict:
    reduced = Fraction(numerator, denominator)
    return {
        "numerator": numerator,
        "denominator": denominator,
        "reduced": f"{reduced.numerator}/{reduced.denominator}",
        "decimal": float(reduced),
    }


def transcript_value(path: Path, suffix: str) -> str:
    hits = [
        line.split("=", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if "=" in line and line.split("=", 1)[0].endswith(suffix)
    ]
    if len(hits) != 1:
        raise RuntimeError(f"{path}: expected one {suffix}")
    return hits[0]


def main() -> None:
    rows = json.loads(W1.read_text(encoding="utf-8"))["records"]
    by_id = {row["case_id"]: row for row in rows}
    index_artifact = json.loads(INDEX.read_text(encoding="utf-8"))
    if (
        index_artifact["status"] != "COMPLETE"
        or index_artifact["completed_representative_count"] != 8200
    ):
        raise RuntimeError("genuine index ledger is incomplete")
    indices = {
        row["case_id"]: row for row in index_artifact["records"]
    }
    if any(row["predicate_provenance"] != "GENUINE" for row in indices.values()):
        raise RuntimeError("non-genuine index record")

    trivial = {
        row["case_id"]
        for row in rows
        if row["engine"] == "A" and row["support_count"] == 0
    }
    engine_a = {
        row["case_id"]
        for row in rows
        if row["engine"] == "A" and row["support_count"] > 0
    }
    b_data = json.loads(B_DEDUP.read_text(encoding="utf-8"))
    engine_b = {row["case_id"] for row in b_data["records"]}
    c_old = json.loads(C_OLD.read_text(encoding="utf-8"))
    c_new = json.loads(C_NEW.read_text(encoding="utf-8"))
    engine_c = set(c_old["complete_c_case_ids"]) | {
        row["case_id"]
        for row in c_new["records"]
        if row["classification"] == "C_ELIGIBLE"
    }
    populations = [trivial, engine_a, engine_b, engine_c]
    if any(
        populations[i] & populations[j]
        for i in range(len(populations))
        for j in range(i + 1, len(populations))
    ):
        raise RuntimeError("engine populations overlap")
    frontier = set(by_id) - set().union(*populations)

    id_queue = json.loads(ID_QUEUES.read_text(encoding="utf-8"))[
        "engine_b"
    ]
    exponent_cap = set(id_queue["degree_above_40_pending_case_ids"])
    exponent_cap |= {
        row["case_id"] for row in rows
        if row["obstruction"] == "EXPONENT_CAP"
    }
    # Genuine reconstruction exposed eight additional index-two cases whose
    # actual normal closure exceeds the frozen degree-40 identification cap.
    exponent_cap |= {
        case_id
        for case_id in frontier
        if indices[case_id]["derived_subgroup_order"] == 2
        and 2 * indices[case_id]["normal_closure_relative_degree"] > 40
    }
    tool_blocked = set(c_old["tool_blocked_case_ids"]) | {
        row["case_id"]
        for row in c_new["records"]
        if row["classification"] == "HAS_TOOL_BLOCK"
    }

    frontier_records = []
    taxonomy = Counter()
    for case_id in sorted(frontier):
        row = by_id[case_id]
        index = indices[case_id]
        if case_id in exponent_cap:
            obstruction = "EXPONENT_CAP"
        elif case_id in tool_blocked:
            obstruction = "TOOL_BLOCKED"
        elif (
            not row["b03_positive_not_minus_one"]
            or not row["b06_negative_norm_not_one"]
        ):
            obstruction = "UNIT_CONGRUENCE_FAIL"
        elif index["derived_subgroup_order"] != 2:
            obstruction = "INDEX_GT_2"
        elif not row["exactly_one_real_place_splitting"]:
            obstruction = "REAL_PLACE_SPLITTING_FAIL"
        else:
            raise RuntimeError(f"{case_id}: unclassified genuine frontier")
        taxonomy[obstruction] += 1
        frontier_records.append(
            {
                "case_id": case_id,
                "obstruction": obstruction,
                "predicate_provenance": "GENUINE",
                "derived_subgroup_order":
                    index["derived_subgroup_order"],
                "normal_closure_relative_degree":
                    index["normal_closure_relative_degree"],
                "unit_predicates": [
                    row["b03_positive_not_minus_one"],
                    row["b06_negative_norm_not_one"],
                ],
                "real_place_split_predicate":
                    row["exactly_one_real_place_splitting"],
            }
        )

    expected_histogram = {
        "PROVED_TRIVIAL": 3899,
        "ENGINE_A_NONTRIVIAL_ELIGIBLE": 1560,
        "ENGINE_B_ELIGIBLE": 232,
        "ENGINE_C_ELIGIBLE": 881,
        "FRONTIER": 1628,
    }
    actual_histogram = {
        "PROVED_TRIVIAL": len(trivial),
        "ENGINE_A_NONTRIVIAL_ELIGIBLE": len(engine_a),
        "ENGINE_B_ELIGIBLE": len(engine_b),
        "ENGINE_C_ELIGIBLE": len(engine_c),
        "FRONTIER": len(frontier),
    }
    if actual_histogram != expected_histogram:
        raise RuntimeError(f"v5 histogram changed: {actual_histogram}")
    expected_taxonomy = {
        "EXPONENT_CAP": 502,
        "INDEX_GT_2": 1088,
        "REAL_PLACE_SPLITTING_FAIL": 2,
        "TOOL_BLOCKED": 5,
        "UNIT_CONGRUENCE_FAIL": 31,
    }
    if dict(sorted(taxonomy.items())) != expected_taxonomy:
        raise RuntimeError(f"v5 taxonomy changed: {taxonomy}")

    # C packet-field deduplication: the old inventory already contains one
    # canonical polynomial per 393 field. Add every packet in newly complete
    # C rows, using the same polredbest output convention.
    old_c_fields = {
        row["absolute_polynomial"]
        for row in json.loads(
            C_INVENTORY.read_text(encoding="utf-8")
        )["field_records"]
    }
    new_c_packet_polynomials = []
    for row in c_new["records"]:
        if row["classification"] != "C_ELIGIBLE":
            continue
        for packet in row["packets"]:
            new_c_packet_polynomials.append(
                transcript_value(
                    ROOT / packet["transcript"],
                    "_ABSOLUTE_POLYNOMIAL",
                )
            )
    c_fields = old_c_fields | set(new_c_packet_polynomials)
    if (
        len(old_c_fields) != 393
        or len(new_c_packet_polynomials) != 198
        or len(c_fields) != 447
    ):
        raise RuntimeError("C packet-field deduplication changed")

    classification_records = []
    for case_id in sorted(by_id):
        if case_id in trivial:
            verdict = "PROVED_TRIVIAL"
        elif case_id in engine_a:
            verdict = "ENGINE_A_NONTRIVIAL_ELIGIBLE"
        elif case_id in engine_b:
            verdict = "ENGINE_B_ELIGIBLE"
        elif case_id in engine_c:
            verdict = "ENGINE_C_ELIGIBLE"
        else:
            verdict = "FRONTIER"
        classification_records.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "predicate_provenance": "GENUINE",
                "derived_subgroup_order":
                    indices[case_id]["derived_subgroup_order"],
            }
        )

    by_norm = defaultdict(lambda: [0, 0])
    for row in rows:
        norm = int(row["finite_norm"])
        by_norm[norm][0] += 1
        by_norm[norm][1] += row["case_id"] in frontier
    quartiles = []
    for left, right in ((1, 25), (26, 50), (51, 75), (76, 100)):
        total = sum(by_norm[n][0] for n in range(left, right + 1))
        count = sum(by_norm[n][1] for n in range(left, right + 1))
        quartiles.append(
            {
                "norm_interval": [left, right],
                "total": total,
                "frontier": count,
                "frontier_share": ratio(count, total),
            }
        )
    monotone = all(
        Fraction(
            quartiles[i]["frontier"], quartiles[i]["total"]
        )
        < Fraction(
            quartiles[i + 1]["frontier"],
            quartiles[i + 1]["total"],
        )
        for i in range(3)
    )
    if not monotone:
        raise RuntimeError("v5 norm trend is not strictly monotone")

    odd = [
        row for row in index_artifact["records"]
        if row["derived_subgroup_order"] > 2
        and row["derived_subgroup_order"] % 2 == 1
    ]
    if len(odd) != 446 or any(
        by_id[row["case_id"]]["support_count"] > 0 for row in odd
    ):
        raise RuntimeError("odd-index landscape changed")

    v4 = json.loads(V4.read_text(encoding="utf-8"))
    payload = {
        "schema": "effective-stark-full-census-yield-v5",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_GENUINE_CENSUS",
        "predicate_provenance": "GENUINE",
        "representative_count": 8200,
        "histogram": actual_histogram,
        "distinct_objects": {
            "PROVED_TRIVIAL": 1,
            "ENGINE_A_ABSOLUTE_FIELDS": 912,
            "ENGINE_B_NORMAL_CLOSURES": 88,
            "ENGINE_C_PACKET_FIELDS": 447,
            "ENGINE_C_PACKET_OCCURRENCES": 1163
                + len(new_c_packet_polynomials),
        },
        "frontier_taxonomy": expected_taxonomy,
        "frontier_records": frontier_records,
        "classification_records": classification_records,
        "yield_checkpoint": {
            "pre_registered_threshold_beyond_anchors": 15,
            "eligible_including_trivial": 6572,
            "substantive_eligible": 2673,
            "eligible_beyond_seven_anchors": 6565,
            "verdict": "PASS_CENSUS_PAPER_FRAMING",
            "boundary": "route eligibility, not W3 packet promotion",
        },
        "genuine_index_histogram": index_artifact["index_histogram"],
        "odd_index_landscape": {
            "odd_index_above_two_count": 446,
            "nonempty_support_count": 0,
            "finding": (
                "every genuine odd index occurs on an empty-support "
                "PROVED_TRIVIAL row"
            ),
        },
        "frontier_norm_quartiles": quartiles,
        "frontier_share_strictly_increases_by_norm_quartile":
            monotone,
        "historical_proxy_trend": {
            "shares_percent": [9.93, 21.60, 27.26, 31.65],
            "status": "SUPERSEDED_NOT_EVIDENCE",
        },
        "recovery_changes": {
            "B": "195 -> 232 eligible occurrences",
            "C": "728 -> 881 eligible rows",
            "FRONTIER": "1818 -> 1628 rows",
            "trend": (
                "strict monotonicity survives, with lower genuine "
                "shares"
            ),
            "case_level_theorem_retractions": 0,
        },
        "rq007500": {
            "outcome": "RE_PASSES",
            "effective_tag": "VERIFIED_W2_GENUINE_RECOVERY",
        },
        "w4_gate": {
            "open": False,
            "closed_recovery_requirements": [
                "241-row genuine B recovery",
                "252-row complete-C catch-up",
                "8200-row genuine index ledger",
            ],
            "remaining_requirement":
                "occurrence transport for the B closure corpus",
        },
        "revision_history": v4["revision_history"] + [
            {
                "revision": "v5",
                "artifact":
                    "artifacts/full-census-yield-declaration-v5.json",
                "role": (
                    "all classification populations rebuilt on "
                    "GENUINE provenance"
                ),
            }
        ],
        "paper_fork": {
            "results_paper_independent": True,
            "census_paper_may_now_use_v5_counts": True,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                W1,
                INDEX,
                B_DEDUP,
                C_OLD,
                C_INVENTORY,
                C_NEW,
                ID_QUEUES,
                B_SUMMARY,
                C_SUMMARY,
                R13,
                V4,
                Path(__file__),
            )
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
