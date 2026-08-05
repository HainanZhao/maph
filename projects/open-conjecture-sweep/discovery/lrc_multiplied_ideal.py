#!/usr/bin/env python3
"""Cycle 41: first exact multiplied ownership-ideal completion test."""
from __future__ import annotations

from collections import defaultdict
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal"
WALL_CAP = 3600


def enumerate_coordinate(coordinate: int) -> dict[str, object]:
    resource.setrlimit(resource.RLIMIT_AS, (1_600_000_000, 1_600_000_000))
    row = c40.coordinate_classes(coordinate)
    return {
        "coordinate": coordinate,
        "rank_two_tuples": row["rank_two_tuples"],
        "rank_three_tuples": row["rank_three_tuples"],
        "rank_two_pairs": row["rank_two_pairs"],
        "induced_pair_deletions": row["induced_pair_deletions"],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << coordinate for coordinate, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = type_id
    c40._TYPE_MASKS = masks

    prior = json.loads((ROOT / "discovery/out/cycle40-signed-moments/result.json").read_text(encoding="utf-8"))
    selected = []
    for type_index, rows in enumerate(prior["singleton_marginals_by_complete_type"]):
        if len(rows) != 1 or rows[0][1:] != [1, 1]:
            raise AssertionError("Cycle 40 singleton solution is not integral")
        owner = int(rows[0][0])
        if not masks[type_index] & (1 << owner):
            raise AssertionError("selected owner outside support")
        selected.append(owner)

    with multiprocessing.Pool(3) as pool:
        coordinate_rows = pool.map(enumerate_coordinate, range(13), chunksize=1)
    original_pair_deleted: dict[tuple[int, int], int] = defaultdict(int)
    induced: dict[tuple[int, int], int] = defaultdict(int)
    for row in coordinate_rows:
        coordinate = int(row["coordinate"])
        for pair in row["rank_two_pairs"]:
            original_pair_deleted[tuple(pair)] |= 1 << coordinate
        for pair in row["induced_pair_deletions"]:
            induced[tuple(pair)] |= 1 << coordinate

    def selected_conflicts(deletions: dict[tuple[int, int], int]):
        rows = []
        counts = [0] * 13
        for (left, right), deleted in sorted(deletions.items()):
            if selected[left] == selected[right] and deleted & (1 << selected[left]):
                counts[selected[left]] += 1
                if len(rows) < 100:
                    rows.append({"left_type": left, "right_type": right, "owner": selected[left], "deleted_diagonal": deleted})
        return rows, counts

    violations, violation_owner_counts = selected_conflicts(original_pair_deleted)
    induced_violations, induced_violation_owner_counts = selected_conflicts(induced)

    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "stage": "INTEGRAL_WITNESS_PAIR_SAFETY",
        "complete_types": len(complete_types),
        "rank_two_type_tuples": sum(int(row["rank_two_tuples"]) for row in coordinate_rows),
        "rank_three_type_tuples": sum(int(row["rank_three_tuples"]) for row in coordinate_rows),
        "original_rank_two_pair_classes": len(original_pair_deleted),
        "cycle40_induced_pair_deletion_classes": len(induced),
        "selected_owner_rank_two_violations": sum(violation_owner_counts),
        "violation_owner_counts": violation_owner_counts,
        "first_violations": violations,
        "selected_owner_cycle40_induced_deletion_violations": sum(induced_violation_owner_counts),
        "induced_violation_owner_counts": induced_violation_owner_counts,
        "first_induced_violations": induced_violations,
        "integral_delta_witness_extends": not any(violation_owner_counts),
        "next_stage": "CONSTRAINED_TRIPLE_COMPLETION" if not any(violation_owner_counts) else "GENERAL_SIGNED_PAIR_AND_TRIPLE_SYSTEM",
        "claim_boundary": "A violation refutes only the delta-pair extension of Cycle 40's selected integral singleton marginals; signed pair transports may still satisfy every multiplied relation.",
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({key: result[key] for key in ("status", "selected_owner_rank_two_violations", "integral_delta_witness_extends", "next_stage", "wall_seconds")}, sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
