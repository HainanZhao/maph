"""Benchmark sparse phase-recovery rules against a repair certificate.

The experiment is deliberately synthetic: it isolates the phase-recovery
and local-conditioning questions before introducing a full OPF solver.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import itertools
import math
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.conditioning_aware import solve_conditioning_aware_sweep
from src.lossless_graph import GraphRepairScore, score_projection
from src.sparse_phase_lp import (
    PhaseEdge,
    SparsePhaseProjection,
    solve_minimax_phase_lp,
    solve_tree_phase_recovery,
    solve_weighted_phase_least_squares,
)


EDGE_PAIRS = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))


@dataclass(frozen=True)
class Scenario:
    name: str
    maximum_base_difference: float
    phase_noise: float


SCENARIOS = (
    Scenario("secure / moderate noise", 0.30, 0.010),
    Scenario("loaded / moderate noise", 1.20, 0.010),
    Scenario("near-boundary / high noise", 1.45, 0.030),
)


def spanning_trees() -> tuple[tuple[int, ...], ...]:
    """Enumerate spanning trees of the fixed four-bus test graph."""

    trees = []
    for selection in itertools.combinations(range(len(EDGE_PAIRS)), 3):
        adjacency = [set() for _ in range(4)]
        for edge_index in selection:
            u, v = EDGE_PAIRS[edge_index]
            adjacency[u].add(v)
            adjacency[v].add(u)
        seen = {0}
        stack = [0]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) == 4:
            trees.append(selection)
    return tuple(trees)


def random_instance(
    rng: np.random.Generator, scenario: Scenario
) -> tuple[PhaseEdge, ...]:
    """Generate a phase-inconsistent relaxation around a physical base point."""

    raw_theta = np.concatenate(([0.0], rng.normal(size=3)))
    maximum_difference = max(
        abs(raw_theta[u] - raw_theta[v]) for u, v in EDGE_PAIRS
    )
    base_theta = (
        raw_theta * scenario.maximum_base_difference / maximum_difference
    )
    weights = np.exp(
        rng.uniform(math.log(0.5), math.log(2.0), len(EDGE_PAIRS))
    )
    noise = rng.normal(0.0, scenario.phase_noise, len(EDGE_PAIRS))
    return tuple(
        PhaseEdge(
            u,
            v,
            float(base_theta[u] - base_theta[v] + noise[index]),
            float(weights[index]),
        )
        for index, (u, v) in enumerate(EDGE_PAIRS)
    )


def candidate_scores(
    edges: tuple[PhaseEdge, ...],
    trees: tuple[tuple[int, ...], ...],
) -> dict[str, GraphRepairScore]:
    """Score LP, least-squares, and an oracle-selected spanning tree."""

    candidates: dict[str, SparsePhaseProjection] = {
        "minimax LP": solve_minimax_phase_lp(4, edges),
        "weighted LS": solve_weighted_phase_least_squares(4, edges),
    }
    sweep = solve_conditioning_aware_sweep(
        4,
        edges,
        candidates["weighted LS"].theta,
        (0.0, 0.0025, 0.005, 0.01, 0.02, 0.04, 0.08),
    )
    conditioned_candidates = (
        candidates["minimax LP"],
        candidates["weighted LS"],
        sweep.projection,
    )
    candidates["conditioned selection"] = min(
        conditioned_candidates,
        key=lambda candidate: score_projection(4, edges, candidate).h_bound,
    )
    tree_candidates = tuple(
        solve_tree_phase_recovery(4, edges, selection)
        for selection in trees
    )
    tree_scores = tuple(
        score_projection(4, edges, candidate)
        for candidate in tree_candidates
    )
    best_tree_index = min(
        range(len(tree_scores)), key=lambda index: tree_scores[index].h_bound
    )
    candidates["oracle tree"] = tree_candidates[best_tree_index]
    return {
        name: score_projection(4, edges, candidate)
        for name, candidate in candidates.items()
    }


def run_benchmark(trials: int, seed: int) -> None:
    rng = np.random.default_rng(seed)
    trees = spanning_trees()
    print(
        "| scenario | method | certified | median h | 90% h | "
        "median residual |"
    )
    print("|---|---|---:|---:|---:|---:|")
    for scenario in SCENARIOS:
        records = {
            name: []
            for name in (
                "minimax LP",
                "weighted LS",
                "conditioned selection",
                "oracle tree",
            )
        }
        lp_better_residual = 0
        lp_better_score = 0
        conditioning_reversals = 0
        for _ in range(trials):
            edges = random_instance(rng, scenario)
            scores = candidate_scores(edges, trees)
            for name, score in scores.items():
                records[name].append(score)
            lp_score = scores["minimax LP"]
            ls_score = scores["weighted LS"]
            lp_residual_wins = (
                lp_score.residual_bound < ls_score.residual_bound - 1e-12
            )
            lp_score_wins = lp_score.h_bound < ls_score.h_bound - 1e-12
            lp_better_residual += lp_residual_wins
            lp_better_score += lp_score_wins
            conditioning_reversals += lp_residual_wins and not lp_score_wins

        for name, scores in records.items():
            h_values = np.asarray([score.h_bound for score in scores])
            residuals = np.asarray(
                [score.residual_bound for score in scores]
            )
            certified = sum(score.certified for score in scores)
            print(
                f"| {scenario.name} | {name} | {certified}/{trials} | "
                f"{np.median(h_values):.4f} | "
                f"{np.quantile(h_values, 0.9):.4f} | "
                f"{np.median(residuals):.5f} |"
            )
        print(
            f"\n{scenario.name}: LP beats LS in residual on "
            f"{lp_better_residual}/{trials}, in composed score on "
            f"{lp_better_score}/{trials}; conditioning reverses "
            f"{conditioning_reversals} residual rankings.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260726)
    arguments = parser.parse_args()
    if arguments.trials <= 0:
        raise ValueError("--trials must be positive")
    run_benchmark(arguments.trials, arguments.seed)


if __name__ == "__main__":
    main()
