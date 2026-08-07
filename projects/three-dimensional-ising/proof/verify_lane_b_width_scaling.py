#!/usr/bin/env python3
"""Exact width-two/three/four rank and genus audit for Gate B5."""

from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from proof.verify_lane_b_intersection import _graph_result  # noqa: E402
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_genus3 import BOX_4X3X3_GENUS_THREE_ROTATION  # noqa: E402
from src.lane_b_recursive_family import recursive_rotation  # noqa: E402
from src.lane_b_width_scaling import (  # noqa: E402
    checkerboard_boundary_rotation,
    genus_bounds,
    physical_frontier_dimension,
    symbolic_rank_upper_bound,
)


PRIMES = (1_000_000_007, 1_000_000_009)


def _fwht(values: list[int], prime: int, inverse: bool = False) -> list[int]:
    result = values[:]
    length = 1
    while length < len(result):
        for start in range(0, len(result), 2 * length):
            for offset in range(length):
                left = result[start + offset]
                right = result[start + offset + length]
                result[start + offset] = (left + right) % prime
                result[start + offset + length] = (left - right) % prime
        length *= 2
    if inverse:
        scale = pow(len(result), prime - 2, prime)
        result = [value * scale % prime for value in result]
    return result


def _rank_mod(matrix: list[list[int]], prime: int) -> int:
    rows = [row[:] for row in matrix]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][column] % prime), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [value * inverse % prime for value in rows[rank]]
        for row in range(rank + 1, len(rows)):
            if rows[row][column]:
                factor = rows[row][column]
                rows[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(rows[row], rows[rank])
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def _det_certificate(matrix: list[list[int]], prime: int) -> dict[str, object]:
    if any(len(row) != len(matrix) for row in matrix):
        raise ValueError("determinant requires a square matrix")
    rows = [row[:] for row in matrix]
    row_ids = list(range(len(rows)))
    determinant = 1
    pivot_rows: list[int] = []
    pivot_values: list[int] = []
    swaps: list[list[int]] = []
    for column in range(len(rows)):
        pivot = next((row for row in range(column, len(rows)) if rows[row][column]), None)
        if pivot is None:
            return {"determinant": 0, "pivot_columns": list(range(column)), "pivot_rows": pivot_rows}
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            row_ids[column], row_ids[pivot] = row_ids[pivot], row_ids[column]
            swaps.append([column, pivot])
            determinant = -determinant
        pivot_value = rows[column][column]
        pivot_rows.append(row_ids[column])
        pivot_values.append(pivot_value)
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, len(rows)):
            factor = rows[row][column] * inverse % prime
            for index in range(column, len(rows)):
                rows[row][index] = (rows[row][index] - factor * rows[column][index]) % prime
    return {
        "determinant": determinant % prime,
        "pivot_columns": list(range(len(rows))),
        "pivot_original_rows": pivot_rows,
        "pivot_values_before_normalization": pivot_values,
        "row_swaps": swaps,
        "minor_rows": list(range(len(rows))),
        "minor_columns": list(range(len(rows))),
    }


def _quadratic_value(intersection: list[int], vector: int) -> int:
    value = 0
    dimension = len(intersection)
    for left in range(dimension):
        if not (vector >> left) & 1:
            continue
        for right in range(left + 1, dimension):
            if (vector >> right) & 1 and (intersection[left] >> right) & 1:
                value ^= 1
    return value


def _f_values_from_walsh(g_values: list[int], intersection: list[int], prime: int) -> list[int]:
    sectors = _fwht(g_values, prime, inverse=True)
    signed = [
        (-value) % prime if _quadratic_value(intersection, homology) else value
        for homology, value in enumerate(sectors)
    ]
    return _fwht(signed, prime)


def _profiles(values: list[int], dimension: int, prime: int) -> tuple[list[int], dict[str, object]]:
    ranks: list[int] = []
    determinants: dict[str, object] = {}
    for cut in range(1, dimension):
        row_count = 1 << cut
        column_count = 1 << (dimension - cut)
        matrix = [
            [values[row | (column << cut)] for column in range(column_count)]
            for row in range(row_count)
        ]
        rank = _rank_mod(matrix, prime)
        ranks.append(rank)
        if row_count == column_count:
            determinants[f"cut_{cut}"] = _det_certificate(matrix, prime)
    return ranks, determinants


def _rotation_and_genus(n: int, w: int):
    if w == 3 and n >= 4:
        return recursive_rotation(n), n - 1
    if w == 4 and n % 2 == 0:
        return checkerboard_boundary_rotation(n, w), 2 * n - 3
    raise ValueError("rank controls use (n,w)=(4,3) or even-n width four")


