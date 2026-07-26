"""Full polar-coordinate AC power-flow equations for MATPOWER cases."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from src.matpower import MatpowerCase


# Zero-based MATPOWER column indices.
BUS_I, BUS_TYPE, PD, QD, GS, BS, _, VM, VA = range(9)
GEN_BUS, PG, QG = range(3)
GEN_STATUS = 7
F_BUS, T_BUS, BR_R, BR_X, BR_B, RATE_A = range(6)
TAP, SHIFT, BR_STATUS = 8, 9, 10
ANGMIN, ANGMAX = 11, 12
PQ, PV, REF = 1, 2, 3


@dataclass(frozen=True)
class PowerFlowResult:
    """A Newton power-flow result with fixed PV and reference magnitudes."""

    voltage_magnitudes: tuple[float, ...]
    voltage_angles: tuple[float, ...]
    injections: tuple[complex, ...]
    converged: bool
    iterations: int
    mismatch_inf: float


@dataclass(frozen=True)
class BranchAdmittance:
    """The four terminal-admittance coefficients of one active branch."""

    row_index: int
    from_bus: int
    to_bus: int
    y_ff: complex
    y_ft: complex
    y_tf: complex
    y_tt: complex


@dataclass(frozen=True)
class QLimitedPowerFlowResult:
    """A power-flow result after PV/reference reactive-limit switching."""

    power_flow: PowerFlowResult
    switched_buses: tuple[int, ...]


def bus_index(case: MatpowerCase) -> dict[int, int]:
    external_ids = [int(value) for value in case.bus[:, BUS_I]]
    if len(set(external_ids)) != len(external_ids):
        raise ValueError("bus identifiers must be unique")
    return {external_id: index for index, external_id in enumerate(external_ids)}


def build_ybus(case: MatpowerCase) -> np.ndarray:
    """Build Ybus using MATPOWER's line, transformer, and shunt convention."""

    count = case.bus.shape[0]
    ybus = np.zeros((count, count), dtype=complex)
    for branch in branch_admittances(case):
        ybus[branch.from_bus, branch.from_bus] += branch.y_ff
        ybus[branch.from_bus, branch.to_bus] += branch.y_ft
        ybus[branch.to_bus, branch.from_bus] += branch.y_tf
        ybus[branch.to_bus, branch.to_bus] += branch.y_tt
    ybus[np.diag_indices(count)] += (
        case.bus[:, GS] + 1j * case.bus[:, BS]
    ) / case.base_mva
    return ybus


def branch_admittances(case: MatpowerCase) -> tuple[BranchAdmittance, ...]:
    """Return MATPOWER terminal admittances for all in-service branches."""

    index = bus_index(case)
    coefficients = []
    for row_index, row in enumerate(case.branch):
        if row[BR_STATUS] <= 0:
            continue
        try:
            from_bus = index[int(row[F_BUS])]
            to_bus = index[int(row[T_BUS])]
        except KeyError as error:
            raise ValueError("branch references an unknown bus") from error
        impedance = complex(row[BR_R], row[BR_X])
        if impedance == 0:
            raise ValueError("an in-service branch has zero series impedance")
        series = 1.0 / impedance
        charging = float(row[BR_B])
        tap_magnitude = float(row[TAP]) if row[TAP] != 0 else 1.0
        tap = tap_magnitude * np.exp(1j * math.radians(float(row[SHIFT])))
        y_tt = series + 0.5j * charging
        coefficients.append(
            BranchAdmittance(
                row_index,
                from_bus,
                to_bus,
                y_tt / (tap * np.conj(tap)),
                -series / np.conj(tap),
                -series / tap,
                y_tt,
            )
        )
    return tuple(coefficients)


def initial_voltage(case: MatpowerCase) -> tuple[np.ndarray, np.ndarray]:
    return case.bus[:, VM].copy(), np.radians(case.bus[:, VA].copy())


def complex_voltage(
    voltage_magnitudes: Sequence[float], voltage_angles: Sequence[float]
) -> np.ndarray:
    magnitudes = np.asarray(voltage_magnitudes, dtype=float)
    angles = np.asarray(voltage_angles, dtype=float)
    if magnitudes.shape != angles.shape:
        raise ValueError("voltage magnitude and angle vectors must have equal shape")
    return magnitudes * np.exp(1j * angles)


def complex_injections(
    ybus: np.ndarray,
    voltage_magnitudes: Sequence[float],
    voltage_angles: Sequence[float],
) -> np.ndarray:
    voltage = complex_voltage(voltage_magnitudes, voltage_angles)
    return voltage * np.conj(ybus @ voltage)


def specified_injections(case: MatpowerCase) -> np.ndarray:
    """Return generation minus fixed load in per unit."""

    index = bus_index(case)
    specified = -(case.bus[:, PD] + 1j * case.bus[:, QD]) / case.base_mva
    for row in case.gen:
        if row[GEN_STATUS] > 0:
            try:
                position = index[int(row[GEN_BUS])]
            except KeyError as error:
                raise ValueError("generator references an unknown bus") from error
            specified[position] += complex(row[PG], row[QG]) / case.base_mva
    return specified


