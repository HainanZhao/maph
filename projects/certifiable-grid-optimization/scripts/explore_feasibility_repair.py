#!/usr/bin/env python3
"""Explore local feasibility certificates and their collapse failure mode."""

from pathlib import Path
import math
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.lossless_triangle import (  # noqa: E402
    injections,
    kantorovich_certificate,
    newton_solve,
)


def main():
    print("Certified small-injection repair")
    initial = (0.0, 0.0)
    target = (0.01, -0.006)
    certificate = kantorovich_certificate(initial, target)
    solution = newton_solve(initial, target)
    print("  certificate:", certificate)
    print("  Newton solution:", tuple(round(value, 12) for value in solution))

    print("Arbitrarily small but infeasible residual at collapse")
    collapse = (math.pi / 2.0, math.pi / 2.0)
    for epsilon in (1e-3, 1e-6, 1e-9):
        target = (1.0 + epsilon, 1.0 + epsilon)
        certificate = kantorovich_certificate(collapse, target)
        print(
            f"  epsilon={epsilon:g}, "
            f"residual={certificate.residual_inf:g}, "
            f"certified={certificate.certified}"
        )
    print("  obstruction: target p1+p2 > 2, while every feasible p1+p2 <= 2")
    print("  collapse injection:", injections(collapse))


if __name__ == "__main__":
    main()
