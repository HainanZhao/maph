#!/usr/bin/env python3
"""Test whether the finite d=8 TCC equations select quartic orientations."""

from __future__ import annotations

import cmath
import math
from pathlib import Path
import re
import subprocess

import numpy

from explore_dimension_eight import principal_overlap


ROOT = Path(__file__).resolve().parents[1]
GP_SCRIPT = ROOT / "scripts" / "dimension_eight_orientation_sieve.gp"
DIMENSION = 8
ORIENTATION = re.compile(r"^ORIENTATION=(\d+),(\d+)$")
CHARACTERISTIC = re.compile(
    r"^CHARACTERISTIC=(\d+),(\d+) LOG_SQUARE=(.+)$"
)


def orientation_packets() -> dict[
    tuple[int, int], dict[tuple[int, int], float]
]:
    process = subprocess.run(
        ["gp", "-q", str(GP_SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    packets: dict[tuple[int, int], dict[tuple[int, int], float]] = {}
    current: tuple[int, int] | None = None
    for line in process.stdout.splitlines():
        orientation_match = ORIENTATION.match(line)
        if orientation_match:
            current = tuple(map(int, orientation_match.groups()))
            packets[current] = {}
            continue
        characteristic_match = CHARACTERISTIC.match(line)
        if characteristic_match:
            if current is None:
                raise RuntimeError("characteristic precedes orientation")
            first, second = map(int, characteristic_match.groups()[:2])
            packets[current][first, second] = float(
                characteristic_match.group(3)
            )
    if len(packets) != 64:
        raise RuntimeError(f"expected 64 orientations, found {len(packets)}")
    if any(len(packet) != 48 for packet in packets.values()):
        raise RuntimeError("an orientation packet is incomplete")
    return packets


def principal_sign(first: int, second: int) -> int:
    exponent = (
        DIMENSION * (first + second)
        + first * second
        + min(DIMENSION, first + second)
    )
    return (-1) ** exponent


def overlap_table(
    packet: dict[tuple[int, int], float],
    lower_conductor: dict[tuple[int, int], float],
) -> list[list[float]]:
    table: list[list[float]] = []
    for first in range(DIMENSION):
        row = []
        for second in range(DIMENSION):
            characteristic = first, second
            if characteristic == (0, 0):
                value = math.sqrt(DIMENSION + 1)
            elif characteristic in packet:
                value = principal_sign(first, second) * math.exp(
                    packet[characteristic] / 2
                )
            else:
                value = lower_conductor[characteristic]
            row.append(value)
        table.append(row)
    return table


def reconstruct(
    table: list[list[float]], determinant: int
) -> numpy.ndarray:
    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    omega = cmath.exp(2 * math.pi * 1j / DIMENSION)
    matrix = numpy.zeros((DIMENSION, DIMENSION), dtype=complex)
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            transformed_second = determinant * second % DIMENSION
            wrap_sign = (
                (-1) ** first
                if determinant == -1 and second != 0
                else 1
            )
            for column in range(DIMENSION):
                row = (column + first) % DIMENSION
                matrix[row, column] += (
                    table[first][second]
                    * wrap_sign
                    * tau ** (first * transformed_second)
                    * omega ** (transformed_second * column)
                    / (DIMENSION * math.sqrt(DIMENSION + 1))
                )
    return matrix


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


def matrix_score(matrix: numpy.ndarray) -> tuple[float, float, float]:
    trace_residual = abs(numpy.trace(matrix) - 1)
    idempotency_residual = float(
        numpy.max(numpy.abs(matrix @ matrix - matrix))
    )
    minor_residual = maximum_minor(matrix)
    return trace_residual, idempotency_residual, minor_residual


def main() -> None:
    packets = orientation_packets()
    primitive = set(next(iter(packets.values())))
    lower_conductor = {
        (first, second): principal_overlap(first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
        if (first, second) != (0, 0)
        and (first, second) not in primitive
    }

    records = []
    for orientation, packet in packets.items():
        table = overlap_table(packet, lower_conductor)
        diagnostics = [
            matrix_score(reconstruct(table, determinant))
            for determinant in (1, -1)
        ]
        score = max(value for triple in diagnostics for value in triple)
        records.append((score, orientation, diagnostics))
    records.sort()

    baseline = next(record for record in records if record[1] == (0, 0))
    threshold = 1e-6
    passing = [record for record in records if record[0] < threshold]

    print(f"ORIENTATION_COUNT={len(records)}")
    print(f"LOWER_CONDUCTOR_CHARACTERISTIC_COUNT={len(lower_conductor)}")
    print(f"BASELINE_SCORE={baseline[0]:.12e}")
    print(f"PASSING_ORIENTATION_COUNT={len(passing)}")
    for rank, (score, orientation, diagnostics) in enumerate(
        records[:10], start=1
    ):
        print(
            f"RANK_{rank}_ORIENTATION={orientation[0]},{orientation[1]} "
            f"SCORE={score:.12e} "
            f"SHIFT_1={diagnostics[0]} SHIFT_0={diagnostics[1]}"
        )
    if not passing:
        raise RuntimeError("no quartic orientation satisfies the TCC threshold")


if __name__ == "__main__":
    main()
