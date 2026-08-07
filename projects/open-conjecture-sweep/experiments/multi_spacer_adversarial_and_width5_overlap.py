#!/usr/bin/env python3
"""Exact adversarial and width-five coverage checks for the multi-spacer criterion."""

from __future__ import annotations

import itertools
import json
import math


STEPS = (2, 3, 5)
RANK = {2: 3, 3: 4, 5: 5}


def qbracket(length: int, step: int = 1) -> list[int]:
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


def is_unimodal(coefficients: list[int]) -> bool:
    center = (len(coefficients) - 1) // 2
    return all(
        coefficients[index] <= coefficients[index + 1]
        for index in range(center)
    )


def fibonacci(limit: int) -> list[int]:
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def bounded_weight_hits_interval(
    weights: tuple[int, ...], bounds: tuple[int, ...], lower: int, upper: int
) -> bool:
    """Decide exactly whether sum weights[j]*x[j] hits [lower, upper]."""
    if lower > upper:
        return False
    modulus = math.lcm(*weights) if weights else 1
    residue_ranges = [
        range(min(bound, modulus // weight - 1) + 1)
        for weight, bound in zip(weights, bounds)
    ]
    for residues in itertools.product(*residue_ranges):
        base = sum(weight * residue for weight, residue in zip(weights, residues))
        cycles = sum(
            (bound - residue) // (modulus // weight)
            for weight, bound, residue in zip(weights, bounds, residues)
        )
        first_cycle = max(0, (lower - base + modulus - 1) // modulus)
        last_cycle = min(cycles, (upper - base) // modulus)
        if first_cycle <= last_cycle:
            return True
    return False


def brute_bounded_weight_hits_interval(
    weights: tuple[int, ...], bounds: tuple[int, ...], lower: int, upper: int
) -> bool:
    return any(
        lower <= sum(weight * value for weight, value in zip(weights, values)) <= upper
        for values in itertools.product(*(range(bound + 1) for bound in bounds))
    )


def verify_bounded_solver() -> int:
    rows = 0
    for bounds in itertools.product(range(6), repeat=3):
        maximum = sum(weight * bound for weight, bound in zip(STEPS, bounds))
        for lower in range(maximum + 2):
            for upper in range(lower, maximum + 2):
                assert bounded_weight_hits_interval(STEPS, bounds, lower, upper) == (
                    brute_bounded_weight_hits_interval(STEPS, bounds, lower, upper)
                )
                rows += 1
    return rows


def matrix_feasible(ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]) -> bool:
    demands = tuple(length - 1 for _, length in spacers)
    if not spacers:
        return True
    if not ordinary:
        return all(demand == 0 for demand in demands)
    capacities = tuple(length - 1 for length in ordinary)
    total_weight = sum(step * demand for (step, _), demand in zip(spacers, demands))
    if len(ordinary) == 1:
        return total_weight <= capacities[0]
    if len(ordinary) == 2:
        lower = max(0, total_weight - capacities[1])
        upper = min(total_weight, capacities[0])
        return bounded_weight_hits_interval(
            tuple(step for step, _ in spacers), demands, lower, upper
        )
    raise ValueError("This checker only needs zero, one, or two residual smooth factors")


def absorption_only(ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]) -> bool:
    active = tuple(index for index, (_, length) in enumerate(spacers) if length > 1)
    for targets in itertools.product(range(len(ordinary)), repeat=len(active)):
        if len(set(targets)) != len(targets):
            continue
        if all(
            ordinary[target] % spacers[index][0] == 0
            for index, target in zip(active, targets)
        ):
            return True
    return not active


def hybrid_feasible(ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]) -> bool:
    ordinary_indices = range(len(ordinary))
    spacer_indices = range(len(spacers))
    for size in range(min(len(ordinary), len(spacers)) + 1):
        for chosen_spacers in itertools.combinations(spacer_indices, size):
            for chosen_ordinary in itertools.permutations(ordinary_indices, size):
                if not all(
                    ordinary[i] % spacers[j][0] == 0
                    for j, i in zip(chosen_spacers, chosen_ordinary)
                ):
                    continue
                remaining_ordinary = tuple(
                    value for i, value in enumerate(ordinary) if i not in chosen_ordinary
                )
                remaining_spacers = tuple(
                    value for j, value in enumerate(spacers) if j not in chosen_spacers
                )
                if matrix_feasible(remaining_ordinary, remaining_spacers):
                    return True
    return False


def width_five_rows() -> dict[str, object]:
    fib = fibonacci(125)
    coverage = {"matrix_only": [], "absorption_only": [], "hybrid": []}
    undecomposable = []
    for residue in range(60):
        m = 120 if residue == 0 else 60 + residue
        adjacency = {
            step: tuple(offset for offset in range(1, 6) if (m + offset) % RANK[step] == 0)
            for step in STEPS
        }
        assignments = []
        for targets in itertools.product(*(adjacency[step] for step in STEPS)):
            if len(set(targets)) != len(targets):
                continue
            assigned = dict(zip(STEPS, targets))
            ordinary = tuple(
                fib[m + offset]
                for offset in range(1, 6)
                if offset not in assigned.values()
            )
            spacers = tuple((step, fib[m + assigned[step]] // step) for step in STEPS)
            assignments.append(
                {
                    "targets": targets,
                    "matrix_only": matrix_feasible(ordinary, spacers),
                    "absorption_only": absorption_only(ordinary, spacers),
                    "hybrid": hybrid_feasible(ordinary, spacers),
                }
            )
        if not assignments:
            undecomposable.append(residue)
        for route in coverage:
            if any(row[route] for row in assignments):
                coverage[route].append(residue)
    return {
        "coverage": coverage,
        "coverage_counts": {key: len(value) for key, value in coverage.items()},
        "undecomposable": undecomposable,
    }


def adversarial_rows() -> dict[str, object]:
    different_steps = []
    equal_steps = []
    for a in range(1, 16):
        product_23 = multiply(multiply(qbracket(a), qbracket(2, 2)), qbracket(2, 3))
        product_22 = multiply(multiply(qbracket(a), qbracket(2, 2)), qbracket(2, 2))
        different_steps.append(
            {"a": a, "matrix_applies": a >= 6, "unimodal": is_unimodal(product_23)}
        )
        equal_steps.append(
            {"a": a, "matrix_applies": a >= 5, "unimodal": is_unimodal(product_22)}
        )
    no_smooth = multiply(qbracket(2, 2), qbracket(2, 3))
    assert not is_unimodal(no_smooth)
    assert different_steps[3] == {"a": 4, "matrix_applies": False, "unimodal": False}
    assert different_steps[4] == {"a": 5, "matrix_applies": False, "unimodal": True}
    assert all(row["unimodal"] for row in different_steps[5:])
    assert equal_steps[1] == {"a": 2, "matrix_applies": False, "unimodal": True}
    return {
        "different_steps": different_steps,
        "equal_steps": equal_steps,
        "no_smooth_coefficients": no_smooth,
        "large_step_rule": (
            "If b_j>=2 and r_j exceeds sum_i(a_i-1), its row cannot be funded, "
            "so the matrix criterion is silent."
        ),
        "r_equals_one_rule": (
            "For k=s=1 and r=1 the matrix condition is b<=a; swapping the two "
            "ordinary brackets covers the complementary ordering."
        ),
    }


def verify_hybrid_small() -> int:
    rows = 0
    for ordinary_count in (1, 2):
        for ordinary in itertools.product(range(1, 7), repeat=ordinary_count):
            for spacer_count in (1, 2):
                spacer_options = tuple(itertools.product(range(1, 5), range(1, 5)))
                for spacers in itertools.product(spacer_options, repeat=spacer_count):
                    if not hybrid_feasible(ordinary, spacers):
                        continue
                    polynomial = [1]
                    for length in ordinary:
                        polynomial = multiply(polynomial, qbracket(length))
                    for step, length in spacers:
                        polynomial = multiply(polynomial, qbracket(length, step))
                    assert is_unimodal(polynomial)
                    rows += 1

    # At s=1 the hybrid is exactly the two branches of the proved criterion.
    for ordinary_count in (1, 2):
        for ordinary in itertools.product(range(1, 9), repeat=ordinary_count):
            for step in range(1, 6):
                for length in range(1, 7):
                    one_spacer = ((step, length),)
                    known_condition = any(value % step == 0 for value in ordinary) or (
                        length <= 1 + sum(value // step for value in ordinary)
                    )
                    assert hybrid_feasible(ordinary, one_spacer) == known_condition
    return rows


def main() -> None:
    result = {
        "adversarial": adversarial_rows(),
        "bounded_solver_bruteforce_rows": verify_bounded_solver(),
        "claim_boundary": "Exact applicability census; not a proof of width-five unimodality.",
        "hybrid_small_rows": verify_hybrid_small(),
        "status": "PASS",
        "width_five": width_five_rows(),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
