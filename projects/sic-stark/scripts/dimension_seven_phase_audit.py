#!/usr/bin/env python3
"""Exact AFK phase audit for the canonical dimension-seven tuple."""

from __future__ import annotations

from fractions import Fraction
import json
import math

from explore_dimension_seven import principal_overlap


DIMENSION = 7
FORM = (1, -6, 1)
STABILIZER = ((204, -35), (35, -6))
ZETA_ORDER = 56


def sawtooth(value: Fraction) -> Fraction:
    if value.denominator == 1:
        return Fraction()
    return value - value.numerator // value.denominator - Fraction(1, 2)


def dedekind_sum(first: int, second: int) -> Fraction:
    return sum(
        (
            sawtooth(Fraction(index, second))
            * sawtooth(Fraction(first * index, second))
            for index in range(1, abs(second))
        ),
        Fraction(),
    )


def rademacher(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Fraction:
    first, _, lower, last = (
        matrix[0][0],
        matrix[0][1],
        matrix[1][0],
        matrix[1][1],
    )
    trace = first + last
    return (
        Fraction(trace, lower)
        - 3 * (1 if lower * trace > 0 else -1)
        - 12 * (1 if lower > 0 else -1) * dedekind_sum(first, lower)
    )


def form_value(first: int, second: int) -> int:
    return first * first - 6 * first * second + second * second


def phase_exponent(first: int, second: int) -> int:
    # For d=7, f=f_1=2 and j=m=1.  Definition 1.30 becomes
    # phi_p=-exp(-3*pi*i/4)*xi_7^{-Q(p)}.  With
    # zeta_56=exp(2*pi*i/56) and xi_7=zeta_56^32, this is
    # zeta_56^(7-32Q(p)).
    return (7 - 32 * form_value(first, second)) % ZETA_ORDER


def sign_exponent(value: float) -> int:
    return 0 if value > 0 else ZETA_ORDER // 2


def main() -> None:
    psi = rademacher(STABILIZER)
    if psi != 9:
        raise AssertionError(f"expected Rademacher invariant 9, got {psi}")

    records = []
    reciprocal_residual = 0.0
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            if first == second == 0:
                continue
            overlap = principal_overlap(first, second)
            opposite = principal_overlap(
                (-first) % DIMENSION, (-second) % DIMENSION
            )
            reciprocal_residual = max(
                reciprocal_residual, abs(overlap * opposite - 1)
            )
            sf_phase = phase_exponent(first, second)
            overlap_phase = sign_exponent(overlap)
            records.append(
                {
                    "characteristic": [first, second],
                    "form_value": form_value(first, second),
                    "sf_phase_zeta56_exponent": sf_phase,
                    "sf_phase_square_zeta28_exponent": sf_phase % 28,
                    "normalized_overlap_sign": 1 if overlap > 0 else -1,
                    "raw_shin_zeta56_exponent": (
                        overlap_phase - sf_phase
                    )
                    % ZETA_ORDER,
                    "log_absolute_normalized_overlap": math.log(abs(overlap)),
                }
            )

    if len(records) != 48:
        raise AssertionError("incomplete characteristic packet")
    if reciprocal_residual > 1e-7:
        raise AssertionError("reciprocity audit failed")

    output = {
        "schema": "sic-stark-dimension-seven-phase-v1",
        "dimension": DIMENSION,
        "rank": 1,
        "form": list(FORM),
        "form_conductor": 2,
        "form_discriminant": 32,
        "fixed_point": "3+2*sqrt(2)",
        "dimension_grid_indices": {"j": 1, "m": 1},
        "stabilizer": [list(row) for row in STABILIZER],
        "rademacher_dedekind_sum": "-37/70",
        "rademacher_invariant": int(psi),
        "phase_formula": "zeta_56^(7-32*Q(p))",
        "reciprocal_residual": reciprocal_residual,
        "records": records,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
