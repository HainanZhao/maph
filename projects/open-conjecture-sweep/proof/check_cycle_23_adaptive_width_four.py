#!/usr/bin/env python3
"""Independent direct-CNF audit of the Cycle 23 adaptive width-four output."""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_adaptive_width_four_oracle as oracle
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle23-adaptive-width-four"


def read(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def keys(rows):
    return [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows]


def independent_triple_partitions(items: tuple[int, ...]):
    first, rest = items[0], items[1:]
    for pair in itertools.combinations(rest, 2):
        first_block = tuple(sorted((first, *pair)))
        remaining = tuple(item for item in rest if item not in pair)
        second = remaining[0]
        for second_pair in itertools.combinations(remaining[1:], 2):
            second_block = tuple(sorted((second, *second_pair)))
            third_block = tuple(item for item in remaining[1:] if item not in second_pair)
            yield tuple(sorted((first_block, second_block, third_block)))


def independent_select(savings):
    block_scores = {
        block: sum(savings[tuple(sorted(pair))] for pair in itertools.combinations(block, 2))
        for width in (3, 4)
        for block in itertools.combinations(range(cycle21.K), width)
    }
    best_score, best_partition, candidates = None, None, 0
    universe = tuple(range(cycle21.K))
    for four_block in itertools.combinations(universe, 4):
        remainder = tuple(item for item in universe if item not in four_block)
        for triples in independent_triple_partitions(remainder):
            partition = tuple(sorted((four_block, *triples)))
            score = block_scores[four_block] + sum(block_scores[block] for block in triples)
            candidates += 1
            if best_score is None or score > best_score or (score == best_score and partition < best_partition):
                best_score, best_partition = score, partition
    assert candidates == 200_200
    return best_score, best_partition


def independent_exact_savings(coverage, allowed, weights):
    singletons = {
        coordinate: max(int(weights[coverage[:, coordinate, digit]].sum()) for digit in allowed[coordinate])
        for coordinate in range(cycle21.K)
    }
    savings = {}
    for left in range(cycle21.K):
        for right in range(left + 1, cycle21.K):
            maximum = max(
                int(weights[coverage[:, left, first] | coverage[:, right, second]].sum())
                for first in allowed[left]
                for second in allowed[right]
            )
            savings[left, right] = singletons[left] + singletons[right] - maximum
            assert savings[left, right] >= 0
    return savings


def independent_float_savings(coverage, allowed, weights):
    singletons = {
        coordinate: max(float(weights[coverage[:, coordinate, digit]].sum()) for digit in allowed[coordinate])
        for coordinate in range(cycle21.K)
    }
    savings = {}
    for left in range(cycle21.K):
        for right in range(left + 1, cycle21.K):
            maximum = max(
                float(weights[coverage[:, left, first] | coverage[:, right, second]].sum())
                for first in allowed[left]
                for second in allowed[right]
            )
            saving = singletons[left] + singletons[right] - maximum
            assert saving >= -1e-10
            savings[left, right] = max(0.0, saving)
    return savings


def direct_certificate(row: dict[str, str], partition_text: str) -> None:
    base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
    clauses = list(map(int, row["source_clauses"].split(",")))
    values = list(map(int, row["weights"].split(",")))
    assert len(clauses) == len(values) == int(row["support"]) <= 256
    weights = np.zeros(cycle21.P * cycle21.C, dtype=np.int64)
    for clause, value in zip(clauses, values, strict=True):
        point = clause - width4.FIRST_TIME
        assert 0 <= point < len(weights) and value > 0 and weights[point] == 0
        weights[point] = value
    allowed = direct.allowed_digits(cycle21.read_bases()[base_index], ordinal)
    coverage = width4.raw_coverage(direct.CNFS[base_index])
    upper, maxima = direct.exact_capacity(oracle.parse_partition(partition_text), allowed, coverage, weights)
    assert int(weights.sum()) == int(row["W"])
    assert upper == int(row["U"])
    assert maxima == list(map(int, row["block_maxima"].split(",")))
    assert upper < int(row["W"])


def audit() -> dict[str, object]:
    expected = oracle.targets()
    initial = read("oracle.tsv")
    assert keys(initial) == expected and len(initial) == 60
    assert all(int(row["candidate_partitions"]) == 200_200 for row in initial)
    assert all(row["status"] in {"NEED_LP", "CERTIFIED_TRANSFER"} for row in initial)
    source = oracle.source()
    source_points = np.asarray([int(clause) - width4.FIRST_TIME for clause in source["source_clauses"].split(",")])
    source_weights = np.asarray([int(value) for value in source["weights"].split(",")], dtype=np.int64)
    for row in initial:
        base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        allowed = direct.allowed_digits(cycle21.read_bases()[base_index], ordinal)
        active_coverage = width4.raw_coverage(direct.CNFS[base_index])[source_points]
        score, partition = independent_select(independent_exact_savings(active_coverage, allowed, source_weights))
        assert int(row["oracle_score"]) == score
        assert row["partition"] == ",".join("-".join(map(str, block)) for block in partition)
        upper, maxima = width4.capacity(partition, allowed, active_coverage, source_weights)
        assert int(row["W"]) == int(source_weights.sum())
        assert int(row["U"]) == upper
        assert row["block_maxima"] == ",".join(map(str, maxima))
        assert row["status"] == ("CERTIFIED_TRANSFER" if upper < int(source_weights.sum()) else "NEED_LP")
        if row["status"] == "CERTIFIED_TRANSFER":
            direct_certificate(row, row["partition"])

    wave_zero = read("wave0.tsv")
    assert keys(wave_zero) == expected and len(wave_zero) == 60
    assert all(row["partition"] == first["partition"] for row, first in zip(wave_zero, initial, strict=True))
    for row in wave_zero:
        assert row["status"] in {"CERTIFIED_DEFICIT", "NEED_RESELECT", "CAP", "LP_ERROR"}
        if row["status"] == "CERTIFIED_DEFICIT":
            direct_certificate(row, row["partition"])
        if row["status"] == "NEED_RESELECT":
            floating = np.asarray([float(value) for value in row["floating_weights"].split(",")])
            assert floating.shape == (cycle21.P * cycle21.C,)
            assert (floating >= -1e-12).all() and abs(float(floating.sum()) - 1.0) <= 1e-9

    wave_one = read("wave1.tsv")
    assert keys(wave_one) == expected and len(wave_one) == 60
    for row, zero in zip(wave_one, wave_zero, strict=True):
        assert row["initial_partition"] == zero["partition"]
        assert row["status"] in {"CERTIFIED_DEFICIT", "UNRESOLVED", "UNCHANGED", "CAP", "LP_ERROR"}
        base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
        allowed = direct.allowed_digits(cycle21.read_bases()[base_index], ordinal)
        coverage = width4.raw_coverage(direct.CNFS[base_index])
        floating = np.asarray([float(value) for value in zero["floating_weights"].split(",")])
        assert floating.shape == (len(coverage),) and float(floating.min()) >= -1e-12
        assert abs(float(floating.sum()) - 1.0) <= 1e-12
        floating[floating < 0] = 0.0
        floating /= floating.sum()
        reselected_score, reselected_partition = independent_select(independent_float_savings(coverage, allowed, floating))
        reselected_text = ",".join("-".join(map(str, block)) for block in reselected_partition)
        assert row["reselected_partition"] == reselected_text
        assert abs(float(row["reselected_score"]) - reselected_score) <= 1e-11
        if row["status"] == "UNCHANGED":
            assert row["reselected_partition"] == row["initial_partition"]
        else:
            assert row["reselected_partition"] != row["initial_partition"]
        if row["status"] == "CERTIFIED_DEFICIT":
            direct_certificate(row, row["reselected_partition"])

    certificates = [row for row in wave_zero if row["status"] == "CERTIFIED_DEFICIT"]
    certificates += [row for row in wave_one if row["status"] == "CERTIFIED_DEFICIT"]
    return {
        "status": "PASS",
        "epistemic_status": "PROVED" if certificates else "OBSERVED",
        "targets": len(expected),
        "initial_transfers": {status: sum(row["status"] == status for row in initial) for status in sorted({row["status"] for row in initial})},
        "wave_zero": {status: sum(row["status"] == status for row in wave_zero) for status in sorted({row["status"] for row in wave_zero})},
        "wave_one": {status: sum(row["status"] == status for row in wave_one) for status in sorted({row["status"] for row in wave_one})},
        "certified_leaves": [{"base_index": int(row["base_index"]), "leaf_ordinal": int(row["leaf_ordinal"]), "W": int(row["W"]), "U": int(row["U"])} for row in certificates],
        "claim_boundary": "Only named rows carrying direct U<W certificates are proved; all selector and floating LP results remain discovery evidence.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
