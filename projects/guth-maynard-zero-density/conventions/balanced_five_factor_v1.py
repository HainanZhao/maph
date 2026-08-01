"""Exact exponent and combinatorial conventions for Cycle 12."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations


Q = Fraction
FACTOR_COUNT = 5
SELECT_COUNT = 2
SUBSETS = tuple(combinations(range(FACTOR_COUNT), SELECT_COUNT))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def combinatorial_rows() -> dict[str, object]:
    require(len(SUBSETS) == 10, "two-subset count mismatch")
    selected_counts = [sum(1 for subset in SUBSETS if index in subset) for index in range(FACTOR_COUNT)]
    require(selected_counts == [4, 4, 4, 4, 4], "factor selection multiplicity mismatch")
    total_moment_exponents = [2 * len(SUBSETS) + selected for selected in selected_counts]
    require(total_moment_exponents == [24, 24, 24, 24, 24], "geometric-mean exponent mismatch")
    geometric_exponent = Q(total_moment_exponents[0], len(SUBSETS))
    require(geometric_exponent == Q(12, 5), "fractional tensor exponent mismatch")
    return {
        "subsets": [list(subset) for subset in SUBSETS],
        "subset_count": len(SUBSETS),
        "selected_counts": selected_counts,
        "total_moment_exponents": total_moment_exponents,
        "geometric_exponent": geometric_exponent,
    }


def length_rows(exponents: tuple[Fraction, ...]) -> dict[str, object]:
    require(len(exponents) == FACTOR_COUNT, "factor exponent count mismatch")
    require(all(value >= 0 for value in exponents), "factor exponents must be nonnegative")
    require(sum(exponents, Q(0)) == 5, "factor exponents must sum to five")
    moment_lengths = {"_".join(str(index) for index in subset): 10 + sum((exponents[index] for index in subset), Q(0)) for subset in SUBSETS}
    return {"factor_exponents": list(exponents), "moment_lengths": moment_lengths, "maximum": max(moment_lengths.values()), "minimum": min(moment_lengths.values())}


def enumerate_balance_grid() -> dict[str, object]:
    denominator = 5
    total_units = 25
    maximum_units = 15
    checked = 0
    uniformly_admissible: list[list[Fraction]] = []
    for a in range(maximum_units + 1):
        for b in range(a, maximum_units + 1):
            for c in range(b, maximum_units + 1):
                for d in range(c, maximum_units + 1):
                    e = total_units - a - b - c - d
                    if e < d or e > maximum_units:
                        continue
                    checked += 1
                    values = (Q(a, denominator), Q(b, denominator), Q(c, denominator), Q(d, denominator), Q(e, denominator))
                    row = length_rows(values)
                    if row["maximum"] <= 12:
                        uniformly_admissible.append(list(values))
    require(checked < 60_000, "registered balance-grid cap exceeded")
    require(uniformly_admissible == [[Q(1), Q(1), Q(1), Q(1), Q(1)]], "balance-grid survivor mismatch")
    return {"checked": checked, "uniformly_admissible": uniformly_admissible, "denominator": denominator, "maximum_units": maximum_units}


def critical_exponent_rows() -> dict[str, Fraction]:
    global_height = Q(13)
    original_length = Q(5)
    local_height = Q(12)
    sigma = Q(7, 10)
    threshold = original_length * sigma
    fractional_tensor = Q(12, 5)
    transformed_length = original_length * fractional_tensor
    transformed_threshold = threshold * fractional_tensor
    squared_threshold = 2 * transformed_threshold
    mean_value = 2 * local_height
    local_rows = mean_value - squared_threshold
    baseline_local = Q(8)
    local_gain = baseline_local - local_rows
    global_rows = local_rows + (global_height - local_height)
    density_coefficient = global_rows / (global_height * (1 - sigma))
    baseline_coefficient = Q(30, 13)
    coefficient_gain = baseline_coefficient - density_coefficient
    conditional_interval = 1 - 1 / density_coefficient
    delta_loss = 2 * fractional_tensor
    require(transformed_length == local_height, "fractional length balance mismatch")
    require(local_rows == Q(36, 5), "local row exponent mismatch")
    require(local_gain == Q(4, 5), "local gain mismatch")
    require(global_rows == Q(41, 5), "global anchor exponent mismatch")
    require(density_coefficient == Q(82, 39), "density anchor mismatch")
    require(coefficient_gain == Q(8, 39), "density gain mismatch")
    require(conditional_interval == Q(43, 82), "conditional interval target mismatch")
    require(delta_loss == Q(24, 5), "delta loss mismatch")
    return {
        "global_height": global_height,
        "original_length": original_length,
        "local_height": local_height,
        "sigma": sigma,
        "threshold": threshold,
        "fractional_tensor": fractional_tensor,
        "transformed_length": transformed_length,
        "transformed_threshold": transformed_threshold,
        "squared_threshold": squared_threshold,
        "mean_value": mean_value,
        "local_rows": local_rows,
        "delta_loss": delta_loss,
        "baseline_local": baseline_local,
        "local_gain": local_gain,
        "global_rows": global_rows,
        "density_coefficient": density_coefficient,
        "baseline_coefficient": baseline_coefficient,
        "coefficient_gain": coefficient_gain,
        "conditional_interval": conditional_interval,
    }


def symbolic_balance_proof() -> dict[str, object]:
    pair_multiplicity = FACTOR_COUNT - 1
    pair_sum_total = Q(pair_multiplicity * 5)
    pair_count = Q(len(SUBSETS))
    average_pair_sum = pair_sum_total / pair_count
    require(average_pair_sum == 2, "average pair sum mismatch")
    return {
        "pair_multiplicity": pair_multiplicity,
        "pair_sum_total": pair_sum_total,
        "pair_count": pair_count,
        "average_pair_sum": average_pair_sum,
        "proof": "If every pair sum is at most 2, their average 2 forces every pair sum to equal 2; comparing pairs with one common index forces all five exponents equal, hence each is 1.",
    }


def verify_all() -> dict[str, object]:
    combinatorics = combinatorial_rows()
    balanced = length_rows((Q(1), Q(1), Q(1), Q(1), Q(1)))
    require(balanced["minimum"] == 12 and balanced["maximum"] == 12, "balanced length row mismatch")
    unbalanced = length_rows((Q(1, 2), Q(1, 2), Q(1), Q(3, 2), Q(3, 2)))
    require(unbalanced["maximum"] == 13, "unbalanced countermodel length mismatch")
    grid = enumerate_balance_grid()
    exponents = critical_exponent_rows()
    proof = symbolic_balance_proof()
    return {"combinatorics": combinatorics, "balanced_lengths": balanced, "unbalanced_countermodel": unbalanced, "balance_grid": grid, "critical_exponents": exponents, "symbolic_balance": proof}
