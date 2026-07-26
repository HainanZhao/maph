"""Operational feasibility audit for repaired AC power-flow points."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from src.ac_power_flow import (
    ANGMAX,
    ANGMIN,
    GEN_BUS,
    GEN_STATUS,
    PD,
    QD,
    RATE_A,
    BranchAdmittance,
    PowerFlowResult,
    branch_admittances,
    bus_index,
    complex_voltage,
)
from src.matpower import MatpowerCase
from src.socp_relaxation import (
    PMAX,
    PMIN,
    QMAX,
    QMIN,
    VMAX,
    VMIN,
    evaluate_generation_cost,
)


@dataclass(frozen=True)
class ACFeasibilityAudit:
    """Independently recomputed operational violations in native units."""

    power_flow_converged: bool
    voltage_pu: float
    generation_mva: float
    power_balance_mva: float
    angle_degrees: float
    thermal_mva: float

    @property
    def maximum_violation(self) -> float:
        return max(
            self.voltage_pu,
            self.generation_mva,
            self.power_balance_mva,
            self.angle_degrees,
            self.thermal_mva,
        )


@dataclass(frozen=True)
class RecoveredDispatch:
    """A repaired voltage plus a feasible-or-best-effort generator allocation."""

    generator_p_mw: tuple[float, ...]
    generator_q_mvar: tuple[float, ...]
    objective: float
    audit: ACFeasibilityAudit


def _allocate_total(
    required: float,
    lower: np.ndarray,
    upper: np.ndarray,
    preferred: np.ndarray,
) -> tuple[np.ndarray, float]:
    values = np.clip(preferred, lower, upper)
    difference = required - float(np.sum(values))
    if difference > 0:
        for index in range(len(values)):
            change = min(difference, upper[index] - values[index])
            values[index] += change
            difference -= change
            if difference <= 1e-12:
                break
    elif difference < 0:
        for index in range(len(values)):
            change = min(-difference, values[index] - lower[index])
            values[index] -= change
            difference += change
            if difference >= -1e-12:
                break
    return values, abs(difference)


def _branch_flows(
    branch: BranchAdmittance, voltage: np.ndarray
) -> tuple[complex, complex]:
    u, v = branch.from_bus, branch.to_bus
    from_current = branch.y_ff * voltage[u] + branch.y_ft * voltage[v]
    to_current = branch.y_tf * voltage[u] + branch.y_tt * voltage[v]
    return voltage[u] * np.conj(from_current), voltage[v] * np.conj(to_current)


def branch_thermal_overloads_mva(
    case: MatpowerCase, power_flow: PowerFlowResult
) -> np.ndarray:
    """Return each branch's both-end overload against its original rating."""

    overloads = np.zeros(len(case.branch))
    voltage = complex_voltage(
        power_flow.voltage_magnitudes, power_flow.voltage_angles
    )
    for branch in branch_admittances(case):
        limit = case.branch[branch.row_index, RATE_A]
        if limit <= 0:
            continue
        from_flow, to_flow = _branch_flows(branch, voltage)
        overloads[branch.row_index] = max(
            0.0,
            case.base_mva * abs(from_flow) - limit,
            case.base_mva * abs(to_flow) - limit,
        )
    return overloads


