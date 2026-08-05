#!/usr/bin/env python3
"""Independent direct-CNF audit of Cycle 26's width-five transfer sweep."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4
import lrc_width_five_transfer as transfer

OUT = ROOT / "discovery/out/cycle26-width-five-transfer"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def independent_block_maximum(block, allowed, coverage, weights) -> int:
    """Enumerate all direct options in vectorized batches, independently of search."""
    active = np.flatnonzero(weights)
    states = np.zeros((1, len(active)), dtype=bool)
    for coordinate in block:
        choices = coverage[active][:, coordinate, list(allowed[coordinate])].T
        states = np.logical_or(states[:, None, :], choices[None, :, :]).reshape(-1, len(active))
    expected = 1
    for coordinate in block:
        expected *= len(allowed[coordinate])
    assert len(states) == expected <= 14**5
    return int((states @ weights[active]).max())


def audit() -> dict[str, object]:
    control = transfer.source_control()
    assert control["status"] == "PASS"
    result, prior = rows(OUT / "results.tsv"), transfer.target_rows()
    assert len(result) == len(prior) == 60
    assert [(row["base_index"], row["leaf_ordinal"]) for row in result] == [(row["base_index"], row["leaf_ordinal"]) for row in prior]
    assert all(row["status"] == "UNRESOLVED" for row in result)
    weights = transfer.source_weights()
    for row in result:
        base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        allowed = direct.allowed_digits(coupled.read_bases()[base_index], ordinal)
        blocks = transfer.partition(allowed)
        coverage = width4.raw_coverage(direct.CNFS[base_index])
        maxima = [independent_block_maximum(block, allowed, coverage, weights) for block in blocks]
        upper = sum(maxima)
        counts = [transfer.option_count(block, allowed) for block in blocks]
        assert row["partition"] == transfer.partition_text(blocks)
        assert int(row["W"]) == int(weights.sum()) == 65528
        assert int(row["U"]) == upper
        assert row["block_maxima"] == ",".join(map(str, maxima))
        assert row["block_option_counts"] == ",".join(map(str, counts))
    gaps = [int(row["U"]) - int(row["W"]) for row in result]
    return {"status": "PASS", "epistemic_status": "OBSERVED", "targets": 60, "source_recovery": control["source"], "certified_leaves": [], "minimum_nondeficit_gap": min(gaps), "maximum_nondeficit_gap": max(gaps)}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
