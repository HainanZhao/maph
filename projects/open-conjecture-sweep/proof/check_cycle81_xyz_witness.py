#!/usr/bin/env python3
"""Independent exact check of the first C81 XYZ-only separating model."""
from __future__ import annotations

from itertools import combinations, permutations
import json


WEIGHTS = (7, 2, 5, 0, 0, 0, 0, 1, 6, 9, 5, 0)
ORDERS = tuple(order for order in permutations(range(4)) if order.index(0) < order.index(1))


def probability_numerator(predicate) -> int:
    return sum(weight for weight, ranking in zip(WEIGHTS, ORDERS) if predicate(ranking))


def precedes(ranking: tuple[int, ...], left: int, right: int) -> bool:
    return ranking.index(left) < ranking.index(right)


def arc(left: int, right: int) -> bool:
    return probability_numerator(lambda ranking: precedes(ranking, left, right)) * 2 > sum(WEIGHTS)


def four_cycle(restricted: bool) -> bool:
    return any(
        arc(a, b) and arc(b, c) and arc(c, d) and arc(d, a)
        and (not restricted or all({left, right} != {0, 1}
                                   for left, right in ((a, b), (b, c), (c, d), (d, a))))
        for a, b, c, d in permutations(range(4))
    )


def main() -> None:
    total = sum(WEIGHTS)
    inequalities = []
    for pivot in range(4):
        for left, right in combinations([v for v in range(4) if v != pivot], 2):
            first = probability_numerator(lambda r: precedes(r, pivot, left))
            second = probability_numerator(lambda r: precedes(r, pivot, right))
            joint = probability_numerator(lambda r: precedes(r, pivot, left) and precedes(r, pivot, right))
            inequalities.append([pivot, left, right, joint * total - first * second])
    assert all(margin >= 0 for *_, margin in inequalities)
    assert all(precedes(order, 0, 1) for order, weight in zip(ORDERS, WEIGHTS) if weight)
    assert four_cycle(False) and not four_cycle(True)
    print(json.dumps({
        "epistemic_status": "PROVED",
        "total_weight": total,
        "xyz_margins": inequalities,
        "full_has_4_cycle": True,
        "restricted_has_4_cycle": False,
        "scope": "XYZ-only finite ranking model, not uniform linear extensions",
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
