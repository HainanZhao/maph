#!/usr/bin/env python3
"""Finite-shot weighted local reconstruction for the sparse F4 protocol.

This is a deliberately modest end-to-end estimator, not a universal hardware
model.  It uses:

* the exact four-photon cat probabilities at finite probe angle;
* pre-calibrated probe-only baselines treated as exact;
* a local weighted least-squares estimator;
* A-optimal allocation between the two signed probe pairs;
* independent Poisson selected-channel counts with an optional calibrated
  additive background.

All twelve coherent-error coordinates are varied simultaneously.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.analyze_cat_finite_statistics import (
    OUTPUTS,
    OUTPUTS_X,
    OUTPUTS_Y,
    PROBE_X,
    PROBE_Y,
    probabilities,
    selected_contrast_jacobian,
)


def inverse(matrix: list[list[float]]) -> list[list[float]]:
    size = len(matrix)
    augmented = [
        row.copy() + [1.0 if i == j else 0.0 for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = max(
            range(column, size),
            key=lambda row: abs(augmented[row][column]),
        )
        if abs(augmented[pivot][column]) < 1e-14:
            raise ArithmeticError("singular normal matrix")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    augmented[row], augmented[column]
                )
            ]
    return [row[size:] for row in augmented]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def trace(matrix: list[list[float]]) -> float:
    return sum(matrix[index][index] for index in range(len(matrix)))


def optimal_pair_fraction(
    epsilon: float, background: float
) -> tuple[float, float]:
    """A-optimal fraction for the declared signed-contrast estimator.

    The separate raw sign counts contain common-mode information that is
    discarded when they are compressed into the baseline-subtracted
    contrasts used by the manuscript estimator.  Optimize the covariance of
    that estimator itself, with one nominal total trial, so the returned
    objective is N times the covariance trace.
    """

    def objective(fraction: float) -> float:
        jacobian, variances, _ = design_rows(
            epsilon, 1.0, fraction, background
        )
        covariance = weighted_estimate(
            [0.0] * len(jacobian), jacobian, variances
        )[1]
        return trace(covariance)

    left, right = 0.02, 0.98
    ratio = (math.sqrt(5) - 1) / 2
    x1 = right - ratio * (right - left)
    x2 = left + ratio * (right - left)
    f1, f2 = objective(x1), objective(x2)
    for _ in range(80):
        if f1 < f2:
            right, x2, f2 = x2, x1, f1
            x1 = right - ratio * (right - left)
            f1 = objective(x1)
        else:
            left, x1, f1 = x1, x2, f2
            x2 = left + ratio * (right - left)
            f2 = objective(x2)
    fraction = (left + right) / 2
    return fraction, objective(fraction)


def poisson_sample(mean: float, rng: random.Random) -> int:
    """Poisson sampler: inversion for small means, PTRS for large means."""
    if mean < 0:
        raise ValueError("Poisson mean must be nonnegative")
    if mean == 0:
        return 0
    if mean < 30:
        threshold = math.exp(-mean)
        product_value = 1.0
        count = 0
        while product_value > threshold:
            count += 1
            product_value *= rng.random()
        return count - 1
    root = math.sqrt(mean)
    log_mean = math.log(mean)
    b = 0.931 + 2.53 * root
    a = -0.059 + 0.02483 * b
    inverse_alpha = 1.1239 + 1.1328 / (b - 3.4)
    squeeze = 0.9277 - 3.6224 / (b - 2)
    while True:
        u = rng.random() - 0.5
        v = rng.random()
        distance = 0.5 - abs(u)
        candidate = math.floor((2 * a / distance + b) * u + mean + 0.43)
        if distance >= 0.07 and v <= squeeze:
            return candidate
        if candidate < 0 or (distance < 0.013 and v > distance):
            continue
        log_acceptance = math.log(
            v * inverse_alpha / (a / (distance * distance) + b)
        )
        target = (
            -mean
            + candidate * log_mean
            - math.lgamma(candidate + 1)
        )
        if log_acceptance <= target:
            return candidate


def design_rows(
    epsilon: float,
    total_trials: float,
    real_fraction: float,
    background: float,
) -> tuple[list[list[float]], list[float], list[tuple]]:
    jacobian = selected_contrast_jacobian(epsilon)
    settings = []
    variances = []
    zero = [0.0] * 12
    for probe, outputs, pair_fraction in (
        (PROBE_X, OUTPUTS_X, real_fraction),
        (PROBE_Y, OUTPUTS_Y, 1 - real_fraction),
    ):
        sign_trials = total_trials * pair_fraction / 2
        by_sign = {}
        for sign in (1, -1):
            probability = probabilities(zero, probe, sign * epsilon)
            by_sign[sign] = dict(zip(OUTPUTS, probability))
        for output in outputs:
            variance = (
                (by_sign[1][output] + background) / sign_trials
                + (by_sign[-1][output] + background) / sign_trials
            ) / epsilon**2
            variances.append(variance)
            settings.append(
                (
                    probe,
                    output,
                    sign_trials,
                    by_sign[1][output],
                    by_sign[-1][output],
                )
            )
    return jacobian, variances, settings


def weighted_estimate(
    response: list[float],
    jacobian: list[list[float]],
    variances: list[float],
) -> tuple[list[float], list[list[float]]]:
    normal = [[0.0] * 12 for _ in range(12)]
    right = [0.0] * 12
    for row, observed, variance in zip(jacobian, response, variances):
        weight = 1 / variance
        for left_index in range(12):
            right[left_index] += weight * row[left_index] * observed
            for right_index in range(12):
                normal[left_index][right_index] += (
                    weight * row[left_index] * row[right_index]
                )
    covariance = inverse(normal)
    return matvec(covariance, right), covariance


def exact_response(
    theta: list[float], epsilon: float
) -> list[float]:
    zero = [0.0] * 12
    response = []
    for probe, outputs in ((PROBE_X, OUTPUTS_X), (PROBE_Y, OUTPUTS_Y)):
        plus = dict(zip(OUTPUTS, probabilities(theta, probe, epsilon)))
        minus = dict(zip(OUTPUTS, probabilities(theta, probe, -epsilon)))
        plus_zero = dict(zip(OUTPUTS, probabilities(zero, probe, epsilon)))
        minus_zero = dict(zip(OUTPUTS, probabilities(zero, probe, -epsilon)))
        for output in outputs:
            response.append(
                (
                    plus[output]
                    - plus_zero[output]
                    - minus[output]
                    + minus_zero[output]
                )
                / epsilon
            )
    return response


def monte_carlo(
    *,
    epsilon: float,
    total_trials: int,
    background: float,
    error_norm: float,
    repetitions: int,
    seed: int,
) -> dict[str, float]:
    real_fraction, information_trace = optimal_pair_fraction(
        epsilon, background
    )
    jacobian, variances, settings = design_rows(
        epsilon, total_trials, real_fraction, background
    )
    direction = [math.sin(index + 1) for index in range(12)]
    norm = math.sqrt(sum(value * value for value in direction))
    theta = [error_norm * value / norm for value in direction]
    covariance = weighted_estimate([0.0] * 12, jacobian, variances)[1]
    predicted_rmse = math.sqrt(trace(covariance))
    rng = random.Random(seed)
    squared_errors = 0.0
    mean_error = [0.0] * 12
    covered = 0
    information = inverse(covariance)
    true_probabilities = {}
    for probe, outputs in ((PROBE_X, OUTPUTS_X), (PROBE_Y, OUTPUTS_Y)):
        true_probabilities[id(probe)] = (
            dict(zip(OUTPUTS, probabilities(theta, probe, epsilon))),
            dict(zip(OUTPUTS, probabilities(theta, probe, -epsilon))),
        )
    for _ in range(repetitions):
        response = []
        for probe, output, sign_trials, baseline_plus, baseline_minus in settings:
            true_plus, true_minus = true_probabilities[id(probe)]
            plus_count = poisson_sample(
                sign_trials * (true_plus[output] + background), rng
            )
            minus_count = poisson_sample(
                sign_trials * (true_minus[output] + background), rng
            )
            response.append(
                (
                    plus_count / sign_trials
                    - baseline_plus
                    - minus_count / sign_trials
                    + baseline_minus
                )
                / epsilon
            )
        estimate, _ = weighted_estimate(response, jacobian, variances)
        error = [value - target for value, target in zip(estimate, theta)]
        squared_errors += sum(value * value for value in error)
        mean_error = [
            total + value for total, value in zip(mean_error, error)
        ]
        statistic = sum(
            error[row]
            * information[row][column]
            * error[column]
            for row in range(12)
            for column in range(12)
        )
        if statistic <= 21.0261:  # chi-square_12 95% quantile
            covered += 1
    bias_norm = math.sqrt(
        sum((value / repetitions) ** 2 for value in mean_error)
    )
    return {
        "real_fraction": real_fraction,
        "N_times_covariance_trace": information_trace,
        "predicted_rmse": predicted_rmse,
        "empirical_rmse": math.sqrt(squared_errors / repetitions),
        "bias_norm": bias_norm,
        "coverage": covered / repetitions,
    }


def linearity_radius_scan(
    epsilon: float,
    radii: tuple[float, ...] = (1e-4, 1e-3, 3e-3, 1e-2, 3e-2),
    directions: int = 128,
    seed: int = 701,
) -> list[tuple[float, float, float]]:
    """Median and worst relative deterministic inversion error on spheres."""
    rng = random.Random(seed)
    jacobian = selected_contrast_jacobian(epsilon)
    result = []
    for radius in radii:
        relative_errors = []
        for _ in range(directions):
            direction = [rng.gauss(0, 1) for _ in range(12)]
            norm = math.sqrt(sum(value * value for value in direction))
            theta = [radius * value / norm for value in direction]
            estimate, _ = weighted_estimate(
                exact_response(theta, epsilon),
                jacobian,
                [1.0] * 12,
            )
            error = math.sqrt(
                sum(
                    (value - target) ** 2
                    for value, target in zip(estimate, theta)
                )
            )
            relative_errors.append(error / radius)
        relative_errors.sort()
        result.append(
            (
                radius,
                relative_errors[len(relative_errors) // 2],
                relative_errors[-1],
            )
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", type=float, default=0.05)
    parser.add_argument("--trials", type=int, default=2_000_000)
    parser.add_argument("--background", type=float, default=1e-5)
    parser.add_argument("--error-norm", type=float, default=0.002)
    parser.add_argument("--repetitions", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=700)
    args = parser.parse_args()
    result = monte_carlo(
        epsilon=args.epsilon,
        total_trials=args.trials,
        background=args.background,
        error_norm=args.error_norm,
        repetitions=args.repetitions,
        seed=args.seed,
    )
    for key, value in result.items():
        print(f"{key}: {value:.6g}")
    print("radius median_relative_bias max_relative_bias")
    for radius, median, maximum in linearity_radius_scan(args.epsilon):
        print(f"{radius:.1e} {median:.3e} {maximum:.3e}")


if __name__ == "__main__":
    main()
