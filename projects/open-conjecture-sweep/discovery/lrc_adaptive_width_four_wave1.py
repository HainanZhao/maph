#!/usr/bin/env python3
"""Cycle 23's one permitted adaptive width-four reselection wave."""

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
import lrc_adaptive_width_four_oracle as oracle
import lrc_adaptive_width_four_wave0 as wave0
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle23-adaptive-width-four"
WAVE_ZERO = OUT / "wave0.tsv"
STAGE_SECONDS = 2700


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    initial_partition: str
    reselected_partition: str
    initial_score: int
    reselected_score: str
    objective: str
    source_clauses: str
    weights: str
    support: int
    denominator: int
    W: int
    U: int
    block_maxima: str
    detail: str


def wave_zero_rows() -> list[dict[str, str]]:
    with WAVE_ZERO.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 60 or any(row["status"] != "NEED_RESELECT" for row in rows):
        raise AssertionError("wave-zero boundary mismatch")
    return rows


def maxima_and_savings_float(allowed, coverage, weights):
    singletons = []
    for coordinate in range(13):
        singletons.append(max(float(weights[coverage[:, coordinate, digit]].sum()) for digit in allowed[coordinate]))
    savings = {}
    for left in range(13):
        for right in range(left + 1, 13):
            maximum = max(
                float(weights[(coverage[:, left, first] | coverage[:, right, second])].sum())
                for first in allowed[left]
                for second in allowed[right]
            )
            saving = singletons[left] + singletons[right] - maximum
            if saving < -1e-10:
                raise AssertionError(f"floating pair saving below tolerance: {left},{right}={saving}")
            savings[left, right] = max(0.0, saving)
    return savings


def select_partition_float(savings):
    best_score = None
    best_partition = None
    candidates = 0
    coordinates = tuple(range(13))
    for four in itertools.combinations(coordinates, 4):
        remainder = tuple(coordinate for coordinate in coordinates if coordinate not in four)
        for triples in oracle.triple_partitions(remainder):
            partition = tuple(sorted((tuple(four), *triples)))
            score = sum(
                savings[min(left, right), max(left, right)]
                for block in partition
                for left, right in itertools.combinations(block, 2)
            )
            candidates += 1
            if best_score is None or score > best_score or (score == best_score and partition < best_partition):
                best_score, best_partition = score, partition
    if candidates != 200200:
        raise AssertionError(f"candidate census {candidates}")
    return best_partition, best_score


def certify(base_index, ordinal, partition, allowed, coverage, solved, initial, reselected, initial_score, reselected_score, rounds):
    floating = solved.x[: len(coverage)]
    if solved.fun < 1.0 - 1e-9:
        for denominator in wave0.DENOMINATORS:
            weights = np.rint(floating * denominator).astype(np.int64)
            weights[weights < 0] = 0
            active = np.flatnonzero(weights)
            if not 0 < len(active) <= 256:
                continue
            total = int(weights.sum())
            upper, maxima = wave0.exact_capacity(partition, allowed, coverage, weights)
            if upper < total:
                clauses = [width4.FIRST_TIME + int(index) for index in active]
                return Result(
                    base_index, ordinal, "CERTIFIED_DEFICIT", initial, reselected,
                    initial_score, f"{reselected_score:.17g}", f"{solved.fun:.17g}",
                    ",".join(map(str, clauses)), ",".join(str(int(weights[index])) for index in active),
                    len(active), denominator, total, upper, ",".join(map(str, maxima)),
                    f"exact integerized adaptive reselection deficit; separation_rounds={rounds}",
                )
    return Result(
        base_index, ordinal, "UNRESOLVED", initial, reselected, initial_score,
        f"{reselected_score:.17g}", f"{solved.fun:.17g}", "", "", 0, 0, 0, 0, "",
        f"reselected LP did not integerize strictly; separation_rounds={rounds}",
    )


def solve(job: tuple[dict[str, str], float]) -> Result:
    row, deadline = job
    base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
    initial = row["partition"]
    initial_score = int(row["oracle_score"])
    if time.monotonic() >= deadline:
        return Result(base_index, ordinal, "CAP", initial, "", initial_score, "nan", "nan", "", "", 0, 0, 0, 0, "", "wall cap before reselection")
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    coverage = width4.raw_coverage(direct.CNFS[base_index])
    weights = np.asarray([float(value) for value in row["floating_weights"].split(",")], dtype=float)
    if weights.shape != (len(coverage),) or float(weights.min()) < -1e-12 or abs(float(weights.sum()) - 1.0) > 1e-12:
        raise AssertionError("wave-zero floating weight mismatch")
    weights[weights < 0] = 0.0
    weights /= weights.sum()
    reselected_partition, reselected_score = select_partition_float(maxima_and_savings_float(allowed, coverage, weights))
    reselected = oracle.partition_text(reselected_partition)
    if reselected == initial:
        return Result(base_index, ordinal, "UNCHANGED", initial, reselected, initial_score, f"{reselected_score:.17g}", "nan", "", "", 0, 0, 0, 0, "", "adaptive selector retained wave-zero partition")
    block_masks = [wave0.block_option_masks(block, allowed, coverage)[1] for block in reselected_partition]
    solved, rounds, detail = wave0.solve_by_separation(block_masks, deadline)
    if solved is None:
        status = "CAP" if detail.startswith("wall cap") or detail == "separation-round cap" else "LP_ERROR"
        return Result(base_index, ordinal, status, initial, reselected, initial_score, f"{reselected_score:.17g}", "nan", "", "", 0, 0, 0, 0, "", detail)
    return certify(base_index, ordinal, reselected_partition, allowed, coverage, solved, initial, reselected, initial_score, reselected_score, rounds)


def main() -> None:
    started = time.monotonic()
    deadline = started + STAGE_SECONDS
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, [(row, deadline) for row in wave_zero_rows()], chunksize=1)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "wave1.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    summary = "targets=60 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "wave1-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
