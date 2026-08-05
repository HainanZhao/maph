#!/usr/bin/env python3
"""Cycle 24 exact CRT/Ramanujan class control and capacity-dual search."""

from __future__ import annotations

import csv
import itertools
import math
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
import lrc_adaptive_width_four_oracle as prior_oracle
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle24-crt-fourier-class"
PRIOR = ROOT / "discovery/out/cycle23-adaptive-width-four/oracle.tsv"
P, C, K = cycle21.P, cycle21.C, cycle21.K
CLASSES = tuple((epsilon, divisor) for epsilon in (0, 1) for divisor in (1, 2, 7, 14))
CLASS_INDEX = {key: index for index, key in enumerate(CLASSES)}
DENOMINATORS = (4096, 65536, 1048576, 16777216)
SEPARATION_TOLERANCE = 1e-9
MAX_SEPARATION_ROUNDS = 512
STAGE_SECONDS = 3000


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    oracle_score: int
    partition: str
    objective: str
    class_weights: str
    denominator: int
    W: int
    U: int
    block_maxima: str
    separation_rounds: int
    detail: str


def class_of_time(point: int) -> tuple[int, int]:
    return (0 if point % P == 0 else 1, math.gcd(point % C, C))


def class_indices() -> np.ndarray:
    result = np.asarray([CLASS_INDEX[class_of_time(point)] for point in range(P * C)], dtype=np.int8)
    if result.shape != (P * C,):
        raise AssertionError("CRT class shape")
    return result


def class_cardinalities() -> np.ndarray:
    indices = class_indices()
    counts = np.bincount(indices, minlength=len(CLASSES)).astype(np.int64)
    if tuple(counts) != (6, 6, 1, 1, 1188, 1188, 198, 198):
        raise AssertionError(f"CRT class cardinalities {tuple(counts)}")
    return counts


def mobius(squarefree_number: int) -> int:
    factors = 0
    trial = 2
    value = squarefree_number
    while trial * trial <= value:
        if value % trial == 0:
            value //= trial
            if value % trial == 0:
                return 0
            factors += 1
        trial += 1
    if value > 1:
        factors += 1
    return -1 if factors % 2 else 1


