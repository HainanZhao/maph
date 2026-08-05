#!/usr/bin/env python3
"""Cycle 22 exhaustive four-subset transfer via exact uncovered antichains."""

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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as stage_a

OUT = ROOT / "discovery/out/cycle22-width-four"
RESULTS = OUT / "stage-b-results.tsv"
STATE_CAP = 1_000_000
STAGE_SECONDS = 1800


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    four_block: str
    partition: str
    source_clauses: str
    weights: str
    support: int
    W: int
    U: int
    block_maxima: str
    partitions_tested: int
    blocks_evaluated: int
    maximum_antichain_states: int
    detail: str


def rows() -> list[dict[str, str]]:
    with RESULTS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source() -> dict[str, str]:
    certified = [row for row in rows() if row["status"] == "CERTIFIED_DEFICIT"]
    if len(certified) != 1 or (int(certified[0]["base_index"]), int(certified[0]["leaf_ordinal"])) != (4, 952):
        raise AssertionError("Cycle-22 source boundary mismatch")
    return certified[0]


def targets() -> list[tuple[int, int]]:
    result = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows() if row["status"] == "UNRESOLVED"]
    if len(result) != 60:
        raise AssertionError("Cycle-22 continuation target mismatch")
    return result


def partition_for(block4: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    remaining = [coordinate for coordinate in range(cycle21.K) if coordinate not in block4]
    return (block4, tuple(remaining[0:3]), tuple(remaining[3:6]), tuple(remaining[6:9]))


def text(blocks) -> str:
    return ",".join("-".join(map(str, block)) for block in blocks)


def minimize(masks: set[int]) -> list[int]:
    retained: list[int] = []
    for mask in sorted(masks, key=lambda value: (value.bit_count(), value)):
        if not any((prior & mask) == prior for prior in retained):
            retained.append(mask)
    return retained


def solve(job: tuple[int, int, float]) -> Result:
    base_index, ordinal, deadline = job
    src = source()
    clauses = list(map(int, src["source_clauses"].split(",")))
    weights = list(map(int, src["weights"].split(",")))
    points = [clause - stage_a.FIRST_TIME for clause in clauses]
    total = sum(weights)
    coverage = stage_a.raw_coverage(direct.CNFS[base_index])
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    full = (1 << len(points)) - 1
    uncovered: list[list[int]] = []
    for coordinate in range(cycle21.K):
        options = []
        for digit in allowed[coordinate]:
            covered = 0
            for bit, point in enumerate(points):
                if coverage[point, coordinate, digit]:
                    covered |= 1 << bit
            options.append(full ^ covered)
        uncovered.append(options)
    byte_tables = []
    for offset in range(0, len(weights), 8):
        chunk = weights[offset:offset + 8]
        byte_tables.append([
            sum(weight for bit, weight in enumerate(chunk) if value & (1 << bit))
            for value in range(256)
        ])

    def mask_weight(mask: int) -> int:
        return sum(table[(mask >> (8 * position)) & 255] for position, table in enumerate(byte_tables))

    cache: dict[tuple[int, ...], tuple[int, int]] = {}
    maximum_states = 1

    def block_maximum(block: tuple[int, ...]) -> tuple[int, bool]:
        nonlocal maximum_states
        if block in cache:
            return cache[block][0], False
        frontier = [full]
        for coordinate in block:
            candidates = {mask & option for mask in frontier for option in uncovered[coordinate]}
            frontier = minimize(candidates)
            maximum_states = max(maximum_states, len(frontier))
            if len(frontier) > STATE_CAP:
                raise OverflowError("minimal-uncovered state cap")
        value = total - min(mask_weight(mask) for mask in frontier)
        cache[block] = (value, len(frontier))
        return value, True

    tested = 0
    try:
        for block4 in itertools.combinations(range(cycle21.K), 4):
            if time.monotonic() >= deadline:
                return Result(base_index, ordinal, "CAP", "", "", "", "", 0, 0, 0, "", tested, len(cache), maximum_states, "aggregate wall cap")
            partition = partition_for(block4)
            maxima = []
            for block in partition:
                value, _ = block_maximum(tuple(block))
                maxima.append(value)
            tested += 1
            upper = sum(maxima)
            if upper < total:
                return Result(
                    base_index, ordinal, "CERTIFIED_TRANSFER", "-".join(map(str, block4)),
                    text(partition), src["source_clauses"], src["weights"], len(weights),
                    total, upper, ",".join(map(str, maxima)), tested, len(cache),
                    maximum_states, "exact all-four-subset direct-CNF deficit",
                )
    except OverflowError as error:
        return Result(base_index, ordinal, "CAP", "", "", "", "", 0, 0, 0, "", tested, len(cache), maximum_states, str(error))
    return Result(base_index, ordinal, "UNRESOLVED", "", "", "", "", 0, 0, 0, "", tested, len(cache), maximum_states, "all 715 frozen four-subsets completed without deficit")


def main() -> None:
    started = time.monotonic()
    deadline = started + STAGE_SECONDS
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, [(base, leaf, deadline) for base, leaf in targets()], chunksize=1)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "exhaustive-transfer.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    summary = "targets=60 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "exhaustive-transfer-result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
