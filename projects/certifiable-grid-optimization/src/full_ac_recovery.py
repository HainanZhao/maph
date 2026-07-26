"""Recovery and residual scoring for edge-relaxed complex AC moments."""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from typing import Iterable

import numpy as np

from src.ac_power_flow import (
    BUS_TYPE,
    PQ,
    REF,
    build_ybus,
    complex_injections,
    polar_jacobian,
)
from src.matpower import MatpowerCase
from src.sparse_phase_lp import (
    PhaseEdge,
    SparsePhaseProjection,
    solve_minimax_phase_lp,
    solve_tree_phase_recovery,
    solve_weighted_phase_least_squares,
)


@dataclass(frozen=True)
class FullACRecovery:
    """A rank-one voltage recovered from edge-relaxed moment data."""

    voltage_magnitudes: tuple[float, ...]
    voltage_angles: tuple[float, ...]
    phase_projection: SparsePhaseProjection


@dataclass(frozen=True)
class FullACRecoveryScore:
    """Exact residuals and local conditioning at a recovered voltage."""

    injection_residual_inf: float
    moment_residual_bound: float
    inverse_reduced_jacobian_inf: float
    newton_step_upper_bound: float


def edge_pairs(ybus: np.ndarray, *, tolerance: float = 1e-12) -> tuple[tuple[int, int], ...]:
    """Return undirected bus pairs represented in Ybus."""

    count = ybus.shape[0]
    return tuple(
        (u, v)
        for u in range(count)
        for v in range(u + 1, count)
        if abs(ybus[u, v]) > tolerance or abs(ybus[v, u]) > tolerance
    )


def relaxed_injections(ybus: np.ndarray, moments: np.ndarray) -> np.ndarray:
    """Evaluate S_i = sum_j conjugate(Y_ij) W_ij."""

    if moments.shape != ybus.shape:
        raise ValueError("moment matrix and Ybus must have equal shape")
    return np.sum(np.conj(ybus) * moments, axis=1)


def generate_edge_relaxed_moments(
    ybus: np.ndarray,
    voltage_magnitudes: Iterable[float],
    voltage_angles: Iterable[float],
    rng: np.random.Generator,
    *,
    phase_sigma: float,
    radial_sigma: float,
) -> np.ndarray:
    """Generate locally PSD edge moments around a physical voltage."""

    if phase_sigma < 0 or radial_sigma < 0:
        raise ValueError("noise scales must be nonnegative")
    vm = np.asarray(tuple(voltage_magnitudes), dtype=float)
    va = np.asarray(tuple(voltage_angles), dtype=float)
    if len(vm) != ybus.shape[0] or vm.shape != va.shape:
        raise ValueError("voltage and Ybus dimensions do not match")
    moments = np.zeros_like(ybus, dtype=complex)
    moments[np.diag_indices(len(vm))] = vm * vm
    for u, v in edge_pairs(ybus):
        physical = vm[u] * vm[v] * cmath.exp(1j * (va[u] - va[v]))
        contraction = math.exp(-abs(float(rng.normal(0.0, radial_sigma))))
        phase_error = float(rng.normal(0.0, phase_sigma))
        perturbed = physical * contraction * cmath.exp(1j * phase_error)
        moments[u, v] = perturbed
        moments[v, u] = np.conj(perturbed)
    return moments


def _phase_problem(
    ybus: np.ndarray, moments: np.ndarray
) -> tuple[tuple[PhaseEdge, ...], tuple[float, ...]]:
    count = ybus.shape[0]
    diagonal = np.real(np.diag(moments))
    if np.any(diagonal <= 0):
        raise ValueError("moment diagonals must be positive")
    vm = np.sqrt(diagonal)
    offsets = [0.0] * count
    edges = []
    for u, v in edge_pairs(ybus):
        target = moments[u, v]
        if abs(target) == 0:
            raise ValueError("edge moment must be nonzero for phase recovery")
        rank_one_magnitude = vm[u] * vm[v]
        radial_defect = abs(rank_one_magnitude - abs(target))
        admittance_weight = max(abs(ybus[u, v]), abs(ybus[v, u]))
        edges.append(
            PhaseEdge(
                u,
                v,
                cmath.phase(target),
                admittance_weight * rank_one_magnitude,
            )
        )
        radial_contribution = admittance_weight * radial_defect
        offsets[u] += radial_contribution
        offsets[v] += radial_contribution
    return tuple(edges), tuple(offsets)


