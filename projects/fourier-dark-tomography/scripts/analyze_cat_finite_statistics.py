#!/usr/bin/env python3
"""Finite-angle and Fisher analysis for the four-mode cat protocol.

This file is deliberately independent of the search script.  It evaluates
the normalized four-photon probabilities from their defining polynomial,
uses the exact derivative of exp(i H(theta)) at theta=0, and implements two
explicit count models:

* a multinomial model with a uniform background mixture;
* independent Poisson counts on the selected outcomes with an additive
  per-shot background floor.

No hardware-independent sample-complexity claim is inferred from either
model.  They are local design diagnostics.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fourier_suppression import occupation_vectors  # noqa: E402


Matrix = list[list[complex]]
Vector = list[float]
Occupation = tuple[int, int, int, int]
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
COORDINATES = tuple(
    (kind, pair) for pair in PAIRS for kind in ("X", "Y")
)
OUTPUTS = tuple(occupation_vectors(4, 4))
OUTPUTS_X = (
    (0, 0, 2, 2),
    (0, 1, 1, 2),
    (0, 3, 1, 0),
    (1, 0, 2, 1),
    (1, 0, 3, 0),
    (1, 1, 0, 2),
)
OUTPUTS_Y = (
    (0, 0, 2, 2),
    (0, 1, 1, 2),
    (0, 2, 2, 0),
    (0, 3, 1, 0),
    (1, 0, 2, 1),
    (1, 1, 0, 2),
)


def zero_matrix(size: int = 4) -> Matrix:
    return [[0j for _ in range(size)] for _ in range(size)]


def identity_matrix(size: int = 4) -> Matrix:
    result = zero_matrix(size)
    for index in range(size):
        result[index][index] = 1
    return result


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [a + b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_scale(scale: complex, matrix: Matrix) -> Matrix:
    return [[scale * value for value in row] for row in matrix]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    columns = tuple(zip(*right))
    return [
        [sum(a * b for a, b in zip(row, column)) for column in columns]
        for row in left
    ]


def matrix_max_row_norm(matrix: Matrix) -> float:
    return max(sum(abs(value) for value in row) for row in matrix)


def matrix_exponential(matrix: Matrix, tolerance: float = 2e-16) -> Matrix:
    """Scaling-and-squaring Taylor exponential for a small dense matrix."""
    norm = matrix_max_row_norm(matrix)
    squarings = max(0, math.ceil(math.log2(norm / 0.25))) if norm else 0
    scaled = matrix_scale(2.0 ** (-squarings), matrix)
    result = identity_matrix(len(matrix))
    term = identity_matrix(len(matrix))
    for order in range(1, 160):
        term = matrix_scale(1 / order, matrix_multiply(term, scaled))
        result = matrix_add(result, term)
        if matrix_max_row_norm(term) < tolerance:
            break
    else:
        raise ArithmeticError("matrix exponential series did not converge")
    for _ in range(squarings):
        result = matrix_multiply(result, result)
    return result


def fourier_four() -> Matrix:
    return [
        [(1j ** (row * column)) / 2 for column in range(4)]
        for row in range(4)
    ]


def generator(kind: str, pair: tuple[int, int]) -> Matrix:
    left, right = pair
    result = zero_matrix()
    if kind == "X":
        result[left][right] = 1
        result[right][left] = 1
    elif kind == "Y":
        result[left][right] = -1j
        result[right][left] = 1j
    else:
        raise ValueError(f"unknown generator kind {kind!r}")
    return result


GENERATORS = tuple(generator(kind, pair) for kind, pair in COORDINATES)
PROBE_X = matrix_add(GENERATORS[0], matrix_scale(-1, GENERATORS[2]))
PROBE_Y = matrix_add(GENERATORS[1], matrix_scale(-1, GENERATORS[3]))


def hermitian_from_coordinates(theta: Vector) -> Matrix:
    if len(theta) != 12:
        raise ValueError("theta must contain twelve coordinates")
    result = zero_matrix()
    for weight, basis in zip(theta, GENERATORS):
        result = matrix_add(result, matrix_scale(weight, basis))
    return result


def probe_unitary(probe: Matrix, epsilon: float) -> Matrix:
    """Exact closed form for the two probes, whose cube is 2H."""
    root_two = math.sqrt(2)
    linear = 1j * math.sin(root_two * epsilon) / root_two
    quadratic = (math.cos(root_two * epsilon) - 1) / 2
    return matrix_add(
        matrix_add(identity_matrix(), matrix_scale(linear, probe)),
        matrix_scale(quadratic, matrix_multiply(probe, probe)),
    )


def interferometer(theta: Vector, probe: Matrix, epsilon: float) -> Matrix:
    unknown = matrix_exponential(
        matrix_scale(1j, hermitian_from_coordinates(theta))
    )
    return matrix_multiply(
        matrix_multiply(probe_unitary(probe, epsilon), unknown),
        fourier_four(),
    )


def cat_amplitude(output: Occupation, unitary: Matrix) -> complex:
    """Amplitude from (|4000>+|0400>+|0040>+|0004>)/2."""
    prefactor = math.sqrt(
        math.factorial(4)
        / math.prod(math.factorial(count) for count in output)
    ) / 2
    total = 0j
    for input_mode in range(4):
        product_value = 1 + 0j
        for output_mode, count in enumerate(output):
            product_value *= unitary[output_mode][input_mode] ** count
        total += product_value
    return prefactor * total


def cat_amplitude_directional_derivative(
    output: Occupation,
    unitary: Matrix,
    direction: Matrix,
) -> complex:
    """Derivative of the cat amplitude polynomial U -> U+t*direction."""
    prefactor = math.sqrt(
        math.factorial(4)
        / math.prod(math.factorial(count) for count in output)
    ) / 2
    total = 0j
    for input_mode in range(4):
        for differentiated_mode, count in enumerate(output):
            if not count:
                continue
            term = count * direction[differentiated_mode][input_mode]
            for output_mode, exponent in enumerate(output):
                if output_mode == differentiated_mode:
                    exponent -= 1
                term *= unitary[output_mode][input_mode] ** exponent
            total += term
    return prefactor * total


def probabilities(theta: Vector, probe: Matrix, epsilon: float) -> list[float]:
    unitary = interferometer(theta, probe, epsilon)
    return [abs(cat_amplitude(output, unitary)) ** 2 for output in OUTPUTS]


def probability_jacobian_at_zero(
    probe: Matrix,
    epsilon: float,
) -> list[list[float]]:
    """Rows are outputs and columns are the twelve theta derivatives."""
    q = probe_unitary(probe, epsilon)
    nominal = matrix_multiply(q, fourier_four())
    directions = [
        matrix_multiply(
            matrix_multiply(q, matrix_scale(1j, basis)),
            fourier_four(),
        )
        for basis in GENERATORS
    ]
    rows = []
    for output in OUTPUTS:
        amplitude = cat_amplitude(output, nominal)
        rows.append([
            2 * (
                amplitude.conjugate()
                * cat_amplitude_directional_derivative(
                    output, nominal, direction
                )
            ).real
            for direction in directions
        ])
    return rows


def selected_contrast_jacobian(epsilon: float) -> list[list[float]]:
    """Jacobian of [P(+eps)-P(-eps)]/eps for the 12 selected contrasts."""
    by_output_x = {
        output: (plus, minus)
        for output, plus, minus in zip(
            OUTPUTS,
            probability_jacobian_at_zero(PROBE_X, epsilon),
            probability_jacobian_at_zero(PROBE_X, -epsilon),
        )
    }
    by_output_y = {
        output: (plus, minus)
        for output, plus, minus in zip(
            OUTPUTS,
            probability_jacobian_at_zero(PROBE_Y, epsilon),
            probability_jacobian_at_zero(PROBE_Y, -epsilon),
        )
    }
    rows = []
    for output in OUTPUTS_X:
        plus, minus = by_output_x[output]
        rows.append([(a - b) / epsilon for a, b in zip(plus, minus)])
    for output in OUTPUTS_Y:
        plus, minus = by_output_y[output]
        rows.append([(a - b) / epsilon for a, b in zip(plus, minus)])
    return rows


def limiting_contrast_jacobian() -> list[list[float]]:
    """The exact rational matrix from the rank certificate, as floats."""
    x_rows = (
        (0, -1.5, 0, 0, -1.5, 0),
        (0.75, 0, 0, 0.75, 0, 1.5),
        (2.25, 0, 0, 0.75, 0, 0),
        (0.75, 0, 0.75, 0, 0, 1.5),
        (0, -4, 0, 0, 0, 0),
        (0.75, 0, 1.5, 0.75, 0, 0),
    )
    y_rows = (
        (0, -1.5, 0, 0, -1.5, 0),
        (0.75, 0, 0, 0.75, 0, 1.5),
        (0, -1.5, 0, 0, 1.5, 0),
        (2.25, 0, 0, 0.75, 0, 0),
        (0.75, 0, -0.75, 0, 0, 1.5),
        (0.75, 0, -1.5, 0.75, 0, 0),
    )
    rows = []
    x_columns = (0, 2, 4, 6, 8, 10)
    y_columns = (1, 3, 5, 7, 9, 11)
    for block_row in x_rows:
        row = [0.0] * 12
        for column, value in zip(x_columns, block_row):
            row[column] = value
        rows.append(row)
    for block_row in y_rows:
        row = [0.0] * 12
        for column, value in zip(y_columns, block_row):
            row[column] = value
        rows.append(row)
    return rows


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def gram_matrix(rows: list[list[float]]) -> list[list[float]]:
    columns = transpose(rows)
    return [
        [sum(a * b for a, b in zip(left, right)) for right in columns]
        for left in columns
    ]


def jacobi_eigenvalues(
    symmetric: list[list[float]],
    tolerance: float = 1e-13,
) -> list[float]:
    """Eigenvalues of a real symmetric matrix via cyclic Jacobi rotations."""
    matrix = [row.copy() for row in symmetric]
    size = len(matrix)
    for _ in range(80 * size * size):
        p, q, largest = 0, 1, 0.0
        for row in range(size):
            for column in range(row + 1, size):
                value = abs(matrix[row][column])
                if value > largest:
                    p, q, largest = row, column, value
        if largest < tolerance:
            break
        angle = 0.5 * math.atan2(
            2 * matrix[p][q], matrix[q][q] - matrix[p][p]
        )
        cosine, sine = math.cos(angle), math.sin(angle)
        app, aqq, apq = matrix[p][p], matrix[q][q], matrix[p][q]
        matrix[p][p] = (
            cosine * cosine * app
            - 2 * sine * cosine * apq
            + sine * sine * aqq
        )
        matrix[q][q] = (
            sine * sine * app
            + 2 * sine * cosine * apq
            + cosine * cosine * aqq
        )
        matrix[p][q] = matrix[q][p] = 0.0
        for index in range(size):
            if index in (p, q):
                continue
            aip, aiq = matrix[index][p], matrix[index][q]
            matrix[index][p] = matrix[p][index] = cosine * aip - sine * aiq
            matrix[index][q] = matrix[q][index] = sine * aip + cosine * aiq
    return sorted(matrix[index][index] for index in range(size))


def spectral_condition(rows: list[list[float]]) -> float:
    eigenvalues = jacobi_eigenvalues(gram_matrix(rows))
    if eigenvalues[0] <= 0:
        return math.inf
    return math.sqrt(eigenvalues[-1] / eigenvalues[0])


def frobenius_relative_error(
    matrix: list[list[float]], reference: list[list[float]]
) -> float:
    numerator = sum(
        (value - target) ** 2
        for row, reference_row in zip(matrix, reference)
        for value, target in zip(row, reference_row)
    )
    denominator = sum(value * value for row in reference for value in row)
    return math.sqrt(numerator / denominator)


def outer_add(
    information: list[list[float]], derivative: list[float], weight: float
) -> None:
    for row in range(12):
        for column in range(12):
            information[row][column] += (
                weight * derivative[row] * derivative[column]
            )


def multinomial_information(
    epsilon: float, background_fraction: float = 0.0
) -> list[list[float]]:
    """Selected-channel FI for four equally allocated multinomial settings.

    The observation law is q_s=(1-beta)p_s+beta/35.  This is a normalized
    multinomial background model, unlike an additive dark-count rate.  The
    six selected outputs are resolved and all other outputs are pooled into
    one category, so bright outcomes do not silently add tomography data.
    """
    if not 0 <= background_fraction < 1:
        raise ValueError("background_fraction must lie in [0,1)")
    information = [[0.0] * 12 for _ in range(12)]
    zero = [0.0] * 12
    for (probe, selected_outputs), sign in product(
        ((PROBE_X, OUTPUTS_X), (PROBE_Y, OUTPUTS_Y)), (1, -1)
    ):
        probability = probabilities(zero, probe, sign * epsilon)
        jacobian = probability_jacobian_at_zero(probe, sign * epsilon)
        by_output = dict(zip(OUTPUTS, zip(probability, jacobian)))
        selected_probability = 0.0
        selected_derivative = [0.0] * 12
        for output in selected_outputs:
            p_value, derivative = by_output[output]
            selected_probability += p_value
            selected_derivative = [
                left + right
                for left, right in zip(selected_derivative, derivative)
            ]
            q_value = (
                (1 - background_fraction) * p_value
                + background_fraction / len(OUTPUTS)
            )
            observed_derivative = [
                (1 - background_fraction) * value for value in derivative
            ]
            if q_value > 2e-15:
                outer_add(
                    information, observed_derivative, 0.25 / q_value
                )
            elif max(abs(value) for value in observed_derivative) > 2e-12:
                raise ArithmeticError("nonzero score on a zero-probability event")
        other_probability = 1 - selected_probability
        other_q = (
            (1 - background_fraction) * other_probability
            + background_fraction
            * (len(OUTPUTS) - len(selected_outputs))
            / len(OUTPUTS)
        )
        other_derivative = [
            -(1 - background_fraction) * value
            for value in selected_derivative
        ]
        outer_add(information, other_derivative, 0.25 / other_q)
    return information


def selected_poisson_information(
    epsilon: float, background_floor: float = 0.0
) -> list[list[float]]:
    """Per-total-shot FI from selected independent Poisson count channels.

    Each selected channel has mean N_setting*(p_s+b), with equal allocation
    among the four settings.  The floor b is a count probability per input
    trial and per selected outcome.  Unselected outcomes are discarded.
    """
    if background_floor < 0:
        raise ValueError("background_floor cannot be negative")
    information = [[0.0] * 12 for _ in range(12)]
    zero = [0.0] * 12
    for probe, outputs in ((PROBE_X, OUTPUTS_X), (PROBE_Y, OUTPUTS_Y)):
        for sign in (1, -1):
            probability = dict(
                zip(OUTPUTS, probabilities(zero, probe, sign * epsilon))
            )
            jacobian = dict(
                zip(
                    OUTPUTS,
                    probability_jacobian_at_zero(probe, sign * epsilon),
                )
            )
            for output in outputs:
                mean = probability[output] + background_floor
                if mean > 2e-15:
                    outer_add(information, jacobian[output], 0.25 / mean)
    return information


def information_root_condition(information: list[list[float]]) -> float:
    """Condition of a whitened sensitivity; square gives FI condition."""
    eigenvalues = jacobi_eigenvalues(information)
    if eigenvalues[0] <= 0:
        return math.inf
    return math.sqrt(eigenvalues[-1] / eigenvalues[0])


def selected_probe_probabilities(epsilon: float) -> tuple[float, float]:
    zero = [0.0] * 12
    values = []
    for probe, outputs in ((PROBE_X, OUTPUTS_X), (PROBE_Y, OUTPUTS_Y)):
        probability = dict(zip(OUTPUTS, probabilities(zero, probe, epsilon)))
        values.extend(probability[output] for output in outputs)
    return min(values), max(values)


@dataclass(frozen=True)
class Diagnostic:
    epsilon: float
    relative_bias: float
    contrast_condition: float
    min_probe_probability: float
    max_probe_probability: float
    poisson_condition_no_floor: float
    poisson_condition_floor_1e6: float
    poisson_condition_floor_1e4: float
    multinomial_condition_beta_1e3: float


def diagnostic(epsilon: float) -> Diagnostic:
    finite = selected_contrast_jacobian(epsilon)
    limiting = limiting_contrast_jacobian()
    min_probability, max_probability = selected_probe_probabilities(epsilon)
    return Diagnostic(
        epsilon=epsilon,
        relative_bias=frobenius_relative_error(finite, limiting),
        contrast_condition=spectral_condition(finite),
        min_probe_probability=min_probability,
        max_probe_probability=max_probability,
        poisson_condition_no_floor=information_root_condition(
            selected_poisson_information(epsilon)
        ),
        poisson_condition_floor_1e6=information_root_condition(
            selected_poisson_information(epsilon, 1e-6)
        ),
        poisson_condition_floor_1e4=information_root_condition(
            selected_poisson_information(epsilon, 1e-4)
        ),
        multinomial_condition_beta_1e3=information_root_condition(
            multinomial_information(epsilon, 1e-3)
        ),
    )


def self_check() -> None:
    zero = [0.0] * 12
    for probe, epsilon in (
        (PROBE_X, 0.173),
        (PROBE_Y, -0.219),
    ):
        total = sum(probabilities(zero, probe, epsilon))
        assert abs(total - 1) < 2e-13
    theta = [
        0.003 * math.sin(index + 1) for index in range(12)
    ]
    total = sum(probabilities(theta, PROBE_X, 0.11))
    assert abs(total - 1) < 3e-13

    limiting = limiting_contrast_jacobian()
    errors = []
    for epsilon in (0.04, 0.02, 0.01):
        errors.append(
            frobenius_relative_error(
                selected_contrast_jacobian(epsilon), limiting
            )
        )
    assert errors[0] / errors[1] > 3.9
    assert errors[1] / errors[2] > 3.9

    # Compare the analytic probability derivative with a symmetric numerical
    # derivative through the full matrix exponential.
    epsilon = 0.137
    analytic = probability_jacobian_at_zero(PROBE_X, epsilon)
    step = 2e-6
    for coordinate in (0, 3, 8, 11):
        positive = zero.copy()
        negative = zero.copy()
        positive[coordinate] = step
        negative[coordinate] = -step
        plus = probabilities(positive, PROBE_X, epsilon)
        minus = probabilities(negative, PROBE_X, epsilon)
        for output_index in range(len(OUTPUTS)):
            numerical = (plus[output_index] - minus[output_index]) / (2 * step)
            assert abs(numerical - analytic[output_index][coordinate]) < 3e-9


def main() -> None:
    self_check()
    print("finite-angle probability and derivative checks passed")
    print(
        "epsilon  rel_bias  kappa(J)  selected p[min,max]  "
        "kappa_P(b=0,1e-6,1e-4)  kappa_M(beta=1e-3)"
    )
    for epsilon in (0.005, 0.01, 0.02, 0.05, 0.10, 0.15, 0.20):
        item = diagnostic(epsilon)
        print(
            f"{item.epsilon:7.3f}  {item.relative_bias:8.3e}  "
            f"{item.contrast_condition:8.3f}  "
            f"[{item.min_probe_probability:.3e},"
            f"{item.max_probe_probability:.3e}]  "
            f"[{item.poisson_condition_no_floor:.3f},"
            f"{item.poisson_condition_floor_1e6:.3f},"
            f"{item.poisson_condition_floor_1e4:.3f}]  "
            f"{item.multinomial_condition_beta_1e3:.3f}"
        )


if __name__ == "__main__":
    main()
