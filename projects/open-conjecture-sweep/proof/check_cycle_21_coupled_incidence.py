#!/usr/bin/env python3
"""Independent direct-CNF audit of Cycle 21 certificates."""

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

RESULTS = ROOT / "discovery/out/cycle21-coupled-incidence/results.tsv"
INTERFACE = ROOT / "discovery/out/cycle21-coupled-incidence/interface.tsv"
TRANSFER = ROOT / "discovery/out/cycle21-coupled-incidence/transfer.tsv"


def parse_partition(text: str) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def audit() -> dict[str, object]:
    controls = cycle21.interface_controls()
    with INTERFACE.open(newline="", encoding="utf-8") as handle:
        interface_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(controls) == len(interface_rows) == 295
    assert sum(row[4] for row in controls) == 1_873_178
    for expected, observed in zip(controls, interface_rows, strict=True):
        assert tuple(observed[key] for key in ("family", "index", "p", "c", "predicate_comparisons", "cnf_sha256")) == tuple(map(str, expected))

    with RESULTS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows] == cycle21.targets()
    certified = [row for row in rows if row["status"] == "CERTIFIED_DEFICIT"]
    assert len(rows) == 76 and len(certified) == 15
    bases = cycle21.read_bases()
    margins = []
    by_base = {4: 0, 3: 0}
    for row in certified:
        base_index = int(row["base_index"])
        ordinal = int(row["leaf_ordinal"])
        partition = parse_partition(row["partition"])
        family = cycle21.partitions(ordinal)
        rank = int(row["partition_rank"])
        assert family[rank] == partition
        source, coverage = direct.time_signatures(direct.CNFS[base_index])
        allowed = direct.allowed_digits(bases[base_index], ordinal)
        assert allowed == cycle21.allowed_digits(bases[base_index], ordinal)
        named = list(map(int, row["source_clauses"].split(",")))
        weights0 = list(map(int, row["weights"].split(",")))
        assert len(named) == len(weights0) == int(row["support"]) <= 256
        source_to_index = {clause: index for index, clause in enumerate(source)}
        assert len(source_to_index) == len(source)
        weights = np.zeros(len(source), dtype=np.int64)
        for clause, weight in zip(named, weights0, strict=True):
            assert clause in source_to_index and weight > 0
            weights[source_to_index[clause]] = weight
        upper, maxima = direct.exact_capacity(partition, allowed, coverage, weights)
        total = int(weights.sum())
        assert total == int(row["W"])
        assert upper == int(row["U"])
        assert maxima == list(map(int, row["block_maxima"].split(",")))
        assert upper < total
        margins.append(total - upper)
        by_base[base_index] += 1
    assert by_base == {4: 9, 3: 6}
    assert sum(row["status"] == "UNRESOLVED" for row in rows) == 61
    with TRANSFER.open(newline="", encoding="utf-8") as handle:
        transfer_rows = list(csv.DictReader(handle, delimiter="\t"))
    unresolved_targets = [
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in rows if row["status"] == "UNRESOLVED"
    ]
    assert [
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in transfer_rows
    ] == unresolved_targets
    assert len(transfer_rows) == 61
    assert all(row["status"] == "UNRESOLVED" and int(row["trials"]) == 195 for row in transfer_rows)
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "interface_instances": 295,
        "interface_predicate_comparisons": 1_873_178,
        "certified_leaves": 15,
        "base4": 9,
        "base3": 6,
        "minimum_exact_margin": min(margins),
        "maximum_exact_margin": max(margins),
        "transfer_trials": 11_895,
        "transfer_certificates": 0,
        "claim_boundary": "Fifteen named leaves only; neither base is complete.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
