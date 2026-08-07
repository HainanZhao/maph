#!/usr/bin/env python3
"""Exact symbolic unimodality check for the 18 width-five R2 bad classes."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


BAD_RESIDUES = {
    9, 10, 12, 16, 17, 18, 21, 27, 33,
    36, 37, 38, 42, 44, 45, 56, 57, 58,
}
PARTS = (1, 2, 3, 5)
PERIOD = 30


def fibonacci(limit: int) -> list[int]:
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def partition_values(limit: int) -> list[int]:
    values = [0] * (limit + 1)
    values[0] = 1
    for part in PARTS:
        for total in range(part, limit + 1):
            values[total] += values[total - part]
    return values


def cubic_from_four(values: list[int | Fraction]) -> tuple[Fraction, ...]:
    y0, y1, y2, y3 = map(Fraction, values)
    d1 = y1 - y0
    d2 = y2 - 2 * y1 + y0
    d3 = y3 - 3 * y2 + 3 * y1 - y0
    return (
        y0,
        d1 - d2 / 2 + d3 / 3,
        d2 / 2 - d3 / 2,
        d3 / 6,
    )


def evaluate(coefficients: tuple[Fraction, ...], x: int) -> Fraction:
    total = Fraction(0)
    for coefficient in reversed(coefficients):
        total = total * x + coefficient
    return total


def partition_quasipolynomials() -> tuple[tuple[Fraction, ...], ...]:
    direct = partition_values(PERIOD * 13)
    rows = []
    for residue in range(PERIOD):
        coefficients = cubic_from_four(
            [direct[residue + PERIOD * u] for u in range(4)]
        )
        for u in range(13):
            assert evaluate(coefficients, u) == direct[residue + PERIOD * u]
        rows.append(coefficients)
    return tuple(rows)


QUASI = partition_quasipolynomials()


def p(total: int) -> int:
    if total < 0:
        return 0
    residue = total % PERIOD
    u = total // PERIOD
    value = evaluate(QUASI[residue], u)
    assert value.denominator == 1 and value >= 0
    return value.numerator


def subset_shifts(lengths: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    combined: dict[int, int] = {}
    for mask in range(1 << len(lengths)):
        shift = sum(lengths[i] for i in range(len(lengths)) if mask >> i & 1)
        sign = -1 if mask.bit_count() % 2 else 1
        combined[shift] = combined.get(shift, 0) + sign
    return tuple(sorted((shift, sign) for shift, sign in combined.items() if sign))


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def critical_candidates(
    coefficients: tuple[Fraction, ...], upper: int
) -> set[int]:
    candidates = {0, upper}
    c0, c1, c2, c3 = coefficients
    del c0
    a = 3 * c3
    b = 2 * c2
    c = c1

    def derivative(x: int) -> Fraction:
        return (a * x + b) * x + c

    split_points = {0, upper}
    if a:
        vertex = floor_fraction(-b / (2 * a))
        for delta in range(-2, 3):
            split_points.add(min(upper, max(0, vertex + delta)))
    ordered = sorted(split_points)
    for point in ordered:
        for delta in range(-3, 4):
            candidate = point + delta
            if 0 <= candidate <= upper:
                candidates.add(candidate)

    # On each interval split at the quadratic derivative's vertex, the
    # derivative is monotone. Locate every integer sign boundary exactly.
    for left, right in zip(ordered, ordered[1:]):
        left_value = derivative(left)
        right_value = derivative(right)
        if left_value == 0 or right_value == 0 or left_value * right_value < 0:
            low, high = left, right
            low_sign = (left_value > 0) - (left_value < 0)
            while high - low > 1:
                middle = (low + high) // 2
                middle_value = derivative(middle)
                middle_sign = (middle_value > 0) - (middle_value < 0)
                if middle_sign == 0:
                    low = high = middle
                    break
                if middle_sign == low_sign:
                    low = middle
                else:
                    high = middle
            for boundary in (low, high):
                for delta in range(-3, 4):
                    candidate = boundary + delta
                    if 0 <= candidate <= upper:
                        candidates.add(candidate)
    return candidates


def interval_minimum(
    active: tuple[tuple[int, int], ...], residue: int, first_u: int, last_u: int
) -> tuple[int, int]:
    def extended_value(u: int) -> int:
        total = residue + PERIOD * u
        return sum(sign * p(total - shift) for shift, sign in active)

    values = [extended_value(first_u + offset) for offset in range(4)]
    coefficients = cubic_from_four(values)
    width = last_u - first_u
    candidates = critical_candidates(coefficients, width)
    checked = [(evaluate(coefficients, x), first_u + x) for x in candidates]
    value, location = min(checked)
    assert value.denominator == 1
    return value.numerator, residue + PERIOD * location


def verify_m(m: int, fib: list[int]) -> tuple[int, int, int]:
    lengths = tuple(fib[m + offset] for offset in range(1, 6))
    degree = sum(lengths) - 12
    midpoint = degree // 2
    shifts = subset_shifts(lengths)
    breakpoints = sorted({0, *(shift for shift, _ in shifts if 0 <= shift <= midpoint)})
    minimum = None
    minimum_t = None
    interval_count = 0
    for index, lower in enumerate(breakpoints):
        upper = midpoint
        if index + 1 < len(breakpoints):
            upper = min(upper, breakpoints[index + 1] - 1)
        if lower > upper:
            continue
        active = tuple((shift, sign) for shift, sign in shifts if shift <= lower)
        for residue in range(PERIOD):
            first_t = lower + ((residue - lower) % PERIOD)
            if first_t > upper:
                continue
            last_t = upper - ((upper - residue) % PERIOD)
            value, location = interval_minimum(
                active, residue, first_t // PERIOD, last_t // PERIOD
            )
            if minimum is None or value < minimum:
                minimum = value
                minimum_t = location
            interval_count += 1
    assert minimum is not None and minimum_t is not None

    # A direct coefficient-by-coefficient route remains feasible for the
    # small cases and checks the symbolic interval machinery independently.
    if midpoint <= 200_000:
        direct_p = partition_values(midpoint)
        direct_minimum = min(
            sum(
                sign * (direct_p[t - shift] if t >= shift else 0)
                for shift, sign in shifts
            )
            for t in range(midpoint + 1)
        )
        assert direct_minimum == minimum
    return minimum, minimum_t, interval_count


def main() -> None:
    maximum_m = 240
    fib = fibonacci(maximum_m + 5)
    rows = []
    for m in range(1, maximum_m + 1):
        if m % 60 not in BAD_RESIDUES:
            continue
        minimum, location, intervals = verify_m(m, fib)
        if minimum < 0:
            print(
                json.dumps(
                    {
                        "m": m,
                        "minimum_difference": minimum,
                        "minimum_location": location,
                        "status": "COUNTEREXAMPLE_CANDIDATE",
                    },
                    sort_keys=True,
                )
            )
            raise SystemExit(2)
        rows.append((m, minimum, location, intervals))

    print(
        json.dumps(
            {
                "bad_residues": sorted(BAD_RESIDUES),
                "instances_checked": len(rows),
                "maximum_m": maximum_m,
                "minimum_difference_overall": min(row[1] for row in rows),
                "quasipolynomial_period": PERIOD,
                "status": "ALL_UNIMODAL",
                "symbolic_residue_intervals_checked": sum(row[3] for row in rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
