#!/usr/bin/env python3
"""Direct cyclic transfer of Cycle 21's exact width-three certificates."""

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

RESULTS = ROOT / "discovery/out/cycle21-coupled-incidence/results.tsv"
OUT = ROOT / "discovery/out/cycle21-coupled-incidence"
FIRST_TIME_CLAUSE = 1197
TRANSFER_SECONDS = 1200


class Transfer(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    source_base: int
    source_leaf: int
    shift: int
    partition: str
    source_clauses: str
    weights: str
    W: int
    U: int
    block_maxima: str
    trials: int
    detail: str


def rows() -> list[dict[str, str]]:
    with RESULTS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_partition(text: str) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def rotate(partition: tuple[tuple[int, ...], ...], shift: int) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(tuple(sorted((coordinate + shift) % cycle21.K for coordinate in block)) for block in partition))


def partition_text(partition: tuple[tuple[int, ...], ...]) -> str:
    return ",".join("-".join(map(str, block)) for block in partition)


def raw_coverage(path: Path) -> np.ndarray:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    clauses = [tuple(map(int, line.split()[:-1])) for line in lines[1:]]
    time_clauses = clauses[FIRST_TIME_CLAUSE - 1:FIRST_TIME_CLAUSE - 1 + cycle21.P * cycle21.C]
    if len(time_clauses) != cycle21.P * cycle21.C:
        raise AssertionError("direct time-clause slice mismatch")
    coverage = np.zeros((cycle21.P * cycle21.C, cycle21.K, cycle21.C), dtype=bool)
    for point, clause in enumerate(time_clauses):
        for literal in clause:
            variable = literal - 1
            coverage[point, variable // cycle21.C, variable % cycle21.C] = True
    return coverage


def capacity(
    partition: tuple[tuple[int, ...], ...],
    allowed: tuple[tuple[int, ...], ...],
    active_coverage: np.ndarray,
    active_weights: np.ndarray,
) -> tuple[int, list[int]]:
    maxima = []
    for block in partition:
        maximum = 0
        for option in itertools.product(*(allowed[coordinate] for coordinate in block)):
            mask = np.zeros(len(active_weights), dtype=bool)
            for coordinate, digit in zip(block, option, strict=True):
                mask |= active_coverage[:, coordinate, digit]
            maximum = max(maximum, int(active_weights[mask].sum()))
        maxima.append(maximum)
    return sum(maxima), maxima


def solve(job: tuple[int, int, float]) -> Transfer:
    base_index, ordinal, deadline = job
    if time.monotonic() >= deadline:
        return Transfer(base_index, ordinal, "CAP", -1, -1, -1, "", "", "", 0, 0, "", 0, "transfer wall cap before target")
    all_rows = rows()
    sources = [row for row in all_rows if row["status"] == "CERTIFIED_DEFICIT"]
    coverage = raw_coverage(direct.CNFS[base_index])
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    trials = 0
    for source in sources:
        source_partition = parse_partition(source["partition"])
        clauses = list(map(int, source["source_clauses"].split(",")))
        values = list(map(int, source["weights"].split(",")))
        points = np.asarray([clause - FIRST_TIME_CLAUSE for clause in clauses], dtype=int)
        if np.any(points < 0) or np.any(points >= cycle21.P * cycle21.C):
            raise AssertionError("source time outside direct range")
        active_coverage = coverage[points]
        active_weights = np.asarray(values, dtype=np.int64)
        total = int(active_weights.sum())
        for shift in range(cycle21.K):
            if time.monotonic() >= deadline:
                return Transfer(base_index, ordinal, "CAP", -1, -1, -1, "", "", "", 0, 0, "", trials, "transfer wall cap during target")
            partition = rotate(source_partition, shift)
            upper, maxima = capacity(partition, allowed, active_coverage, active_weights)
            trials += 1
            if upper < total:
                return Transfer(
                    base_index, ordinal, "CERTIFIED_TRANSFER",
                    int(source["base_index"]), int(source["leaf_ordinal"]), shift,
                    partition_text(partition), source["source_clauses"], source["weights"],
                    total, upper, ",".join(map(str, maxima)), trials,
                    "fresh direct-CNF width-three deficit from transferred weights",
                )
    return Transfer(base_index, ordinal, "UNRESOLVED", -1, -1, -1, "", "", "", 0, 0, "", trials, "no frozen direct transfer produced a deficit")


def main() -> None:
    all_rows = rows()
    targets = [
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in all_rows if row["status"] == "UNRESOLVED"
    ]
    if len(targets) != 61:
        raise AssertionError("transfer target boundary mismatch")
    started = time.monotonic()
    deadline = started + TRANSFER_SECONDS
    with multiprocessing.Pool(processes=3) as pool:
        transferred = pool.map(solve, [(base, leaf, deadline) for base, leaf in targets], chunksize=1)
    lines = ["\t".join(Transfer._fields)]
    lines.extend("\t".join(map(str, row)) for row in transferred)
    (OUT / "transfer.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in transferred) for status in sorted({row.status for row in transferred})}
    summary = "targets=61 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "transfer-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
