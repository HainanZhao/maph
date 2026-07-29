#!/usr/bin/env python3
"""Numerical gate for the missing discriminant-eight d=7 tuple.

The direct six-factor cocycle supplies signs.  Independently computed
ray-class partial-zeta derivatives supply magnitudes, avoiding loss of
accuracy in the exploratory binary64 double-sine quadrature.
"""

from __future__ import annotations

import cmath
import math
import re
import subprocess
from pathlib import Path

import numpy

from certify_dimension_eight_maximal_cocycle import (
    psl2_word,
    q_pochhammer_exp,
    sigma_factor,
)
from dimension_seven_tcc_shifts import audit_shift


ROOT = Path(__file__).resolve().parents[1]
DIMENSION = 7
ALPHA = 2 + math.sqrt(2)
AT = numpy.array([[239, -140], [70, -41]], dtype=int)
TAU = -cmath.exp(math.pi * 1j / DIMENSION)


def periods() -> tuple[list[int], numpy.ndarray, numpy.ndarray]:
    word = psl2_word(AT)
    if word != [4, 2, 4, 2, 4, 2, 0]:
        raise AssertionError(f"unexpected PSL2 word: {word}")
    rows = numpy.zeros((len(word) + 1, 2))
    rows[:2] = AT
    for index in range(len(word) - 1):
        rows[index + 2] = (
            numpy.array([-1, word[index]]) @ rows[index : index + 2]
        )
    values = rows @ numpy.array([ALPHA, 1.0])
    return word, values, values / numpy.roll(values, -1)


WORD, PERIODS, RATIOS = periods()


def direct_overlap(first: int, second: int) -> complex:
    """Evaluate the AFK cocycle with exploratory binary64 quadrature."""

    z_value = (
        PERIODS[0] * second - PERIODS[1] * first
    ) / DIMENSION
    finite_count = (
        -AT[1, 0] * first + (AT[0, 0] - 1) * second
    ) // DIMENSION
    form_value = (
        first * first - 4 * first * second + 2 * second * second
    )
    value = (
        -TAU ** (-2 * form_value)
        / q_pochhammer_exp(
            (second * ALPHA - first) / DIMENSION,
            ALPHA,
            int(finite_count),
        )
    )
    for index in range(len(WORD) - 1):
        value *= sigma_factor(
            z_value / PERIODS[index + 2],
            RATIOS[index + 1],
        )
    return value


def ray_log_squares() -> dict[tuple[int, int], float]:
    process = subprocess.run(
        ["gp", "-q", "scripts/dimension_seven_maximal_tuple_audit.gp"],
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
    if len(result) != DIMENSION**2 - 1:
        raise AssertionError(f"expected 48 ray records, got {len(result)}")
    return result


def overlap_table() -> list[list[float]]:
    logs = ray_log_squares()
    table: list[list[float]] = []
    maximum_phase_residual = 0.0
    for first in range(DIMENSION):
        row = []
        for second in range(DIMENSION):
            if first == second == 0:
                row.append(math.sqrt(DIMENSION + 1))
                continue
            direct = direct_overlap(first, second)
            maximum_phase_residual = max(
                maximum_phase_residual, abs(direct.imag)
            )
            row.append(
                math.copysign(
                    math.exp(logs[first, second] / 2),
                    direct.real,
                )
            )
        table.append(row)
    if maximum_phase_residual > 2e-6:
        raise AssertionError("direct cocycle did not resolve real signs")
    print(f"DIRECT_PHASE_MAX_RESIDUAL={maximum_phase_residual:.3e}")
    return table


def main() -> None:
    table = overlap_table()
    reciprocal_residual = max(
        abs(
            table[first][second]
            * table[-first % DIMENSION][-second % DIMENSION]
            - 1
        )
        for first in range(DIMENSION)
        for second in range(DIMENSION)
        if first or second
    )
    print(f"PSL2_WORD={WORD}")
    print(f"RECIPROCAL_MAX_RESIDUAL={reciprocal_residual:.3e}")
    for shift, determinant in ((1, 1), (0, -1)):
        audit = audit_shift(shift, determinant, table)
        print(
            f"SHIFT_{shift}_IDEMPOTENCY_RESIDUAL="
            f"{audit['idempotency_residual']:.3e}"
        )
        print(
            f"SHIFT_{shift}_MAXIMUM_MINOR="
            f"{audit['maximum_minor_residual']:.3e}"
        )
        if (
            audit["idempotency_residual"] > 1e-12
            or audit["maximum_minor_residual"] > 1e-12
        ):
            raise AssertionError(f"shift {shift} did not close")
    print("DIMENSION_SEVEN_DISCRIMINANT_EIGHT_NUMERICAL_GATE=1")


if __name__ == "__main__":
    main()
