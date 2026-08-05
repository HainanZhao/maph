#!/usr/bin/env python3
"""Cycle 23 global pair-savings partition oracle and initial exact transfer."""

from __future__ import annotations

import csv
import itertools
import multiprocessing
import os
from pathlib import Path
import sys
import time
from typing import NamedTuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

SOURCE = ROOT / "discovery/out/cycle22-width-four/stage-b-results.tsv"
OUT = ROOT / "discovery/out/cycle23-adaptive-width-four"


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    oracle_score: int
    partition: str
    source_clauses: str
    weights: str
    support: int
    W: int
    U: int
    block_maxima: str
    candidate_partitions: int
    detail: str


def source_rows() -> list[dict[str, str]]:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source() -> dict[str, str]:
    certified = [row for row in source_rows() if row["status"] == "CERTIFIED_DEFICIT"]
    if len(certified) != 1:
        raise AssertionError("Cycle-22 source count mismatch")
    row = certified[0]
    if (int(row["base_index"]), int(row["leaf_ordinal"]), int(row["support"]), int(row["W"]), int(row["U"])) != (4, 952, 176, 65528, 65440):
        raise AssertionError("Cycle-22 source boundary mismatch")
    return row


def targets() -> list[tuple[int, int]]:
    result = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in source_rows() if row["status"] == "UNRESOLVED"]
    if len(result) != 60:
        raise AssertionError("Cycle-23 target boundary mismatch")
    return result


def triple_partitions(items: tuple[int, ...]):
    first = items[0]
    rest = items[1:]
    for pair in itertools.combinations(rest, 2):
        block1 = tuple(sorted((first, *pair)))
        left = tuple(item for item in rest if item not in pair)
        second = left[0]
        for pair2 in itertools.combinations(left[1:], 2):
            block2 = tuple(sorted((second, *pair2)))
            block3 = tuple(item for item in left[1:] if item not in pair2)
            yield tuple(sorted((block1, block2, block3)))


def partition_text(partition) -> str:
    return ",".join("-".join(map(str, block)) for block in partition)


def parse_partition(text: str):
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def maxima_and_savings(coverage: np.ndarray, allowed, weights: np.ndarray):
    singleton = {}
    for coordinate in range(cycle21.K):
        singleton[coordinate] = max(int(weights[coverage[:, coordinate, digit]].sum()) for digit in allowed[coordinate])
    savings = {}
    for left in range(cycle21.K):
        for right in range(left + 1, cycle21.K):
            maximum = 0
            for dl in allowed[left]:
                for dr in allowed[right]:
                    maximum = max(maximum, int(weights[coverage[:, left, dl] | coverage[:, right, dr]].sum()))
            savings[(left, right)] = singleton[left] + singleton[right] - maximum
            if savings[(left, right)] < 0:
                raise AssertionError("negative exact pair saving")
    return singleton, savings


def select_partition(savings: dict[tuple[int, int], int]):
    block_scores = {}
    for size in (3, 4):
        for block in itertools.combinations(range(cycle21.K), size):
            block_scores[block] = sum(savings[tuple(sorted(pair))] for pair in itertools.combinations(block, 2))
    best_score = -1
    best = None
    count = 0
    universe = tuple(range(cycle21.K))
    for block4 in itertools.combinations(universe, 4):
        remaining = tuple(item for item in universe if item not in block4)
        for triples in triple_partitions(remaining):
            partition = tuple(sorted((block4, *triples)))
            score = block_scores[block4] + sum(block_scores[block] for block in triples)
            count += 1
            if score > best_score or (score == best_score and (best is None or partition < best)):
                best_score, best = score, partition
    if count != 200_200 or best is None:
        raise AssertionError("adaptive partition census mismatch")
    return best_score, best, count


def solve(job: tuple[int, int]) -> Result:
    base_index, ordinal = job
    src = source()
    clauses = list(map(int, src["source_clauses"].split(",")))
    values = np.asarray(list(map(int, src["weights"].split(","))), dtype=np.int64)
    points = np.asarray([clause - width4.FIRST_TIME for clause in clauses], dtype=int)
    coverage = width4.raw_coverage(direct.CNFS[base_index])[points]
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    _, savings = maxima_and_savings(coverage, allowed, values)
    score, partition, count = select_partition(savings)
    upper, block_maxima = width4.capacity(partition, allowed, coverage, values)
    total = int(values.sum())
    status = "CERTIFIED_TRANSFER" if upper < total else "NEED_LP"
    return Result(
        base_index, ordinal, status, score, partition_text(partition),
        src["source_clauses"], src["weights"], len(values), total, upper,
        ",".join(map(str, block_maxima)), count,
        "exact direct-CNF transfer" if upper < total else "oracle partition requires fresh LP",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, targets(), chunksize=1)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "oracle.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    summary = "targets=60 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "oracle-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
