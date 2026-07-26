"""Edge-based SOCP relaxation of MATPOWER AC optimal power flow."""

from __future__ import annotations

from dataclasses import dataclass
import math

import cvxpy as cp
import numpy as np

from src.ac_power_flow import (
    ANGMAX,
    ANGMIN,
    F_BUS,
    GEN_BUS,
    GEN_STATUS,
    PD,
    QD,
    RATE_A,
    T_BUS,
    branch_admittances,
    build_ybus,
    bus_index,
)
from src.full_ac_recovery import edge_pairs, relaxed_injections
from src.matpower import MatpowerCase


QMAX, QMIN = 3, 4
PMAX, PMIN = 8, 9
VMAX, VMIN = 11, 12
MODEL, NCOST = 0, 3


@dataclass(frozen=True)
class SOCPSolution:
    """A solved edge-SOCP point."""

    status: str
    objective: float
    moments: np.ndarray
    generator_p: tuple[float, ...]
    generator_q: tuple[float, ...]
    thermal_limits_mva: tuple[float, ...]
    solve_time: float | None
    iterations: int | None


@dataclass(frozen=True)
class SOCPAudit:
    """Independently recomputed primal and objective violations."""

    hermitian: float
    voltage: float
    generator: float
    power_balance: float
    edge_psd: float
    angle: float
    thermal: float
    objective_difference: float

    @property
    def maximum_violation(self) -> float:
        return max(
            self.hermitian,
            self.voltage,
            self.generator,
            self.power_balance,
            self.edge_psd,
            self.angle,
            self.thermal,
            self.objective_difference,
        )


def _polynomial_cost_expression(
    case: MatpowerCase, generator_p: cp.Variable
) -> cp.Expression:
    if case.gencost is None or len(case.gencost) < len(case.gen):
        raise ValueError("active-power generator costs are required")
    terms = []
    for index, row in enumerate(case.gencost[: len(case.gen)]):
        if int(row[MODEL]) != 2:
            raise ValueError("only polynomial generator costs are supported")
        count = int(row[NCOST])
        coefficients = row[4 : 4 + count]
        if len(coefficients) != count or count < 1 or count > 3:
            raise ValueError("only constant, linear, and quadratic costs are supported")
        power_mw = case.base_mva * generator_p[index]
        if count == 3:
            quadratic, linear, constant = coefficients
            if quadratic < 0:
                raise ValueError("generator cost must be convex")
            terms.append(
                quadratic * cp.square(power_mw) + linear * power_mw + constant
            )
        elif count == 2:
            linear, constant = coefficients
            terms.append(linear * power_mw + constant)
        else:
            terms.append(float(coefficients[0]))
    return cp.sum(cp.hstack(terms))


def evaluate_generation_cost(
    case: MatpowerCase, generator_p: np.ndarray
) -> float:
    """Recompute the active generation cost from MATPOWER coefficients."""

    if case.gencost is None or len(case.gencost) < len(case.gen):
        raise ValueError("active-power generator costs are required")
    total = 0.0
    for power_pu, row in zip(generator_p, case.gencost[: len(case.gen)]):
        if int(row[MODEL]) != 2:
            raise ValueError("only polynomial generator costs are supported")
        count = int(row[NCOST])
        coefficients = row[4 : 4 + count]
        total += float(np.polyval(coefficients, case.base_mva * power_pu))
    return total


def _angle_constraints(
    case: MatpowerCase, moments: cp.Variable, mapping: dict[int, int]
) -> list[cp.Constraint]:
    constraints = []
    for row in case.branch:
        if row[10] <= 0:
            continue
        minimum = float(row[ANGMIN])
        maximum = float(row[ANGMAX])
        if minimum == 0 and maximum == 0:
            continue
        if minimum <= -360 and maximum >= 360:
            continue
        if minimum <= -90 or maximum >= 90:
            raise ValueError(
                "the tangent angle wedge requires bounds inside (-90, 90)"
            )
        u = mapping[int(row[F_BUS])]
        v = mapping[int(row[T_BUS])]
        real = cp.real(moments[u, v])
        imaginary = cp.imag(moments[u, v])
        constraints.extend(
            (
                real >= 0,
                imaginary >= math.tan(math.radians(minimum)) * real,
                imaginary <= math.tan(math.radians(maximum)) * real,
            )
        )
    return constraints


