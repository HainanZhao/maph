#!/usr/bin/env python3
"""Numerical convention audit for the maximal-order d=8 AFK tuple.

This is a transparent Python transcription of the generic rank-one
continued-fraction evaluator in Zauner.jl, revision
dcff219c986208ce900e2ddaaed8eae2bae6756f.  It is a convention and
root-label certificate; the exact finite certificate is separate.
"""

from __future__ import annotations

import cmath
import math
import re
import subprocess
from pathlib import Path

import numpy

from explore_dimension_four_double_sine import double_sine


ROOT = Path(__file__).resolve().parents[1]
DIMENSION = 8
BETA = (3 + math.sqrt(5)) / 2
AT = numpy.array([[377, -144], [144, -55]], dtype=int)
TAU = -cmath.exp(math.pi * 1j / DIMENSION)
OMEGA = cmath.exp(2j * math.pi / DIMENSION)


def exponential(value: complex) -> complex:
    return cmath.exp(2j * math.pi * value)


def q_pochhammer(first: complex, second: complex, count: int) -> complex:
    result = 1 + 0j
    power = 1 + 0j
    for _ in range(count):
        result *= 1 - first * power
        power *= second
    return result


def q_pochhammer_exp(argument: float, period: float, count: int) -> complex:
    if count >= 0:
        return q_pochhammer(
            exponential(argument), exponential(period), count
        )
    return (1 - exponential(argument)) / q_pochhammer(
        exponential(argument), exponential(-period), 1 - count
    )


def psl2_word(matrix: numpy.ndarray) -> list[int]:
    reduced = matrix.astype(object).copy()
    word: list[int] = []
    identity = numpy.eye(2, dtype=object)
    while not numpy.array_equal(abs(reduced), identity):
        if reduced[1, 0] == 0:
            word.append(
                (1 if reduced[0, 0] > 0 else -1) * reduced[0, 1]
            )
            return word
        quotient = max(
            0, math.ceil(reduced[0, 0] / reduced[1, 0])
        )
        word.append(quotient)
        reduced = numpy.array(
            [
                [reduced[1, 0], reduced[1, 1]],
                [
                    quotient * reduced[1, 0] - reduced[0, 0],
                    quotient * reduced[1, 1] - reduced[0, 1],
                ],
            ],
            dtype=object,
        )
    word.append(0)
    return word


def periods() -> numpy.ndarray:
    word = psl2_word(AT)
    assert word == [3, 3, 3, 3, 3, 3, 0]
    rows = numpy.zeros((len(word) + 1, 2))
    rows[:2] = AT
    for index in range(len(word) - 1):
        rows[index + 2] = (
            numpy.array([-1, word[index]]) @ rows[index : index + 2]
        )
    return rows @ numpy.array([BETA, 1.0])


PERIODS = periods()
RATIOS = PERIODS / numpy.roll(PERIODS, -1)


def sigma_factor(argument: float, period: float) -> complex:
    shift = math.floor(-argument) + math.floor(period / 2)
    finite = q_pochhammer_exp(
        argument / period, -1 / period, -shift
    )
    phase = exponential(
        (
            6 * (argument + shift) ** 2
            + 6 * (1 - period) * (argument + shift)
            + period**2
            - 3 * period
            + 1
        )
        / (24 * period)
    )
    return (
        finite
        * phase
        * double_sine(argument + shift + 1, period, 1.0)
    )


def overlap(first: int, second: int) -> float:
    if first == second == 0:
        return 3.0
    z_value = (
        PERIODS[0] * second - PERIODS[1] * first
    ) / DIMENSION
    finite_count = (
        -AT[1, 0] * first + (AT[0, 0] - 1) * second
    ) // DIMENSION
    form_value = first * first - 3 * first * second + second * second
    parity = (1 + first) * (1 + second)
    value = (
        TAU ** (-3 * form_value)
        * (-1) ** parity
        / q_pochhammer_exp(
            (second * BETA - first) / DIMENSION,
            BETA,
            int(finite_count),
        )
    )
    for index in range(6):
        value *= sigma_factor(
            z_value / PERIODS[index + 2], RATIOS[index + 1]
        )
    if abs(value.imag) > 2e-10:
        raise AssertionError(
            f"nonreal overlap at {(first, second)}: {value}"
        )
    return value.real


def ray_log_squares() -> dict[tuple[int, int], float]:
    process = subprocess.run(
        ["gp", "-q", "scripts/dimension_eight_maximal_tuple_audit.gp"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    result: dict[tuple[int, int], float] = {}
    pattern = re.compile(
        r"CHARACTERISTIC=(\d+),(\d+).*LOG_SQUARE=([^ ]+)"
    )
    for line in process.stdout.splitlines():
        match = pattern.search(line)
        if match:
            result[(int(match[1]), int(match[2]))] = float(match[3])
    if len(result) != 63:
        raise AssertionError(f"expected 63 ray records, got {len(result)}")
    return result


def reconstructed_matrix(
    table: numpy.ndarray, determinant: int
) -> numpy.ndarray:
    result = numpy.zeros((DIMENSION, DIMENSION), dtype=complex)
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            first = (row - column) % DIMENSION
            for second in range(DIMENSION):
                transformed_second = (determinant * second) % DIMENSION
                wrap_sign = (
                    (-1) ** first
                    if determinant == -1 and second != 0
                    else 1
                )
                result[row, column] += (
                    table[first, second]
                    * wrap_sign
                    * TAU ** (first * transformed_second)
                    * OMEGA ** (transformed_second * column)
                    / 24
                )
    return result


def maximum_minor(matrix: numpy.ndarray) -> float:
    return max(
        abs(
            matrix[first_row, first_column]
            * matrix[second_row, second_column]
            - matrix[first_row, second_column]
            * matrix[second_row, first_column]
        )
        for first_row in range(DIMENSION)
        for second_row in range(first_row + 1, DIMENSION)
        for first_column in range(DIMENSION)
        for second_column in range(first_column + 1, DIMENSION)
    )


def main() -> None:
    table = numpy.array(
        [
            [overlap(first, second) for second in range(DIMENSION)]
            for first in range(DIMENSION)
        ]
    )
    logs = ray_log_squares()
    log_residual = max(
        abs(2 * math.log(abs(table[index])) - value)
        for index, value in logs.items()
    )
    print("ZAUNER_REVISION=dcff219c986208ce900e2ddaaed8eae2bae6756f")
    print(f"PSL2_WORD={psl2_word(AT)}")
    print(f"RAY_LOG_SQUARE_MAX_RESIDUAL={log_residual:.3e}")
    for shift, determinant in ((1, 1), (0, -1)):
        matrix = reconstructed_matrix(table, determinant)
        idempotency = float(numpy.max(abs(matrix @ matrix - matrix)))
        minor = maximum_minor(matrix)
        print(f"SHIFT_{shift}_TRACE_RESIDUAL={abs(numpy.trace(matrix)-1):.3e}")
        print(f"SHIFT_{shift}_IDEMPOTENCY_RESIDUAL={idempotency:.3e}")
        print(f"SHIFT_{shift}_MAXIMUM_MINOR={minor:.3e}")
        if idempotency > 2e-9 or minor > 2e-9:
            raise AssertionError(f"shift {shift} did not close numerically")
    if log_residual > 2e-9:
        raise AssertionError("cocycle/ray logarithms do not match")


if __name__ == "__main__":
    main()