def polar_jacobian(
    ybus: np.ndarray,
    voltage_magnitudes: Sequence[float],
    voltage_angles: Sequence[float],
) -> np.ndarray:
    """Return d(P,Q)/d(theta,Vm), with all buses included."""

    vm = np.asarray(voltage_magnitudes, dtype=float)
    va = np.asarray(voltage_angles, dtype=float)
    if ybus.shape != (len(vm), len(vm)) or vm.shape != va.shape:
        raise ValueError("incompatible Ybus or voltage dimensions")
    if np.any(vm <= 0):
        raise ValueError("voltage magnitudes must be positive")
    injections = complex_injections(ybus, vm, va)
    p = injections.real
    q = injections.imag
    conductance = ybus.real
    susceptance = ybus.imag
    count = len(vm)
    p_angle = np.zeros((count, count))
    p_magnitude = np.zeros((count, count))
    q_angle = np.zeros((count, count))
    q_magnitude = np.zeros((count, count))

    for i in range(count):
        for k in range(count):
            if i == k:
                p_angle[i, i] = -q[i] - susceptance[i, i] * vm[i] ** 2
                q_angle[i, i] = p[i] - conductance[i, i] * vm[i] ** 2
                p_magnitude[i, i] = p[i] / vm[i] + conductance[i, i] * vm[i]
                q_magnitude[i, i] = q[i] / vm[i] - susceptance[i, i] * vm[i]
                continue
            difference = va[i] - va[k]
            cosine = math.cos(difference)
            sine = math.sin(difference)
            g = conductance[i, k]
            b = susceptance[i, k]
            p_angle[i, k] = vm[i] * vm[k] * (g * sine - b * cosine)
            q_angle[i, k] = -vm[i] * vm[k] * (g * cosine + b * sine)
            p_magnitude[i, k] = vm[i] * (g * cosine + b * sine)
            q_magnitude[i, k] = vm[i] * (g * sine - b * cosine)
    return np.block([[p_angle, p_magnitude], [q_angle, q_magnitude]])


def solve_power_flow(
    case: MatpowerCase,
    *,
    tolerance: float = 1e-10,
    maximum_iterations: int = 30,
) -> PowerFlowResult:
    """Solve the standard REF/PV/PQ power flow by Newton's method.

    Generator reactive limits and bus-type switching are intentionally not
    enforced in this first validation solver.
    """

    vm, va = initial_voltage(case)
    return solve_power_flow_to_injections(
        case,
        specified_injections(case),
        vm,
        va,
        tolerance=tolerance,
        maximum_iterations=maximum_iterations,
    )


def solve_power_flow_to_injections(
    case: MatpowerCase,
    specified: Sequence[complex],
    initial_magnitudes: Sequence[float],
    initial_angles: Sequence[float],
    *,
    tolerance: float = 1e-10,
    maximum_iterations: int = 30,
) -> PowerFlowResult:
    """Solve REF/PV/PQ equations for a supplied complex injection target.

    Active injection is enforced at every nonreference bus and reactive
    injection at every PQ bus.  Reference-bus active power and PV/reference
    reactive powers remain free, as in a standard power-flow problem.
    """

    if tolerance <= 0 or maximum_iterations <= 0:
        raise ValueError("solver tolerances and iteration limit must be positive")
    bus_types = case.bus[:, BUS_TYPE].astype(int)
    reference = np.flatnonzero(bus_types == REF)
    if len(reference) != 1:
        raise ValueError("exactly one reference bus is required")
    pq = np.flatnonzero(bus_types == PQ)
    if np.any(~np.isin(bus_types, (PQ, PV, REF))):
        raise ValueError("isolated or unsupported bus types are present")

    target = np.asarray(specified, dtype=complex)
    vm = np.asarray(initial_magnitudes, dtype=float).copy()
    va = np.asarray(initial_angles, dtype=float).copy()
    if target.shape != (len(case.bus),):
        raise ValueError("specified injection vector has the wrong length")
    if vm.shape != target.shape or va.shape != target.shape:
        raise ValueError("initial voltage vectors have the wrong length")
    if np.any(vm <= 0):
        raise ValueError("initial voltage magnitudes must be positive")
    return _solve_power_flow_equations(
        case,
        target,
        vm,
        va,
        q_equation_buses=pq,
        tolerance=tolerance,
        maximum_iterations=maximum_iterations,
    )


