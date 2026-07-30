#!/usr/bin/env python3
"""Freeze recovery sequencing, estimate, and change-boundary claims."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
OUTPUT = ARTIFACTS / "r13-recovery-plan-and-claim-boundary-v1.json"
SOURCES = [
    ARTIFACTS / "proxy-recovery-queue-v1.json",
    ARTIFACTS / "predicate-provenance-ledger-r13-v1.json",
    ARTIFACTS / "rq007500-genuine-recovery-v1.json",
    ARTIFACTS / "genuine-b-battery-anchor-v2.json",
    ARTIFACTS / "r13-genuine-anchor-reproduction-v1.json",
    ARTIFACTS / "results-paper-scope-seal-v1.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    payload = {
        "schema": "effective-stark-r13-recovery-plan-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "FROZEN_BEFORE_POPULATION_RECLASSIFICATION",
        "strict_order": [
            {
                "track": "a",
                "work": "genuine Engine-B reconstruction and reclassification",
                "population": 241,
                "estimated_research_cycles": [5, 8],
                "gates": ["B counts", "B-side W3", "part of FRONTIER ledger"],
            },
            {
                "track": "b",
                "work": "complete-C geometry catch-up",
                "population": 252,
                "estimated_research_cycles": [2, 3],
                "gates": ["exact C completeness count"],
            },
            {
                "track": "c",
                "work": "genuine index reconstruction",
                "population": 8200,
                "estimated_research_cycles": [6, 10],
                "execution": "background after genuine controls",
                "gates": ["W4", "index distribution", "norm trend"],
            },
        ],
        "estimate": {
            "total_case_cycles": [13, 21],
            "estimated_wall_clock_research_cycles_with_background_overlap": [
                10,
                16,
            ],
            "qualification": (
                "RQ-007500 completed in seconds, but the first queued "
                "degree-40 control exposed a multi-minute tail; the "
                "one-node-hour cap remains binding and capped cases "
                "become named FRONTIER results"
            ),
            "anti_plumbing_tripwire": (
                "no industrial scheduler or shared infrastructure will "
                "be built; one process per case, resumable case files"
            ),
        },
        "claims_that_can_change": [
            "Engine-B eligible count and closure count",
            "FRONTIER total and obstruction taxonomy",
            "Engine-C exact completeness count (existing positives cannot fall)",
            "FRONTIER-share-versus-conductor-norm trend",
            "odd-index population and correlates",
        ],
        "claims_that_cannot_change": [
            "all seven anchors",
            "all 25 promoted case-level theorem identities",
            "the first order-six pair",
            "the first order-ten packet",
            "RQ-000458 dual-route theorem",
            "RQ-000129 and RQ-002057",
            "the Q(sqrt(35)) generic Engine-C closure",
            "the uniform Engine-A theorem",
            "the complete-C geometric predicate on already screened packets",
            "the absolute-abelian one-place no-go lemma",
            "every theorem statement in the results paper",
        ],
        "trend_status": (
            "PROVISIONAL_WITHDRAWN: 9.93, 21.60, 27.26, 31.65 percent "
            "are historical proxy-derived values and may not appear "
            "unflagged before census v5"
        ),
        "census_v5_gate": {
            "open": False,
            "requirements": [
                "track a complete",
                "track b complete",
                "track c complete",
                "all effective predicates GENUINE",
            ],
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path) for path in SOURCES
        }
        | {"scripts/freeze_r13_recovery_plan.py": sha(Path(__file__))},
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
