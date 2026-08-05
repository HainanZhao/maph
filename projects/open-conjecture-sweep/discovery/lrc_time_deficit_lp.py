#!/usr/bin/env python3
"""Cycle 17 deterministic LP proposal and exact integerization."""

from __future__ import annotations

import csv
import multiprocessing
import os
from pathlib import Path
from typing import NamedTuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle17-time-deficit"
BASES_PATH = ROOT / "discovery/out/cycle8-p199-strata.txt"
CNFS = {
    4: ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf",
    3: ROOT / "discovery/out/cycle11-certified-sat/p199/003.cnf",
}
K, P, C = 13, 199, 14
DENOMINATORS = (4096, 65536, 1048576, 16777216)


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    objective: str
    source_clauses: str
    weights: str
    support: int
    denominator: int
    W: int
    U: int
    coordinate_maxima: str
    detail: str


def read_bases() -> list[tuple[int, ...]]:
    return [tuple(map(int, line.split())) for line in BASES_PATH.read_text().splitlines() if line]


def time_signatures(path: Path) -> list[tuple[int, tuple[frozenset[int], ...]]]:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    retained: dict[frozenset[int], int] = {}
    for clause_index, line in enumerate(lines[1:], 1):
        if 1197 <= clause_index <= 3982:
            values = tuple(map(int, line.split()))[:-1]
            retained.setdefault(frozenset(values), clause_index)
    result = []
    for clause, clause_index in sorted(retained.items(), key=lambda item: item[1]):
        masks = tuple(frozenset((literal - 1) % C for literal in clause if (literal - 1) // C == coordinate) for coordinate in range(K))
        result.append((clause_index, masks))
    return result


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


def exact_capacity(
    allowed: tuple[tuple[int, ...], ...],
    signatures: list[tuple[int, tuple[frozenset[int], ...]]],
    integer_weights: np.ndarray,
) -> tuple[int, list[int]]:
    active = np.flatnonzero(integer_weights)
    maxima = []
    for coordinate, digits in enumerate(allowed):
        maxima.append(max(sum(int(integer_weights[index]) for index in active if digit in signatures[index][1][coordinate]) for digit in digits))
    return sum(maxima), maxima


def solve(job: tuple[int, int]) -> Result:
    base_index, ordinal = job
    bases = read_bases()
    signatures = time_signatures(CNFS[base_index])
    allowed = allowed_digits(bases[base_index], ordinal)
    n = len(signatures)
    row_indices, col_indices, data = [], [], []
    constraint = 0
    for coordinate, digits in enumerate(allowed):
        for digit in digits:
            for index, (_, masks) in enumerate(signatures):
                if digit in masks[coordinate]:
                    row_indices.append(constraint)
                    col_indices.append(index)
                    data.append(1.0)
            row_indices.append(constraint)
            col_indices.append(n + coordinate)
            data.append(-1.0)
            constraint += 1
    a_ub = csr_matrix((data, (row_indices, col_indices)), shape=(constraint, n + K))
    c = np.concatenate((np.zeros(n), np.ones(K)))
    a_eq = csr_matrix((np.ones(n), (np.zeros(n, dtype=int), np.arange(n))), shape=(1, n + K))
    solved = linprog(c, A_ub=a_ub, b_ub=np.zeros(constraint), A_eq=a_eq, b_eq=np.array([1.0]), bounds=(0, None), method="highs-ds", options={"presolve": True})
    objective = "nan" if solved.fun is None else f"{solved.fun:.17g}"
    if solved.status != 0:
        return Result(base_index, ordinal, "LP_ERROR", objective, "", "", 0, 0, 0, 0, "", solved.message.replace("\t", " "))
    if solved.fun >= 1.0 - 1e-9:
        return Result(base_index, ordinal, "NO_LP_DEFICIT", objective, "", "", 0, 0, 0, 0, "", "optimum not below frozen margin")
    for denominator in DENOMINATORS:
        integer_weights = np.rint(solved.x[:n] * denominator).astype(np.int64)
        integer_weights[integer_weights < 0] = 0
        active = np.flatnonzero(integer_weights)
        if not 0 < len(active) <= 192:
            continue
        total = int(integer_weights.sum())
        upper, maxima = exact_capacity(allowed, signatures, integer_weights)
        if upper < total:
            return Result(
                base_index, ordinal, "CERTIFIED_DEFICIT", objective,
                ",".join(str(signatures[index][0]) for index in active),
                ",".join(str(int(integer_weights[index])) for index in active),
                len(active), denominator, total, upper, ",".join(map(str, maxima)),
                "exact integerized weighted deficit",
            )
    return Result(base_index, ordinal, "INTEGERIZATION_FAILED", objective, "", "", 0, 0, 0, 0, "", "no frozen denominator produced exact U<W")


def main() -> None:
    with (OUT / "results.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    jobs = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in rows if row["status"] == "UNCOVERED"]
    if len(jobs) != 477 or jobs != sorted(jobs, key=lambda item: ((0 if item[0] == 4 else 1), item[1])):
        raise AssertionError("frozen uncovered-row set mismatch")
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, jobs)
    header = Result._fields
    lines = ["\t".join(header)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "lp-results.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(row.status == status for row in results) for status in sorted({row.status for row in results})}
    summary = "rows=477 " + " ".join(f"{key.lower()}={value}" for key, value in counts.items())
    (OUT / "lp.result").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
