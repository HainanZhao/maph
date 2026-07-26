"""Sparse fixed-winding phase projection via linear programming."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class PhaseEdge:
    """An oriented target phase theta_u-theta_v and a physical weight."""

    u: int
    v: int
    phase: float
    weight: float = 1.0


@dataclass(frozen=True)
class SparsePhaseProjection:
    """A checked phase projection result."""

    theta: tuple[float, ...]
    corrections: tuple[float, ...]
    linear_bound: float
    exact_bound: float
    solver_status: int
    solver_message: str


def _validate_graph(vertex_count: int, edges: Sequence[PhaseEdge], root: int) -> None:
    if vertex_count < 2:
        raise ValueError("vertex_count must be at least two")
    if root < 0 or root >= vertex_count:
        raise ValueError("root is outside the graph")
    if not edges:
        raise ValueError("at least one edge is required")
    adjacency = [[] for _ in range(vertex_count)]
    for index, edge in enumerate(edges):
        if edge.u == edge.v:
            raise ValueError("self-loops are not supported")
        if min(edge.u, edge.v) < 0 or max(edge.u, edge.v) >= vertex_count:
            raise ValueError("edge endpoint is outside the graph")
        if edge.weight < 0:
            raise ValueError("edge weights must be nonnegative")
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    seen = {root}
    stack = [root]
    while stack:
        u = stack.pop()
        for v, _ in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    if len(seen) != vertex_count:
        raise ValueError("the graph must be connected")


def phase_corrections(
    theta: Sequence[float], edges: Sequence[PhaseEdge]
) -> tuple[float, ...]:
    """Return theta_u-theta_v-alpha_e for every oriented edge."""

    return tuple(
        float(theta[edge.u]) - float(theta[edge.v]) - float(edge.phase)
        for edge in edges
    )


def buswise_bounds(
    vertex_count: int,
    edges: Sequence[PhaseEdge],
    corrections: Sequence[float],
    *,
    linearized: bool,
    bus_offsets: Sequence[float] | None = None,
) -> tuple[float, ...]:
    """Return each bus's weighted incident phase-recovery residual."""

    if bus_offsets is None:
        values = [0.0] * vertex_count
    else:
        if len(bus_offsets) != vertex_count:
            raise ValueError("bus_offsets has the wrong length")
        values = [float(value) for value in bus_offsets]
        if any(value < 0 for value in values):
            raise ValueError("bus_offsets must be nonnegative")
    for edge, correction in zip(edges, corrections):
        if linearized:
            residual = abs(float(correction))
        else:
            residual = 2.0 * abs(math.sin(0.5 * float(correction)))
        contribution = edge.weight * residual
        values[edge.u] += contribution
        values[edge.v] += contribution
    return tuple(values)


