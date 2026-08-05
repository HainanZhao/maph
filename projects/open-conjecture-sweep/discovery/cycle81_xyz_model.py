#!/usr/bin/env python3
"""Exact finite-model screen: XYZ correlation alone versus C81's 4-cycle claim."""
from __future__ import annotations

import itertools
import json
import random
import sys


VERTICES = range(4)
ORDERS = [order for order in itertools.permutations(VERTICES)
          if order.index(0) < order.index(1)]  # the forced comparable edge 0 < 1


def count(weights: tuple[int, ...], predicate) -> int:
    return sum(weight for weight, order in zip(weights, ORDERS) if predicate(order))


def before(order: tuple[int, ...], left: int, right: int) -> bool:
    return order.index(left) < order.index(right)


def majority(weights: tuple[int, ...], left: int, right: int) -> bool:
    return count(weights, lambda order: before(order, left, right)) * 2 > sum(weights)


def xyz(weights: tuple[int, ...]) -> bool:
    total = sum(weights)
    for pivot in VERTICES:
        others = [vertex for vertex in VERTICES if vertex != pivot]
        for left, right in itertools.combinations(others, 2):
            p_left = count(weights, lambda order: before(order, pivot, left))
            p_right = count(weights, lambda order: before(order, pivot, right))
            both = count(weights, lambda order: before(order, pivot, left)
                         and before(order, pivot, right))
            if both * total < p_left * p_right:
                return False
    return True


def has_four_cycle(weights: tuple[int, ...], restricted: bool) -> bool:
    def edge(left: int, right: int) -> bool:
        return majority(weights, left, right) and not (
            restricted and {left, right} == {0, 1}
        )
    return any(edge(a, b) and edge(b, c) and edge(c, d) and edge(d, a)
               for a, b, c, d in itertools.permutations(VERTICES))


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) == 2 else 81201
    rng = random.Random(seed)
    for attempt in range(100_000):
        weights = tuple(rng.randrange(10) for _ in ORDERS)
        if sum(weights) == 0 or not xyz(weights):
            continue
        if has_four_cycle(weights, False) and not has_four_cycle(weights, True):
            print(json.dumps({
                "epistemic_status": "PROVED",
                "model": "finite ranking distribution with forced 0<1",
                "scope": "XYZ inequalities alone, not uniform linear extensions",
                "seed": seed,
                "attempt": attempt,
                "weights": weights,
                "xyz": True,
                "full_has_4_cycle": True,
                "restricted_has_4_cycle": False,
                "status": "PASS",
            }, sort_keys=True))
            return
    print(json.dumps({
        "epistemic_status": "OBSERVED",
        "scope": "frozen finite-model search only",
        "seed": seed,
        "attempts": 100_000,
        "status": "NO_HIT",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