def _edge_payload(n: int, w: int, rotation, genus: int) -> tuple[str, list[int], list[int]]:
    vertices, edges = cubic_box((n, w, w))
    face_masks, face_walks = _rotation_faces(vertices, edges, rotation)
    labels, face_rank = _edge_homology_labels(len(edges), face_masks, _cycle_basis(vertices, edges), genus)
    topology = _graph_result((n, w, w), rotation, genus)
    lines: list[str] = []
    for edge, label in zip(edges, labels):
        axis = next(index for index in range(3) if edge.u[index] != edge.v[index])
        left = w * edge.u[1] + edge.u[2]
        right = w * edge.v[1] + edge.v[2]
        lines.append(f"{edge.u[0]} {axis} {left} {right} {label}")
    euler_genus = (2 - (len(vertices) - len(edges) + len(face_walks))) // 2
    if euler_genus != genus or topology["face_boundary_rank"] != face_rank:
        raise AssertionError("embedding/topology regression")
    return "\n".join(lines), labels, topology["intersection_matrix_rows"]


def _compile(temporary: Path, prime: int) -> tuple[Path, str]:
    source = ROOT / "proof" / "lane_b_width4_character_transfer.cpp"
    executable = temporary / f"width-transfer-{prime}"
    command = [
        "g++", "-std=c++20", "-O3", "-DNDEBUG", "-fopenmp",
        f"-DMODULUS={prime}ULL", str(source), "-o", str(executable),
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    version = subprocess.run(["g++", "--version"], text=True, capture_output=True, check=True).stdout.splitlines()[0]
    if result.stderr:
        raise RuntimeError(result.stderr)
    return executable, version


def _run_case(executable: Path, n: int, w: int, prime: int) -> dict[str, object]:
    rotation, genus = _rotation_and_genus(n, w)
    edge_text, labels, intersection = _edge_payload(n, w, rotation, genus)
    _, edges = cubic_box((n, w, w))
    cases: dict[str, object] = {}
    for regime, name in (
        (0, "nonuniform"),
        (1, "homogeneous_anisotropic"),
        (2, "homogeneous_isotropic"),
    ):
        header = f"{n} {w} {2 * genus} {len(edges)} {regime}\n"
        started = time.perf_counter()
        environment = dict(os.environ)
        environment["OMP_NUM_THREADS"] = "3"
        result = subprocess.run(
            [str(executable)], input=header + edge_text + "\n", text=True,
            capture_output=True, check=True, env=environment, timeout=1800,
        )
        elapsed = time.perf_counter() - started
        g_values = [int(line) for line in result.stdout.splitlines()]
        if len(g_values) != 1 << (2 * genus):
            raise AssertionError("character transfer returned the wrong tensor size")
        f_values = _f_values_from_walsh(g_values, intersection, prime)
        profile, determinants = _profiles(f_values, 2 * genus, prime)
        if any(value["determinant"] == 0 for value in determinants.values()):
            raise AssertionError("declared central nonzero minor vanished")
        cases[name] = {
            "weight_specialization": (
                "independent deterministic nonzero edge values"
                if regime == 0 else (
                    "(t_x,t_y,t_z)=(2,3,5)" if regime == 1 else "t_x=t_y=t_z=2"
                )
            ),
            "binary_flattening_ranks": profile,
            "central_full_minor_mod_prime": determinants,
            "wall_seconds": round(elapsed, 6),
        }
    label_union = 0
    for label in labels:
        label_union |= label
    return {
        "shape": [n, w, w],
        "genus": genus,
        "homology_bits": 2 * genus,
        "edge_label_union_dimension": label_union.bit_length(),
        "field": f"GF({prime})",
        "edge_order": "src.conventions.cubic_box lexicographic canonical edge order",
        "homology_label_sha256": hashlib.sha256(
            json.dumps(labels, separators=(",", ":")).encode()
        ).hexdigest(),
        "homology_labels": labels,
        "flattening_order": "row = low cut bits; column = high cut bits; both ascending binary",
        "normalization": {
            "spin_to_parity_factor": f"2^{n*w*w}",
            "factor_nonzero_mod_prime": pow(2, n * w * w, prime) != 0,
            "inverse_walsh_denominator": 1 << (2 * genus),
            "denominator_invertible_mod_prime": (1 << (2 * genus)) % prime != 0,
        },
        "cases": cases,
        "lifting": (
            "Every reported nonzero determinant is the reduction of an integer polynomial "
            "minor at the pinned specialization; hence that symbolic minor is nonzero."
        ),
    }


def _independent_w3_transfer_control(executable: Path, prime: int) -> dict[str, object]:
    n, w, genus = 4, 3, 3
    rotation = BOX_4X3X3_GENUS_THREE_ROTATION
    edge_text, labels, _ = _edge_payload(n, w, rotation, genus)
    vertices, edges = cubic_box((n, w, w))
    header = f"{n} {w} {2 * genus} {len(edges)} 2\n"
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    result = subprocess.run(
        [str(executable)], input=header + edge_text + "\n", text=True,
        capture_output=True, check=True, env=environment, timeout=120,
    )
    spin_values = [int(line) for line in result.stdout.splitlines()]
    scale = pow(2, len(vertices), prime)
    def edge_boundary(edge) -> int:
        return (1 << (w * edge.u[1] + edge.u[2])) | (1 << (w * edge.v[1] + edge.v[2]))

    def parity_value(character: int) -> int:
        transverse = [[] for _ in range(n)]
        connectors = [[] for _ in range(n - 1)]
        for edge, label in zip(edges, labels):
            axis = next(index for index in range(3) if edge.u[index] != edge.v[index])
            (connectors if axis == 0 else transverse)[edge.u[0]].append((edge, label))
        even = [mask for mask in range(1 << (w * w)) if mask.bit_count() % 2 == 0]
        state = {0: 1}
        for layer in range(n):
            kernel = [0] * (1 << (w * w))
            kernel[0] = 1
            for edge, label in transverse[layer]:
                flip = edge_boundary(edge)
                weight = -2 if (character & label).bit_count() % 2 else 2
                updated = kernel[:]
                for mask, value in enumerate(kernel):
                    if value:
                        updated[mask ^ flip] = (updated[mask ^ flip] + value * weight) % prime
                kernel = updated
            if layer == n - 1:
                return sum(value * kernel[mask] for mask, value in state.items()) % prime
            updated_state = {mask: 0 for mask in even}
            for incoming, value in state.items():
                for outgoing in even:
                    connector_weight = pow(2, outgoing.bit_count(), prime)
                    updated_state[outgoing] = (
                        updated_state[outgoing]
                        + value * kernel[incoming ^ outgoing] * connector_weight
                    ) % prime
            state = updated_state
        raise AssertionError("unreachable parity-transfer exit")

    frontier_values = [parity_value(character) for character in range(1 << (2 * genus))]
    if spin_values != [scale * value % prime for value in frontier_values]:
        raise AssertionError("optimized spin and independent parity transfers disagree")
    return {
        "shape": [n, w, w],
        "characters": 1 << (2 * genus),
        "uniform_t": 2,
        "identity": "Z_spin_normalized(mu)=2^|V| G_parity(mu)",
        "all_agree": True,
    }


def _w2_control() -> dict[str, object]:
    lower, upper = genus_bounds(4, 2)
    if (lower, upper) != (0, 0):
        raise AssertionError("width-two planar calibration failed")
    return {
        "width": 2,
        "physical_frontier_dimension": physical_frontier_dimension(2),
        "genus": "0 for every n",
        "spin_structure_tensor_entries": 1,
        "all_flattening_ranks": 1,
        "generic_nonuniform_rank": 1,
        "homogeneous_anisotropic_rank": 1,
    }


def verify() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="lane-b-width-") as directory:
        audits: dict[str, object] = {}
        compiler = ""
        for prime in PRIMES:
            executable, compiler = _compile(Path(directory), prime)
            audits[str(prime)] = {
                "independent_transfer_control": _independent_w3_transfer_control(executable, prime),
                "w3": _run_case(executable, 4, 3, prime),
                "w4": _run_case(executable, 4, 4, prime),
            }
    genus_table = {
        "w2": "g(n,2)=0",
        "w3": "g(n,3)=n-1",
        "w4_even_n": "g(n,4)=2n-3",
        "w4_odd_n": "2n-3 <= g(n,4) <= 2n-2",
    }
    return {
        "claim_status": "CERTIFIED_NUMERICAL ranks with exact finite-field minor lifting",
        "compiler": compiler,
        "prime_audits": audits,
        "genus_table": genus_table,
        "widths": {
            "2": _w2_control(),
            "3": {
                "physical_frontier_dimension": physical_frontier_dimension(3),
                "constructed_handle_TT_bound": 1024,
                "constructed_binary_TT_bound": 2048,
                "rank_control": "see prime_audits[*].w3",
            },
            "4": {
                "physical_frontier_dimension": physical_frontier_dimension(4),
                "constructed_binary_TT_bound": symbolic_rank_upper_bound(4),
                "rank_control": "see prime_audits[*].w4",
            },
        },
        "symbolic_bound": {
            "formula": "R(w)=2^(w^2-1+4*floor((w-1)^2/4))",
            "status": "CONJECTURED outside the exercised w=3,4 constructions",
            "scope": (
                "Conditional repeated-handle binary-coordinate ansatz bound; it is not part "
                "of the certified Gate B5 claims and does not imply favorable width scaling."
            ),
        },
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
