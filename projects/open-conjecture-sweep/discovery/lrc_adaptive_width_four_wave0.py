#!/usr/bin/env python3
"""Cycle 23 LP wave zero on globally selected width-four partitions."""

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
import lrc_adaptive_width_four_oracle as oracle
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle23-adaptive-width-four"
ORACLE = OUT / "oracle.tsv"
DENOMINATORS = (4096, 65536, 1048576, 16777216)
STAGE_SECONDS = 2200
SEPARATION_TOLERANCE = 1e-9
MAX_SEPARATION_ROUNDS = 512


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    oracle_score: int
    partition: str
    objective: str
    source_clauses: str
    weights: str
    support: int
    denominator: int
    W: int
    U: int
    block_maxima: str
    floating_weights: str
    detail: str


def oracle_rows() -> list[dict[str, str]]:
    with ORACLE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 60 or any(row["status"] != "NEED_LP" for row in rows):
        raise AssertionError("oracle boundary mismatch")
    return rows


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


def block_option_masks(block, allowed, coverage):
    """Return canonically ordered options and their direct-CNF cover masks."""
    options = list(itertools.product(*(allowed[coordinate] for coordinate in block)))
    masks = np.empty((len(options), coverage.shape[0]), dtype=np.uint8)
    for index, option in enumerate(options):
        masks[index] = option_vector(block, option, coverage)
    return options, masks


def solve_by_separation(block_masks, deadline):
    """Solve the all-option LP with exact, deterministic constraint separation."""
    n = block_masks[0].shape[1]
    active_constraints = [(block, 0) for block in range(len(block_masks))]
    active_set = set(active_constraints)
    for round_number in range(1, MAX_SEPARATION_ROUNDS + 1):
        if time.monotonic() >= deadline:
            return None, round_number, "wall cap before separation LP"
        rows = np.vstack([block_masks[block][option] for block, option in active_constraints])
        left = csr_matrix(rows, dtype=float)
        row_indices = np.arange(len(active_constraints))
        block_ids = np.asarray([block for block, _ in active_constraints])
        right = csr_matrix(
            (-np.ones(len(active_constraints)), (row_indices, block_ids)),
            shape=(len(active_constraints), len(block_masks)),
        )
        a_ub = hstack((left, right), format="csr")
        objective = np.concatenate((np.zeros(n), np.ones(len(block_masks))))
        a_eq = csr_matrix(
            (np.ones(n), (np.zeros(n, dtype=int), np.arange(n))),
            shape=(1, n + len(block_masks)),
        )
        solved = linprog(
            objective,
            A_ub=a_ub,
            b_ub=np.zeros(len(active_constraints)),
            A_eq=a_eq,
            b_eq=np.array([1.0]),
            bounds=(0, None),
            method="highs-ds",
            options={"presolve": True, "time_limit": max(1.0, deadline - time.monotonic())},
        )
        if solved.status != 0:
            if solved.status == 1 and time.monotonic() >= deadline:
                return None, round_number, "wall cap in separation LP"
            return None, round_number, solved.message.replace("\t", " ")
        weights = solved.x[:n]
        violations = []
        for block, masks in enumerate(block_masks):
            maximum_index = int(np.argmax(masks @ weights))
            maximum = float(masks[maximum_index] @ weights)
            if maximum > float(solved.x[n + block]) + SEPARATION_TOLERANCE:
                violations.append((block, maximum_index))
        if not violations:
            return solved, round_number, "exact all-option separation converged"
        for constraint in violations:
            if constraint in active_set:
                return None, round_number, "separation returned an already-active violated constraint"
            active_constraints.append(constraint)
            active_set.add(constraint)
    return None, MAX_SEPARATION_ROUNDS, "separation-round cap"


def solve(job: tuple[dict[str, str], float]) -> Result:
    row, deadline = job
    base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
    partition = oracle.parse_partition(row["partition"])
    if time.monotonic() >= deadline:
        return Result(base_index, ordinal, "CAP", int(row["oracle_score"]), row["partition"], "nan", "", "", 0, 0, 0, 0, "", "", "wall cap before LP")
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    coverage = width4.raw_coverage(direct.CNFS[base_index])
    n = len(coverage)
    block_masks = [block_option_masks(block, allowed, coverage)[1] for block in partition]
    solved, rounds, detail = solve_by_separation(block_masks, deadline)
    if solved is None:
        status = "CAP" if detail.startswith("wall cap") or detail == "separation-round cap" else "LP_ERROR"
        return Result(base_index, ordinal, status, int(row["oracle_score"]), row["partition"], "nan", "", "", 0, 0, 0, 0, "", "", detail)
    floating = ",".join(f"{value:.17g}" for value in solved.x[:n])
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
                clauses = [width4.FIRST_TIME + int(index) for index in active]
                return Result(
                    base_index, ordinal, "CERTIFIED_DEFICIT", int(row["oracle_score"]),
                    row["partition"], f"{solved.fun:.17g}", ",".join(map(str, clauses)),
                    ",".join(str(int(weights[index])) for index in active), len(active), denominator,
                    total, upper, ",".join(map(str, maxima)), floating,
                    f"exact integerized adaptive width-four deficit; separation_rounds={rounds}",
                )
    return Result(base_index, ordinal, "NEED_RESELECT", int(row["oracle_score"]), row["partition"], f"{solved.fun:.17g}", "", "", 0, 0, 0, 0, "", floating, f"wave-zero LP did not integerize strictly; separation_rounds={rounds}")


def main() -> None:
    started = time.monotonic()
    deadline = started + STAGE_SECONDS
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, [(row, deadline) for row in oracle_rows()], chunksize=1)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "wave0.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    summary = "targets=60 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "wave0-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
