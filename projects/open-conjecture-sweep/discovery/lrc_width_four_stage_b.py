#!/usr/bin/env python3
"""Cycle 22 Stage B: breadth-first targeted width-four LP search."""

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
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as stage_a

OUT = ROOT / "discovery/out/cycle22-width-four"
DENOMINATORS = (4096, 65536, 1048576, 16777216)
STAGE_SECONDS = 3200


class Trial(NamedTuple):
    base_index: int
    leaf_ordinal: int
    partition_rank: int
    status: str
    partition: str
    objective: str
    source_clauses: str
    weights: str
    support: int
    denominator: int
    W: int
    U: int
    block_maxima: str
    detail: str


def option_vector(block, option, coverage):
    result = np.zeros(coverage.shape[0], dtype=bool)
    for coordinate, digit in zip(block, option, strict=True):
        result |= coverage[:, coordinate, digit]
    return result


def exact_capacity(partition, allowed, coverage, weights):
    active = np.flatnonzero(weights)
    active_weights = weights[active]
    maxima = []
    for block in partition:
        maximum = 0
        for option in itertools.product(*(allowed[coordinate] for coordinate in block)):
            value = int(active_weights[option_vector(block, option, coverage)[active]].sum())
            maximum = max(maximum, value)
        maxima.append(maximum)
    return sum(maxima), maxima


def solve(job: tuple[int, int, int, float]) -> Trial:
    base_index, ordinal, rank, deadline = job
    if time.monotonic() >= deadline:
        return Trial(base_index, ordinal, rank, "CAP", "", "nan", "", "", 0, 0, 0, 0, "", "stage wall cap before trial")
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    partition = stage_a.partitions(allowed)[rank]
    coverage = stage_a.raw_coverage(direct.CNFS[base_index])
    n = coverage.shape[0]
    vectors = []
    block_ids = []
    for block_index, block in enumerate(partition):
        for option in itertools.product(*(allowed[coordinate] for coordinate in block)):
            vectors.append(option_vector(block, option, coverage))
            block_ids.append(block_index)
    left = csr_matrix(np.vstack(vectors).astype(float))
    row_indices = np.arange(len(vectors))
    right = csr_matrix((-np.ones(len(vectors)), (row_indices, np.asarray(block_ids))), shape=(len(vectors), len(partition)))
    a_ub = hstack((left, right), format="csr")
    objective = np.concatenate((np.zeros(n), np.ones(len(partition))))
    a_eq = csr_matrix((np.ones(n), (np.zeros(n, dtype=int), np.arange(n))), shape=(1, n + len(partition)))
    remaining = max(1.0, deadline - time.monotonic())
    solved = linprog(
        objective, A_ub=a_ub, b_ub=np.zeros(len(vectors)), A_eq=a_eq,
        b_eq=np.array([1.0]), bounds=(0, None), method="highs-ds",
        options={"presolve": True, "time_limit": remaining},
    )
    ptext = stage_a.text(partition)
    if solved.status == 1 and time.monotonic() >= deadline:
        return Trial(base_index, ordinal, rank, "CAP", ptext, "nan", "", "", 0, 0, 0, 0, "", "stage wall cap in LP")
    if solved.status != 0:
        return Trial(base_index, ordinal, rank, "LP_ERROR", ptext, "nan", "", "", 0, 0, 0, 0, "", solved.message.replace("\t", " "))
    if solved.fun < 1.0 - 1e-9:
        for denominator in DENOMINATORS:
            weights = np.rint(solved.x[:n] * denominator).astype(np.int64)
            weights[weights < 0] = 0
            active = np.flatnonzero(weights)
            if not 0 < len(active) <= 256:
                continue
            total = int(weights.sum())
            upper, maxima = exact_capacity(partition, allowed, coverage, weights)
            if upper < total:
                clauses = [stage_a.FIRST_TIME + int(index) for index in active]
                return Trial(
                    base_index, ordinal, rank, "CERTIFIED_DEFICIT", ptext,
                    f"{solved.fun:.17g}", ",".join(map(str, clauses)),
                    ",".join(str(int(weights[index])) for index in active), len(active),
                    denominator, total, upper, ",".join(map(str, maxima)),
                    "exact integerized targeted width-four deficit",
                )
    return Trial(base_index, ordinal, rank, "UNRESOLVED", ptext, f"{solved.fun:.17g}", "", "", 0, 0, 0, 0, "", "no exact deficit at frozen partition rank")


def write_trials(trials: list[Trial]) -> None:
    lines = ["\t".join(Trial._fields)]
    lines.extend("\t".join(map(str, row)) for row in trials)
    (OUT / "stage-b-trials.tsv").write_text("\n".join(lines) + "\n")


def main() -> None:
    started = time.monotonic()
    deadline = started + STAGE_SECONDS
    live = stage_a.targets()
    all_trials: list[Trial] = []
    certified: dict[tuple[int, int], Trial] = {}
    capped: set[tuple[int, int]] = set()
    with multiprocessing.Pool(processes=3) as pool:
        for rank in range(10):
            jobs = [(base, leaf, rank, deadline) for base, leaf in live if (base, leaf) not in certified and (base, leaf) not in capped]
            if not jobs:
                break
            wave = pool.map(solve, jobs, chunksize=1)
            all_trials.extend(wave)
            for row in wave:
                key = (row.base_index, row.leaf_ordinal)
                if row.status == "CERTIFIED_DEFICIT":
                    certified[key] = row
                elif row.status in ("CAP", "LP_ERROR"):
                    capped.add(key)
            write_trials(all_trials)
            if time.monotonic() >= deadline:
                break
    final = []
    attempted = {(row.base_index, row.leaf_ordinal): row for row in all_trials}
    for key in live:
        if key in certified:
            final.append(certified[key])
        elif key in capped or time.monotonic() >= deadline:
            last = attempted.get(key)
            rank = last.partition_rank if last else -1
            final.append(Trial(*key, rank, "CAP", "", "nan", "", "", 0, 0, 0, 0, "", "stage aggregate cap"))
        else:
            last = attempted[key]
            final.append(Trial(*key, last.partition_rank, "UNRESOLVED", last.partition, last.objective, "", "", 0, 0, 0, 0, "", "all ten frozen partitions completed without deficit"))
    lines = ["\t".join(Trial._fields)]
    lines.extend("\t".join(map(str, row)) for row in final)
    (OUT / "stage-b-results.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in final) for status in sorted({row.status for row in final})}
    summary = "targets=61 trials=" + str(len(all_trials)) + " " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "stage-b-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