def solve_socp_relaxation(
    case: MatpowerCase,
    *,
    tolerance: float = 1e-8,
    maximum_iterations: int = 500,
    thermal_limits_mva: np.ndarray | None = None,
) -> SOCPSolution:
    """Solve the edge-PSD SOCP relaxation with Clarabel."""

    if tolerance <= 0 or maximum_iterations <= 0:
        raise ValueError("solver settings must be positive")
    count = len(case.bus)
    generator_count = len(case.gen)
    mapping = bus_index(case)
    ybus = build_ybus(case)
    pairs = set(edge_pairs(ybus))
    original_limits = case.branch[:, RATE_A].astype(float)
    if thermal_limits_mva is None:
        effective_limits = original_limits.copy()
    else:
        effective_limits = np.asarray(thermal_limits_mva, dtype=float)
        if effective_limits.shape != original_limits.shape:
            raise ValueError("thermal_limits_mva has the wrong shape")
        if np.any(effective_limits < 0):
            raise ValueError("thermal limits must be nonnegative")
        limited = original_limits > 0
        if np.any(effective_limits[limited] > original_limits[limited] + 1e-12):
            raise ValueError("adaptive thermal limits may not exceed case limits")

    moments = cp.Variable((count, count), hermitian=True, name="W")
    generator_p = cp.Variable(generator_count, name="Pg")
    generator_q = cp.Variable(generator_count, name="Qg")
    constraints: list[cp.Constraint] = []

    diagonal = cp.real(cp.diag(moments))
    constraints.extend(
        (
            diagonal >= np.square(case.bus[:, VMIN]),
            diagonal <= np.square(case.bus[:, VMAX]),
        )
    )
    for u in range(count):
        for v in range(u + 1, count):
            if (u, v) not in pairs:
                constraints.append(moments[u, v] == 0)
                continue
            constraints.append(
                cp.SOC(
                    diagonal[u] + diagonal[v],
                    cp.hstack(
                        (
                            2 * cp.real(moments[u, v]),
                            2 * cp.imag(moments[u, v]),
                            diagonal[u] - diagonal[v],
                        )
                    ),
                )
            )

    active = case.gen[:, GEN_STATUS] > 0
    lower_p = np.where(active, case.gen[:, PMIN], 0.0) / case.base_mva
    upper_p = np.where(active, case.gen[:, PMAX], 0.0) / case.base_mva
    lower_q = np.where(active, case.gen[:, QMIN], 0.0) / case.base_mva
    upper_q = np.where(active, case.gen[:, QMAX], 0.0) / case.base_mva
    constraints.extend(
        (
            generator_p >= lower_p,
            generator_p <= upper_p,
            generator_q >= lower_q,
            generator_q <= upper_q,
        )
    )

    injections = cp.sum(cp.multiply(np.conj(ybus), moments), axis=1)
    generators_by_bus = [[] for _ in range(count)]
    for generator_index, row in enumerate(case.gen):
        generators_by_bus[mapping[int(row[GEN_BUS])]].append(generator_index)
    for position in range(count):
        generator_indices = generators_by_bus[position]
        bus_p = (
            cp.sum(generator_p[generator_indices]) if generator_indices else 0.0
        )
        bus_q = (
            cp.sum(generator_q[generator_indices]) if generator_indices else 0.0
        )
        constraints.extend(
            (
                bus_p - case.bus[position, PD] / case.base_mva
                == cp.real(injections[position]),
                bus_q - case.bus[position, QD] / case.base_mva
                == cp.imag(injections[position]),
            )
        )

    constraints.extend(_angle_constraints(case, moments, mapping))
    for branch in branch_admittances(case):
        row = case.branch[branch.row_index]
        effective_limit_mva = effective_limits[branch.row_index]
        if effective_limit_mva <= 0:
            continue
        u, v = branch.from_bus, branch.to_bus
        from_flow = (
            np.conj(branch.y_ff) * moments[u, u]
            + np.conj(branch.y_ft) * moments[u, v]
        )
        to_flow = (
            np.conj(branch.y_tf) * moments[v, u]
            + np.conj(branch.y_tt) * moments[v, v]
        )
        limit = float(effective_limit_mva / case.base_mva)
        constraints.extend(
            (
                cp.norm(cp.hstack((cp.real(from_flow), cp.imag(from_flow))))
                <= limit,
                cp.norm(cp.hstack((cp.real(to_flow), cp.imag(to_flow))))
                <= limit,
            )
        )

    objective = cp.Minimize(_polynomial_cost_expression(case, generator_p))
    problem = cp.Problem(objective, constraints)
    problem.solve(
        solver=cp.CLARABEL,
        tol_gap_abs=tolerance,
        tol_gap_rel=tolerance,
        tol_feas=tolerance,
        max_iter=maximum_iterations,
        verbose=False,
    )
    if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        raise ValueError(f"SOCP solve failed with status {problem.status}")
    if moments.value is None or generator_p.value is None or generator_q.value is None:
        raise AssertionError("solver returned no primal point")
    stats = problem.solver_stats
    return SOCPSolution(
        str(problem.status),
        float(problem.value),
        np.asarray(moments.value, dtype=complex),
        tuple(float(value) for value in generator_p.value),
        tuple(float(value) for value in generator_q.value),
        tuple(float(value) for value in effective_limits),
        None if stats.solve_time is None else float(stats.solve_time),
        None if stats.num_iters is None else int(stats.num_iters),
    )


