"""Edge-rank and cycle-holonomy certificates for complex voltage moments."""

from __future__ import annotations

import cmath
import math
from collections import deque
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class EdgeMoment:
    """A stored oriented edge moment W_uv = v_u conjugate(v_v)."""

    u: int
    v: int
    value: complex


@dataclass(frozen=True)
class DefectRepairCertificate:
    """A conservative defect-to-feasibility Newton certificate."""

    certified: bool
    residual_bound: float
    newton_step_bound: float
    h_bound: float
    radius_bound: float | None


def _edge_map(edges: Iterable[EdgeMoment]) -> dict[tuple[int, int], complex]:
    result: dict[tuple[int, int], complex] = {}
    for edge in edges:
        if edge.u == edge.v:
            raise ValueError("self-loops are not supported")
        if (edge.u, edge.v) in result or (edge.v, edge.u) in result:
            raise ValueError(f"duplicate undirected edge {edge.u}-{edge.v}")
        result[(edge.u, edge.v)] = complex(edge.value)
    return result


def oriented_value(
    edge_values: Mapping[tuple[int, int], complex], u: int, v: int
) -> complex:
    """Return W_uv, conjugating a stored reverse orientation if necessary."""

    if (u, v) in edge_values:
        return edge_values[(u, v)]
    if (v, u) in edge_values:
        return edge_values[(v, u)].conjugate()
    raise KeyError(f"missing edge {u}-{v}")


def radial_defect(diagonal: Mapping[int, float], edge: EdgeMoment) -> float:
    """Return 1-|W_uv|^2/(W_uu W_vv)."""

    product = float(diagonal[edge.u]) * float(diagonal[edge.v])
    if product <= 0:
        raise ValueError("all endpoint diagonal moments must be positive")
    return 1.0 - abs(edge.value) ** 2 / product


def cycle_holonomy(edges: Iterable[EdgeMoment], cycle: Sequence[int]) -> complex:
    """Return the product of normalized edge phases around a cycle."""

    if len(cycle) < 3:
        raise ValueError("a cycle must contain at least three vertices")
    edge_values = _edge_map(edges)
    product = 1.0 + 0.0j
    for index, u in enumerate(cycle):
        v = cycle[(index + 1) % len(cycle)]
        value = oriented_value(edge_values, u, v)
        if value == 0:
            raise ValueError("holonomy is undefined for a zero edge moment")
        product *= value / abs(value)
    return product


def cycle_phase_defect(edges: Iterable[EdgeMoment], cycle: Sequence[int]) -> float:
    """Return |1-H_C| for the normalized cycle holonomy H_C."""

    return abs(1.0 - cycle_holonomy(edges, cycle))


def reconstruct_from_tree(
    diagonal: Mapping[int, float],
    edges: Iterable[EdgeMoment],
    tree_edges: Iterable[tuple[int, int]],
    root: int,
) -> dict[int, complex]:
    """Recover voltage magnitudes and phases using a spanning tree.

    The result exactly matches the specified diagonal moments and the phases,
    though not necessarily the magnitudes, of the selected tree-edge moments.
    """

    if root not in diagonal:
        raise KeyError(f"root {root} has no diagonal moment")
    if any(float(value) <= 0 for value in diagonal.values()):
        raise ValueError("all diagonal moments must be positive")

    edge_values = _edge_map(edges)
    adjacency: dict[int, list[int]] = {vertex: [] for vertex in diagonal}
    for u, v in tree_edges:
        if u not in adjacency or v not in adjacency:
            raise KeyError(f"tree edge {u}-{v} has an unknown endpoint")
        oriented_value(edge_values, u, v)
        adjacency[u].append(v)
        adjacency[v].append(u)

    voltage: dict[int, complex] = {root: complex(math.sqrt(diagonal[root]))}
    queue: deque[int] = deque([root])
    while queue:
        u = queue.popleft()
        theta_u = cmath.phase(voltage[u])
        for v in adjacency[u]:
            if v in voltage:
                continue
            theta_v = theta_u - cmath.phase(oriented_value(edge_values, u, v))
            voltage[v] = math.sqrt(diagonal[v]) * cmath.exp(1j * theta_v)
            queue.append(v)

    if set(voltage) != set(diagonal):
        missing = sorted(set(diagonal) - set(voltage))
        raise ValueError(f"tree edges do not connect all vertices: {missing}")
    return voltage


def edge_residual(voltage: Mapping[int, complex], edge: EdgeMoment) -> float:
    """Return |v_u conjugate(v_v)-W_uv|."""

    recovered = voltage[edge.u] * voltage[edge.v].conjugate()
    return abs(recovered - edge.value)


def residual_identity(
    diagonal: Mapping[int, float],
    voltage: Mapping[int, complex],
    edge: EdgeMoment,
) -> tuple[float, float]:
    """Return both sides of the squared residual identity."""

    recovered = voltage[edge.u] * voltage[edge.v].conjugate()
    a = math.sqrt(diagonal[edge.u] * diagonal[edge.v])
    b = abs(edge.value)
    if b == 0:
        delta = 0.0
    else:
        delta = cmath.phase(recovered / edge.value)
    left = abs(recovered - edge.value) ** 2
    right = (a - b) ** 2 + 2.0 * a * b * (1.0 - math.cos(delta))
    return left, right


