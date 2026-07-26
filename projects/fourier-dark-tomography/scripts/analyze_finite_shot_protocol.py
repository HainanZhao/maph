#!/usr/bin/env python3
"""Finite-shot benchmark calculations for four-photon directional leakage.

The physical model is deliberately explicit:

* an ideal F_4 followed by a calibrated two-mode X or Y rotation;
* a phenomenological visibility mixture

      P_obs = V P_ind + (1-V) P_dist,

  where ``P_dist`` is the probability for fully distinguishable labelled
  photons in the same single-particle network;
* optional additive background probability per accepted trial.

The mixture is not a general partial-distinguishability model.  It is a
transparent nuisance-floor model used to estimate whether the exact-null
versus transverse-response contrast is statistically resolvable.
"""

from __future__ import annotations

import argparse
import cmath
import math
from collections import defaultdict
from functools import lru_cache


Occupation = tuple[int, int, int, int]
Matrix = tuple[tuple[complex, ...], ...]


def fourier_four() -> Matrix:
    return tuple(
        tuple((1j ** (row * column)) / 2 for column in range(4))
        for row in range(4)
    )


def append_mixer(
    matrix: Matrix,
    pair: tuple[int, int],
    generator: str,
    epsilon: float,
) -> Matrix:
    """Return exp(i epsilon G_pair) times ``matrix``."""
    p, q = pair
    cosine = math.cos(epsilon)
    sine = math.sin(epsilon)
    mixer = [
        [complex(row == column) for column in range(4)]
        for row in range(4)
    ]
    if generator == "X":
        mixer[p][p] = cosine
        mixer[q][q] = cosine
        mixer[p][q] = 1j * sine
        mixer[q][p] = 1j * sine
    elif generator == "Y":
        mixer[p][p] = cosine
        mixer[q][q] = cosine
        mixer[p][q] = sine
        mixer[q][p] = -sine
    else:
        raise ValueError("generator must be X or Y")
    return tuple(
        tuple(
            sum(mixer[row][middle] * matrix[middle][column]
                for middle in range(4))
            for column in range(4)
        )
        for row in range(4)
    )


def repeated_matrix(
    matrix: Matrix,
    input_occupation: Occupation,
    output_occupation: Occupation,
) -> tuple[tuple[complex, ...], ...]:
    input_modes = tuple(
        mode
        for mode, multiplicity in enumerate(input_occupation)
        for _ in range(multiplicity)
    )
    output_modes = tuple(
        mode
        for mode, multiplicity in enumerate(output_occupation)
        for _ in range(multiplicity)
    )
    return tuple(
        tuple(matrix[output_mode][input_mode] for input_mode in input_modes)
        for output_mode in output_modes
    )


def permanent(matrix: tuple[tuple[complex, ...], ...]) -> complex:
    """Ryser-independent bit-mask recurrence, sufficient for N <= 11."""
    size = len(matrix)

    @lru_cache(maxsize=None)
    def recurse(row: int, available: int) -> complex:
        if row == size:
            return 1.0 + 0.0j
        total = 0.0 + 0.0j
        bits = available
        while bits:
            bit = bits & -bits
            column = bit.bit_length() - 1
            total += matrix[row][column] * recurse(row + 1, available ^ bit)
            bits ^= bit
        return total

    return recurse(0, (1 << size) - 1)


def indistinguishable_probability(
    matrix: Matrix,
    input_occupation: Occupation,
    output_occupation: Occupation,
) -> float:
    repeated = repeated_matrix(matrix, input_occupation, output_occupation)
    denominator = 1
    for multiplicity in input_occupation + output_occupation:
        denominator *= math.factorial(multiplicity)
    return abs(permanent(repeated)) ** 2 / denominator


