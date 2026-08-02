#!/usr/bin/env python3
"""Exploratory rational-grid search for a Cycle 76 denominator wedge."""
from fractions import Fraction as Q
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from conventions.denominator_geometry_v1 import exponent_cell


def denominator_bound(theta: Q, kappa: Q, alpha: Q) -> Q:
    derivative = Q(1, 10) + alpha / 6 + theta / 3
    tube = 2 * theta / 3 - Q(2, 15) - kappa / 3
    ratio = (-1 + 3 * theta - alpha - kappa) / 3
    fixed_a = min(theta, max(Q(0), derivative, tube, ratio))
    return alpha + fixed_a


def main() -> None:
    best = None
    for denominator in range(25, 301):
        for theta_n in range(denominator + 1):
            theta = Q(theta_n, denominator)
            for kappa_n in range(denominator + 1):
                kappa = Q(kappa_n, denominator)
                if theta + kappa > Q(11, 25):
                    continue
                for alpha_n in range(theta_n + 1):
                    alpha = Q(alpha_n, denominator)
                    old = exponent_cell(theta, kappa, alpha)
                    if not old["live_residual"]:
                        continue
                    new = denominator_bound(theta, kappa, alpha)
                    target = Q(6, 25) - kappa
                    if new < target:
                        margin = target - new
                        row = (margin, theta, kappa, alpha, old["banked_count_bound"], new)
                        if best is None or row > best:
                            best = row
        if best is not None:
            break
    print(best)


if __name__ == "__main__":
    main()
