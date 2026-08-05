#!/usr/bin/env python3
"""Cycle 18 conditional pair-choice Hall certificate search."""

from __future__ import annotations

import csv
import itertools
import multiprocessing
import os
from pathlib import Path
from typing import NamedTuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "discovery/out/cycle17-time-deficit"
OUT = ROOT / "discovery/out/cycle18-pair-choice"
BASES_PATH = ROOT / "discovery/out/cycle8-p199-strata.txt"
CNFS = {4: ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf", 3: ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf"}
K, P, C = 13, 199, 14
DENOMINATORS = (4096, 65536, 1048576, 16777216)


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    partition: str
    partition_rank: int
    objective: str
    source_clauses: str
    weights: str
    support: int
    denominator: int
    W: int
    U: int
    block_maxima: str
    partitions_tested: int
    detail: str


def read_bases() -> list[tuple[int, ...]]:
    return [tuple(map(int, line.split())) for line in BASES_PATH.read_text().splitlines() if line]


def time_signatures(path: Path) -> tuple[list[int], np.ndarray]:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    retained: dict[frozenset[int], int] = {}
    for clause_index, line in enumerate(lines[1:], 1):
        if 1197 <= clause_index <= 3982:
            retained.setdefault(frozenset(map(int, line.split()[:-1])), clause_index)
    ordered = sorted(retained.items(), key=lambda item: item[1])
    source = [clause_index for _, clause_index in ordered]
    coverage = np.zeros((len(ordered), K, C), dtype=bool)
    for index, (clause, _) in enumerate(ordered):
        for literal in clause:
            variable = literal - 1
            coverage[index, variable // C, variable % C] = True
    return source, coverage


def pair_list() -> list[tuple[int, int]]:
    return [(left, right) for left in range(K) for right in range(left + 1, K)]


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    result = {coordinate: True for coordinate in range(left)}
    result[left] = False
    result.update({coordinate: True for coordinate in range(left + 1, right)})
    result[right] = False
    return result


def allowed_digits(base: tuple[int, ...], ordinal: int) -> tuple[tuple[int, ...], ...]:
    pairs = pair_list()
    req2, req7 = requirements(pairs[ordinal // 78]), requirements(pairs[ordinal % 78])
    allowed = []
    for coordinate in range(K):
        digits = []
        for digit in range(C):
            residue = (base[coordinate] + P * digit) % C
            if coordinate in req2 and ((residue % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((residue % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        allowed.append(tuple(digits))
    return tuple(allowed)


def canonical(blocks: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    normalized = tuple(sorted(tuple(sorted(block)) for block in blocks))
    if sorted(coordinate for block in normalized for coordinate in block) != list(range(K)):
        raise AssertionError("not a coordinate partition")
    if any(len(block) not in (1, 2) for block in normalized):
        raise AssertionError("bad block size")
    return normalized


def complete(forced: tuple[tuple[int, int], ...]) -> tuple[tuple[int, ...], ...] | None:
    flat = [coordinate for pair in forced for coordinate in pair]
    if len(flat) != len(set(flat)):
        return None
    remaining = [coordinate for coordinate in range(K) if coordinate not in flat]
    blocks: list[tuple[int, ...]] = list(forced)
    while len(remaining) > 1:
        blocks.append((remaining.pop(0), remaining.pop(0)))
    if remaining:
        blocks.append((remaining[0],))
    return canonical(blocks)


def partitions(ordinal: int) -> list[tuple[tuple[int, ...], ...]]:
    pairs = pair_list()
    pair2, pair7 = pairs[ordinal // 78], pairs[ordinal % 78]
    candidates = [complete((pair2,)), complete((pair7,)), complete((pair2, pair7))]
    for singleton in range(K):
        order = [((singleton + offset) % K) for offset in range(1, K)]
        blocks = [(singleton,)] + [(order[index], order[index + 1]) for index in range(0, 12, 2)]
        candidates.append(canonical(blocks))
    candidates.extend(complete((pair,)) for pair in pairs)
    result = []
    seen = set()
    for candidate in candidates:
        if candidate is not None and candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
    if len(result) > 94:
        raise AssertionError("partition cap exceeded")
    return result


def block_options(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...]) -> list[tuple[int, ...]]:
    return list(itertools.product(*(allowed[coordinate] for coordinate in block)))


def option_vector(block: tuple[int, ...], option: tuple[int, ...], coverage: np.ndarray) -> np.ndarray:
    result = np.zeros(coverage.shape[0], dtype=bool)
    for coordinate, digit in zip(block, option, strict=True):
        result |= coverage[:, coordinate, digit]
    return result


def exact_capacity(
    partition: tuple[tuple[int, ...], ...], allowed: tuple[tuple[int, ...], ...],
    coverage: np.ndarray, integer_weights: np.ndarray,
) -> tuple[int, list[int]]:
    active = np.flatnonzero(integer_weights)
    maxima = []
    for block in partition:
        maxima.append(max(int(integer_weights[active][option_vector(block, option, coverage)[active]].sum()) for option in block_options(block, allowed)))
    return sum(maxima), maxima


def partition_text(partition: tuple[tuple[int, ...], ...]) -> str:
    return ",".join("-".join(map(str, block)) for block in partition)


def solve(job: tuple[int, int]) -> Result:
    base_index, ordinal = job
    bases = read_bases()
    source, coverage = time_signatures(CNFS[base_index])
    allowed = allowed_digits(bases[base_index], ordinal)
    best_objective = float("inf")
    best_partition = ""
    family = partitions(ordinal)
    n = len(source)
    for rank, partition in enumerate(family):
        vectors, block_ids = [], []
        for block_index, block in enumerate(partition):
            for option in block_options(block, allowed):
                vectors.append(option_vector(block, option, coverage))
                block_ids.append(block_index)
        left = csr_matrix(np.vstack(vectors).astype(float))
        rows = np.arange(len(vectors))
        right = csr_matrix((-np.ones(len(vectors)), (rows, np.asarray(block_ids))), shape=(len(vectors), len(partition)))
        a_ub = hstack((left, right), format="csr")
        c = np.concatenate((np.zeros(n), np.ones(len(partition))))
        a_eq = csr_matrix((np.ones(n), (np.zeros(n, dtype=int), np.arange(n))), shape=(1, n + len(partition)))
        solved = linprog(c, A_ub=a_ub, b_ub=np.zeros(len(vectors)), A_eq=a_eq, b_eq=np.array([1.0]), bounds=(0, None), method="highs-ds", options={"presolve": True})
        if solved.status != 0:
            return Result(base_index, ordinal, "LP_ERROR", partition_text(partition), rank, "nan", "", "", 0, 0, 0, 0, "", rank + 1, solved.message.replace("\t", " "))
        if solved.fun < best_objective:
            best_objective, best_partition = float(solved.fun), partition_text(partition)
        if solved.fun >= 1.0 - 1e-9:
            continue
        for denominator in DENOMINATORS:
            integer_weights = np.rint(solved.x[:n] * denominator).astype(np.int64)
            integer_weights[integer_weights < 0] = 0
            active = np.flatnonzero(integer_weights)
            if not 0 < len(active) <= 256:
                continue
            total = int(integer_weights.sum())
            upper, maxima = exact_capacity(partition, allowed, coverage, integer_weights)
            if upper < total:
                return Result(
                    base_index, ordinal, "CERTIFIED_DEFICIT", partition_text(partition), rank,
                    f"{solved.fun:.17g}", ",".join(str(source[index]) for index in active),
                    ",".join(str(int(integer_weights[index])) for index in active), len(active), denominator,
                    total, upper, ",".join(map(str, maxima)), rank + 1, "exact integerized pair-choice deficit",
                )
    return Result(base_index, ordinal, "UNRESOLVED", best_partition, -1, f"{best_objective:.17g}", "", "", 0, 0, 0, 0, "", len(family), "no frozen partition produced exact deficit")


def targets() -> list[tuple[int, int]]:
    with (OLD / "results.tsv").open(newline="") as handle:
        bounded = list(csv.DictReader(handle, delimiter="\t"))
    with (OLD / "lp-results.tsv").open(newline="") as handle:
        lp = list(csv.DictReader(handle, delimiter="\t"))
    old_uncovered = {(int(row["base_index"]), int(row["leaf_ordinal"])) for row in bounded if row["status"] == "UNCOVERED"}
    result = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in lp if row["status"] == "NO_LP_DEFICIT"]
    expected_order = sorted(result, key=lambda item: ((0 if item[0] == 4 else 1), item[1]))
    if len(result) != 80 or result != expected_order or any(item not in old_uncovered for item in result):
        raise AssertionError("Cycle-17 target boundary mismatch")
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = targets()
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, jobs)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "results.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    by_base = {base: sum(row.status == "CERTIFIED_DEFICIT" and row.base_index == base for row in results) for base in (4, 3)}
    summary = "rows=80 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items()) + f" base4={by_base[4]} base3={by_base[3]}"
    (OUT / "result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
