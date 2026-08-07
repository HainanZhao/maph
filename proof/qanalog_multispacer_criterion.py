#!/usr/bin/env python3
"""One-command exact regression suite for the combined criterion paper."""

from __future__ import annotations

import json
import random
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def bracket(length: int, step: int = 1) -> tuple[int, ...]:
    coefficients = [0] * (step * (length - 1) + 1)
    for index in range(length):
        coefficients[step * index] = 1
    return tuple(coefficients)


def convolution(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    coefficients = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            coefficients[i + j] += x * y
    return tuple(coefficients)


def polynomial_product(factors: list[tuple[int, ...]]) -> tuple[int, ...]:
    result = (1,)
    for factor in factors:
        result = convolution(result, factor)
    return result


def symmetric_unimodal(coefficients: tuple[int, ...]) -> bool:
    midpoint = (len(coefficients) - 1) // 2
    return coefficients == coefficients[::-1] and all(
        coefficients[index] <= coefficients[index + 1]
        for index in range(midpoint)
    )


def direct_product(lengths: list[int], spacers: list[tuple[int, int]]) -> tuple[int, ...]:
    return polynomial_product(
        [bracket(length) for length in lengths]
        + [bracket(length, step) for step, length in spacers]
    )


def independent_spot_checks() -> dict[str, int]:
    rng = random.Random(820260807)

    identity_rows = 0
    for _ in range(20):
        a = rng.randint(1, 18)
        b = rng.randint(1, 10)
        r = rng.randint(1, 7)
        left = convolution(bracket(a + r), bracket(b + 1, r))
        old = convolution(bracket(a), bracket(b, r))
        translated = (0,) * r + old
        correction = bracket(a + r * (b + 1))
        width = max(len(translated), len(correction))
        right = tuple(
            (translated[index] if index < len(translated) else 0)
            + (correction[index] if index < len(correction) else 0)
            for index in range(width)
        )
        assert left == right
        identity_rows += 1

    matrix_rows = 0
    for _ in range(20):
        k = rng.randint(1, 4)
        s = rng.randint(1, 4)
        steps = [rng.randint(1, 5) for _ in range(s)]
        allocation = [[rng.randint(0, 2) for _ in range(k)] for _ in range(s)]
        spacer_lengths = [1 + sum(row) for row in allocation]
        residual = [rng.randint(1, 4) for _ in range(k)]
        lengths = [
            residual[i] + sum(steps[j] * allocation[j][i] for j in range(s))
            for i in range(k)
        ]
        product = direct_product(lengths, list(zip(steps, spacer_lengths)))
        assert symmetric_unimodal(product)
        matrix_rows += 1

    absorption_rows = 0
    for _ in range(10):
        step = rng.randint(1, 6)
        quotient = rng.randint(1, 7)
        spacer_length = rng.randint(1, 7)
        other_lengths = [rng.randint(1, 8) for _ in range(rng.randint(0, 3))]
        product = direct_product(
            [step * quotient, *other_lengths], [(step, spacer_length)]
        )
        assert symmetric_unimodal(product)
        absorption_rows += 1

    family_23 = {
        a: symmetric_unimodal(direct_product([a], [(2, 2), (3, 2)]))
        for a in range(1, 16)
    }
    assert family_23[4] is False and family_23[5] is True
    assert all(family_23[a] for a in range(6, 16))
    family_22 = {
        a: symmetric_unimodal(direct_product([a], [(2, 2), (2, 2)]))
        for a in range(1, 16)
    }
    assert family_22[2] is True and all(family_22[a] for a in range(5, 16))
    assert not symmetric_unimodal(direct_product([], [(2, 2), (3, 2)]))

    return {
        "absorption_rows": absorption_rows,
        "identity_rows": identity_rows,
        "matrix_rows": matrix_rows,
        "threshold_rows": len(family_23) + len(family_22),
    }


def main() -> None:
    # Retain the mature one-spacer and matrix-recursion suites, then execute
    # a separately written direct-product corpus for the merged statement.
    runpy.run_path(
        str(ROOT / "proof" / "qanalog_conjecture54_sufficiency.py"),
        run_name="__main__",
    )
    runpy.run_path(
        str(ROOT / "discovery" / "multi_spacer_aligned_recursion_check.py"),
        run_name="__main__",
    )
    runpy.run_path(
        str(ROOT / "experiments" / "multi_spacer_adversarial_and_width5_overlap.py"),
        run_name="__main__",
    )
    rows = independent_spot_checks()
    print(json.dumps({**rows, "status": "COMBINED_CRITERION_PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