def _solve_power_flow_equations(
    case: MatpowerCase,
    target: np.ndarray,
    vm: np.ndarray,
    va: np.ndarray,
    *,
    q_equation_buses: Sequence[int],
    tolerance: float,
    maximum_iterations: int,
) -> PowerFlowResult:
    bus_types = case.bus[:, BUS_TYPE].astype(int)
    nonreference = np.flatnonzero(bus_types != REF)
    q_buses = np.asarray(tuple(q_equation_buses), dtype=int)
    if len(set(int(value) for value in q_buses)) != len(q_buses):
        raise ValueError("reactive-equation buses must be distinct")
    if np.any(q_buses < 0) or np.any(q_buses >= len(case.bus)):
        raise ValueError("reactive-equation bus is outside the case")
    ybus = build_ybus(case)
    mismatch_inf = math.inf
    for iteration in range(maximum_iterations + 1):
        injections = complex_injections(ybus, vm, va)
        mismatch = np.concatenate(
            (
                target.real[nonreference] - injections.real[nonreference],
                target.imag[q_buses] - injections.imag[q_buses],
            )
        )
        mismatch_inf = float(np.linalg.norm(mismatch, ord=np.inf))
        if mismatch_inf <= tolerance:
            return PowerFlowResult(
                tuple(float(value) for value in vm),
                tuple(float(value) for value in va),
                tuple(complex(value) for value in injections),
                True,
                iteration,
                mismatch_inf,
            )
        if iteration == maximum_iterations:
            break
        full_jacobian = polar_jacobian(ybus, vm, va)
        count = len(vm)
        rows = np.concatenate((nonreference, count + q_buses))
        columns = np.concatenate((nonreference, count + q_buses))
        reduced = full_jacobian[np.ix_(rows, columns)]
        try:
            step = np.linalg.solve(reduced, mismatch)
        except np.linalg.LinAlgError:
            break
        va[nonreference] += step[: len(nonreference)]
        vm[q_buses] += step[len(nonreference) :]
        if np.any(vm <= 0):
            break

    injections = complex_injections(ybus, vm, va)
    return PowerFlowResult(
        tuple(float(value) for value in vm),
        tuple(float(value) for value in va),
        tuple(complex(value) for value in injections),
        False,
        iteration,
        mismatch_inf,
    )


def solve_power_flow_with_q_limits(
    case: MatpowerCase,
    specified: Sequence[complex],
    initial_magnitudes: Sequence[float],
    initial_angles: Sequence[float],
    *,
    q_limit_tolerance_mvar: float = 1e-7,
    tolerance: float = 1e-10,
    maximum_iterations: int = 30,
) -> QLimitedPowerFlowResult:
    """Repair injections while enforcing aggregate generator reactive limits."""

    if q_limit_tolerance_mvar < 0:
        raise ValueError("q_limit_tolerance_mvar must be nonnegative")
    if tolerance <= 0 or maximum_iterations <= 0:
        raise ValueError("solver tolerances and iteration limit must be positive")
    bus_types = case.bus[:, BUS_TYPE].astype(int)
    reference = np.flatnonzero(bus_types == REF)
    if len(reference) != 1:
        raise ValueError("exactly one reference bus is required")
    if np.any(~np.isin(bus_types, (PQ, PV, REF))):
        raise ValueError("isolated or unsupported bus types are present")
    mapping = bus_index(case)
    q_lower = np.zeros(len(case.bus))
    q_upper = np.zeros(len(case.bus))
    has_generator = np.zeros(len(case.bus), dtype=bool)
    for row in case.gen:
        if row[GEN_STATUS] <= 0:
            continue
        position = mapping[int(row[GEN_BUS])]
        has_generator[position] = True
        q_lower[position] += row[4]
        q_upper[position] += row[3]

    target = np.asarray(specified, dtype=complex).copy()
    vm = np.asarray(initial_magnitudes, dtype=float).copy()
    va = np.asarray(initial_angles, dtype=float).copy()
    q_buses = set(int(value) for value in np.flatnonzero(bus_types == PQ))
    switched: list[int] = []
    result: PowerFlowResult | None = None
    for _ in range(len(case.bus) + 1):
        result = _solve_power_flow_equations(
            case,
            target,
            vm,
            va,
            q_equation_buses=tuple(sorted(q_buses)),
            tolerance=tolerance,
            maximum_iterations=maximum_iterations,
        )
        if not result.converged:
            return QLimitedPowerFlowResult(result, tuple(switched))
        vm = np.asarray(result.voltage_magnitudes)
        va = np.asarray(result.voltage_angles)
        injections = np.asarray(result.injections)
        new_switches = []
        for position in np.flatnonzero(
            np.isin(bus_types, (PV, REF)) & has_generator
        ):
            if int(position) in q_buses:
                continue
            required_q = (
                case.base_mva * injections[position].imag
                + case.bus[position, QD]
            )
            if required_q < q_lower[position] - q_limit_tolerance_mvar:
                bound = q_lower[position]
            elif required_q > q_upper[position] + q_limit_tolerance_mvar:
                bound = q_upper[position]
            else:
                continue
            target[position] = complex(
                target[position].real,
                (bound - case.bus[position, QD]) / case.base_mva,
            )
            q_buses.add(int(position))
            switched.append(int(position))
            new_switches.append(int(position))
        if not new_switches:
            return QLimitedPowerFlowResult(result, tuple(switched))
    assert result is not None
    return QLimitedPowerFlowResult(result, tuple(switched))