def distinguishable_probability(
    matrix: Matrix,
    input_occupation: Occupation,
    output_occupation: Occupation,
) -> float:
    """Probability for labelled, mutually distinguishable input photons."""
    distribution: dict[Occupation, float] = {(0, 0, 0, 0): 1.0}
    for input_mode, multiplicity in enumerate(input_occupation):
        for _ in range(multiplicity):
            updated: dict[Occupation, float] = defaultdict(float)
            for occupation, probability in distribution.items():
                for output_mode in range(4):
                    next_occupation = list(occupation)
                    next_occupation[output_mode] += 1
                    updated[tuple(next_occupation)] += (
                        probability * abs(matrix[output_mode][input_mode]) ** 2
                    )
            distribution = dict(updated)
    return distribution.get(output_occupation, 0.0)


def observed_probability(
    matrix: Matrix,
    input_occupation: Occupation,
    output_occupation: Occupation,
    visibility: float,
    background: float,
) -> float:
    return (
        visibility
        * indistinguishable_probability(
            matrix, input_occupation, output_occupation
        )
        + (1 - visibility)
        * distinguishable_probability(
            matrix, input_occupation, output_occupation
        )
        + background
    )


def trials_for_z_score(
    probability_a: float,
    probability_b: float,
    z_score: float,
) -> int:
    """Equal trials per setting for a normal-approximation difference test."""
    difference = abs(probability_a - probability_b)
    if difference == 0:
        return math.inf
    variance = (
        probability_a * (1 - probability_a)
        + probability_b * (1 - probability_b)
    )
    return math.ceil(z_score ** 2 * variance / difference ** 2)


def certify_exact_formula() -> None:
    occupation = (0, 1, 2, 1)
    for epsilon in (0.03, 0.1, 0.27, -0.19):
        x_matrix = append_mixer(fourier_four(), (1, 3), "X", epsilon)
        y_matrix = append_mixer(fourier_four(), (1, 3), "Y", epsilon)
        expected_x = math.sin(2 * epsilon) ** 2 / 16
        calculated_x = indistinguishable_probability(
            x_matrix, occupation, occupation
        )
        calculated_y = indistinguishable_probability(
            y_matrix, occupation, occupation
        )
        assert math.isclose(calculated_x, expected_x, abs_tol=1e-13)
        assert calculated_y < 1e-28


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--visibility", type=float, default=0.99)
    parser.add_argument("--background", type=float, default=0.0)
    parser.add_argument("--z-score", type=float, default=5.0)
    args = parser.parse_args()
    if not 0 <= args.visibility <= 1:
        parser.error("--visibility must lie in [0,1]")
    if args.background < 0:
        parser.error("--background must be nonnegative")

    certify_exact_formula()

    occupation = (0, 1, 2, 1)
    base = fourier_four()
    x_matrix = append_mixer(base, (1, 3), "X", args.epsilon)
    y_matrix = append_mixer(base, (1, 3), "Y", args.epsilon)
    probability_x = observed_probability(
        x_matrix,
        occupation,
        occupation,
        args.visibility,
        args.background,
    )
    probability_y = observed_probability(
        y_matrix,
        occupation,
        occupation,
        args.visibility,
        args.background,
    )
    trials = trials_for_z_score(
        probability_x, probability_y, args.z_score
    )

    print("Four-photon quadrature benchmark")
    print(f"epsilon={args.epsilon:g}")
    print(f"visibility={args.visibility:g}")
    print(f"background={args.background:g}")
    print(
        "ideal P_X13="
        f"{indistinguishable_probability(x_matrix, occupation, occupation):.12g}"
    )
    print(
        "ideal P_Y13="
        f"{indistinguishable_probability(y_matrix, occupation, occupation):.12g}"
    )
    print(
        "distinguishable P_X13="
        f"{distinguishable_probability(x_matrix, occupation, occupation):.12g}"
    )
    print(
        "distinguishable P_Y13="
        f"{distinguishable_probability(y_matrix, occupation, occupation):.12g}"
    )
    print(f"observed P_X13={probability_x:.12g}")
    print(f"observed P_Y13={probability_y:.12g}")
    print(
        f"equal trials/setting for {args.z_score:g}-sigma "
        f"normal-approximation contrast: {trials}"
    )
    print("Exact formula certificate passed.")


if __name__ == "__main__":
    main()
