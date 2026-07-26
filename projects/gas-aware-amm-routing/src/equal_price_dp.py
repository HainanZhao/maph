"""Dynamic programming for equal-price parallel constant-product pools."""

from dataclasses import dataclass
from math import inf, isclose
from typing import Sequence, Tuple

from .parallel_cpmm import Pool, Route, evaluate_route


@dataclass(frozen=True)
class EqualPriceDPSolution:
    """An exact equal-price solution and its aggregate-reserve state."""

    route: Route
    selected_indices: Tuple[int, ...]
    aggregate_input_reserve: int


def _common_parameters(
    pools: Sequence[Pool], tolerance: float
) -> Tuple[float, float]:
    if not pools:
        raise ValueError("at least one pool is required")
    price = pools[0].output_reserve / pools[0].input_reserve
    fee_factor = pools[0].fee_factor
    for pool in pools[1:]:
        candidate_price = pool.output_reserve / pool.input_reserve
        if not isclose(candidate_price, price, rel_tol=tolerance, abs_tol=tolerance):
            raise ValueError("all pools must have the same initial price")
        if not isclose(
            pool.fee_factor,
            fee_factor,
            rel_tol=tolerance,
            abs_tol=tolerance,
        ):
            raise ValueError("all pools must have the same fee factor")
    return price, fee_factor


def aggregate_output(
    price: float, fee_factor: float, total_input: float, aggregate_reserve: float
) -> float:
    """Gross output of an optimally split equal-price route."""

    if price <= 0 or not 0 < fee_factor <= 1:
        raise ValueError("invalid price or fee factor")
    if total_input < 0 or aggregate_reserve <= 0:
        raise ValueError("invalid input or aggregate reserve")
    return (
        price
        * fee_factor
        * total_input
        * aggregate_reserve
        / (aggregate_reserve + fee_factor * total_input)
    )


def _minimum_cost_subsets(
    weights: Sequence[int], fixed_costs: Sequence[float]
) -> Tuple[list, list]:
    """Return minimum cost and a realizing subset for every attainable sum."""

    total_weight = sum(weights)
    costs = [inf] * (total_weight + 1)
    choices = [None] * (total_weight + 1)
    costs[0] = 0.0
    choices[0] = ()

    reachable_max = 0
    for index, (weight, fixed_cost) in enumerate(zip(weights, fixed_costs)):
        for aggregate in range(reachable_max, -1, -1):
            if choices[aggregate] is None:
                continue
            candidate_aggregate = aggregate + weight
            candidate_cost = costs[aggregate] + fixed_cost
            if candidate_cost < costs[candidate_aggregate]:
                costs[candidate_aggregate] = candidate_cost
                choices[candidate_aggregate] = choices[aggregate] + (index,)
        reachable_max += weight
    return costs, choices


def exact_integer_reserve_dp(
    pools: Sequence[Pool],
    total_input: float,
    tolerance: float = 1e-10,
) -> EqualPriceDPSolution:
    """Solve equal-price routing exactly for integer input reserves.

    The running time and memory are pseudo-polynomial in the sum of input
    reserves.  Fixed costs may be arbitrary nonnegative real numbers.
    """

    if total_input <= 0:
        raise ValueError("total_input must be positive")
    price, fee_factor = _common_parameters(pools, tolerance)

    weights = []
    for pool in pools:
        rounded = round(pool.input_reserve)
        if rounded <= 0 or not isclose(
            pool.input_reserve,
            rounded,
            rel_tol=0.0,
            abs_tol=tolerance,
        ):
            raise ValueError("input reserves must be positive integers")
        weights.append(int(rounded))

    total_reserve = sum(weights)
    costs, choices = _minimum_cost_subsets(
        weights, [pool.fixed_cost for pool in pools]
    )

    best_reserve = max(
        range(1, total_reserve + 1),
        key=lambda reserve: (
            -inf
            if choices[reserve] is None
            else aggregate_output(
                price, fee_factor, total_input, reserve
            )
            - costs[reserve]
        ),
    )
    selected = choices[best_reserve]
    assert selected is not None

    allocation = [0.0] * len(pools)
    for index in selected:
        allocation[index] = (
            pools[index].input_reserve / best_reserve * total_input
        )
    route = evaluate_route(pools, allocation)
    return EqualPriceDPSolution(route, selected, best_reserve)


def rounded_reserve_dp(
    pools: Sequence[Pool],
    total_input: float,
    reserve_quantum: float,
    tolerance: float = 1e-10,
) -> EqualPriceDPSolution:
    """Route after flooring reserves to a common positive quantum.

    Let ``p`` be the common initial price and ``m`` the number of pools.
    The returned route has true net output at least

    ``OPT - p * m * reserve_quantum``.

    The bound follows because aggregate output is
    ``p*gamma*Q*A/(A+gamma*Q)`` and has derivative at most ``p`` in
    aggregate reserve ``A``.
    """

    if reserve_quantum <= 0:
        raise ValueError("reserve_quantum must be positive")
    price, fee_factor = _common_parameters(pools, tolerance)
    scaled_weights = []
    original_indices = []
    for index, pool in enumerate(pools):
        scaled = int(pool.input_reserve // reserve_quantum)
        if scaled == 0:
            continue
        scaled_weights.append(scaled)
        original_indices.append(index)

    if not scaled_weights:
        # The guarantee is useful only when the grid resolves at least one
        # pool.  Failing explicitly prevents a silent empty route.
        raise ValueError("reserve_quantum is larger than every reserve")

    costs, choices = _minimum_cost_subsets(
        scaled_weights,
        [pools[index].fixed_cost for index in original_indices],
    )
    best_scaled_reserve = max(
        range(1, sum(scaled_weights) + 1),
        key=lambda reserve: (
            -inf
            if choices[reserve] is None
            else aggregate_output(
                price,
                fee_factor,
                total_input,
                reserve_quantum * reserve,
            )
            - costs[reserve]
        ),
    )
    scaled_selected = choices[best_scaled_reserve]
    assert scaled_selected is not None
    selected = tuple(
        original_indices[index]
        for index in scaled_selected
    )
    aggregate = sum(pools[index].input_reserve for index in selected)
    allocation = [0.0] * len(pools)
    for index in selected:
        allocation[index] = (
            pools[index].input_reserve / aggregate * total_input
        )
    route = evaluate_route(pools, allocation)
    return EqualPriceDPSolution(
        route,
        selected,
        best_scaled_reserve,
    )
