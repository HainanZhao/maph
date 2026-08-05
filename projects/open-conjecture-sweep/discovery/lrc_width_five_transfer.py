#!/usr/bin/env python3
"""Cycle 26 exact 5+4+4 transfer of Cycle 22's proved integer weight."""
from __future__ import annotations

import csv
import itertools
import json
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
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle26-width-five-transfer"
SOURCE = ROOT / "discovery/out/cycle22-width-four/stage-b-results.tsv"
TARGETS = ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv"
MAX_OPTIONS_PER_BLOCK = 14**5
STAGE_SECONDS = 3000


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    partition: str
    W: int
    U: int
    block_maxima: str
    block_option_counts: str
    detail: str


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_partition(text: str) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def source_row() -> dict[str, str]:
    rows = read_rows(SOURCE)
    certified = [row for row in rows if row["status"] == "CERTIFIED_DEFICIT"]
    if len(certified) != 1:
        raise AssertionError("Cycle-22 source certificate boundary")
    row = certified[0]
    if (int(row["base_index"]), int(row["leaf_ordinal"]), int(row["support"]), int(row["W"]), int(row["U"])) != (4, 952, 176, 65528, 65440):
        raise AssertionError("Cycle-22 source certificate identity")
    return row


def source_weights() -> np.ndarray:
    row = source_row()
    clauses = list(map(int, row["source_clauses"].split(",")))
    values = list(map(int, row["weights"].split(",")))
    if not (len(clauses) == len(values) == 176):
        raise AssertionError("source support length")
    weights = np.zeros(coupled.P * coupled.C, dtype=np.int64)
    for clause, value in zip(clauses, values, strict=True):
        point = clause - width4.FIRST_TIME
        if not 0 <= point < len(weights) or value <= 0 or weights[point] != 0:
            raise AssertionError("source clause/value")
        weights[point] = value
    if int(weights.sum()) != 65528 or int(np.count_nonzero(weights)) != 176:
        raise AssertionError("source weight total")
    return weights


def target_rows() -> list[dict[str, str]]:
    rows = read_rows(TARGETS)
    keys = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows]
    if len(rows) != 60 or len(set(keys)) != 60 or any(row["status"] != "UNRESOLVED" for row in rows):
        raise AssertionError("Cycle-25 target boundary")
    return rows


def partition(allowed: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    order = sorted(range(coupled.K), key=lambda coordinate: (len(allowed[coordinate]), coordinate))
    blocks = tuple(sorted((tuple(sorted(order[:5])), tuple(sorted(order[5:9])), tuple(sorted(order[9:13])))))
    if sorted(map(len, blocks)) != [4, 4, 5] or sorted(coordinate for block in blocks for coordinate in block) != list(range(coupled.K)):
        raise AssertionError("bad 5+4+4 partition")
    return blocks


def partition_text(blocks: tuple[tuple[int, ...], ...]) -> str:
    return ",".join("-".join(map(str, block)) for block in blocks)


def option_count(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...]) -> int:
    result = 1
    for coordinate in block:
        result *= len(allowed[coordinate])
    if not 0 < result <= MAX_OPTIONS_PER_BLOCK:
        raise AssertionError("option cap")
    return result


def block_maximum(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...], active_coverage: np.ndarray, active_weights: np.ndarray) -> int:
    states = np.zeros((1, len(active_weights)), dtype=bool)
    for coordinate in block:
        choices = active_coverage[:, coordinate, list(allowed[coordinate])].T
        states = np.logical_or(states[:, None, :], choices[None, :, :]).reshape(-1, len(active_weights))
    if len(states) != option_count(block, allowed):
        raise AssertionError("option enumeration")
    return int((states @ active_weights).max())


def source_control() -> dict[str, object]:
    row = source_row()
    weights = source_weights()
    source_partition = parse_partition(row["partition"])
    coverage = width4.raw_coverage(direct.CNFS[4])
    allowed = direct.allowed_digits(coupled.read_bases()[4], 952)
    upper, maxima = direct.exact_capacity(source_partition, allowed, coverage, weights)
    if (int(weights.sum()), upper, maxima) != (65528, 65440, [7587, 12454, 21481, 23918]):
        raise AssertionError("source direct recovery")
    rows = target_rows()
    checked = []
    for row in rows:
        allowed = direct.allowed_digits(coupled.read_bases()[int(row["base_index"])], int(row["leaf_ordinal"]))
        checked.append(partition_text(partition(allowed)))
    return {"status": "PASS", "source": {"base_index": 4, "leaf_ordinal": 952, "support": 176, "W": 65528, "U": 65440, "margin": 88}, "targets": len(rows), "distinct_target_partitions": len(set(checked))}


def solve(job: tuple[int, int]) -> Result:
    base_index, ordinal = job
    weights = source_weights()
    active = np.flatnonzero(weights)
    coverage = width4.raw_coverage(direct.CNFS[base_index])[active]
    allowed = direct.allowed_digits(coupled.read_bases()[base_index], ordinal)
    blocks = partition(allowed)
    counts = [option_count(block, allowed) for block in blocks]
    maxima = [block_maximum(block, allowed, coverage, weights[active]) for block in blocks]
    upper = sum(maxima)
    status = "CERTIFIED_DEFICIT" if upper < int(weights.sum()) else "UNRESOLVED"
    detail = "fresh direct-CNF width-five transferred deficit" if status == "CERTIFIED_DEFICIT" else "source weight has no strict deficit on frozen partition"
    return Result(base_index, ordinal, status, partition_text(blocks), int(weights.sum()), upper, ",".join(map(str, maxima)), ",".join(map(str, counts)), detail)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    control = source_control()
    (OUT / "control.json").write_text(json.dumps(control, indent=2, sort_keys=True) + "\n")
    started = time.monotonic()
    with multiprocessing.Pool(processes=3) as pool:
        rows = pool.map(solve, [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in target_rows()], chunksize=1)
    (OUT / "results.tsv").write_text("\t".join(Result._fields) + "\n" + "\n".join("\t".join(map(str, row)) for row in rows) + "\n")
    counts = {status: sum(row.status == status for row in rows) for status in sorted({row.status for row in rows})}
    text = "targets=60 " + " ".join(f"{status.lower()}={count}" for status, count in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "result.txt").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
