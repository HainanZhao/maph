#!/usr/bin/env python3
"""Cycle 21 exact coupled CRT incidence and width-three deficit search."""

from __future__ import annotations

import csv
import hashlib
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
import lrc_certified_sat as cycle11

OUT = ROOT / "discovery/out/cycle21-coupled-incidence"
P47_INPUT = ROOT / "discovery/out/partitioned-k6.txt"
P199_INPUT = ROOT / "discovery/out/cycle8-p199-strata.txt"
CONTROL_RESULTS = ROOT / "discovery/out/cycle11-certified-sat/controls.tsv"
P199_RESULTS = ROOT / "discovery/out/cycle11-certified-sat/p199.tsv"
CYCLE17 = ROOT / "discovery/out/cycle17-time-deficit/lp-results.tsv"
CYCLE18 = ROOT / "discovery/out/cycle18-pair-choice/results.tsv"
K, P, C = 13, 199, 14
DENOMINATORS = (4096, 65536, 1048576, 16777216)
AGGREGATE_SECONDS = 3500


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


def crt_is_bad(k: int, p: int, c: int, speed: int, point: int) -> bool:
    if c != k + 1 or math.gcd(p, c) != 1:
        raise AssertionError("CRT interface hypotheses failed")
    alpha, beta = point % p, point % c
    xp = (alpha * (speed % p)) % p
    local = ((speed % c) * beta) % c
    return local == xp % c or (xp != 0 and local == (xp - p) % c)


def encode_crt(base: tuple[int, ...], p: int, c: int) -> cycle11.Formula:
    k = len(base)
    q = p * c
    factors = cycle11.prime_factors(c)
    x_variables = k * c

    def x(coordinate: int, digit: int) -> int:
        return 1 + coordinate * c + digit

    def y(factor_index: int, coordinate: int) -> int:
        return x_variables + 1 + factor_index * k + coordinate

    clauses: list[tuple[int, ...]] = []
    for coordinate in range(k):
        choices = tuple(x(coordinate, digit) for digit in range(c))
        clauses.append(choices)
        clauses.extend((-left, -right) for left, right in itertools.combinations(choices, 2))
    for point in range(q):
        clauses.append(tuple(
            x(coordinate, digit)
            for coordinate in range(k)
            for digit in range(c)
            if crt_is_bad(k, p, c, base[coordinate] + p * digit, point)
        ))
    for factor_index, factor in enumerate(factors):
        for coordinate in range(k):
            divisible = tuple(
                x(coordinate, digit)
                for digit in range(c)
                if (base[coordinate] + p * digit) % factor == 0
            )
            if not divisible:
                raise AssertionError("missing divisible digit")
            clauses.extend((-literal, y(factor_index, coordinate)) for literal in divisible)
            clauses.append((-y(factor_index, coordinate), *divisible))
        for selected in itertools.combinations(range(k), k - 1):
            clauses.append(tuple(-y(factor_index, coordinate) for coordinate in selected))
    if any(not clause for clause in clauses):
        raise AssertionError("CRT encoding generated an empty input clause")
    return cycle11.Formula(x_variables + len(factors) * k, tuple(clauses), k, p, c)


