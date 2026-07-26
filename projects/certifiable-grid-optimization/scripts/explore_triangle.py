#!/usr/bin/env python3
"""Print exact and adversarial three-bus cycle certificates."""

from pathlib import Path
import cmath
import math
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.cycle_certificate import (  # noqa: E402
    balanced_unit_triangle_recovery,
    EdgeMoment,
    cycle_phase_defect,
    edge_residual,
    radial_defect,
    reconstruct_from_tree,
)


def summarize(name, diagonal, edges):
    recovered = reconstruct_from_tree(
        diagonal, edges, [(0, 1), (1, 2)], root=0
    )
    print(name)
    print("  radial defects:", [round(radial_defect(diagonal, edge), 12)
                                for edge in edges])
    print("  cycle defect:", round(cycle_phase_defect(edges, [0, 1, 2]), 12))
    print("  recovery residuals:", [round(edge_residual(recovered, edge), 12)
                                    for edge in edges])


def main():
    diagonal = {0: 1.0, 1: 1.0, 2: 1.0}
    exact_edges = [
        EdgeMoment(0, 1, cmath.exp(0.2j)),
        EdgeMoment(1, 2, cmath.exp(-0.5j)),
        EdgeMoment(0, 2, cmath.exp(-0.3j)),
    ]
    summarize("exact rank-one triangle", diagonal, exact_edges)

    radial_slack = [
        EdgeMoment(0, 1, 0.8),
        EdgeMoment(1, 2, 0.8),
        EdgeMoment(0, 2, 0.8),
    ]
    summarize("zero holonomy but radial slack", diagonal, radial_slack)

    phase_slack = [
        exact_edges[0],
        exact_edges[1],
        EdgeMoment(0, 2, exact_edges[2].value * cmath.exp(0.15j)),
    ]
    summarize("edge saturation but nonzero holonomy", diagonal, phase_slack)

    tree_voltage = reconstruct_from_tree(
        diagonal, phase_slack, [(0, 1), (1, 2)], root=0
    )
    balanced_voltage = balanced_unit_triangle_recovery(phase_slack)
    tree_error = sum(
        edge_residual(tree_voltage, edge) ** 2 for edge in phase_slack
    )
    balanced_error = sum(
        edge_residual(balanced_voltage, edge) ** 2 for edge in phase_slack
    )
    print("phase projection comparison")
    print("  spanning-tree squared error:", round(tree_error, 12))
    print("  balanced squared error:", round(balanced_error, 12))
    print("  improvement factor:", round(tree_error / balanced_error, 6))


if __name__ == "__main__":
    main()
