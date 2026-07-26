"""Solve genuine SOCP relaxations and audit AC recovery attempts."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ac_feasibility import recover_operational_dispatch
from src.ac_power_flow import build_ybus, solve_power_flow_with_q_limits
from src.full_ac_recovery import (
    recover_full_ac_candidates,
    relaxed_injections,
    score_full_ac_recovery,
)
from src.matpower import load_matpower_case
from src.socp_relaxation import audit_socp_solution, solve_socp_relaxation


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"
CASES = (
    "pglib_opf_case5_pjm.m",
    "pglib_opf_case14_ieee.m",
    "pglib_opf_case5_pjm__api.m",
    "pglib_opf_case14_ieee__api.m",
)


def main() -> None:
    print(
        "| case | method | SOCP lower bound | rho | beta*rho | "
        "PF iterations | AC cost | max operational violation |"
    )
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for filename in CASES:
        case = load_matpower_case(DATA / filename)
        relaxation = solve_socp_relaxation(case)
        relaxation_audit = audit_socp_solution(case, relaxation)
        if relaxation_audit.maximum_violation > 2e-6:
            raise RuntimeError(
                f"SOCP audit failed for {filename}: {relaxation_audit}"
            )
        ybus = build_ybus(case)
        target = relaxed_injections(ybus, relaxation.moments)
        for method, recovery in recover_full_ac_candidates(
            case, relaxation.moments
        ).items():
            score = score_full_ac_recovery(
                case, relaxation.moments, recovery
            )
            limited_power_flow = solve_power_flow_with_q_limits(
                case,
                target,
                recovery.voltage_magnitudes,
                recovery.voltage_angles,
            )
            power_flow = limited_power_flow.power_flow
            dispatch = recover_operational_dispatch(
                case,
                power_flow,
                relaxation.generator_p,
                relaxation.generator_q,
            )
            print(
                f"| {filename.removesuffix('.m')} | {method} | "
                f"{relaxation.objective:.6f} | "
                f"{score.moment_residual_bound:.6g} | "
                f"{score.newton_step_upper_bound:.6g} | "
                f"{power_flow.iterations}"
                f" (+{len(limited_power_flow.switched_buses)} Q switches) | "
                f"{dispatch.objective:.6f} | "
                f"{dispatch.audit.maximum_violation:.6g} |"
            )


if __name__ == "__main__":
    main()