def recover_operational_dispatch(
    case: MatpowerCase,
    power_flow: PowerFlowResult,
    preferred_p_pu: Sequence[float],
    preferred_q_pu: Sequence[float],
) -> RecoveredDispatch:
    """Allocate repaired bus injections to generators and audit all limits."""

    preferred_p = case.base_mva * np.asarray(preferred_p_pu, dtype=float)
    preferred_q = case.base_mva * np.asarray(preferred_q_pu, dtype=float)
    if preferred_p.shape != (len(case.gen),) or preferred_q.shape != (
        len(case.gen),
    ):
        raise ValueError("preferred generator vectors have the wrong length")
    mapping = bus_index(case)
    generators_by_bus = [[] for _ in range(len(case.bus))]
    for generator_index, row in enumerate(case.gen):
        generators_by_bus[mapping[int(row[GEN_BUS])]].append(generator_index)

    required = (
        case.base_mva * np.asarray(power_flow.injections)
        + case.bus[:, PD]
        + 1j * case.bus[:, QD]
    )
    generator_p = np.zeros(len(case.gen))
    generator_q = np.zeros(len(case.gen))
    allocation_violation = 0.0
    for position, generator_indices in enumerate(generators_by_bus):
        if not generator_indices:
            allocation_violation = max(
                allocation_violation, abs(required[position])
            )
            continue
        indices = np.asarray(generator_indices, dtype=int)
        active = case.gen[indices, GEN_STATUS] > 0
        lower_p = np.where(active, case.gen[indices, PMIN], 0.0)
        upper_p = np.where(active, case.gen[indices, PMAX], 0.0)
        lower_q = np.where(active, case.gen[indices, QMIN], 0.0)
        upper_q = np.where(active, case.gen[indices, QMAX], 0.0)
        allocated_p, p_violation = _allocate_total(
            float(required[position].real),
            lower_p,
            upper_p,
            preferred_p[indices],
        )
        allocated_q, q_violation = _allocate_total(
            float(required[position].imag),
            lower_q,
            upper_q,
            preferred_q[indices],
        )
        generator_p[indices] = allocated_p
        generator_q[indices] = allocated_q
        allocation_violation = max(
            allocation_violation, p_violation, q_violation
        )

    vm = np.asarray(power_flow.voltage_magnitudes)
    va = np.asarray(power_flow.voltage_angles)
    voltage_violation = max(
        float(np.max(case.bus[:, VMIN] - vm)),
        float(np.max(vm - case.bus[:, VMAX])),
        0.0,
    )
    lower_p = np.where(
        case.gen[:, GEN_STATUS] > 0, case.gen[:, PMIN], 0.0
    )
    upper_p = np.where(
        case.gen[:, GEN_STATUS] > 0, case.gen[:, PMAX], 0.0
    )
    lower_q = np.where(
        case.gen[:, GEN_STATUS] > 0, case.gen[:, QMIN], 0.0
    )
    upper_q = np.where(
        case.gen[:, GEN_STATUS] > 0, case.gen[:, QMAX], 0.0
    )
    generation_violation = max(
        float(np.max(lower_p - generator_p)),
        float(np.max(generator_p - upper_p)),
        float(np.max(lower_q - generator_q)),
        float(np.max(generator_q - upper_q)),
        allocation_violation,
        0.0,
    )

    supplied = -(case.bus[:, PD] + 1j * case.bus[:, QD])
    for generator_index, row in enumerate(case.gen):
        supplied[mapping[int(row[GEN_BUS])]] += complex(
            generator_p[generator_index], generator_q[generator_index]
        )
    power_balance_violation = float(
        np.max(
            np.abs(
                supplied
                - case.base_mva * np.asarray(power_flow.injections)
            )
        )
    )

    angle_violation = 0.0
    thermal_violation = 0.0
    voltage = complex_voltage(vm, va)
    for branch in branch_admittances(case):
        row = case.branch[branch.row_index]
        minimum, maximum = float(row[ANGMIN]), float(row[ANGMAX])
        if not (minimum == 0 and maximum == 0) and not (
            minimum <= -360 and maximum >= 360
        ):
            difference = math.degrees(va[branch.from_bus] - va[branch.to_bus])
            angle_violation = max(
                angle_violation, minimum - difference, difference - maximum
            )
        if row[RATE_A] > 0:
            from_flow, to_flow = _branch_flows(branch, voltage)
            thermal_violation = max(
                thermal_violation,
                case.base_mva * abs(from_flow) - row[RATE_A],
                case.base_mva * abs(to_flow) - row[RATE_A],
            )

    objective = evaluate_generation_cost(
        case, generator_p / case.base_mva
    )
    audit = ACFeasibilityAudit(
        power_flow.converged,
        max(0.0, voltage_violation),
        max(0.0, generation_violation),
        power_balance_violation,
        max(0.0, angle_violation),
        max(0.0, thermal_violation),
    )
    return RecoveredDispatch(
        tuple(float(value) for value in generator_p),
        tuple(float(value) for value in generator_q),
        objective,
        audit,
    )
