"""Conditioning bounds for fixed-magnitude lossless power-flow graphs."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence

import numpy as np

from src.sparse_phase_lp import PhaseEdge, SparsePhaseProjection


@dataclass(frozen=True)
class GraphRepairScore:
    """A conservative beta^2 L rho repair score."""

    residual_bound: float
    inverse_jacobian_inf: float
    jacobian_lipschitz: float
    h_bound: float
    certified: bool


@dataclass(frozen=True)
class ReferenceConditioningBound:
    """A Banach-lemma inverse-Jacobian bound in an angle trust region."""

    reference_inverse_jacobian_inf: float
    jacobian_lipschitz: float
    radius: float
    inverse_jacobian_upper_bound: float


def reduced_jacobian(
    vertex_count: int,
    edges: Iterable[PhaseEdge],
    theta: Sequence[float],
    *,
    root: int = 0,
) -> np.ndarray:
    """Return the reduced active-power Jacobian."""

    nonroot = [vertex for vertex in range(vertex_count) if vertex != root]
    column = {vertex: index for index, vertex in enumerate(nonroot)}
    matrix = np.zeros((len(nonroot), len(nonroot)))
    for edge in edges:
        coefficient = edge.weight * math.cos(
            float(theta[edge.u]) - float(theta[edge.v])
        )
        if edge.u != root:
            matrix[column[edge.u], column[edge.u]] += coefficient
            if edge.v != root:
                matrix[column[edge.u], column[edge.v]] -= coefficient
        if edge.v != root:
            matrix[column[edge.v], column[edge.v]] += coefficient
            if edge.u != root:
                matrix[column[edge.v], column[edge.u]] -= coefficient
    return matrix


def jacobian_lipschitz_bound(
    vertex_count: int,
    edges: Iterable[PhaseEdge],
    *,
    root: int = 0,
) -> float:
    """Global infinity-norm Lipschitz bound for the reduced Jacobian."""

    row_bounds = [0.0] * vertex_count
    for edge in edges:
        if edge.u != root:
            row_bounds[edge.u] += edge.weight * (
                1.0 if edge.v == root else 4.0
            )
        if edge.v != root:
            row_bounds[edge.v] += edge.weight * (
                1.0 if edge.u == root else 4.0
            )
    return max(row_bounds[vertex] for vertex in range(vertex_count) if vertex != root)


def score_projection(
    vertex_count: int,
    edges: Iterable[PhaseEdge],
    projection: SparsePhaseProjection,
    *,
    root: int = 0,
) -> GraphRepairScore:
    """Score a phase projection using the conservative repair condition."""

    edge_tuple = tuple(edges)
    matrix = reduced_jacobian(
        vertex_count, edge_tuple, projection.theta, root=root
    )
    try:
        inverse = np.linalg.inv(matrix)
        beta = float(np.linalg.norm(inverse, ord=np.inf))
    except np.linalg.LinAlgError:
        beta = math.inf
    lipschitz = jacobian_lipschitz_bound(
        vertex_count, edge_tuple, root=root
    )
    rho = projection.exact_bound
    h_bound = beta * beta * lipschitz * rho
    return GraphRepairScore(
        rho,
        beta,
        lipschitz,
        h_bound,
        math.isfinite(h_bound) and h_bound <= 0.5,
    )


def reference_conditioning_bound(
    vertex_count: int,
    edges: Iterable[PhaseEdge],
    reference_theta: Sequence[float],
    radius: float,
    *,
    root: int = 0,
) -> ReferenceConditioningBound:
    """Bound inverse-Jacobian norms throughout an angle trust region.

    The radius is the infinity-norm displacement of the reduced angle
    vector.  The result is infinite when the Banach perturbation condition
    cannot certify invertibility throughout the region.
    """

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    edge_tuple = tuple(edges)
    reference_matrix = reduced_jacobian(
        vertex_count, edge_tuple, reference_theta, root=root
    )
    try:
        reference_inverse = np.linalg.inv(reference_matrix)
        beta_zero = float(np.linalg.norm(reference_inverse, ord=np.inf))
    except np.linalg.LinAlgError:
        beta_zero = math.inf
    lipschitz = jacobian_lipschitz_bound(
        vertex_count, edge_tuple, root=root
    )
    denominator = 1.0 - beta_zero * lipschitz * radius
    if denominator <= 0 or not math.isfinite(denominator):
        upper_bound = math.inf
    else:
        upper_bound = beta_zero / denominator
    return ReferenceConditioningBound(
        beta_zero,
        lipschitz,
        radius,
        upper_bound,
    )
