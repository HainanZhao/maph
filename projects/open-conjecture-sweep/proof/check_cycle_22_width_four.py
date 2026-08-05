#!/usr/bin/env python3
"""Independent direct-CNF audit of Cycle 22 width-four output."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as stage_a

OUT = ROOT / "discovery/out/cycle22-width-four"


def read(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_partition(text: str) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def audit() -> dict[str, object]:
    stage_a_rows = read("stage-a.tsv")
    assert [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in stage_a_rows] == stage_a.targets()
    assert len(stage_a_rows) == 61
    assert all(row["status"] == "UNRESOLVED" and int(row["trials"]) == 150 for row in stage_a_rows)

    trials = read("stage-b-trials.tsv")
    assert len(trials) == 602
    counts = {rank: sum(int(row["partition_rank"]) == rank for row in trials) for rank in range(10)}
    assert counts == {0: 61, 1: 61, 2: 60, 3: 60, 4: 60, 5: 60, 6: 60, 7: 60, 8: 60, 9: 60}
    certified_trials = [row for row in trials if row["status"] == "CERTIFIED_DEFICIT"]
    assert len(certified_trials) == 1

    final = read("stage-b-results.tsv")
    assert [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in final] == stage_a.targets()
    assert len(final) == 61
    certified = [row for row in final if row["status"] == "CERTIFIED_DEFICIT"]
    assert len(certified) == 1 and sum(row["status"] == "UNRESOLVED" for row in final) == 60
    row = certified[0]
    assert (int(row["base_index"]), int(row["leaf_ordinal"])) == (4, 952)
    base = cycle21.read_bases()[4]
    allowed = direct.allowed_digits(base, 952)
    partition = parse_partition(row["partition"])
    rank = int(row["partition_rank"])
    assert rank == 1 and stage_a.partitions(allowed)[rank] == partition
    coverage = stage_a.raw_coverage(direct.CNFS[4])
    clauses = list(map(int, row["source_clauses"].split(",")))
    values = list(map(int, row["weights"].split(",")))
    assert len(clauses) == len(values) == int(row["support"]) <= 256
    weights = np.zeros(cycle21.P * cycle21.C, dtype=np.int64)
    for clause, value in zip(clauses, values, strict=True):
        point = clause - stage_a.FIRST_TIME
        assert 0 <= point < len(weights) and value > 0 and weights[point] == 0
        weights[point] = value
    upper, maxima = direct.exact_capacity(partition, allowed, coverage, weights)
    total = int(weights.sum())
    assert total == int(row["W"]) == 65_528
    assert upper == int(row["U"]) == 65_440
    assert maxima == list(map(int, row["block_maxima"].split(",")))
    assert total - upper == 88
    exhaustive = read("exhaustive-transfer.tsv")
    assert len(exhaustive) == 60
    assert all(row["status"] == "CAP" for row in exhaustive)
    partial = [
        (int(row["base_index"]), int(row["leaf_ordinal"]), int(row["partitions_tested"]), int(row["blocks_evaluated"]), int(row["maximum_antichain_states"]))
        for row in exhaustive if int(row["partitions_tested"]) > 0
    ]
    assert partial == [(4, 78, 339, 407, 16464), (4, 79, 472, 544, 16464), (4, 80, 529, 602, 30408)]
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "stage_a_trials": 9_150,
        "stage_b_trials": 602,
        "certified_leaves": [{"base_index": 4, "leaf_ordinal": 952, "W": total, "U": upper, "margin": 88}],
        "remaining_leaves": 60,
        "exhaustive_transfer_caps": 60,
        "exhaustive_transfer_partially_executed": 3,
        "exhaustive_transfer_unstarted": 57,
        "claim_boundary": "One named leaf only; neither base is complete.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
