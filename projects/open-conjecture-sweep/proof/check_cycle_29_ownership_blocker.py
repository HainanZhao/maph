#!/usr/bin/env python3
"""Lightweight exact audit for the Cycle 29 ownership/blocker lift."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle29-ownership-blocker"


def load(name: str) -> dict[str, object]:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def audit() -> dict[str, object]:
    primary = load("result.json")
    independent = load("independent-replay.json")
    assert primary["status"] == independent["status"] == "PASS"

    synthetic = primary["synthetic"]
    expected_synthetic = {
        "interfaces": 327680,
        "feasible_interfaces": 292592,
        "map_checks": 1487872,
        "blockers_checked": 1114112,
    }
    assert {key: synthetic[key] for key in expected_synthetic} == expected_synthetic
    assert independent["synthetic"] == expected_synthetic
    assert synthetic["corpora"] == [
        {"coordinates": 2, "digits": 2, "interfaces": 65536, "times": 4},
        {"coordinates": 3, "digits": 2, "interfaces": 262144, "times": 3},
    ]

    h11 = primary["h11"]
    expected_h11 = {
        "lifted_assignments": 64000,
        "raw_full_cover_assignments": 720,
        "raw_ownership_map_checks": 720,
        "gcd_admissible_assignments": 32000,
        "parity_signature_counts": {
            "coordinate_0_even": 8000,
            "coordinate_1_even": 8000,
            "coordinate_2_even": 8000,
            "none_even": 8000,
        },
        "retained_improper_bases": 0,
    }
    assert {key: h11[key] for key in expected_h11} == expected_h11
    assert independent["h11"] == expected_h11

    p199 = primary["p199"]
    assert (p199["base_index"], p199["leaf_ordinal"], p199["times"]) == (4, 78, 2786)
    expected_p199 = {
        "symbolic_pattern_count": 12264,
        "concrete_blocker_count": 190867444,
        "symbolic_rank_counts": {"1": 13, "2": 9311, "3": 2940},
        "concrete_rank_counts": {"1": 4844, "2": 27482360, "3": 163380240},
        "max_rank": 3,
        "same_color_distinct_mask_witness": {
            "coordinate": 0,
            "left_digit": 0,
            "right_digit": 4,
            "color": [0, 0],
            "distinguishing_time": 1,
            "left_covers": True,
            "right_covers": False,
        },
    }
    assert {key: p199[key] for key in expected_p199} == expected_p199
    assert independent["p199"] == expected_p199
    coordinates = p199["coordinates"]
    assert [row["coordinate"] for row in coordinates] == list(range(13))
    assert sum(len(row["patterns"]) for row in coordinates) == 12264
    assert sum(row["concrete_blocker_count"] for row in coordinates) == 190867444
    ranks = Counter()
    concrete_ranks = Counter()
    for row in coordinates:
        signatures = {item["signature"]: item["count"] for item in row["signature_classes"]}
        for pattern in row["patterns"]:
            rank = len(pattern["signatures"])
            multiplicity = 1
            for signature in pattern["signatures"]:
                multiplicity *= signatures[signature]
            assert pattern["rank"] == rank
            assert pattern["concrete_multiplicity"] == multiplicity
            ranks[rank] += 1
            concrete_ranks[rank] += multiplicity
    assert {str(key): value for key, value in sorted(ranks.items())} == expected_p199["symbolic_rank_counts"]
    assert {str(key): value for key, value in sorted(concrete_ranks.items())} == expected_p199["concrete_rank_counts"]

    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "finite exact controls and base-4/leaf-78 census only",
        "synthetic_interfaces": 327680,
        "h11_assignments": 64000,
        "p199_symbolic_patterns": 12264,
        "p199_concrete_blockers": 190867444,
        "p199_max_rank": 3,
        "independent_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
