#!/usr/bin/env python3
"""Lightweight direct-interface audit for Cycle 27's complete LP census."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4
import lrc_width_five_lp as lp

OUT = ROOT / "discovery/out/cycle27-width-five-lp"

def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))

def audit():
    source = lp.source_row(); weights = lp.source_weights(); blocks = lp.parse_partition(source["partition"])
    allowed = direct.allowed_digits(coupled.read_bases()[4], 952); coverage = width4.raw_coverage(direct.CNFS[4])
    upper, maxima = lp.exact_capacity(blocks, allowed, coverage, weights)
    assert (int(weights.sum()), upper, maxima) == (65528, 65440, [7587, 12454, 21481, 23918])
    result, prior = rows(OUT / "results.tsv"), lp.target_rows()
    assert len(result) == len(prior) == 60
    assert [(row["base_index"], row["leaf_ordinal"]) for row in result] == [(row["base_index"], row["leaf_ordinal"]) for row in prior]
    assert all(row["status"] == "UNRESOLVED" for row in result)
    rounds=[]; cuts=[]
    for row in result:
        base, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        expected = lp.target_partition(direct.allowed_digits(coupled.read_bases()[base], ordinal))
        assert row["partition"] == lp.partition_text(expected)
        assert float(row["objective"]) >= 1 - lp.TOL
        assert 1 <= int(row["separation_rounds"]) <= lp.TARGET_ROUNDS
        assert int(row["cuts"]) >= 3
        rounds.append(int(row["separation_rounds"])); cuts.append(int(row["cuts"]))
    return {"status":"PASS","epistemic_status":"OBSERVED","targets":60,"source_direct_recovery":{"W":65528,"U":65440,"margin":88},"fully_separated_unresolved":60,"rounds_min":min(rounds),"rounds_max":max(rounds),"cuts_min":min(cuts),"cuts_max":max(cuts),"certified_leaves":[]}

if __name__ == "__main__": print(json.dumps(audit(), indent=2, sort_keys=True))
