"""Benchmark full-complex-voltage recovery on pinned PGLib cases."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ac_power_flow import (
    BUS_TYPE,
    PQ,
    REF,
    build_ybus,
    solve_power_flow,
    solve_power_flow_to_injections,
)
from src.full_ac_recovery import (
    generate_edge_relaxed_moments,
    recover_full_ac_candidates,
    relaxed_injections,
    score_full_ac_recovery,
)
from src.matpower import load_matpower_case


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"
CASES = ("pglib_opf_case5_pjm.m", "pglib_opf_case14_ieee.m")
METHODS = (
    "radial-aware minimax LP",
    "phase-only minimax LP",
    "weighted phase LS",
    "maximum-weight tree",
)


def run(trials: int, seed: int, phase_sigma: float, radial_sigma: float) -> None:
    rng = np.random.default_rng(seed)
    print(
        "| case | method | median exact P/Q residual | "
        "median moment bound | median beta*rho | wins | repaired | "
        "median correction |"
    )
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for filename in CASES:
        case = load_matpower_case(DATA / filename)
        solution = solve_power_flow(case)
        if not solution.converged:
            raise RuntimeError(f"base power flow failed for {filename}")
        ybus = build_ybus(case)
        records = {method: [] for method in METHODS}
        repairs = {method: [] for method in METHODS}
        wins = {method: 0 for method in METHODS}
        for _ in range(trials):
            moments = generate_edge_relaxed_moments(
                ybus,
                solution.voltage_magnitudes,
                solution.voltage_angles,
                rng,
                phase_sigma=phase_sigma,
                radial_sigma=radial_sigma,
            )
            candidates = recover_full_ac_candidates(case, moments)
            scores = {
                method: score_full_ac_recovery(case, moments, recovery)
                for method, recovery in candidates.items()
            }
            target = relaxed_injections(ybus, moments)
            bus_types = case.bus[:, BUS_TYPE].astype(int)
            nonreference = np.flatnonzero(bus_types != REF)
            pq = np.flatnonzero(bus_types == PQ)
            for method, recovery in candidates.items():
                repaired = solve_power_flow_to_injections(
                    case,
                    target,
                    recovery.voltage_magnitudes,
                    recovery.voltage_angles,
                )
                angle_correction = max(
                    abs(
                        repaired.voltage_angles[index]
                        - recovery.voltage_angles[index]
                    )
                    for index in nonreference
                )
                magnitude_correction = max(
                    (
                        abs(
                            repaired.voltage_magnitudes[index]
                            - recovery.voltage_magnitudes[index]
                        )
                        for index in pq
                    ),
                    default=0.0,
                )
                repairs[method].append(
                    (
                        repaired.converged,
                        max(angle_correction, magnitude_correction),
                    )
                )
            best = min(
                scores,
                key=lambda method: scores[method].newton_step_upper_bound,
            )
            wins[best] += 1
            for method, score in scores.items():
                records[method].append(score)
        for method in METHODS:
            scores = records[method]
            method_repairs = repairs[method]
            print(
                f"| {filename.removesuffix('.m')} | {method} | "
                f"{np.median([s.injection_residual_inf for s in scores]):.6g} | "
                f"{np.median([s.moment_residual_bound for s in scores]):.6g} | "
                f"{np.median([s.newton_step_upper_bound for s in scores]):.6g} | "
                f"{wins[method]}/{trials} | "
                f"{sum(value[0] for value in method_repairs)}/{trials} | "
                f"{np.median([value[1] for value in method_repairs]):.6g} |"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--phase-sigma", type=float, default=0.01)
    parser.add_argument("--radial-sigma", type=float, default=0.005)
    arguments = parser.parse_args()
    if arguments.trials <= 0:
        raise ValueError("--trials must be positive")
    run(
        arguments.trials,
        arguments.seed,
        arguments.phase_sigma,
        arguments.radial_sigma,
    )


if __name__ == "__main__":
    main()