def residual_from_defects(
    diagonal: Mapping[int, float],
    edge: EdgeMoment,
    phase_defect: float,
) -> float:
    """Compute the recovery residual from radial and phase defects.

    ``phase_defect`` is |1-exp(i delta)|, where delta is the phase mismatch
    induced by the selected spanning-tree recovery.  For a tree edge it is
    zero; for a non-tree edge it is the corresponding fundamental-cycle
    defect.
    """

    r = radial_defect(diagonal, edge)
    if r < -1e-12 or r > 1.0 + 1e-12:
        raise ValueError("the edge moment does not satisfy its 2x2 PSD bound")
    if phase_defect < 0 or phase_defect > 2.0 + 1e-12:
        raise ValueError("a phase defect must lie in [0, 2]")
    r = min(1.0, max(0.0, r))
    h = min(2.0, phase_defect)
    a = math.sqrt(diagonal[edge.u] * diagonal[edge.v])
    magnitude_ratio = math.sqrt(1.0 - r)
    squared = (
        (1.0 - magnitude_ratio) ** 2
        + magnitude_ratio * h**2
    )
    return a * math.sqrt(max(0.0, squared))


def injection_residual_bound(
    vertex: int,
    incident_edges: Iterable[tuple[EdgeMoment, float]],
    admittance_magnitudes: Mapping[int, float],
    diagonal: Mapping[int, float],
) -> float:
    """Bound an AC bus-injection residual after voltage recovery.

    The complex injection map in moment variables is
    S_i(W) = sum_j conjugate(Y_ij) W_ij.  If the diagonal is preserved, the
    triangle inequality gives sum_j |Y_ij| |W_hat_ij-W_ij|.  Each incident
    item contains an edge and its tree-induced phase defect.
    """

    total = 0.0
    for edge, phase_defect in incident_edges:
        if vertex == edge.u:
            neighbor = edge.v
        elif vertex == edge.v:
            neighbor = edge.u
        else:
            raise ValueError(f"edge {edge.u}-{edge.v} is not incident to {vertex}")
        total += (
            float(admittance_magnitudes[neighbor])
            * residual_from_defects(diagonal, edge, phase_defect)
        )
    return total


def defect_to_repair_certificate(
    residual_bound: float,
    inverse_jacobian_norm: float,
    jacobian_lipschitz: float,
) -> DefectRepairCertificate:
    """Compose a physical-residual bound with Newton--Kantorovich.

    If rho bounds ||F(x0)-p||, beta bounds ||DF(x0)^-1||, and the Jacobian is
    L-Lipschitz, then eta <= beta*rho and h <= beta^2*L*rho.  The returned
    radius is therefore conservative; it uses only certified upper bounds.
    """

    rho = float(residual_bound)
    beta = float(inverse_jacobian_norm)
    lipschitz = float(jacobian_lipschitz)
    if rho < 0 or beta < 0 or lipschitz < 0:
        raise ValueError("certificate inputs must be nonnegative")
    eta_bound = beta * rho
    h_bound = beta * lipschitz * eta_bound
    denominator = beta * lipschitz
    if not math.isfinite(h_bound) or h_bound > 0.5:
        return DefectRepairCertificate(
            False, rho, eta_bound, h_bound, None
        )
    if denominator == 0.0:
        radius = eta_bound
    else:
        radius = (
            1.0 - math.sqrt(max(0.0, 1.0 - 2.0 * h_bound))
        ) / denominator
    return DefectRepairCertificate(
        True, rho, eta_bound, h_bound, radius
    )


def principal_angle(angle: float) -> float:
    """Wrap an angle to (-pi, pi]."""

    wrapped = (float(angle) + math.pi) % (2.0 * math.pi) - math.pi
    if wrapped <= -math.pi:
        return math.pi
    return wrapped


def balanced_unit_triangle_recovery(
    edges: Iterable[EdgeMoment],
) -> dict[int, complex]:
    """Distribute a unit-triangle holonomy equally across its three edges.

    The expected stored orientations are 0->1, 1->2, and 0->2, and all edge
    magnitudes must be one.  This is the equal-weight phase projection.
    """

    edge_values = _edge_map(edges)
    w01 = oriented_value(edge_values, 0, 1)
    w12 = oriented_value(edge_values, 1, 2)
    w02 = oriented_value(edge_values, 0, 2)
    for value in (w01, w12, w02):
        if not math.isclose(abs(value), 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("balanced recovery requires unit edge magnitudes")

    alpha01 = cmath.phase(w01)
    alpha12 = cmath.phase(w12)
    alpha02 = cmath.phase(w02)
    holonomy_angle = principal_angle(alpha01 + alpha12 - alpha02)
    corrected01 = alpha01 - holonomy_angle / 3.0
    corrected12 = alpha12 - holonomy_angle / 3.0
    theta0 = 0.0
    theta1 = theta0 - corrected01
    theta2 = theta1 - corrected12
    return {
        0: cmath.exp(1j * theta0),
        1: cmath.exp(1j * theta1),
        2: cmath.exp(1j * theta2),
    }
