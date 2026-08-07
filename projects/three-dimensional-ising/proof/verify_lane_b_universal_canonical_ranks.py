#!/usr/bin/env python3
"""Finite-field rank certificates in the universal canonical coordinates."""

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

from proof.verify_lane_b_arbitrary_width_frontier import (  # noqa: E402
    _case,
    _matrix_vector,
    _quadratic_standard,
)
from proof.verify_lane_b_width_scaling import (  # noqa: E402
    _compile,
    _det_certificate,
    _edge_payload,
    _f_values_from_walsh,
    _profiles,
    _quadratic_value,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
    universal_embedding_genus,
)


PRIMES = (1_000_000_007, 1_000_000_009)
REGIMES = {
    0: "nonuniform",
    1: "homogeneous_anisotropic_(2,3,5)",
    2: "homogeneous_isotropic_t=2",
}


def _transpose(rows: list[int], dimension: int) -> list[int]:
    return [
        sum(((rows[row] >> column) & 1) << row for row in range(dimension))
        for column in range(dimension)
    ]


def _canonical_reindex(values: list[int], row: dict[str, object]) -> tuple[list[int], int]:
    dimension = int(row["homology_bits"])
    genus = int(row["genus"])
    change = list(row["raw_to_atomic_rows"])
    intersection = list(row["raw_intersection"])
    correction = 0
    for bit in range(dimension):
        if _quadratic_standard(_matrix_vector(change, 1 << bit), genus) ^ _quadratic_value(
            intersection, 1 << bit
        ):
            correction |= 1 << bit
    transpose = _transpose(change, dimension)
    return [
        values[correction ^ _matrix_vector(transpose, linear)]
        for linear in range(1 << dimension)
    ], correction


def _rank_minor(matrix: list[list[int]], prime: int) -> dict[str, object]:
    rows = [row[:] for row in matrix]
    row_ids = list(range(len(rows)))
    rank = 0
    pivot_rows: list[int] = []
    pivot_columns: list[int] = []
    for column in range(len(rows[0]) if rows else 0):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
        pivot_rows.append(row_ids[rank])
        pivot_columns.append(column)
        inverse = pow(rows[rank][column], prime - 2, prime)
        for row in range(rank + 1, len(rows)):
            factor = rows[row][column] * inverse % prime
            if factor:
                rows[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == len(rows):
            break
    minor = [[matrix[row][column] for column in pivot_columns] for row in pivot_rows]
    certificate = _det_certificate(minor, prime)
    if certificate["determinant"] == 0:
        raise AssertionError("rank-revealing pivot minor vanished on replay")
    return {
        "rank": rank,
        "minor_rows": pivot_rows,
        "minor_columns": pivot_columns,
        "minor_determinant": certificate["determinant"],
        "minor_lu": certificate,
    }


def _case_certificate(executable: Path, prime: int, n: int, w: int, regime: int) -> dict[str, object]:
    genus = universal_embedding_genus(n, w)
    dimension = 2 * genus
    rotation = universal_checkerboard_rotation(n, w)
    edge_text, labels, intersection = _edge_payload(n, w, rotation, genus)
    _, edges = cubic_box((n, w, w))
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    started = time.perf_counter()
    result = subprocess.run(
        [str(executable)],
        input=f"{n} {w} {dimension} {len(edges)} {regime}\n{edge_text}\n",
        text=True,
        capture_output=True,
        check=True,
        env=environment,
        timeout=1800,
    )
    raw_g = [int(value) for value in result.stdout.splitlines()]
    if len(raw_g) != 1 << dimension:
        raise AssertionError("character transfer returned the wrong tensor size")
    raw_f = _f_values_from_walsh(raw_g, intersection, prime)
    structural = _case(w, n)["length_rows"][-1]
    canonical_f, correction = _canonical_reindex(raw_f, structural)
    ranks, square_determinants = _profiles(canonical_f, dimension, prime)
    central_cut = dimension // 2
    row_count = 1 << central_cut
    central = [
        [canonical_f[row | (column << central_cut)] for column in range(1 << (dimension-central_cut))]
        for row in range(row_count)
    ]
    central_certificate = _rank_minor(central, prime)
    return {
        "shape": [n, w, w],
        "genus": genus,
        "homology_bits": dimension,
        "regime": REGIMES[regime],
        "prime": prime,
        "canonical_binary_rank_profile": ranks,
        "central_cut": central_cut,
        "central_certificate": central_certificate,
        "square_full_determinants": square_determinants,
        "raw_to_canonical_affine_correction": correction,
        "edge_label_sha256": hashlib.sha256(
            json.dumps(labels, separators=(",", ":")).encode()
        ).hexdigest(),
        "row_column_order": "ascending low bits | ascending high bits",
        "walsh_normalization": "inverse transform divides by 2^(2g)",
        "normalization_invertible": pow(1 << dimension, prime - 2, prime) != 0,
        "wall_seconds": round(time.perf_counter() - started, 6),
    }


def verify() -> dict[str, object]:
    cases = []
    compilers = {}
    with tempfile.TemporaryDirectory(prefix="lane-b-universal-canonical-") as temporary:
        for prime in PRIMES:
            executable, compiler = _compile(Path(temporary), prime)
            compilers[str(prime)] = compiler
            for n, w in ((4, 4), (10, 3)):
                for regime in REGIMES:
                    cases.append(_case_certificate(executable, prime, n, w, regime))
    w3 = [case for case in cases if case["shape"] == [10, 3, 3]]
    if any(case["canonical_binary_rank_profile"][7:10] != [256, 256, 256] for case in w3):
        raise AssertionError("canonical width-three central ranks regressed")
    w4 = [case for case in cases if case["shape"] == [4, 4, 4]]
    if any(case["canonical_binary_rank_profile"] != [2,4,8,16,32,16,8,4,2] for case in w4):
        raise AssertionError("canonical width-four rank profile regressed")
    return {
        "claim_status": "CERTIFIED_NUMERICAL",
        "primes": list(PRIMES),
        "compilers": compilers,
        "embedding": "universal checkerboard rotation",
        "canonical_basis": "filtration-adapted atomic Lagrangian basis from the structural verifier",
        "cases": cases,
        "lifting": (
            "A nonzero determinant modulo either prime is a nonzero integer-polynomial "
            "minor at the frozen integral specialization."
        ),
        "claim_boundary": (
            "The w=3 certificates prove saturation at the tested sizes and weights. "
            "The w=4 tensor has too few spin-structure bits at n=4 to test saturation "
            "of d_4=32768. No arbitrary-width lower bound follows."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
