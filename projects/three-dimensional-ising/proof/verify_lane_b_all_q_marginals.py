#!/usr/bin/env python3
"""Exact all-q TT application: every single-handle Walsh marginal.

The construction is deliberately finite-field and is a validation of the
general TT contraction algorithm.  It does not use the Arf sum and it does
not compare against ordinary transfer for a single partition function.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import _case  # noqa: E402
from proof.verify_lane_b_universal_canonical_ranks import _canonical_reindex  # noqa: E402
from proof.verify_lane_b_width_scaling import (  # noqa: E402
    _compile,
    _edge_payload,
    _f_values_from_walsh,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
    universal_embedding_genus,
)


PRIMES = (1_000_000_007, 1_000_000_009)


def _inverse(matrix: list[list[int]], prime: int) -> list[list[int]]:
    n = len(matrix)
    work = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        scale = pow(work[column][column], prime - 2, prime)
        work[column] = [value * scale % prime for value in work[column]]
        for row in range(n):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[column])
            ]
    return [row[n:] for row in work]


def _rank_factor(matrix: list[list[int]], prime: int) -> tuple[list[list[int]], list[list[int]]]:
    """Return exact M=C D with C formed from pivot columns."""
    row_count = len(matrix)
    column_count = len(matrix[0])
    echelon = [row[:] for row in matrix]
    pivot_columns = []
    pivot_rows = []
    rank = 0
    for column in range(column_count):
        pivot = next((row for row in range(rank, row_count) if echelon[row][column]), None)
        if pivot is None:
            continue
        echelon[rank], echelon[pivot] = echelon[pivot], echelon[rank]
        pivot_rows.append(pivot)
        pivot_columns.append(column)
        inverse = pow(echelon[rank][column], prime - 2, prime)
        for row in range(rank + 1, row_count):
            factor = echelon[row][column] * inverse % prime
            if factor:
                echelon[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(echelon[row], echelon[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    columns = [[matrix[row][column] for column in pivot_columns] for row in range(row_count)]
    # Find independent rows of C afresh; row swaps above refer to a changing
    # matrix and are not suitable as row indices of the original C.
    transposed = [[columns[row][column] for row in range(row_count)] for column in range(rank)]
    row_echelon = [row[:] for row in transposed]
    selected_rows = []
    rr = 0
    for column in range(row_count):
        pivot = next((row for row in range(rr, rank) if row_echelon[row][column]), None)
        if pivot is None:
            continue
        row_echelon[rr], row_echelon[pivot] = row_echelon[pivot], row_echelon[rr]
        selected_rows.append(column)
        inv = pow(row_echelon[rr][column], prime - 2, prime)
        for row in range(rr + 1, rank):
            factor = row_echelon[row][column] * inv % prime
            if factor:
                row_echelon[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(row_echelon[row], row_echelon[rr])
                ]
        rr += 1
        if rr == rank:
            break
    square = [[columns[row][column] for column in range(rank)] for row in selected_rows]
    square_inverse = _inverse(square, prime)
    coefficients = [[0] * column_count for _ in range(rank)]
    for column in range(column_count):
        target = [matrix[row][column] for row in selected_rows]
        for output in range(rank):
            coefficients[output][column] = sum(
                square_inverse[output][j] * target[j] for j in range(rank)
            ) % prime
    if any(
        sum(columns[row][k] * coefficients[k][column] for k in range(rank)) % prime
        != matrix[row][column]
        for row in range(row_count)
        for column in range(column_count)
    ):
        raise AssertionError("rank factorization reconstruction failed")
    return columns, coefficients


def _tt(values: list[int], genus: int, prime: int) -> list[list[list[list[int]]]]:
    """Exact four-state cores indexed [site][state][left][right]."""
    if genus == 0:
        return []
    current = [values[:]]
    left_rank = 1
    cores = []
    for site in range(genus - 1):
        suffix = 4 ** (genus - site - 1)
        matrix = [
            [current[left][state + 4 * rest] for rest in range(suffix)]
            for left in range(left_rank)
            for state in range(4)
        ]
        columns, current = _rank_factor(matrix, prime)
        right_rank = len(current)
        cores.append([
            [[columns[4 * left + state][right] for right in range(right_rank)]
             for left in range(left_rank)]
            for state in range(4)
        ])
        left_rank = right_rank
    cores.append([
        [[current[left][state]] for left in range(left_rank)]
        for state in range(4)
    ])
    return cores


def _matvec(left: list[int], matrix: list[list[int]], prime: int) -> list[int]:
    return [
        sum(left[row] * matrix[row][column] for row in range(len(left))) % prime
        for column in range(len(matrix[0]))
    ]


def _matcol(matrix: list[list[int]], right: list[int], prime: int) -> list[int]:
    return [sum(value * right[column] for column, value in enumerate(row)) % prime for row in matrix]


def _weighted_matrix(core, weights: list[int], prime: int) -> list[list[int]]:
    return [[
        sum(weights[state] * core[state][left][right] for state in range(4)) % prime
        for right in range(len(core[0][0]))
    ] for left in range(len(core[0]))]


def _all_single_handle_walsh(cores, weights: list[list[int]], prime: int) -> list[list[int]]:
    genus = len(cores)
    weighted = [_weighted_matrix(core, weights[i], prime) for i, core in enumerate(cores)]
    left = [[1]]
    for matrix in weighted:
        left.append(_matvec(left[-1], matrix, prime))
    right = [[1] for _ in range(genus + 1)]
    for i in range(genus - 1, -1, -1):
        right[i] = _matcol(weighted[i], right[i + 1], prime)
    answer = []
    for i, core in enumerate(cores):
        fixed = [
            sum(
                left[i][a] * core[state][a][b] * right[i + 1][b]
                for a in range(len(left[i]))
                for b in range(len(right[i + 1]))
            ) % prime
            for state in range(4)
        ]
        answer.append([
            sum(((-1) ** ((character & state).bit_count())) * fixed[state]
                for state in range(4)) % prime
            for character in range(4)
        ])
    return answer


def _brute(values: list[int], genus: int, weights: list[list[int]], prime: int) -> list[list[int]]:
    answer = [[0] * 4 for _ in range(genus)]
    for index, value in enumerate(values):
        states = [(index >> (2 * i)) & 3 for i in range(genus)]
        for held in range(genus):
            factor = value
            for i, state in enumerate(states):
                if i != held:
                    factor = factor * weights[i][state] % prime
            for character in range(4):
                sign = -1 if (character & states[held]).bit_count() & 1 else 1
                answer[held][character] = (answer[held][character] + sign * factor) % prime
    return answer


def _tensor(executable: Path, prime: int, n: int, w: int) -> tuple[list[int], str]:
    genus = universal_embedding_genus(n, w)
    rotation = universal_checkerboard_rotation(n, w)
    edge_text, labels, intersection = _edge_payload(n, w, rotation, genus)
    _, edges = cubic_box((n, w, w))
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    result = subprocess.run(
        [str(executable)],
        input=f"{n} {w} {2 * genus} {len(edges)} 0\n{edge_text}\n",
        text=True,
        capture_output=True,
        check=True,
        env=environment,
        timeout=1800,
    )
    raw_g = [int(value) for value in result.stdout.splitlines()]
    raw_f = _f_values_from_walsh(raw_g, intersection, prime)
    structural = _case(w, n)["length_rows"][-1]
    canonical, _ = _canonical_reindex(raw_f, structural)
    return canonical, hashlib.sha256(json.dumps(labels, separators=(",", ":")).encode()).hexdigest()


def verify() -> dict[str, object]:
    rows = []
    compilers = {}
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="lane-b-all-q-") as temporary:
        for prime in PRIMES:
            executable, compiler = _compile(Path(temporary), prime)
            compilers[str(prime)] = compiler
            for n in (6, 7):
                w = 3
                genus = universal_embedding_genus(n, w)
                values, label_hash = _tensor(executable, prime, n, w)
                cores = _tt(values, genus, prime)
                weights = [[(17 * i + 11 * state + 3) % prime for state in range(4)] for i in range(genus)]
                compressed = _all_single_handle_walsh(cores, weights, prime)
                direct = _brute(values, genus, weights, prime)
                if compressed != direct:
                    raise AssertionError("compressed and all-sector marginal evaluations disagree")
                rows.append({
                    "shape": [n, w, w],
                    "prime": prime,
                    "genus": genus,
                    "sector_count": 4 ** genus,
                    "pair_tt_ranks": [len(core[0][0]) for core in cores[:-1]],
                    "weight_rule": "omega_i(s)=17*i+11*s+3 mod p, zero-based i,s",
                    "all_single_handle_walsh_marginals": compressed,
                    "direct_enumeration_agrees": True,
                    "edge_label_sha256": label_hash,
                })
    return {
        "claim_status": "CERTIFIED_NUMERICAL exact finite-field validation",
        "operation": "all four Walsh marginals at every handle under arbitrary product-form sector weights",
        "primes": list(PRIMES),
        "compilers": compilers,
        "rows": rows,
        "complexity": {
            "given_TT_dense_environment_contraction": "O(g*p*d^2), p=4",
            "sector_enumeration": "Omega(4^g) tensor entries before per-sector evaluation cost",
            "memory": "O(g*d) environments plus the supplied cores",
        },
        "claim_boundary": (
            "This validates the all-q operation and exact TT algebra on nontrivial strips. "
            "It is not an advantage claim for evaluating the final physical partition function once."
        ),
        "wall_seconds": round(time.perf_counter() - started, 6),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
