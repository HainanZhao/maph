"""Exact Cycle 51 all-harmonic support-partition algebra."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from math import factorial


Polynomial = dict[tuple[int, ...], Q]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def integer_partitions(total: int, maximum: int | None = None) -> list[tuple[int, ...]]:
    if total == 0:
        return [()]
    top = total if maximum is None else min(total, maximum)
    result = []
    for first in range(top, 0, -1):
        for tail in integer_partitions(total - first, first):
            result.append((first, *tail))
    return result


def set_partitions(size: int) -> list[tuple[tuple[int, ...], ...]]:
    if size == 0:
        return [()]
    partitions = [((0,),)]
    for item in range(1, size):
        next_partitions = []
        for partition in partitions:
            for index in range(len(partition)):
                blocks = [list(block) for block in partition]
                blocks[index].append(item)
                next_partitions.append(tuple(tuple(block) for block in blocks))
            next_partitions.append((*partition, (item,)))
        partitions = next_partitions
    return partitions


def add_term(poly: Polynomial, key: tuple[int, ...], coefficient: Q) -> None:
    canonical = tuple(sorted(key))
    poly[canonical] = poly.get(canonical, Q(0)) + coefficient
    if poly[canonical] == 0:
        del poly[canonical]


def monomial_to_power(lam: tuple[int, ...]) -> Polynomial:
    equal_part_factor = 1
    for count in Counter(lam).values():
        equal_part_factor *= factorial(count)
    result: Polynomial = {}
    for partition in set_partitions(len(lam)):
        coefficient = 1
        powers = []
        for block in partition:
            coefficient *= (-1) ** (len(block) - 1) * factorial(len(block) - 1)
            powers.append(sum(lam[index] for index in block))
        add_term(result, tuple(powers), Q(coefficient, equal_part_factor))
    return result


def support_partitions(s: int, m: int) -> list[tuple[int, ...]]:
    require(s >= 1 and m >= 2, "registered parameter range")
    return [lam for lam in integer_partitions(s + m) if lam[0] >= m]


def support_power_polynomial(s: int, m: int) -> Polynomial:
    result: Polynomial = {}
    for lam in support_partitions(s, m):
        for key, coefficient in monomial_to_power(lam).items():
            add_term(result, key, coefficient)
    return result


def complete_homogeneous_power_polynomial(s: int) -> Polynomial:
    result: Polynomial = {}
    for lam in integer_partitions(s):
        for key, coefficient in monomial_to_power(lam).items():
            add_term(result, key, coefficient)
    return result


def multiply_by_power(poly: Polynomial, order: int) -> Polynomial:
    return {tuple(sorted((*key, order))): coefficient for key, coefficient in poly.items()}


def evaluate_power_polynomial(poly: Polynomial, values: tuple[Q, ...]) -> Q:
    power_cache = {order: sum((value**order for value in values), Q(0)) for key in poly for order in key}
    total = Q(0)
    for key, coefficient in poly.items():
        term = coefficient
        for order in key:
            term *= power_cache[order]
        total += term
    return total


def evaluate_support_direct(s: int, m: int, values: tuple[Q, ...]) -> Q:
    total = Q(0)
    for lam in support_partitions(s, m):
        # Sum distinct assignments, divided by permutations of equal parts.
        ordered = Q(0)
        from itertools import permutations

        for indices in permutations(range(len(values)), len(lam)):
            if len(set(indices)) != len(indices):
                continue
            term = Q(1)
            for index, exponent in zip(indices, lam):
                term *= values[index] ** exponent
            ordered += term
        equal_part_factor = 1
        for count in Counter(lam).values():
            equal_part_factor *= factorial(count)
        total += ordered / equal_part_factor
    return total


def verify_all() -> dict[str, object]:
    registered = ((3, 2), (3, 3), (4, 2), (4, 3), (4, 4))
    alphabets = ((Q(2),), (Q(1), Q(2)), (Q(-1), Q(2), Q(3)), (Q(1, 2), Q(-2), Q(3), Q(5)))
    rows = {}
    for s, m in registered:
        poly = support_power_polynomial(s, m)
        for values in alphabets:
            require(evaluate_power_polynomial(poly, values) == evaluate_support_direct(s, m, values), "power polynomial finite check")
        rows[f"s{s}_m{m}"] = {
            "partition_count": len(support_partitions(s, m)),
            "power_monomial_count": len(poly),
            "partitions": support_partitions(s, m),
        }
    for s, m in ((3, 4), (4, 5), (4, 7)):
        general = support_power_polynomial(s, m)
        injective = multiply_by_power(complete_homogeneous_power_polynomial(s), m)
        require(general == injective, "m>s reconciliation")
    return {
        "criterion": "lambda partitions s+m and max(lambda)>=m",
        "registered_small_m": rows,
        "m_gt_s_reconciliations": ["s3_m4", "s4_m5", "s4_m7"],
    }


if __name__ == "__main__":
    print(verify_all())
