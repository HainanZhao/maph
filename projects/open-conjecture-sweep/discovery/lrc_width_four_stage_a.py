#!/usr/bin/env python3
"""Cycle 22 Stage A: exact transferred weights on targeted width-four blocks."""

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

SOURCE = ROOT / "discovery/out/cycle21-coupled-incidence/results.tsv"
OUT = ROOT / "discovery/out/cycle22-width-four"
FIRST_TIME = 1197


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    partition_rank: int
    partition: str
    source_base: int
    source_leaf: int
    source_clauses: str
    weights: str
    support: int
    W: int
    U: int
    block_maxima: str
    trials: int
    detail: str


def source_rows() -> list[dict[str, str]]:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def targets() -> list[tuple[int, int]]:
    rows = source_rows()
    if sum(row["status"] == "CERTIFIED_DEFICIT" for row in rows) != 15:
        raise AssertionError("Cycle-21 certified boundary mismatch")
    result = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows if row["status"] == "UNRESOLVED"]
    if len(result) != 61:
        raise AssertionError("Cycle-21 survivor boundary mismatch")
    return result


def partitions(allowed: tuple[tuple[int, ...], ...]) -> list[tuple[tuple[int, ...], ...]]:
    ordered = sorted(range(cycle21.K), key=lambda coordinate: (len(allowed[coordinate]), coordinate))
    restricted = tuple(sorted(ordered[:3]))
    result = []
    for fourth in range(cycle21.K):
        if fourth in restricted:
            continue
        block4 = tuple(sorted((*restricted, fourth)))
        remaining = [coordinate for coordinate in range(cycle21.K) if coordinate not in block4]
        blocks = [block4, tuple(remaining[0:3]), tuple(remaining[3:6]), tuple(remaining[6:9])]
        canonical = tuple(sorted(tuple(sorted(block)) for block in blocks))
        if sorted(item for block in canonical for item in block) != list(range(cycle21.K)):
            raise AssertionError("bad width-four partition")
        result.append(canonical)
    if len(result) != 10 or len(set(result)) != 10:
        raise AssertionError("width-four partition census mismatch")
    return result


def text(partition: tuple[tuple[int, ...], ...]) -> str:
    return ",".join("-".join(map(str, block)) for block in partition)


def raw_coverage(path: Path) -> np.ndarray:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    clauses = [tuple(map(int, line.split()[:-1])) for line in lines[1:]]
    time_clauses = clauses[FIRST_TIME - 1:FIRST_TIME - 1 + cycle21.P * cycle21.C]
    coverage = np.zeros((cycle21.P * cycle21.C, cycle21.K, cycle21.C), dtype=bool)
    if len(time_clauses) != len(coverage):
        raise AssertionError("time-clause count mismatch")
    for point, clause in enumerate(time_clauses):
        for literal in clause:
            variable = literal - 1
            coverage[point, variable // cycle21.C, variable % cycle21.C] = True
    return coverage


def capacity(partition, allowed, active_coverage, weights) -> tuple[int, list[int]]:
    maxima = []
    for block in partition:
        maximum = 0
        for option in itertools.product(*(allowed[coordinate] for coordinate in block)):
            mask = np.zeros(len(weights), dtype=bool)
            for coordinate, digit in zip(block, option, strict=True):
                mask |= active_coverage[:, coordinate, digit]
            maximum = max(maximum, int(weights[mask].sum()))
        maxima.append(maximum)
    return sum(maxima), maxima


def solve(job: tuple[int, int]) -> Result:
    base_index, ordinal = job
    rows = source_rows()
    sources = [row for row in rows if row["status"] == "CERTIFIED_DEFICIT"]
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    family = partitions(allowed)
    coverage = raw_coverage(direct.CNFS[base_index])
    trials = 0
    for rank, partition in enumerate(family):
        for source in sources:
            clauses = list(map(int, source["source_clauses"].split(",")))
            values = np.asarray(list(map(int, source["weights"].split(","))), dtype=np.int64)
            points = np.asarray([clause - FIRST_TIME for clause in clauses], dtype=int)
            upper, maxima = capacity(partition, allowed, coverage[points], values)
            total = int(values.sum())
            trials += 1
            if upper < total:
                return Result(
                    base_index, ordinal, "CERTIFIED_TRANSFER", rank, text(partition),
                    int(source["base_index"]), int(source["leaf_ordinal"]),
                    source["source_clauses"], source["weights"], len(values), total,
                    upper, ",".join(map(str, maxima)), trials,
                    "fresh direct-CNF width-four deficit from Cycle-21 weights",
                )
    return Result(base_index, ordinal, "UNRESOLVED", -1, "", -1, -1, "", "", 0, 0, 0, "", trials, "no transferred weight produced a deficit")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, targets(), chunksize=1)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "stage-a.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    summary = "targets=61 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "stage-a-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