def maximum_weight_spanning_tree(edges: Iterable[PhaseEdge], vertex_count: int) -> tuple[int, ...]:
    """Return edge indices for a deterministic maximum-weight spanning tree."""

    edge_tuple = tuple(edges)
    parent = list(range(vertex_count))

    def representative(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    selected = []
    for index in sorted(
        range(len(edge_tuple)),
        key=lambda item: (-edge_tuple[item].weight, item),
    ):
        edge = edge_tuple[index]
        u_root = representative(edge.u)
        v_root = representative(edge.v)
        if u_root == v_root:
            continue
        parent[u_root] = v_root
        selected.append(index)
        if len(selected) == vertex_count - 1:
            return tuple(selected)
    raise ValueError("phase graph is disconnected")


def recover_full_ac_candidates(
    case: MatpowerCase, moments: np.ndarray
) -> dict[str, FullACRecovery]:
    """Recover voltages with radial-aware LP and standard phase comparators."""

    ybus = build_ybus(case)
    if moments.shape != ybus.shape:
        raise ValueError("moment matrix has the wrong shape")
    reference = np.flatnonzero(case.bus[:, BUS_TYPE].astype(int) == REF)
    if len(reference) != 1:
        raise ValueError("exactly one reference bus is required")
    root = int(reference[0])
    vm = tuple(float(math.sqrt(value.real)) for value in np.diag(moments))
    edges, offsets = _phase_problem(ybus, moments)
    tree = maximum_weight_spanning_tree(edges, len(vm))
    projections = {
        "radial-aware minimax LP": solve_minimax_phase_lp(
            len(vm), edges, root=root, bus_offsets=offsets
        ),
        "phase-only minimax LP": solve_minimax_phase_lp(
            len(vm), edges, root=root
        ),
        "weighted phase LS": solve_weighted_phase_least_squares(
            len(vm), edges, root=root
        ),
        "maximum-weight tree": solve_tree_phase_recovery(
            len(vm), edges, tree, root=root
        ),
    }
    return {
        name: FullACRecovery(vm, projection.theta, projection)
        for name, projection in projections.items()
    }


def recovered_moments(recovery: FullACRecovery) -> np.ndarray:
    voltage = np.asarray(recovery.voltage_magnitudes) * np.exp(
        1j * np.asarray(recovery.voltage_angles)
    )
    return np.outer(voltage, np.conj(voltage))


def reduced_power_flow_jacobian(
    case: MatpowerCase,
    ybus: np.ndarray,
    voltage_magnitudes: Iterable[float],
    voltage_angles: Iterable[float],
) -> np.ndarray:
    bus_types = case.bus[:, BUS_TYPE].astype(int)
    nonreference = np.flatnonzero(bus_types != REF)
    pq = np.flatnonzero(bus_types == PQ)
    full = polar_jacobian(
        ybus, tuple(voltage_magnitudes), tuple(voltage_angles)
    )
    count = case.bus.shape[0]
    indices = np.concatenate((nonreference, count + pq))
    return full[np.ix_(indices, indices)]


def score_full_ac_recovery(
    case: MatpowerCase,
    moments: np.ndarray,
    recovery: FullACRecovery,
) -> FullACRecoveryScore:
    """Score exact P/Q mismatch and a rigorous moment residual bound."""

    ybus = build_ybus(case)
    recovered = recovered_moments(recovery)
    relaxed_s = relaxed_injections(ybus, moments)
    recovered_s = complex_injections(
        ybus,
        recovery.voltage_magnitudes,
        recovery.voltage_angles,
    )
    exact_residual = float(np.max(np.abs(recovered_s - relaxed_s)))
    buswise_bound = np.sum(np.abs(ybus) * np.abs(recovered - moments), axis=1)
    residual_bound = float(np.max(buswise_bound))
    reduced = reduced_power_flow_jacobian(
        case,
        ybus,
        recovery.voltage_magnitudes,
        recovery.voltage_angles,
    )
    try:
        inverse_norm = float(
            np.linalg.norm(np.linalg.inv(reduced), ord=np.inf)
        )
    except np.linalg.LinAlgError:
        inverse_norm = math.inf
    return FullACRecoveryScore(
        exact_residual,
        residual_bound,
        inverse_norm,
        inverse_norm * residual_bound,
    )
