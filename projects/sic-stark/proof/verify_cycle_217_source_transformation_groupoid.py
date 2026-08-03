#!/usr/bin/env python3
"""Exact source-transformation groupoid audit for Cycle 217/B054.

The calculation distinguishes the raw S--S matrix arrows from an unproved
projective k>0 canonicalization.  It tracks the period pair and affine
argument, so a projective endpoint hit cannot be mistaken for Gamma_M duality.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


State = tuple[int, int, int, int]  # (p,k,r,s)
Pair = tuple[int, int]  # coefficient of (omega1, omega2)

S0: State = (-115, 24, 5, 24)
S_E: State = (-5, 24, 115, 24)


def matrix(state: State) -> tuple[tuple[int, int], tuple[int, int]]:
    p, k, r, s = state
    return ((-p, -s), (k, -r))


def negate(state: State) -> State:
    return tuple(-entry for entry in state)  # type: ignore[return-value]


def f2_raw(state: State) -> State:
    """Displayed M2 in S--S equation (16), before any sign normalization."""
    p, k, r, s = state
    return (-r, -s, -p, -k)


def f3(state: State) -> State:
    """Displayed M3 in S--S equation (17)."""
    p, k, r, s = state
    return (-p, s, -r, k)


def candidate_c2(state: State) -> State:
    """Matrix-only proposal: negate the raw M2 to restore k>0."""
    return negate(f2_raw(state))


def add(left: Pair, right: Pair) -> Pair:
    return (left[0] + right[0], left[1] + right[1])


def scale(coefficient: int, pair: Pair) -> Pair:
    return (coefficient * pair[0], coefficient * pair[1])


def f2_periods(state: State, omega_one: Pair, omega_two: Pair) -> tuple[Pair, Pair]:
    """The two periods printed beside M2 in equation (16)."""
    p, _k, r, _s = state
    return add(scale(p, omega_one), omega_two), add(omega_one, scale(r, omega_two))


def f3_periods(state: State, omega_one: Pair, omega_two: Pair) -> tuple[Pair, Pair]:
    """The two periods printed beside M3 in equation (17)."""
    p, _k, r, _s = state
    return add(omega_one, scale(r, omega_two)), add(scale(p, omega_one), omega_two)


def raw_orbit_audit() -> dict[str, object]:
    orbit = {S0}
    frontier = [S0]
    while frontier:
        current = frontier.pop()
        for image in (f2_raw(current), f3(current)):
            if image not in orbit:
                orbit.add(image)
                frontier.append(image)
    expected = {
        (-115, 24, 5, 24),
        (-5, -24, 115, -24),
        (115, 24, -5, 24),
        (5, -24, -115, -24),
    }
    assert orbit == expected
    two_step = f3(f2_raw(S0))
    assert two_step == negate(S_E)
    assert matrix(two_step) == tuple(tuple(-entry for entry in row) for row in matrix(S_E))
    return {
        "epistemic_status": "PROVED",
        "raw_orbit_states": [list(state) for state in sorted(orbit)],
        "raw_orbit_size": len(orbit),
        "f2_and_f3_involutive": f2_raw(f2_raw(S0)) == S0 and f3(f3(S0)) == S0,
        "two_step_word": "F3 o F2_raw",
        "two_step_state": list(two_step),
        "two_step_matrix": [list(row) for row in matrix(two_step)],
        "two_step_matrix_is_minus_M_E": True,
        "conclusion": "The raw cited matrix orbit is exactly four states and its two-step word reaches -M_E projectively, not the k>0 target representative itself.",
    }


def candidate_canonical_orbit_audit() -> dict[str, object]:
    first = candidate_c2(S0)
    second = f3(first)
    assert first == (5, 24, -115, 24)
    assert second == S_E
    return {
        "epistemic_status": "OBSERVED",
        "candidate_word": "C2 then F3",
        "candidate_intermediate_state": list(first),
        "candidate_endpoint_state": list(second),
        "candidate_endpoint_matrix": [list(row) for row in matrix(second)],
        "matrix_hit": "M_E",
        "scope_warning": "C2 is only the matrix-level negation of the raw equation-(16) M2. No source-proved Gamma_M sign/cocycle/period law has yet made it an admissible arrow.",
    }


def affine_period_argument_audit() -> dict[str, object]:
    """Track the raw two-step source arrow on the frozen period basis."""
    initial_one, initial_two = (1, 0), (0, 1)
    first_periods = f2_periods(S0, initial_one, initial_two)
    assert first_periods == ((-115, 1), (1, 5))
    second_periods = f3_periods(f2_raw(S0), *first_periods)
    assert second_periods == ((0, 576), (576, 0))
    # Equation (16): mu_A=-s*(mu+m*omega2), m_A=0.  Equation (17) at
    # F2_raw(S0) has s_A=-24, so mu_B=576*(mu+m*omega2), m_B=0.
    target_periods = ((-1, 0), (0, 1))
    assert second_periods != target_periods
    assert second_periods != tuple(scale(-1, item) for item in target_periods)
    return {
        "epistemic_status": "PROVED",
        "initial_periods": {"omega1": [1, 0], "omega2": [0, 1]},
        "after_F2_raw_periods": {"Omega1": list(first_periods[0]), "Omega2": list(first_periods[1])},
        "after_F3_periods": {"Omega1": list(second_periods[0]), "Omega2": list(second_periods[1])},
        "after_F3_period_interpretation": "576*(omega2, omega1)",
        "raw_argument_after_F2": "-24*(mu+m*omega2), discrete label 0",
        "raw_argument_after_F3": "576*(mu+m*omega2), discrete label 0",
        "E_target_periods": {"omega1_E": [-1, 0], "omega2_E": [0, 1]},
        "raw_two_step_periods_match_E_target": False,
        "residual_source_factors": "Equation (16) contributes two ordinary gamma factors; equation (17) relates the intermediate gamma_M times the final gamma_M to two further ordinary gamma factors. None has been suppressed or declared scalar.",
        "conclusion": "Even before resolving the C2 sign law, the raw two-step source arrow reaches a swapped/rescaled period pair and a fixed discrete label, not the Cycle-215 E period data.",
    }


def packet_boundary_audit() -> dict[str, object]:
    defects = {12 - first - second for first in range(6) for second in range(6)}
    assert defects == set(range(2, 13))
    return {
        "epistemic_status": "PROVED",
        "all_label_t_defects": sorted(defects),
        "source_arrow_to_packet_t_a_b_map_available": False,
        "cocycle_cancellation_test_performed": False,
        "reason": "The raw source word does not have the E target period/discrete state, and C2 remains source-unvalidated; testing a fitted packet factor would violate the freeze.",
    }


def run() -> dict[str, object]:
    raw = raw_orbit_audit()
    candidate = candidate_canonical_orbit_audit()
    affine = affine_period_argument_audit()
    packet = packet_boundary_audit()
    assert raw["raw_orbit_size"] == 4
    assert raw["two_step_matrix_is_minus_M_E"]
    assert candidate["candidate_endpoint_state"] == list(S_E)
    assert not affine["raw_two_step_periods_match_E_target"]
    assert not packet["source_arrow_to_packet_t_a_b_map_available"]
    return {
        "schema": "sic-stark-cycle-217-source-transformation-groupoid-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The cited raw equations-(16)--(17) matrix orbit has four states and its F3 o F2_raw word reaches -M_E projectively. The tempting k>0 canonicalized word reaches M_E only at matrix level and is OBSERVED because its Gamma_M sign/cocycle/period law is not derived. The raw word instead carries periods to 576*(omega2,omega1) and discrete label zero, not the E target (-omega1,omega2). This does not exhaust a signed-period-cover construction, a new source identity, a source-derived packet map/cocycle, AFK covariance, fusion, Stark, or TCC.",
        "raw_orbit_audit": raw,
        "candidate_canonical_orbit_audit": candidate,
        "affine_period_argument_audit": affine,
        "packet_boundary_audit": packet,
        "gate_outcome": {
            "raw_source_matrix_orbit": "PROVED_FINITE_FOUR_STATE_PROJECTIVE_HIT",
            "canonicalized_M_E_word": "OBSERVED_MATRIX_ONLY_NOT_SOURCE_AUTHORIZED",
            "raw_two_step_E_period_match": "FALSIFIED",
            "remaining_design_problem": "Construct a signed-period-cover or other new Gamma_M transformation that validates canonicalization and maps the full affine period/discrete state to the E target before any all-label cocycle test.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
