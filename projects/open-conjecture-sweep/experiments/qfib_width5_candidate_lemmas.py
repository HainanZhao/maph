#!/usr/bin/env python3
"""Exact tests of the pre-stated width-five direct-attempt lemmas."""

from __future__ import annotations

import importlib.util
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "experiments" / "qfib_width5_bad_class_unimodality.py"
SPEC = importlib.util.spec_from_file_location("width5_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


LOW_ERROR = Fraction(91, 360)
HIGH_ERROR = Fraction(1)


def fibonacci(limit: int) -> list[int]:
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def q(length: int) -> list[int]:
    return [1] * length


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        if x:
            for j, y in enumerate(right):
                if y:
                    out[i + j] += x * y
    return out


def product(factors: list[list[int]]) -> list[int]:
    out = [1]
    for factor in factors:
        out = multiply(out, factor)
    return out


def exact_divide(dividend: list[int], divisor: list[int]) -> list[int]:
    remainder = dividend[:]
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    for shift in range(len(quotient) - 1, -1, -1):
        coefficient = remainder[shift + len(divisor) - 1]
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            remainder[shift + index] -= coefficient * value
    assert all(value == 0 for value in remainder)
    return quotient


def expected_shifts(a: int, b: int) -> dict[int, int]:
    return {
        0: 1,
        a: -1,
        b: -1,
        2 * a + b: 1,
        a + 3 * b: 1,
        2 * a + 3 * b: -1,
    }


def full_subset_shifts(lengths: tuple[int, ...]) -> dict[int, int]:
    combined: dict[int, int] = defaultdict(int)
    for mask in range(1 << len(lengths)):
        shift = sum(lengths[i] for i in range(len(lengths)) if mask >> i & 1)
        combined[shift] += -1 if mask.bit_count() % 2 else 1
    return {shift: sign for shift, sign in combined.items() if sign}


def smooth_part(total: int) -> Fraction:
    return Fraction(total**3, 180) + Fraction(11 * total**2, 120) + Fraction(9 * total, 20)


def envelope_value(active: tuple[tuple[int, int], ...], total: int) -> Fraction:
    value = Fraction(0)
    for shift, sign in active:
        base = smooth_part(total - shift)
        value += base + LOW_ERROR if sign > 0 else -(base + HIGH_ERROR)
    return value


def envelope_minimum(
    active: tuple[tuple[int, int], ...], lower: int, upper: int
) -> tuple[Fraction, int]:
    values = [envelope_value(active, lower + offset) for offset in range(4)]
    coefficients = CHECKER.cubic_from_four(values)
    candidates = CHECKER.critical_candidates(coefficients, upper - lower)
    checked = [(CHECKER.evaluate(coefficients, x), lower + x) for x in candidates]
    return min(checked)


def main() -> None:
    fib = fibonacci(245)

    # L1: exact period-30 formula and frozen error interval.
    rho = []
    for residue, coefficients in enumerate(CHECKER.QUASI):
        for u in range(20):
            total = residue + 30 * u
            exact = CHECKER.p(total)
            smooth = smooth_part(total)
            error = Fraction(exact) - smooth
            if u == 0:
                rho.append(error)
            else:
                assert error == rho[residue]
    assert min(rho) == LOW_ERROR and max(rho) == HIGH_ERROR

    # L2: compare the pre-stated six shifts with full inclusion-exclusion
    # below the midpoint for every m through 240.
    for m in range(1, 241):
        a, b = fib[m + 1], fib[m + 2]
        lengths = (a, b, a + b, a + 2 * b, 2 * a + 3 * b)
        midpoint = (5 * a + 7 * b - 12) // 2
        full = {
            shift: sign
            for shift, sign in full_subset_shifts(lengths).items()
            if shift <= midpoint
        }
        expected = {
            shift: sign
            for shift, sign in expected_shifts(a, b).items()
            if shift <= midpoint
        }
        assert full == expected

    # Direct quotient cross-check of L2 for the tractable initial range.
    direct_rows = 0
    denominator = product([q(2), q(3), q(5)])
    for m in range(1, 9):
        a, b = fib[m + 1], fib[m + 2]
        lengths = (a, b, a + b, a + 2 * b, 2 * a + 3 * b)
        quotient = exact_divide(product([q(length) for length in lengths]), denominator)
        midpoint = (len(quotient) - 1) // 2
        shifts = expected_shifts(a, b)
        for total in range(midpoint + 1):
            formula = sum(sign * CHECKER.p(total - shift) for shift, sign in shifts.items())
            previous = quotient[total - 1] if total else 0
            assert quotient[total] - previous == formula
        direct_rows += 1

    # L3: frozen worst-error envelope for every m=20,...,240.
    envelope_min = None
    envelope_location = None
    envelope_m = None
    envelope_intervals = 0
    for m in range(20, 241):
        a, b = fib[m + 1], fib[m + 2]
        midpoint = (5 * a + 7 * b - 12) // 2
        shifts = expected_shifts(a, b)
        breaks = sorted({0, *(shift for shift in shifts if 0 <= shift <= midpoint)})
        for index, lower in enumerate(breaks):
            upper = midpoint if index + 1 == len(breaks) else breaks[index + 1] - 1
            active = tuple((shift, sign) for shift, sign in shifts.items() if shift <= lower)
            value, location = envelope_minimum(active, lower, upper)
            if envelope_min is None or value < envelope_min:
                envelope_min = value
                envelope_location = location
                envelope_m = m
            envelope_intervals += 1
    assert envelope_min is not None

    # L4: exact symbolic minimization for every finite-remainder case.
    finite = []
    for m in range(1, 20):
        minimum, location, intervals = CHECKER.verify_m(m, fib)
        finite.append((m, minimum, location, intervals))
    finite_min = min(row[1] for row in finite)

    status = "PASS" if envelope_min >= 0 and finite_min >= 0 else "FAIL"
    print(
        json.dumps(
            {
                "L1_rho_max": str(max(rho)),
                "L1_rho_min": str(min(rho)),
                "L2_direct_quotient_rows": direct_rows,
                "L2_symbolic_rows": 240,
                "L3_envelope_intervals": envelope_intervals,
                "L3_minimum": str(envelope_min),
                "L3_minimum_location": envelope_location,
                "L3_minimum_m": envelope_m,
                "L4_cases": 19,
                "L4_minimum": finite_min,
                "status": status,
            },
            sort_keys=True,
        )
    )
    if status != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
