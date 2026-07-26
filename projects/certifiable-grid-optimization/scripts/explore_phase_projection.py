#!/usr/bin/env python3
"""Compare tree, balanced, and certificate-aware triangle projections."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.phase_projection import (  # noqa: E402
    balanced_triangle_projection,
    best_tree_triangle_projection,
    conditioned_triangle_projection,
    grid_optimal_conditioned_triangle_projection,
    grid_optimal_triangle_projection,
)
import math


def report(label, delta, weights):
    tree = best_tree_triangle_projection(delta, weights)
    balanced = balanced_triangle_projection(delta, weights)
    optimized = grid_optimal_triangle_projection(
        delta, weights, grid_steps=600
    )
    print(label)
    for name, result in (
        ("best tree", tree),
        ("balanced", balanced),
        ("grid optimized", optimized),
    ):
        allocation = tuple(round(value, 6) for value in result.allocation)
        print(
            f"  {name:14s} allocation={allocation}, "
            f"worst_bus={result.worst_bus_bound:.9f}"
        )


def main():
    report("equal weights", 0.6, (1.0, 1.0, 1.0))
    report("one expensive edge", 0.6, (5.0, 1.0, 1.0))
    report("fully asymmetric", 0.6, (4.0, 2.0, 1.0))

    delta = 0.18
    measured = (-math.pi / 2.0, 0.0, math.pi / 2.0 + delta)
    singular_tree = conditioned_triangle_projection(
        measured, (0.0, 0.0, delta)
    )
    conditioned = grid_optimal_conditioned_triangle_projection(
        measured, grid_steps=300
    )
    print("near-collapse conditioning-aware projection")
    print("  tree h bound:", singular_tree.h_bound)
    print(
        "  optimized allocation:",
        tuple(round(value, 6) for value in conditioned.allocation),
    )
    print("  optimized theta:", tuple(round(value, 6) for value in conditioned.theta))
    print("  optimized residual bound:", round(conditioned.residual_bound, 9))
    print("  optimized inverse-Jacobian norm:", round(conditioned.inverse_jacobian_inf, 6))
    print("  optimized h bound:", round(conditioned.h_bound, 6))

    print("conditioning threshold sweep")
    for base, delta in ((0.5, 0.1), (1.0, 0.03), (1.3, 0.01), (1.3, 0.03)):
        measured = (-base, 0.0, base + delta)
        result = grid_optimal_conditioned_triangle_projection(
            measured, grid_steps=120
        )
        print(
            f"  base={base:.2f}, delta={delta:.2f}, "
            f"beta={result.inverse_jacobian_inf:.3f}, "
            f"h={result.h_bound:.3f}, certified={result.h_bound <= 0.5}"
        )


if __name__ == "__main__":
    main()