def _positive_violation(values: np.ndarray) -> float:
    return float(max(0.0, np.max(values)))


def audit_socp_solution(case: MatpowerCase, solution: SOCPSolution) -> SOCPAudit:
    """Recompute all modeled constraints without CVXPY expressions."""

    moments = solution.moments
    generator_p = np.asarray(solution.generator_p)
    generator_q = np.asarray(solution.generator_q)
    ybus = build_ybus(case)
    mapping = bus_index(case)
    diagonal = np.real(np.diag(moments))
    hermitian = float(
        max(
            np.max(np.abs(moments - moments.conj().T)),
            np.max(np.abs(np.imag(np.diag(moments)))),
        )
    )
    voltage = max(
        _positive_violation(np.square(case.bus[:, VMIN]) - diagonal),
        _positive_violation(diagonal - np.square(case.bus[:, VMAX])),
    )

    active = case.gen[:, GEN_STATUS] > 0
    lower_p = np.where(active, case.gen[:, PMIN], 0.0) / case.base_mva
    upper_p = np.where(active, case.gen[:, PMAX], 0.0) / case.base_mva
    lower_q = np.where(active, case.gen[:, QMIN], 0.0) / case.base_mva
    upper_q = np.where(active, case.gen[:, QMAX], 0.0) / case.base_mva
    generator = max(
        _positive_violation(lower_p - generator_p),
        _positive_violation(generator_p - upper_p),
        _positive_violation(lower_q - generator_q),
        _positive_violation(generator_q - upper_q),
    )

    specified = -(case.bus[:, PD] + 1j * case.bus[:, QD]) / case.base_mva
    for index, row in enumerate(case.gen):
        specified[mapping[int(row[GEN_BUS])]] += complex(
            generator_p[index], generator_q[index]
        )
    balance = float(
        np.max(np.abs(specified - relaxed_injections(ybus, moments)))
    )
    edge_psd = 0.0
    for u, v in edge_pairs(ybus):
        edge_psd = max(
            edge_psd,
            abs(moments[u, v]) ** 2 - diagonal[u] * diagonal[v],
        )
    edge_psd = max(0.0, float(edge_psd))

    angle = 0.0
    thermal = 0.0
    effective_limits = np.asarray(solution.thermal_limits_mva)
    for branch in branch_admittances(case):
        row = case.branch[branch.row_index]
        minimum, maximum = float(row[ANGMIN]), float(row[ANGMAX])
        if not (minimum == 0 and maximum == 0) and not (
            minimum <= -360 and maximum >= 360
        ):
            phase_degrees = math.degrees(
                float(np.angle(moments[branch.from_bus, branch.to_bus]))
            )
            angle = max(
                angle,
                minimum - phase_degrees,
                phase_degrees - maximum,
            )
        if effective_limits[branch.row_index] > 0:
            u, v = branch.from_bus, branch.to_bus
            from_flow = (
                np.conj(branch.y_ff) * moments[u, u]
                + np.conj(branch.y_ft) * moments[u, v]
            )
            to_flow = (
                np.conj(branch.y_tf) * moments[v, u]
                + np.conj(branch.y_tt) * moments[v, v]
            )
            limit = float(
                effective_limits[branch.row_index] / case.base_mva
            )
            thermal = max(
                thermal, abs(from_flow) - limit, abs(to_flow) - limit
            )
    angle = max(0.0, float(angle))
    thermal = max(0.0, float(thermal))
    recomputed_objective = evaluate_generation_cost(case, generator_p)
    objective_difference = abs(recomputed_objective - solution.objective)
    return SOCPAudit(
        hermitian,
        voltage,
        generator,
        balance,
        edge_psd,
        angle,
        thermal,
        objective_difference,
    )
