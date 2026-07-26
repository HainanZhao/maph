"""Certificate-aware allocation of cycle phase inconsistency."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from src.lossless_triangle import (
    global_jacobian_lipschitz,
    inverse_inf_norm,
    jacobian,
)


@dataclass(frozen=True)
class TriangleProjection:
    """A nonnegative allocation of a principal triangle holonomy."""

    allocation: tuple[float, float, float]
    worst_bus_bound: float


@dataclass(frozen=True)
class ConditionedTriangleProjection:
    """A phase allocation scored by a conditioning-aware repair bound."""

    allocation: tuple[float, float, float]
    theta: tuple[float, float]
    residual_bound: float
    inverse_jacobian_inf: float
    h_bound: float


def edge_phase_residual(angle: float) -> float:
    """Unit-magnitude edge moment error for a phase correction."""

    return 2.0 * abs(math.sin(0.5 * float(angle)))


def phase_linearization_factor(maximum_angle: float) -> float:
    """Return 2 sin(gamma/2)/gamma for gamma in [0, pi]."""

    gamma = float(maximum_angle)
    if gamma < 0 or gamma > math.pi:
        raise ValueError("maximum_angle must lie in [0, pi]")
    if gamma == 0.0:
        return 1.0
    return 2.0 * math.sin(gamma / 2.0) / gamma


def triangle_worst_bus_bound(
    allocation: Sequence[float],
    edge_weights: Sequence[float] = (1.0, 1.0, 1.0),
) -> float:
    """Return the worst buswise weighted edge-residual sum.

    Edge order is (01, 12, 20).  Each bus is incident to two of these edges.
    """

    if len(allocation) != 3 or len(edge_weights) != 3:
        raise ValueError("a triangle requires three allocations and weights")
    if any(value < 0 for value in allocation):
        raise ValueError("allocation magnitudes must be nonnegative")
    if any(weight < 0 for weight in edge_weights):
        raise ValueError("edge weights must be nonnegative")
    contributions = [
        float(weight) * edge_phase_residual(value)
        for value, weight in zip(allocation, edge_weights)
    ]
    return max(
        contributions[0] + contributions[2],
        contributions[0] + contributions[1],
        contributions[1] + contributions[2],
    )


def triangle_linear_worst_bus_bound(
    allocation: Sequence[float],
    edge_weights: Sequence[float] = (1.0, 1.0, 1.0),
) -> float:
    """Worst-bus surrogate using |x| in place of 2sin(|x|/2)."""

    if len(allocation) != 3 or len(edge_weights) != 3:
        raise ValueError("a triangle requires three allocations and weights")
    contributions = [
        float(weight) * abs(float(value))
        for value, weight in zip(allocation, edge_weights)
    ]
    return max(
        contributions[0] + contributions[2],
        contributions[0] + contributions[1],
        contributions[1] + contributions[2],
    )


def balanced_triangle_projection(
    holonomy_angle: float,
    edge_weights: Sequence[float] = (1.0, 1.0, 1.0),
) -> TriangleProjection:
    """Split the principal holonomy magnitude equally among all edges."""

    magnitude = abs(float(holonomy_angle))
    allocation = (magnitude / 3.0,) * 3
    return TriangleProjection(
        allocation,
        triangle_worst_bus_bound(allocation, edge_weights),
    )


def best_tree_triangle_projection(
    holonomy_angle: float,
    edge_weights: Sequence[float] = (1.0, 1.0, 1.0),
) -> TriangleProjection:
    """Put all inconsistency on the best single non-tree edge."""

    magnitude = abs(float(holonomy_angle))
    candidates = []
    for index in range(3):
        allocation = [0.0, 0.0, 0.0]
        allocation[index] = magnitude
        candidate = tuple(allocation)
        candidates.append(
            TriangleProjection(
                candidate,
                triangle_worst_bus_bound(candidate, edge_weights),
            )
        )
    return min(candidates, key=lambda item: item.worst_bus_bound)


def grid_optimal_triangle_projection(
    holonomy_angle: float,
    edge_weights: Sequence[float] = (1.0, 1.0, 1.0),
    grid_steps: int = 600,
) -> TriangleProjection:
    """Exhaustively optimize the triangle allocation on a rational grid.

    This is a reproducible finite computation, not a continuous optimality
    certificate.  ``grid_steps`` subdivisions are used for the total
    principal holonomy magnitude.
    """

    magnitude = abs(float(holonomy_angle))
    if magnitude > math.pi + 1e-12:
        raise ValueError("use a principal holonomy angle in [-pi, pi]")
    if grid_steps <= 0:
        raise ValueError("grid_steps must be positive")

    best: TriangleProjection | None = None
    for first_index in range(grid_steps + 1):
        first = magnitude * first_index / grid_steps
        for second_index in range(grid_steps - first_index + 1):
            second = magnitude * second_index / grid_steps
            third_index = grid_steps - first_index - second_index
            third = magnitude * third_index / grid_steps
            allocation = (first, second, third)
            candidate = TriangleProjection(
                allocation,
                triangle_worst_bus_bound(allocation, edge_weights),
            )
            if best is None or candidate.worst_bus_bound < best.worst_bus_bound:
                best = candidate
    assert best is not None
    return best


def triangle_angles_from_allocation(
    measured_oriented_phases: Sequence[float],
    allocation: Sequence[float],
) -> tuple[float, float]:
    """Recover bus angles after allocating an oriented cycle inconsistency.

    Phase order is 0->1, 1->2, 2->0.  The allocations are nonnegative
    magnitudes with sum equal to the absolute principal holonomy.  Corrections
    are applied with the opposite sign of that holonomy.
    """

    if len(measured_oriented_phases) != 3 or len(allocation) != 3:
        raise ValueError("a triangle requires three phases and allocations")
    raw_holonomy = sum(float(value) for value in measured_oriented_phases)
    holonomy = (raw_holonomy + math.pi) % (2.0 * math.pi) - math.pi
    if not math.isclose(
        sum(allocation), abs(holonomy), rel_tol=0.0, abs_tol=1e-9
    ):
        raise ValueError("allocation must sum to the principal holonomy magnitude")
    direction = -1.0 if holonomy > 0 else (1.0 if holonomy < 0 else 0.0)
    corrected01 = measured_oriented_phases[0] + direction * allocation[0]
    corrected12 = measured_oriented_phases[1] + direction * allocation[1]
    theta1 = -corrected01
    theta2 = theta1 - corrected12
    return theta1, theta2


def conditioned_triangle_projection(
    measured_oriented_phases: Sequence[float],
    allocation: Sequence[float],
    line_weights: Sequence[float] = (1.0, 1.0, 1.0),
) -> ConditionedTriangleProjection:
    """Score an allocation by beta^2 L rho on the lossless triangle."""

    if len(line_weights) != 3:
        raise ValueError("line weights must be (b01, b12, b02)")
    theta = triangle_angles_from_allocation(
        measured_oriented_phases, allocation
    )
    rho = triangle_worst_bus_bound(allocation, line_weights)
    b01, b12, b02 = (float(value) for value in line_weights)
    try:
        beta = inverse_inf_norm(jacobian(theta, b01, b12, b02))
    except ValueError:
        beta = math.inf
    lipschitz = global_jacobian_lipschitz(b01, b12, b02)
    h_bound = beta * beta * lipschitz * rho
    return ConditionedTriangleProjection(
        tuple(float(value) for value in allocation),
        theta,
        rho,
        beta,
        h_bound,
    )


def grid_optimal_conditioned_triangle_projection(
    measured_oriented_phases: Sequence[float],
    line_weights: Sequence[float] = (1.0, 1.0, 1.0),
    grid_steps: int = 300,
) -> ConditionedTriangleProjection:
    """Grid-search the conditioning-aware bound beta^2 L rho."""

    raw_holonomy = sum(float(value) for value in measured_oriented_phases)
    holonomy = (raw_holonomy + math.pi) % (2.0 * math.pi) - math.pi
    magnitude = abs(holonomy)
    best: ConditionedTriangleProjection | None = None
    for first_index in range(grid_steps + 1):
        first = magnitude * first_index / grid_steps
        for second_index in range(grid_steps - first_index + 1):
            second = magnitude * second_index / grid_steps
            third_index = grid_steps - first_index - second_index
            third = magnitude * third_index / grid_steps
            candidate = conditioned_triangle_projection(
                measured_oriented_phases,
                (first, second, third),
                line_weights,
            )
            if best is None or candidate.h_bound < best.h_bound:
                best = candidate
    assert best is not None
    return best
