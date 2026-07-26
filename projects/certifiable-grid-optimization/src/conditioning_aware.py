"""Conditioning-aware selection from a family of tractable phase LPs."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence

from src.lossless_graph import (
    GraphRepairScore,
    ReferenceConditioningBound,
    reference_conditioning_bound,
    score_projection,
)
from src.sparse_phase_lp import (
    PhaseEdge,
    SparsePhaseProjection,
    solve_minimax_phase_lp,
)


@dataclass(frozen=True)
class ConditioningAwareResult:
    """The best verified candidate from a trust-region LP sweep."""

    projection: SparsePhaseProjection
    score: GraphRepairScore
    radius: float
    reference_bound: ReferenceConditioningBound
    attempted_radii: tuple[float, ...]


def solve_conditioning_aware_sweep(
    vertex_count: int,
    edge_iterable: Iterable[PhaseEdge],
    reference_theta: Sequence[float],
    radii: Iterable[float],
    *,
    root: int = 0,
) -> ConditioningAwareResult:
    """Solve trust-region LPs and select the smallest verified repair score."""

    edges = tuple(edge_iterable)
    radius_values = tuple(sorted(set(float(radius) for radius in radii)))
    if not radius_values:
        raise ValueError("at least one trust-region radius is required")
    if radius_values[0] < 0:
        raise ValueError("trust-region radii must be nonnegative")

    candidates = []
    for radius in radius_values:
        projection = solve_minimax_phase_lp(
            vertex_count,
            edges,
            root=root,
            angle_center=reference_theta,
            maximum_angle_displacement=radius,
        )
        score = score_projection(
            vertex_count, edges, projection, root=root
        )
        reference_bound = reference_conditioning_bound(
            vertex_count,
            edges,
            reference_theta,
            radius,
            root=root,
        )
        candidates.append((projection, score, radius, reference_bound))

    projection, score, radius, reference_bound = min(
        candidates,
        key=lambda candidate: (
            candidate[1].h_bound,
            candidate[0].exact_bound,
            candidate[2],
        ),
    )
    if not math.isfinite(score.h_bound):
        # The result remains useful diagnostically, but make the selection
        # deterministic when every candidate is singular.
        projection, score, radius, reference_bound = candidates[0]
    return ConditioningAwareResult(
        projection,
        score,
        radius,
        reference_bound,
        radius_values,
    )
