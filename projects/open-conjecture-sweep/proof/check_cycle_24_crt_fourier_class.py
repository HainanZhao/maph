#!/usr/bin/env python3
"""Direct-mask audit for the Cycle 24 CRT/Ramanujan class run."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_crt_fourier_class as fourier
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle24-crt-fourier-class"


def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def audit():
    assert len(cycle21.interface_controls()) == 295
    for base_index in (3, 4):
        coverage = width4.raw_coverage(direct.CNFS[base_index])
        base = cycle21.read_bases()[base_index]
        for point in range(cycle21.P * cycle21.C):
            for coordinate in range(cycle21.K):
                for digit in range(cycle21.C):
                    residue = ((base[coordinate] + cycle21.P * digit) * point) % (cycle21.P * cycle21.C)
                    direct_bad = cycle21.C * min(residue, cycle21.P * cycle21.C - residue) < cycle21.P * cycle21.C
                    assert bool(coverage[point, coordinate, digit]) == direct_bad
    counts = [0] * 8
    for point in range(cycle21.P * cycle21.C):
        epsilon = 0 if point % cycle21.P == 0 else 1
        divisor = math.gcd(point % cycle21.C, cycle21.C)
        counts[[(0, 1), (0, 2), (0, 7), (0, 14), (1, 1), (1, 2), (1, 7), (1, 14)].index((epsilon, divisor))] += 1
    assert counts == [6, 6, 1, 1, 1188, 1188, 198, 198]
    result = rows(OUT / "results.tsv")
    prior = rows(ROOT / "discovery/out/cycle23-adaptive-width-four/oracle.tsv")
    assert [(r["base_index"], r["leaf_ordinal"]) for r in result] == [(r["base_index"], r["leaf_ordinal"]) for r in prior] and len(result) == 60
    assert all(r["status"] == "UNRESOLVED" for r in result)
    indices = fourier.class_indices()
    for row in result:
        base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        allowed = direct.allowed_digits(cycle21.read_bases()[base_index], ordinal)
        coverage = width4.raw_coverage(direct.CNFS[base_index])
        score, partition = fourier.select_partition(fourier.exact_savings(allowed, coverage, indices))
        assert int(row["oracle_score"]) == score
        assert row["partition"] == fourier.partition_text(partition)
        assert 1 <= int(row["separation_rounds"]) <= 512
    objectives = [float(r["objective"]) for r in result]
    assert min(objectives) >= 1 - 1e-9
    return {"status": "PASS", "epistemic_status": "OBSERVED", "targets": 60, "class_cardinalities": counts, "objective_min": min(objectives), "objective_max": max(objectives), "certified_leaves": []}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