def dimacs_sha256(formula: cycle11.Formula) -> str:
    lines = [f"p cnf {formula.variables} {len(formula.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in formula.clauses)
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def read_expected(path: Path) -> dict[tuple[str, int], str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            (row["family"], int(row["index"])): row["cnf_sha256"]
            for row in csv.DictReader(handle, delimiter="\t")
        }


def interface_controls() -> list[tuple[str, int, int, int, int, str]]:
    expected = read_expected(CONTROL_RESULTS)
    expected.update(read_expected(P199_RESULTS))
    jobs = cycle11.h11_jobs()
    jobs += cycle11.file_jobs("p47", P47_INPUT, 53, 47, 7, 6)
    p199_jobs = cycle11.file_jobs("p199", P199_INPUT, 100, 199, 14, 13)
    jobs += [p199_jobs[3], p199_jobs[4]]
    rows = []
    comparisons = 0
    for job in jobs:
        direct = cycle11.encode(job.base, job.p, job.c)
        local = encode_crt(job.base, job.p, job.c)
        if direct != local:
            raise AssertionError(f"direct/CRT formula mismatch: {job.family} {job.index}")
        digest = dimacs_sha256(local)
        if digest != expected[(job.family, job.index)]:
            raise AssertionError(f"frozen CNF hash mismatch: {job.family} {job.index}")
        count = len(job.base) * job.c * job.p * job.c
        comparisons += count
        rows.append((job.family, job.index, job.p, job.c, count, digest))
    if len(rows) != 295 or comparisons != 1_873_178:
        raise AssertionError("interface census mismatch")
    return rows


def read_bases() -> list[tuple[int, ...]]:
    return [tuple(map(int, line.split())) for line in P199_INPUT.read_text().splitlines() if line]


def pair_list() -> list[tuple[int, int]]:
    return [(left, right) for left in range(K) for right in range(left + 1, K)]


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    result = {coordinate: True for coordinate in range(left)}
    result[left] = False
    result.update({coordinate: True for coordinate in range(left + 1, right)})
    result[right] = False
    return result


def witness_pairs(ordinal: int) -> tuple[tuple[int, int], tuple[int, int]]:
    pairs = pair_list()
    return pairs[ordinal // 78], pairs[ordinal % 78]


def allowed_digits(base: tuple[int, ...], ordinal: int) -> tuple[tuple[int, ...], ...]:
    pair2, pair7 = witness_pairs(ordinal)
    req2, req7 = requirements(pair2), requirements(pair7)
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
        if not digits:
            raise AssertionError("empty allowed-digit block")
        allowed.append(tuple(digits))
    return tuple(allowed)


def canonical(blocks: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    normalized = tuple(sorted(tuple(sorted(block)) for block in blocks))
    if sorted(coordinate for block in normalized for coordinate in block) != list(range(K)):
        raise AssertionError("not a coordinate partition")
    if any(len(block) not in (1, 2, 3) for block in normalized):
        raise AssertionError("bad block size")
    return normalized


def complete(forced: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...] | None:
    flat = [coordinate for block in forced for coordinate in block]
    if len(flat) != len(set(flat)):
        return None
    remaining = [coordinate for coordinate in range(K) if coordinate not in flat]
    blocks: list[tuple[int, ...]] = list(forced)
    while len(remaining) > 2:
        blocks.append(tuple(remaining[:3]))
        del remaining[:3]
    if remaining:
        blocks.append(tuple(remaining))
    return canonical(blocks)


def partitions(ordinal: int) -> list[tuple[tuple[int, ...], ...]]:
    candidates: list[tuple[tuple[int, ...], ...] | None] = []
    for shift in range(K):
        order = tuple((shift + offset) % K for offset in range(K))
        candidates.append(canonical([
            order[0:3], order[3:6], order[6:9], order[9:12], order[12:13]
        ]))
    pair2, pair7 = witness_pairs(ordinal)
    for pair in (pair2, pair7):
        for third in range(K):
            if third not in pair:
                candidates.append(complete((tuple(sorted((*pair, third))),)))
    union = tuple(sorted(set(pair2) | set(pair7)))
    if len(union) <= 3:
        candidates.append(complete((union,)))
    else:
        candidates.append(complete((pair2, pair7)))
    result = []
    seen = set()
    for candidate in candidates:
        if candidate is not None and candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
    if len(result) > 36:
        raise AssertionError("partition cap exceeded")
    return result


def time_signatures(base: tuple[int, ...]) -> tuple[list[int], np.ndarray]:
    formula = encode_crt(base, P, C)
    first = K * (1 + C * (C - 1) // 2)
    time_clauses = formula.clauses[first:first + P * C]
    if len(time_clauses) != P * C:
        raise AssertionError("time-clause slice mismatch")
    retained: dict[frozenset[int], int] = {}
    for offset, clause in enumerate(time_clauses):
        retained.setdefault(frozenset(clause), first + 1 + offset)
    ordered = sorted(retained.items(), key=lambda item: item[1])
    source = [clause_index for _, clause_index in ordered]
    coverage = np.zeros((len(ordered), K, C), dtype=bool)
    for index, (clause, _) in enumerate(ordered):
        for literal in clause:
            variable = literal - 1
            coverage[index, variable // C, variable % C] = True
    return source, coverage


def block_options(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...]):
    return itertools.product(*(allowed[coordinate] for coordinate in block))


def option_vector(
    block: tuple[int, ...], option: tuple[int, ...], coverage: np.ndarray
) -> np.ndarray:
    result = np.zeros(coverage.shape[0], dtype=bool)
    for coordinate, digit in zip(block, option, strict=True):
        result |= coverage[:, coordinate, digit]
    return result


def exact_capacity(
    partition: tuple[tuple[int, ...], ...],
    allowed: tuple[tuple[int, ...], ...],
    coverage: np.ndarray,
    weights: np.ndarray,
) -> tuple[int, list[int]]:
    active = np.flatnonzero(weights)
    maxima = []
    active_weights = weights[active]
    for block in partition:
        maximum = 0
        for option in block_options(block, allowed):
            value = int(active_weights[option_vector(block, option, coverage)[active]].sum())
            maximum = max(maximum, value)
        maxima.append(maximum)
    return sum(maxima), maxima


def partition_text(partition: tuple[tuple[int, ...], ...]) -> str:
    return ",".join("-".join(map(str, block)) for block in partition)


def targets() -> list[tuple[int, int]]:
    with CYCLE18.open(newline="", encoding="utf-8") as handle:
        pair_rows = list(csv.DictReader(handle, delimiter="\t"))
    with CYCLE17.open(newline="", encoding="utf-8") as handle:
        single_rows = list(csv.DictReader(handle, delimiter="\t"))
    result = [
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in pair_rows if row["status"] == "UNRESOLVED"
    ]
    expected_order = sorted(result, key=lambda item: (0 if item[0] == 4 else 1, item[1]))
    prior = {
        (int(row["base_index"]), int(row["leaf_ordinal"]))
        for row in single_rows if row["status"] == "NO_LP_DEFICIT"
    }
    if len(result) != 76 or result != expected_order or any(item not in prior for item in result):
        raise AssertionError("Cycle-21 target boundary mismatch")
    return result


def solve(job: tuple[int, int, float]) -> Result:
    base_index, ordinal, deadline = job
    if time.monotonic() >= deadline:
        return Result(base_index, ordinal, "CAP", "", -1, "nan", "", "", 0, 0, 0, 0, "", 0, "aggregate wall cap before leaf")
    base = read_bases()[base_index]
    source, coverage = time_signatures(base)
    allowed = allowed_digits(base, ordinal)
    family = partitions(ordinal)
    best_objective = float("inf")
    best_partition = ""
    n = len(source)
    for rank, partition in enumerate(family):
        if time.monotonic() >= deadline:
            return Result(base_index, ordinal, "CAP", best_partition, -1, f"{best_objective:.17g}", "", "", 0, 0, 0, 0, "", rank, "aggregate wall cap during leaf")
        vectors: list[np.ndarray] = []
        block_ids: list[int] = []
        for block_index, block in enumerate(partition):
            for option in block_options(block, allowed):
                vectors.append(option_vector(block, option, coverage))
                block_ids.append(block_index)
        left = csr_matrix(np.vstack(vectors).astype(float))
        rows = np.arange(len(vectors))
        right = csr_matrix(
            (-np.ones(len(vectors)), (rows, np.asarray(block_ids))),
            shape=(len(vectors), len(partition)),
        )
        a_ub = hstack((left, right), format="csr")
        objective = np.concatenate((np.zeros(n), np.ones(len(partition))))
        a_eq = csr_matrix(
            (np.ones(n), (np.zeros(n, dtype=int), np.arange(n))),
            shape=(1, n + len(partition)),
        )
        remaining = max(1.0, deadline - time.monotonic())
        solved = linprog(
            objective,
            A_ub=a_ub,
            b_ub=np.zeros(len(vectors)),
            A_eq=a_eq,
            b_eq=np.array([1.0]),
            bounds=(0, None),
            method="highs-ds",
            options={"presolve": True, "time_limit": remaining},
        )
        if solved.status == 1 and time.monotonic() >= deadline:
            return Result(base_index, ordinal, "CAP", partition_text(partition), rank, "nan", "", "", 0, 0, 0, 0, "", rank + 1, "aggregate wall cap in LP")
        if solved.status != 0:
            return Result(base_index, ordinal, "LP_ERROR", partition_text(partition), rank, "nan", "", "", 0, 0, 0, 0, "", rank + 1, solved.message.replace("\t", " "))
        if solved.fun < best_objective:
            best_objective = float(solved.fun)
            best_partition = partition_text(partition)
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
                    ",".join(str(int(integer_weights[index])) for index in active), len(active),
                    denominator, total, upper, ",".join(map(str, maxima)), rank + 1,
                    "exact integerized width-three coupled-incidence deficit",
                )
    return Result(base_index, ordinal, "UNRESOLVED", best_partition, -1, f"{best_objective:.17g}", "", "", 0, 0, 0, 0, "", len(family), "no frozen partition produced exact deficit")


def write_interface(rows: list[tuple[str, int, int, int, int, str]]) -> None:
    lines = ["family\tindex\tp\tc\tpredicate_comparisons\tcnf_sha256"]
    lines.extend("\t".join(map(str, row)) for row in rows)
    (OUT / "interface.tsv").write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    rows = interface_controls()
    write_interface(rows)
    jobs0 = targets()
    deadline = started + AGGREGATE_SECONDS
    jobs = [(base, ordinal, deadline) for base, ordinal in jobs0]
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(solve, jobs, chunksize=1)
    lines = ["\t".join(Result._fields)]
    lines.extend("\t".join(map(str, row)) for row in results)
    (OUT / "results.tsv").write_text("\n".join(lines) + "\n")
    statuses = sorted({row.status for row in results})
    counts = {status: sum(row.status == status for row in results) for status in statuses}
    by_base = {
        base: sum(row.status == "CERTIFIED_DEFICIT" and row.base_index == base for row in results)
        for base in (4, 3)
    }
    elapsed = time.monotonic() - started
    summary = (
        "interface_instances=295 interface_comparisons=1873178 targets=76 "
        + " ".join(f"{key.lower()}={value}" for key, value in counts.items())
        + f" base4={by_base[4]} base3={by_base[3]} wall_seconds={elapsed:.6f}"
    )
    (OUT / "result.txt").write_text(summary + "\n")
    print(summary)


if __name__ == "__main__":
    main()
