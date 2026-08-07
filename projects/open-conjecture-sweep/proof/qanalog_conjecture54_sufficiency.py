#!/usr/bin/env python3
"""Exact replay for the sufficient direction of Conjecture 5.4.

The proof itself is the two-route polynomial identity checked below and the
aligned-center induction described in ``qanalog_conjecture54_sufficiency.md``.
The bounded sweep is a regression test, not the universal proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
import platform
from collections.abc import Iterable


def q_integer(length: int, step: int = 1) -> list[int]:
    if length < 1 or step < 1:
        raise ValueError("length and step must be positive")
    out = [0] * (step * (length - 1) + 1)
    for index in range(length):
        out[step * index] = 1
    return out


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return out


def product(polynomials: Iterable[list[int]]) -> list[int]:
    out = [1]
    for polynomial in polynomials:
        out = multiply(out, polynomial)
    return out


def shift(polynomial: list[int], amount: int) -> list[int]:
    return [0] * amount + polynomial


def add(left: list[int], right: list[int]) -> list[int]:
    out = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def is_symmetric_unimodal(coefficients: list[int]) -> bool:
    if coefficients != coefficients[::-1]:
        return False
    midpoint = (len(coefficients) - 1) // 2
    return all(
        coefficients[index] <= coefficients[index + 1]
        for index in range(midpoint)
    )


def direct_polynomial(lengths: tuple[int, ...], b: int, r: int) -> list[int]:
    return product(
        [q_integer(length) for length in lengths] + [q_integer(b, r)]
    )


def identity_combinatorial_exponents(a: int, b: int, r: int) -> tuple[list[int], list[int]]:
    """Return exponent multisets for the two sides by independent pair partition."""
    left = sorted(x + r * j for x in range(a + r) for j in range(b + 1))

    shifted_old = [r + x + r * j for x in range(a) for j in range(b)]
    complement = list(range(a + r * (b + 1)))
    right = sorted(shifted_old + complement)
    return left, right


def check_identity(a: int, b: int, r: int) -> None:
    left = multiply(q_integer(a + r), q_integer(b + 1, r))
    right = add(
        shift(multiply(q_integer(a), q_integer(b, r)), r),
        q_integer(a + r * (b + 1)),
    )
    if left != right:
        raise AssertionError(("algebraic_identity", a, b, r))

    left_exponents, right_exponents = identity_combinatorial_exponents(a, b, r)
    if left_exponents != right_exponents:
        raise AssertionError(("pair_partition", a, b, r))


def allocation(final_lengths: tuple[int, ...], b: int, r: int) -> list[int]:
    remaining = b - 1
    steps: list[int] = []
    for index, length in enumerate(final_lengths):
        capacity = length // r
        take = min(capacity, remaining)
        steps.extend([index] * take)
        remaining -= take
    if remaining:
        raise ValueError("the sufficient-condition inequality is not satisfied")
    return steps


def check_induction(final_lengths: tuple[int, ...], b: int, r: int) -> None:
    if any(length % r == 0 for length in final_lengths):
        raise ValueError("this checker uses the non-divisible induction branch")

    steps = allocation(final_lengths, b, r)
    used = [steps.count(index) for index in range(len(final_lengths))]
    current = [length - r * count for length, count in zip(final_lengths, used)]
    if any(length < 1 for length in current):
        raise AssertionError(("nonpositive_base_length", final_lengths, b, r))

    current_b = 1
    proved = direct_polynomial(tuple(current), current_b, r)
    if not is_symmetric_unimodal(proved):
        raise AssertionError(("base_not_symmetric_unimodal", current, r))

    for index in steps:
        old_a = current[index]
        others = current[:index] + current[index + 1 :]
        new_b = current_b + 1

        ordinary_term = product(
            [q_integer(old_a + r * new_b)]
            + [q_integer(length) for length in others]
        )
        if not is_symmetric_unimodal(ordinary_term):
            raise AssertionError(("ordinary_term", current, index, current_b, r))

        recursive = add(shift(proved, r), ordinary_term)
        current[index] += r
        direct = direct_polynomial(tuple(current), new_b, r)
        if recursive != direct:
            raise AssertionError(("induction_identity", current, new_b, r))

        new_degree = len(direct) - 1
        shifted_old_center_twice = (len(proved) - 1) + 2 * r
        ordinary_center_twice = len(ordinary_term) - 1
        if shifted_old_center_twice != new_degree or ordinary_center_twice != new_degree:
            raise AssertionError(("center_alignment", current, new_b, r))
        if not is_symmetric_unimodal(direct):
            raise AssertionError(("induction_unimodality", current, new_b, r))

        proved = recursive
        current_b = new_b

    if tuple(current) != final_lengths or current_b != b:
        raise AssertionError(("allocation_reconstruction", current, current_b))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--length-limit", type=int, default=12)
    args = parser.parse_args()
    if args.length_limit < 2:
        raise SystemExit("--length-limit must be at least 2")

    identity_rows = 0
    for r in range(2, 9):
        for a in range(1, 21):
            for b in range(1, 13):
                check_identity(a, b, r)
                identity_rows += 1

    induction_rows = 0
    direct_polynomials = 0
    for r in range(2, 7):
        allowed = [value for value in range(1, args.length_limit + 1) if value % r]
        for k in range(1, 5):
            for lengths in itertools.combinations_with_replacement(allowed, k):
                max_b = 1 + sum(length // r for length in lengths)
                for b in range(1, max_b + 1):
                    check_induction(lengths, b, r)
                    induction_rows += 1
                    direct_polynomials += 1

    # The source explicitly warns that the inequality is not necessary in
    # general. Preserve its smallest displayed example as a scope regression.
    outside_condition = direct_polynomial((3, 3, 3, 3), 2, 4)
    if not is_symmetric_unimodal(outside_condition):
        raise AssertionError("source non-necessity example unexpectedly failed")

    print(json.dumps({
        "claim": "Conjecture 5.4 sufficient direction for all k>=1 and r>=2",
        "direct_induction_rows": induction_rows,
        "direct_polynomials_checked": direct_polynomials,
        "identity_rows_two_routes": identity_rows,
        "length_limit": args.length_limit,
        "nonnecessity_scope_example": "([3]_q)^4[2]_(q^4)",
        "python": platform.python_version(),
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