def ramanujan_sum(modulus: int, value: int) -> int:
    common = math.gcd(modulus, value)
    return sum(divisor * mobius(modulus // divisor) for divisor in range(1, common + 1) if common % divisor == 0)


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    previous = 1
    sign = 1
    for pivot_column in range(len(work) - 1):
        pivot_row = next((row for row in range(pivot_column, len(work)) if work[row][pivot_column]), None)
        if pivot_row is None:
            return 0
        if pivot_row != pivot_column:
            work[pivot_column], work[pivot_row] = work[pivot_row], work[pivot_column]
            sign *= -1
        pivot = work[pivot_column][pivot_column]
        for row in range(pivot_column + 1, len(work)):
            for column in range(pivot_column + 1, len(work)):
                numerator = work[row][column] * pivot - work[row][pivot_column] * work[pivot_column][column]
                work[row][column] = numerator // previous
        previous = pivot
        for row in range(pivot_column + 1, len(work)):
            work[row][pivot_column] = 0
    return sign * work[-1][-1]


def ramanujan_basis() -> list[list[int]]:
    rows = []
    for epsilon, divisor in CLASSES:
        alpha_basis = (1, 198 if epsilon == 0 else -1)
        beta = 0 if divisor == 14 else divisor
        beta_basis = tuple(ramanujan_sum(modulus, beta) for modulus in (1, 2, 7, 14))
        rows.append([left * right for left in alpha_basis for right in beta_basis])
    if bareiss_determinant(rows) == 0:
        raise AssertionError("Ramanujan class basis is singular")
    return rows


def control() -> dict[str, object]:
    cardinalities = class_cardinalities()
    base = cycle21.read_bases()[4]
    coverage = width4.raw_coverage(direct.CNFS[4])
    for point in range(P * C):
        for coordinate in range(K):
            for digit in range(C):
                speed = base[coordinate] + P * digit
                if bool(coverage[point, coordinate, digit]) != cycle21.crt_is_bad(K, P, C, speed, point):
                    raise AssertionError(f"direct/CRT mismatch {point},{coordinate},{digit}")
    return {"status": "PASS", "cardinalities": list(map(int, cardinalities)), "basis_determinant": bareiss_determinant(ramanujan_basis())}


def targets() -> list[dict[str, str]]:
    with PRIOR.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 60 or any(row["status"] != "NEED_LP" for row in rows):
        raise AssertionError("Cycle-24 target boundary")
    return rows


def class_counts(mask: np.ndarray, indices: np.ndarray) -> np.ndarray:
    return np.bincount(indices[mask], minlength=len(CLASSES)).astype(np.int64)


def exact_savings(allowed, coverage, indices):
    singleton = {}
    for coordinate in range(K):
        singleton[coordinate] = np.maximum.reduce([
            class_counts(coverage[:, coordinate, digit], indices)
            for digit in allowed[coordinate]
        ])
    savings = {}
    for left in range(K):
        for right in range(left + 1, K):
            maximum = np.maximum.reduce([
                class_counts(coverage[:, left, first] | coverage[:, right, second], indices)
                for first in allowed[left] for second in allowed[right]
            ])
            value = singleton[left] + singleton[right] - maximum
            if (value < 0).any():
                raise AssertionError("negative class pair saving")
            savings[left, right] = value
    return savings


def triple_partitions(items: tuple[int, ...]):
    first, rest = items[0], items[1:]
    for pair in itertools.combinations(rest, 2):
        first_block = tuple(sorted((first, *pair)))
        remaining = tuple(item for item in rest if item not in pair)
        second = remaining[0]
        for second_pair in itertools.combinations(remaining[1:], 2):
            second_block = tuple(sorted((second, *second_pair)))
            third_block = tuple(item for item in remaining[1:] if item not in second_pair)
            yield tuple(sorted((first_block, second_block, third_block)))


def select_partition(savings):
    block_scores = {
        block: sum((savings[tuple(sorted(pair))] for pair in itertools.combinations(block, 2)), np.zeros(len(CLASSES), dtype=np.int64))
        for width in (3, 4) for block in itertools.combinations(range(K), width)
    }
    best_score, best_partition, candidates = -1, None, 0
    for four in itertools.combinations(range(K), 4):
        remainder = tuple(item for item in range(K) if item not in four)
        for triples in triple_partitions(remainder):
            partition = tuple(sorted((four, *triples)))
            score = int((block_scores[four] + sum((block_scores[block] for block in triples), np.zeros(len(CLASSES), dtype=np.int64))).sum())
            candidates += 1
            if score > best_score or (score == best_score and (best_partition is None or partition < best_partition)):
                best_score, best_partition = score, partition
    if candidates != 200_200 or best_partition is None:
        raise AssertionError("class partition census")
    return best_score, best_partition


def option_counts(block, allowed, coverage, indices):
    options = list(itertools.product(*(allowed[coordinate] for coordinate in block)))
    rows = np.empty((len(options), len(CLASSES)), dtype=np.int64)
    for row, option in enumerate(options):
        mask = np.zeros(len(coverage), dtype=bool)
        for coordinate, digit in zip(block, option, strict=True):
            mask |= coverage[:, coordinate, digit]
        rows[row] = class_counts(mask, indices)
    return rows


def solve_by_separation(block_rows, cardinalities, deadline):
    active = [(block, 0) for block in range(len(block_rows))]
    active_set = set(active)
    for round_number in range(1, MAX_SEPARATION_ROUNDS + 1):
        if time.monotonic() >= deadline:
            return None, round_number, "wall cap before class LP"
        left = csr_matrix(np.vstack([block_rows[block][option] for block, option in active]), dtype=float)
        row_indices = np.arange(len(active))
        block_ids = np.asarray([block for block, _ in active])
        right = csr_matrix((-np.ones(len(active)), (row_indices, block_ids)), shape=(len(active), len(block_rows)))
        a_ub = hstack((left, right), format="csr")
        objective = np.concatenate((np.zeros(len(CLASSES)), np.ones(len(block_rows))))
        a_eq = csr_matrix((cardinalities.astype(float), (np.zeros(len(CLASSES), dtype=int), np.arange(len(CLASSES)))), shape=(1, len(CLASSES) + len(block_rows)))
        solved = linprog(objective, A_ub=a_ub, b_ub=np.zeros(len(active)), A_eq=a_eq, b_eq=np.array([1.0]), bounds=(0, None), method="highs-ds", options={"presolve": True, "time_limit": max(1.0, deadline - time.monotonic())})
        if solved.status != 0:
            if solved.status == 1 and time.monotonic() >= deadline:
                return None, round_number, "wall cap in class LP"
            return None, round_number, solved.message.replace("\t", " ")
        weights = solved.x[:len(CLASSES)]
        violations = []
        for block, rows in enumerate(block_rows):
            option = int(np.argmax(rows @ weights))
            if float(rows[option] @ weights) > float(solved.x[len(CLASSES) + block]) + SEPARATION_TOLERANCE:
                violations.append((block, option))
        if not violations:
            return solved, round_number, "exact class LP separation converged"
        for item in violations:
            if item in active_set:
                return None, round_number, "already-active violated class constraint"
            active.append(item)
            active_set.add(item)
    return None, MAX_SEPARATION_ROUNDS, "separation-round cap"


def partition_text(partition):
    return ",".join("-".join(map(str, block)) for block in partition)


def solve(job: tuple[dict[str, str], float]) -> Result:
    row, deadline = job
    base_index, ordinal = int(row["base_index"]), int(row["leaf_ordinal"])
    if time.monotonic() >= deadline:
        return Result(base_index, ordinal, "CAP", 0, "", "nan", "", 0, 0, 0, "", 0, "wall cap before target")
    base = cycle21.read_bases()[base_index]
    allowed = direct.allowed_digits(base, ordinal)
    coverage = width4.raw_coverage(direct.CNFS[base_index])
    indices, cardinalities = class_indices(), class_cardinalities()
    score, partition = select_partition(exact_savings(allowed, coverage, indices))
    rows = [option_counts(block, allowed, coverage, indices) for block in partition]
    solved, rounds, detail = solve_by_separation(rows, cardinalities, deadline)
    text = partition_text(partition)
    if solved is None:
        status = "CAP" if detail.startswith("wall cap") or detail == "separation-round cap" else "LP_ERROR"
        return Result(base_index, ordinal, status, score, text, "nan", "", 0, 0, 0, "", rounds, detail)
    if solved.fun < 1.0 - 1e-9:
        for denominator in DENOMINATORS:
            values = np.rint(solved.x[:len(CLASSES)] * denominator).astype(np.int64)
            if not values.any():
                continue
            total = int(cardinalities @ values)
            maxima = [int((block @ values).max()) for block in rows]
            upper = sum(maxima)
            if upper < total:
                return Result(base_index, ordinal, "CERTIFIED_DEFICIT", score, text, f"{solved.fun:.17g}", ",".join(map(str, values)), denominator, total, upper, ",".join(map(str, maxima)), rounds, "exact integer CRT-class deficit")
    return Result(base_index, ordinal, "UNRESOLVED", score, text, f"{solved.fun:.17g}", ",".join(f"{value:.17g}" for value in solved.x[:len(CLASSES)]), 0, 0, 0, "", rounds, "class LP did not integerize strictly")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checked = control()
    (OUT / "control.json").write_text(__import__("json").dumps(checked, indent=2, sort_keys=True) + "\n")
    started = time.monotonic()
    deadline = started + STAGE_SECONDS
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, [(row, deadline) for row in targets()], chunksize=1)
    lines = ["\t".join(Result._fields)] + ["\t".join(map(str, result)) for result in results]
    (OUT / "results.tsv").write_text("\n".join(lines) + "\n")
    counts = {status: sum(result.status == status for result in results) for status in sorted({result.status for result in results})}
    summary = "targets=60 " + " ".join(f"{status.lower()}={count}" for status, count in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
