"""Exact Cycle 50 support-kernel symmetric-polynomial identities."""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import comb, factorial


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def power_sum(values: tuple[Q, ...], order: int) -> Q:
    return sum((value**order for value in values), Q(0))


def complete_homogeneous_direct(values: tuple[Q, ...], degree: int) -> Q:
    if degree == 0:
        return Q(1)
    return sum((
        _product(values[index] for index in indices)
        for indices in combinations_with_replacement(range(len(values)), degree)
    ), Q(0))


def _product(values) -> Q:
    result = Q(1)
    for value in values:
        result *= value
    return result


def h3_power_sum(values: tuple[Q, ...]) -> Q:
    p1, p2, p3 = (power_sum(values, j) for j in range(1, 4))
    return (p1**3 + 3 * p1 * p2 + 2 * p3) / 6


def h4_power_sum(values: tuple[Q, ...]) -> Q:
    p1, p2, p3, p4 = (power_sum(values, j) for j in range(1, 5))
    return (p1**4 + 6 * p1**2 * p2 + 3 * p2**2 + 8 * p1 * p3 + 6 * p4) / 24


def support_size(prime_count: int, s: int) -> int:
    require(prime_count >= 1 and s >= 1, "positive sizes")
    return prime_count * comb(prime_count + s - 1, s)


def coefficient_norm_bounds(prime_count: int, s: int) -> dict[str, int]:
    total_mass = prime_count ** (s + 1)
    multiplicity = (1 + s // 2) * factorial(s)
    return {
        "support_size": support_size(prime_count, s),
        "coefficient_mass": total_mass,
        "coefficient_square_lower": total_mass,
        "coefficient_square_upper": multiplicity * total_mass,
    }


def verify_all() -> dict[str, object]:
    alphabets = (
        (Q(2),),
        (Q(1), Q(2)),
        (Q(-1), Q(2), Q(3)),
        (Q(1, 2), Q(-2), Q(3), Q(5)),
    )
    checks = []
    for values in alphabets:
        direct3 = complete_homogeneous_direct(values, 3)
        direct4 = complete_homogeneous_direct(values, 4)
        require(direct3 == h3_power_sum(values), "h3 power-sum identity")
        require(direct4 == h4_power_sum(values), "h4 power-sum identity")
        checks.append({"alphabet_size": len(values), "h3": direct3, "h4": direct4})
    sizes = {f"M{m}_s{s}": support_size(m, s) for m in range(1, 5) for s in (3, 4)}
    require(support_size(2, 4) == 10, "support size example")
    return {
        "identities": {
            "h3": "(P1^3+3 P1 P2+2 P3)/6",
            "h4": "(P1^4+6 P1^2 P2+3 P2^2+8 P1 P3+6 P4)/24",
        },
        "finite_checks": checks,
        "support_sizes": sizes,
        "norm_example_M4_s4": coefficient_norm_bounds(4, 4),
        "injective_range": "m>s",
        "exceptional_harmonics": {"s3": [2, 3], "s4": [2, 3, 4]},
    }


if __name__ == "__main__":
    print(verify_all())
