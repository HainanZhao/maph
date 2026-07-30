#!/usr/bin/env python3
"""Audit index-one ray fields that are abelian over Q."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
W1 = ROOT / "artifacts/w1-full-census-v1.json"
FRONTIER = ROOT / "artifacts/frontier-index-inventory-v1.json"
OUTPUT = ROOT / "artifacts/engine-d-index-one-candidates-v1.json"
EXAMPLE_IDS = ["RQ-000018", "RQ-000032", "RQ-000274"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    rows = w1["records"]
    index_one = [row for row in rows if row["shintani_index"] == 1]
    abelian = [row for row in index_one if row["commutator_size"] == 1]
    open_rows = [row for row in abelian if row["verdict"] == "FRONTIER"]
    substantive = [row for row in open_rows if row["support_count"] > 0]
    examples = [
        next(row for row in substantive if row["case_id"] == case_id)
        for case_id in EXAMPLE_IDS
    ]
    payload = {
        "schema": "effective-stark-engine-d-index-one-candidates-v1",
        "claim_tag": "VERIFIED_EXACT_CANDIDATE_INVENTORY",
        "criterion": (
            "shintani_index=1 and normal-closure commutator_size=1; "
            "the structural screen therefore certifies that the ray "
            "field is abelian over Q"
        ),
        "counts": {
            "all_index_one_occurrences": len(index_one),
            "all_index_one_abelian_over_q_occurrences": len(abelian),
            "already_engine_a_occurrences": sum(
                row["engine"] == "A" for row in abelian
            ),
            "frontier_abelian_over_q_occurrences": len(open_rows),
            "frontier_abelian_over_q_fields": len(
                {row["d"] for row in open_rows}
            ),
            "substantive_frontier_engine_d_candidates": len(substantive),
            "substantive_frontier_engine_d_fields": len(
                {row["d"] for row in substantive}
            ),
        },
        "frontier_obstruction_distribution": dict(
            sorted(Counter(row["obstruction"] for row in open_rows).items())
        ),
        "substantive_support_distribution": [
            {"orders": list(pattern), "count": count}
            for pattern, count in sorted(
                Counter(
                    tuple(row["support_orders"]) for row in substantive
                ).items(),
                key=lambda item: (-item[1], item[0]),
            )
        ],
        "examples": [
            {
                key: row[key]
                for key in (
                    "case_id",
                    "d",
                    "field_discriminant",
                    "finite_ideal_hnf",
                    "finite_norm",
                    "one_cyc",
                    "both_cyc",
                    "support_orders",
                    "source_case_sha256",
                )
            }
            for row in examples
        ],
        "engine_d_question": {
            "answer": "YES",
            "proposed_route": (
                "Decompose the absolute abelian ray character into "
                "Dirichlet characters over Q and apply exact cyclotomic/"
                "ACNF formulas with an explicit regulator/index audit."
            ),
            "status": "CONJECTURAL_ENGINE_DESIGN_NOT_YET_A_THEOREM",
            "next_gate": (
                "Prove one uniform absolute-abelian reduction theorem "
                "and replay the three frozen examples before bulk use."
            ),
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (W1, FRONTIER, SELF)
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"INDEX_ONE_ABELIAN_OVER_Q={len(abelian)}")
    print(f"OPEN_SUBSTANTIVE_ENGINE_D_CANDIDATES={len(substantive)}")
    print("ENGINE_D_QUESTION_ANSWER=YES")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
