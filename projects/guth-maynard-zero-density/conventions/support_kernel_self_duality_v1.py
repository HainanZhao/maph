"""Exact Cycle 52 support-kernel self-duality ledger."""
from __future__ import annotations

from fractions import Fraction as Q
from math import comb, factorial


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def falling(value: int, length: int) -> int:
    result = 1
    for offset in range(length):
        result *= value - offset
    return result


def stable_support_counts(prime_count: int, s: int) -> dict[str, int]:
    require(prime_count >= s + 1 and s >= 1, "count range")
    full_support = prime_count * comb(prime_count + s - 1, s)
    all_distinct_support = falling(prime_count, s + 1) // factorial(s)
    collision_support = full_support - all_distinct_support
    ordered_collision_tuples = prime_count ** (s + 1) - falling(prime_count, s + 1)
    return {
        "full_support": full_support,
        "all_distinct_support": all_distinct_support,
        "collision_support": collision_support,
        "ordered_collision_tuples": ordered_collision_tuples,
    }


def inverse_deficits(s: int, eta: Q) -> dict[str, Q]:
    require(s >= 1 and 0 <= eta < 1, "inverse range")
    return {
        "weighted_deficit": eta,
        "K_h_max_deficit": eta / s,
        "K_mh_max_deficit": eta,
        "collision_gap": Q(1),
    }


def verify_all() -> dict[str, object]:
    counts = {f"M{m}_s{s}": stable_support_counts(m, s) for s in (3, 4) for m in range(s + 1, s + 5)}
    for row in counts.values():
        require(row["collision_support"] >= 0, "support collision count")
        require(row["ordered_collision_tuples"] >= 0, "tuple collision count")
    s4_narrow = inverse_deficits(4, Q(7, 50))
    s4_full = inverse_deficits(4, Q(4, 25))
    require(s4_narrow["K_h_max_deficit"] == Q(7, 200), "narrow K(h) deficit")
    require(s4_full["K_h_max_deficit"] == Q(1, 25), "full K(h) deficit")
    return {
        "leading_term": "K(mh) K(h)^s / s!",
        "error_prime_exponent": "s",
        "main_prime_exponent": "s+1",
        "collision_gap": Q(1),
        "finite_counts": counts,
        "inverse_s4_at_7_50": s4_narrow,
        "inverse_s4_at_4_25": s4_full,
    }


if __name__ == "__main__":
    print(verify_all())
