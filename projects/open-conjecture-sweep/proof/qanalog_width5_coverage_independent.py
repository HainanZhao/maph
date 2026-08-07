#!/usr/bin/env python3
"""Independent reconstruction of the width-five criterion coverage partition."""

from __future__ import annotations

import itertools
import json
import math


SPACER_STEPS = (2, 3, 5)


def fibonacci_up_to(index: int) -> list[int]:
    numbers = [0, 1]
    for _ in range(2, index + 1):
        numbers.append(numbers[-1] + numbers[-2])
    return numbers


def bounded_sum_in_interval(
    weights: tuple[int, ...], limits: tuple[int, ...], low: int, high: int
) -> bool:
    """Exact fixed-dimension bounded knapsack, derived by residue splitting."""
    if low > high:
        return False
    period = math.lcm(*weights) if weights else 1
    residue_limits = tuple(period // weight for weight in weights)
    for residues in itertools.product(
        *(range(min(limit + 1, residue_limit)) for limit, residue_limit in zip(limits, residue_limits))
    ):
        residue_value = sum(weight * value for weight, value in zip(weights, residues))
        available_periods = sum(
            (limit - residue) // residue_limit
            for limit, residue, residue_limit in zip(limits, residues, residue_limits)
        )
        first = max(0, (low - residue_value + period - 1) // period)
        last = min(available_periods, (high - residue_value) // period)
        if first <= last:
            return True
    return False


def matrix_route(ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]) -> bool:
    demands = tuple(length - 1 for _, length in spacers)
    if not ordinary:
        return all(demand == 0 for demand in demands)
    weighted_total = sum(step * demand for (step, _), demand in zip(spacers, demands))
    capacities = tuple(length - 1 for length in ordinary)
    if len(ordinary) == 1:
        return weighted_total <= capacities[0]
    assert len(ordinary) == 2
    return bounded_sum_in_interval(
        tuple(step for step, _ in spacers),
        demands,
        max(0, weighted_total - capacities[1]),
        min(weighted_total, capacities[0]),
    )


def absorption_route(ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]) -> bool:
    active = tuple(index for index, (_, length) in enumerate(spacers) if length > 1)
    if len(active) > len(ordinary):
        return False
    return any(
        all(ordinary[target] % spacers[source][0] == 0 for source, target in zip(active, targets))
        for targets in itertools.permutations(range(len(ordinary)), len(active))
    )


def hybrid_route(ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]) -> bool:
    for pair_count in range(min(len(ordinary), len(spacers)) + 1):
        for spacer_subset in itertools.combinations(range(len(spacers)), pair_count):
            for ordinary_targets in itertools.permutations(range(len(ordinary)), pair_count):
                if not all(
                    ordinary[target] % spacers[source][0] == 0
                    for source, target in zip(spacer_subset, ordinary_targets)
                ):
                    continue
                residual_ordinary = tuple(
                    length for index, length in enumerate(ordinary) if index not in ordinary_targets
                )
                residual_spacers = tuple(
                    spacer for index, spacer in enumerate(spacers) if index not in spacer_subset
                )
                if matrix_route(residual_ordinary, residual_spacers):
                    return True
    return False


def main() -> None:
    fib = fibonacci_up_to(125)
    reached_matrix: set[int] = set()
    reached_absorption: set[int] = set()
    reached_hybrid: set[int] = set()
    undecomposable: set[int] = set()

    for residue in range(60):
        representative = 120 if residue == 0 else 60 + residue
        decompositions = []
        for offsets in itertools.permutations(range(1, 6), 3):
            if not all(fib[representative + offset] % step == 0 for step, offset in zip(SPACER_STEPS, offsets)):
                continue
            assigned = set(offsets)
            ordinary = tuple(
                fib[representative + offset]
                for offset in range(1, 6)
                if offset not in assigned
            )
            spacers = tuple(
                (step, fib[representative + offset] // step)
                for step, offset in zip(SPACER_STEPS, offsets)
            )
            assert len(ordinary) == 2 and all(length > 1 for _, length in spacers)
            decompositions.append((ordinary, spacers))

        if not decompositions:
            undecomposable.add(residue)
            continue
        if any(matrix_route(*decomposition) for decomposition in decompositions):
            reached_matrix.add(residue)
        if any(absorption_route(*decomposition) for decomposition in decompositions):
            reached_absorption.add(residue)
        if any(hybrid_route(*decomposition) for decomposition in decompositions):
            reached_hybrid.add(residue)

    expected_matrix = {
        2, 3, 4, 7, 8, 14, 23, 24, 26, 29, 31, 32, 41, 47, 49, 51, 53, 54
    }
    expected_undecomposable = {
        9, 10, 12, 16, 17, 18, 21, 27, 33, 36, 37, 38, 42, 44, 45, 56, 57, 58
    }
    assert reached_matrix == expected_matrix
    assert reached_hybrid == expected_matrix
    assert reached_absorption == set()
    assert undecomposable == expected_undecomposable
    assert reached_matrix.isdisjoint(undecomposable)

    decomposable_unreached = set(range(60)) - reached_matrix - undecomposable
    assert len(reached_matrix) == len(undecomposable) == 18
    assert len(decomposable_unreached) == 24
    assert reached_matrix | undecomposable | decomposable_unreached == set(range(60))

    print(
        json.dumps(
            {
                "absorption_only": sorted(reached_absorption),
                "decomposable_unreached": sorted(decomposable_unreached),
                "hybrid": sorted(reached_hybrid),
                "matrix_only": sorted(reached_matrix),
                "reached_and_undecomposable_disjoint": True,
                "status": "INDEPENDENT_COVERAGE_PASS",
                "undecomposable": sorted(undecomposable),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
