#!/usr/bin/env python3
"""Exact Stage 1 checks for finite-graph Ising expansion conventions."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.conventions import (  # noqa: E402
    Edge,
    Vertex,
    cubic_box,
    orientable_genus_lower_bound_for_free_box,
)


def spin_signs(vertices: tuple[Vertex, ...], state: int) -> dict[Vertex, int]:
    return {vertex: 1 if (state >> index) & 1 else -1 for index, vertex in enumerate(vertices)}


def spin_energy_histogram(vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]) -> Counter[int]:
    """Count configurations by ``sum_e eta_e sigma_u sigma_v``."""

    histogram: Counter[int] = Counter()
    for state in range(1 << len(vertices)):
        spins = spin_signs(vertices, state)
        exponent = sum(edge.eta * spins[edge.u] * spins[edge.v] for edge in edges)
        histogram[exponent] += 1
    return histogram


def low_temperature_histogram(vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]) -> Counter[int]:
    """Count cut/twist defects with one root spin fixed, including global factor two."""

    histogram: Counter[int] = Counter()
    root_index = 0
    for state in range(1 << (len(vertices) - 1)):
        spins = {vertices[root_index]: 1}
        for shifted_index, vertex in enumerate(vertices[1:]):
            spins[vertex] = 1 if (state >> shifted_index) & 1 else -1
        defects = sum(edge.eta * spins[edge.u] * spins[edge.v] == -1 for edge in edges)
        histogram[defects] += 2
    return histogram


def _gf2_nullspace_basis(rows: list[int], columns: int) -> list[int]:
    """Return a basis for the nullspace of a binary matrix stored as row masks."""

    reduced = [row for row in rows if row]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(columns):
        found = next((r for r in range(pivot_row, len(reduced)) if (reduced[r] >> column) & 1), None)
        if found is None:
            continue
        reduced[pivot_row], reduced[found] = reduced[found], reduced[pivot_row]
        for r in range(len(reduced)):
            if r != pivot_row and ((reduced[r] >> column) & 1):
                reduced[r] ^= reduced[pivot_row]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(reduced):
            break
    reduced = reduced[:pivot_row]
    free_columns = [column for column in range(columns) if column not in set(pivots)]
    basis: list[int] = []
    for free in free_columns:
        vector = 1 << free
        for row_index, pivot in enumerate(pivots):
            if (reduced[row_index] >> free) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def even_subgraph_histogram(vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]) -> Counter[int]:
    """Return signed high-temperature coefficients by exact cycle-space enumeration."""

    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    incidence_rows = [0] * len(vertices)
    negative_mask = 0
    for edge_index, edge in enumerate(edges):
        incidence_rows[vertex_index[edge.u]] |= 1 << edge_index
        incidence_rows[vertex_index[edge.v]] |= 1 << edge_index
        if edge.eta == -1:
            negative_mask |= 1 << edge_index
    basis = _gf2_nullspace_basis(incidence_rows, len(edges))
    histogram: Counter[int] = Counter()
    for coordinates in range(1 << len(basis)):
        subset = 0
        for basis_index, vector in enumerate(basis):
            if (coordinates >> basis_index) & 1:
                subset ^= vector
        sign = -1 if (subset & negative_mask).bit_count() % 2 else 1
        histogram[subset.bit_count()] += sign
    return histogram


def spin_high_temperature_polynomial(
    vertices: tuple[Vertex, ...], edges: tuple[Edge, ...]
) -> tuple[Fraction, ...]:
    """Expand ``2^-|V| sum_sigma product_e(1+t eta_e sigma_u sigma_v)``."""

    coefficients = [0] * (len(edges) + 1)
    for state in range(1 << len(vertices)):
        spins = spin_signs(vertices, state)
        polynomial = [1]
        for edge in edges:
            sign = edge.eta * spins[edge.u] * spins[edge.v]
            updated = [0] * (len(polynomial) + 1)
            for degree, coefficient in enumerate(polynomial):
                updated[degree] += coefficient
                updated[degree + 1] += sign * coefficient
            polynomial = updated
        for degree, coefficient in enumerate(polynomial):
            coefficients[degree] += coefficient
    denominator = 1 << len(vertices)
    return tuple(Fraction(value, denominator) for value in coefficients)


def verify_case(
    name: str,
    shape: tuple[int, int, int],
    *,
    periodic: tuple[int, ...] = (),
    antiperiodic: tuple[int, ...] = (),
) -> dict[str, object]:
    vertices, edges = cubic_box(shape, periodic=periodic, antiperiodic=antiperiodic)
    spin_histogram = spin_energy_histogram(vertices, edges)
    low_histogram = low_temperature_histogram(vertices, edges)
    reconstructed_spin = Counter(
        {len(edges) - 2 * defects: multiplicity for defects, multiplicity in low_histogram.items()}
    )
    if spin_histogram != reconstructed_spin:
        raise AssertionError(f"low-temperature mismatch for {name}")

    even_histogram = even_subgraph_histogram(vertices, edges)
    spin_polynomial = spin_high_temperature_polynomial(vertices, edges)
    even_polynomial = tuple(Fraction(even_histogram.get(k, 0)) for k in range(len(edges) + 1))
    if spin_polynomial != even_polynomial:
        raise AssertionError(f"high-temperature mismatch for {name}")

    return {
        "name": name,
        "shape": list(shape),
        "vertices": len(vertices),
        "edges": len(edges),
        "periodic_axes": list(periodic),
        "antiperiodic_axes": list(antiperiodic),
        "spin_states": 1 << len(vertices),
        "cycle_space_states": 1 << (len(edges) - len(vertices) + 1),
        "high_temperature_coefficients": [int(value) for value in spin_polynomial],
        "low_temperature_defect_counts": {
            str(defects): low_histogram[defects] for defects in sorted(low_histogram)
        },
        "status": "PASS",
    }


def build_report() -> dict[str, object]:
    cases = [
        verify_case("free-2x2x2", (2, 2, 2)),
        verify_case("free-2x2x3", (2, 2, 3)),
        verify_case("periodic-x-3x2x2", (3, 2, 2), periodic=(0,)),
        verify_case("antiperiodic-x-3x2x2", (3, 2, 2), antiperiodic=(0,)),
        verify_case("periodic-2d-3x3x1", (3, 3, 1), periodic=(0, 1)),
        verify_case("antiperiodic-x-2d-3x3x1", (3, 3, 1), periodic=(1,), antiperiodic=(0,)),
    ]
    genus_bounds = {
        str(length): orientable_genus_lower_bound_for_free_box((length, length, length))
        for length in (3, 4, 5, 8)
    }
    expected = {"3": 1, "4": 5, "5": 14, "8": 81}
    if genus_bounds != expected:
        raise AssertionError("orientable-genus lower-bound regression")
    return {
        "status": "PASS",
        "arithmetic": "exact integers and fractions",
        "cases": cases,
        "free_cubic_box_genus_lower_bounds": genus_bounds,
        "claim_boundary": (
            "Finite enumerated instances and the Euler/girth genus lower bound only; "
            "no thermodynamic or exact-solution claim."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2, sort_keys=True))
