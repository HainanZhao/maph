#!/usr/bin/env python3
"""Exact rational audit of the commensurate-window decomposition.

This finite audit checks the algebra used in Cycle 2 on deterministic periodic
step profiles.  It is not a substitute for the arbitrary-profile proof.
"""

from __future__ import annotations

from fractions import Fraction


def periodic_integral(values: tuple[Fraction, ...], period: Fraction,
                      start: Fraction, length: Fraction) -> Fraction:
    """Integrate a cyclic equal-cell step profile over a nonnegative length."""
    if length < 0:
        raise ValueError("length must be nonnegative")
    cells = len(values)
    cell = period / cells
    total = Fraction(0)
    x = start
    remaining = length
    while remaining:
        reduced = x % period
        index = min(int(reduced / cell), cells - 1)
        boundary = (index + 1) * cell
        available = boundary - reduced
        take = min(remaining, available)
        total += take * values[index]
        x += take
        remaining -= take
    return total


def audit() -> int:
    profiles = (
        tuple(Fraction(j * j + 1, 3) for j in range(1, 8)),
        tuple(Fraction((5 * j + 2) % 11 + 1, 7) for j in range(9)),
    )
    checks = 0
    for values in profiles:
        for radius in (Fraction(1), Fraction(3, 2), Fraction(5, 3)):
            window_length = 2 * radius
            for m in range(1, 9):
                # Exercise exact resonance and both signs of a residual no
                # larger than one period.
                for residual_scale in (-1, 0, 1):
                    base = window_length / m
                    period = base + residual_scale * window_length / (34 * m)
                    residual = window_length - m * period
                    if abs(residual) > period:
                        continue
                    mean = sum(values, Fraction(0)) / len(values)
                    for offset_index in range(2 * len(values) + 1):
                        start = Fraction(offset_index, 2 * len(values)) * period
                        window = periodic_integral(
                            values, period, start, window_length
                        )
                        # Remove m complete periods from the left when r>=0.
                        # If r<0, compare with m periods and an oriented
                        # deleted tail.
                        if residual >= 0:
                            rem = periodic_integral(
                                values, period, start + m * period, residual
                            )
                        else:
                            rem = -periodic_integral(
                                values, period, start + window_length, -residual
                            )
                        lhs = window / window_length - mean
                        rhs = (rem - residual * mean) / window_length
                        if lhs != rhs:
                            raise AssertionError(
                                (values, radius, m, period, start, lhs, rhs)
                            )
                        if residual == 0 and window / window_length != mean:
                            raise AssertionError("commensurate average failed")
                        checks += 1
    expected = sum(2 * len(values) + 1 for values in profiles) * 3 * 8 * 3
    if checks != expected:
        raise AssertionError(("coverage", checks, expected))
    print({"status": "PASS", "exact_rational_checks": checks})
    return checks


if __name__ == "__main__":
    audit()
