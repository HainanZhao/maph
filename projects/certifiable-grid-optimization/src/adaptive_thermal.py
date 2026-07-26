"""Recovery-informed adaptive tightening of SOCP thermal limits."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from src.ac_feasibility import (
    RecoveredDispatch,
    branch_thermal_overloads_mva,
    recover_operational_dispatch,
)
from src.ac_power_flow import (
    RATE_A,
    build_ybus,
    solve_power_flow_with_q_limits,
)
from src.full_ac_recovery import recover_full_ac_candidates, relaxed_injections
from src.matpower import MatpowerCase
from src.socp_relaxation import SOCPSolution, solve_socp_relaxation


@dataclass(frozen=True)
class AdaptiveThermalIteration:
    """One relaxation, recovery, and operational audit."""

    iteration: int
    relaxation_objective: float
    dispatch_objective: float
    maximum_overload_mva: float
    maximum_operational_violation: float
    tightened_branch_count: int


@dataclass(frozen=True)
class AdaptiveThermalResult:
    """The adaptive history and its retained original lower bound."""

    original_lower_bound: float
    feasible_upper_bound: float
    converged: bool
    history: tuple[AdaptiveThermalIteration, ...]
    final_relaxation: SOCPSolution
    final_dispatch: RecoveredDispatch

    @property
    def certified_gap_percent(self) -> float:
        if not self.converged or not math.isfinite(self.feasible_upper_bound):
            return math.inf
        return (
            100.0
            * (self.feasible_upper_bound - self.original_lower_bound)
            / self.feasible_upper_bound
        )


def adaptive_thermal_recovery(
    case: MatpowerCase,
    *,
    recovery_method: str = "radial-aware minimax LP",
    gain: float = 1.0,
    minimum_limit_fraction: float = 0.4,
    maximum_iterations: int = 12,
    feasibility_tolerance: float = 2e-5,
) -> AdaptiveThermalResult:
    """Tighten only lines overloaded after recovery and retain the first bound."""

    if gain <= 0:
        raise ValueError("gain must be positive")
    if not 0 < minimum_limit_fraction <= 1:
        raise ValueError("minimum_limit_fraction must lie in (0, 1]")
    if maximum_iterations < 0:
        raise ValueError("maximum_iterations must be nonnegative")

    original_limits = case.branch[:, RATE_A].astype(float)
    effective_limits = original_limits.copy()
    original_relaxation = solve_socp_relaxation(case)
    relaxation = original_relaxation
    history = []
    dispatch: RecoveredDispatch | None = None
    for iteration in range(maximum_iterations + 1):
        ybus = build_ybus(case)
        target = relaxed_injections(ybus, relaxation.moments)
        candidates = recover_full_ac_candidates(case, relaxation.moments)
        if recovery_method not in candidates:
            raise ValueError(f"unknown recovery method: {recovery_method}")
        recovery = candidates[recovery_method]
        limited = solve_power_flow_with_q_limits(
            case,
            target,
            recovery.voltage_magnitudes,
            recovery.voltage_angles,
        )
        dispatch = recover_operational_dispatch(
            case,
            limited.power_flow,
            relaxation.generator_p,
            relaxation.generator_q,
        )
        overloads = branch_thermal_overloads_mva(
            case, limited.power_flow
        )
        maximum_overload = float(np.max(overloads))
        history.append(
            AdaptiveThermalIteration(
                iteration,
                relaxation.objective,
                dispatch.objective,
                maximum_overload,
                dispatch.audit.maximum_violation,
                int(np.count_nonzero(effective_limits < original_limits - 1e-9)),
            )
        )
        if (
            limited.power_flow.converged
            and dispatch.audit.maximum_violation <= feasibility_tolerance
        ):
            return AdaptiveThermalResult(
                original_relaxation.objective,
                dispatch.objective,
                True,
                tuple(history),
                relaxation,
                dispatch,
            )
        if iteration == maximum_iterations or maximum_overload <= 0:
            break
        changed = False
        for branch_index, overload in enumerate(overloads):
            if overload <= feasibility_tolerance or original_limits[branch_index] <= 0:
                continue
            floor = minimum_limit_fraction * original_limits[branch_index]
            tightened = max(
                floor, effective_limits[branch_index] - gain * overload
            )
            if tightened < effective_limits[branch_index] - 1e-9:
                effective_limits[branch_index] = tightened
                changed = True
        if not changed:
            break
        try:
            relaxation = solve_socp_relaxation(
                case, thermal_limits_mva=effective_limits
            )
        except ValueError:
            break

    assert dispatch is not None
    return AdaptiveThermalResult(
        original_relaxation.objective,
        math.inf,
        False,
        tuple(history),
        relaxation,
        dispatch,
    )