def solve_minimax_phase_lp(
    vertex_count: int,
    edge_iterable: Iterable[PhaseEdge],
    *,
    root: int = 0,
    maximum_correction: float = math.pi,
    angle_center: Sequence[float] | None = None,
    maximum_angle_displacement: float | None = None,
    bus_offsets: Sequence[float] | None = None,
) -> SparsePhaseProjection:
    """Minimize the worst-bus weighted absolute phase correction.

    Target edge phases are assumed to have already been placed on a fixed
    winding branch.  The reference angle is fixed to zero.  If a center and
    displacement are supplied, the nonreference angles are restricted to an
    infinity-norm trust region around the gauge-normalized center.
    """

    edges = tuple(edge_iterable)
    _validate_graph(vertex_count, edges, root)
    if maximum_correction <= 0 or maximum_correction > math.pi:
        raise ValueError("maximum_correction must lie in (0, pi]")
    if bus_offsets is None:
        offsets = (0.0,) * vertex_count
    else:
        if len(bus_offsets) != vertex_count:
            raise ValueError("bus_offsets has the wrong length")
        offsets = tuple(float(value) for value in bus_offsets)
        if any(value < 0 for value in offsets):
            raise ValueError("bus_offsets must be nonnegative")
    if (angle_center is None) != (maximum_angle_displacement is None):
        raise ValueError(
            "angle_center and maximum_angle_displacement must be used together"
        )
    normalized_center: tuple[float, ...] | None = None
    if angle_center is not None:
        if len(angle_center) != vertex_count:
            raise ValueError("angle_center has the wrong length")
        if maximum_angle_displacement is None:
            raise AssertionError("validated displacement is unexpectedly absent")
        if maximum_angle_displacement < 0:
            raise ValueError("maximum_angle_displacement must be nonnegative")
        root_angle = float(angle_center[root])
        normalized_center = tuple(
            float(value) - root_angle for value in angle_center
        )

    nonroot = [vertex for vertex in range(vertex_count) if vertex != root]
    angle_column = {vertex: index for index, vertex in enumerate(nonroot)}
    angle_count = len(nonroot)
    edge_count = len(edges)
    u_start = angle_count
    t_column = angle_count + edge_count
    variable_count = t_column + 1

    objective = np.zeros(variable_count)
    objective[t_column] = 1.0
    rows: list[np.ndarray] = []
    right_hand_sides: list[float] = []

    def angle_coefficients(edge: PhaseEdge) -> np.ndarray:
        row = np.zeros(variable_count)
        if edge.u != root:
            row[angle_column[edge.u]] += 1.0
        if edge.v != root:
            row[angle_column[edge.v]] -= 1.0
        return row

    for edge_index, edge in enumerate(edges):
        coefficients = angle_coefficients(edge)
        upper = coefficients.copy()
        upper[u_start + edge_index] = -1.0
        rows.append(upper)
        right_hand_sides.append(edge.phase)

        lower = -coefficients
        lower[u_start + edge_index] = -1.0
        rows.append(lower)
        right_hand_sides.append(-edge.phase)

    for vertex in range(vertex_count):
        row = np.zeros(variable_count)
        for edge_index, edge in enumerate(edges):
            if edge.u == vertex or edge.v == vertex:
                row[u_start + edge_index] += edge.weight
        row[t_column] = -1.0
        rows.append(row)
        right_hand_sides.append(-offsets[vertex])

    if normalized_center is None:
        angle_bounds = [(None, None)] * angle_count
    else:
        assert maximum_angle_displacement is not None
        angle_bounds = [
            (
                normalized_center[vertex] - maximum_angle_displacement,
                normalized_center[vertex] + maximum_angle_displacement,
            )
            for vertex in nonroot
        ]
    bounds = (
        angle_bounds
        + [(0.0, maximum_correction)] * edge_count
        + [(0.0, None)]
    )
    result = linprog(
        objective,
        A_ub=np.asarray(rows),
        b_ub=np.asarray(right_hand_sides),
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        raise ValueError(f"phase LP failed: {result.message}")

    theta = [0.0] * vertex_count
    for vertex, column in angle_column.items():
        theta[vertex] = float(result.x[column])
    corrections = phase_corrections(theta, edges)
    if any(abs(value) > maximum_correction + 1e-8 for value in corrections):
        raise AssertionError("solver returned a correction outside the fixed branch")
    linear_values = buswise_bounds(
        vertex_count,
        edges,
        corrections,
        linearized=True,
        bus_offsets=offsets,
    )
    exact_values = buswise_bounds(
        vertex_count,
        edges,
        corrections,
        linearized=False,
        bus_offsets=offsets,
    )
    linear_bound = max(linear_values)
    exact_bound = max(exact_values)
    if not math.isclose(
        linear_bound, float(result.fun), rel_tol=1e-7, abs_tol=1e-8
    ):
        raise AssertionError("independent LP objective check failed")
    return SparsePhaseProjection(
        tuple(theta),
        corrections,
        linear_bound,
        exact_bound,
        int(result.status),
        str(result.message),
    )


def solve_weighted_phase_least_squares(
    vertex_count: int,
    edge_iterable: Iterable[PhaseEdge],
    *,
    root: int = 0,
) -> SparsePhaseProjection:
    """Weighted phase-only least-squares comparator on a fixed branch."""

    edges = tuple(edge_iterable)
    _validate_graph(vertex_count, edges, root)
    nonroot = [vertex for vertex in range(vertex_count) if vertex != root]
    angle_column = {vertex: index for index, vertex in enumerate(nonroot)}
    matrix = np.zeros((len(edges), len(nonroot)))
    target = np.zeros(len(edges))
    for row, edge in enumerate(edges):
        scale = math.sqrt(edge.weight)
        if edge.u != root:
            matrix[row, angle_column[edge.u]] += scale
        if edge.v != root:
            matrix[row, angle_column[edge.v]] -= scale
        target[row] = scale * edge.phase
    solution, _, _, _ = np.linalg.lstsq(matrix, target, rcond=None)
    theta = [0.0] * vertex_count
    for vertex, column in angle_column.items():
        theta[vertex] = float(solution[column])
    corrections = phase_corrections(theta, edges)
    return SparsePhaseProjection(
        tuple(theta),
        corrections,
        max(buswise_bounds(vertex_count, edges, corrections, linearized=True)),
        max(buswise_bounds(vertex_count, edges, corrections, linearized=False)),
        0,
        "weighted least squares",
    )


def solve_tree_phase_recovery(
    vertex_count: int,
    edge_iterable: Iterable[PhaseEdge],
    tree_edge_indices: Iterable[int],
    *,
    root: int = 0,
) -> SparsePhaseProjection:
    """Recover phases by exactly matching a selected spanning tree."""

    edges = tuple(edge_iterable)
    _validate_graph(vertex_count, edges, root)
    selected = tuple(tree_edge_indices)
    if len(selected) != vertex_count - 1 or len(set(selected)) != len(selected):
        raise ValueError("tree selection must contain n-1 distinct edges")
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(vertex_count)
    ]
    for edge_index in selected:
        if edge_index < 0 or edge_index >= len(edges):
            raise ValueError("tree edge index is outside the edge list")
        edge = edges[edge_index]
        adjacency[edge.u].append((edge.v, edge_index))
        adjacency[edge.v].append((edge.u, edge_index))

    theta: list[float | None] = [None] * vertex_count
    theta[root] = 0.0
    stack = [root]
    while stack:
        u = stack.pop()
        assert theta[u] is not None
        for v, edge_index in adjacency[u]:
            if theta[v] is not None:
                continue
            edge = edges[edge_index]
            if edge.u == u:
                theta[v] = theta[u] - edge.phase
            else:
                theta[v] = theta[u] + edge.phase
            stack.append(v)
    if any(value is None for value in theta):
        raise ValueError("selected edges are not a spanning tree")
    recovered = tuple(float(value) for value in theta if value is not None)
    corrections = phase_corrections(recovered, edges)
    return SparsePhaseProjection(
        recovered,
        corrections,
        max(buswise_bounds(vertex_count, edges, corrections, linearized=True)),
        max(buswise_bounds(vertex_count, edges, corrections, linearized=False)),
        0,
        "spanning-tree recovery",
    )
