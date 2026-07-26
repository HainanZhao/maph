"""Exact small-instance tools for parallel constant-product AMM routing."""

from dataclasses import dataclass
from itertools import combinations
from math import sqrt
from typing import Iterable, Sequence, Tuple


@dataclass(frozen=True)
class Pool:
    """A two-token constant-product pool.

    ``input_reserve`` and ``output_reserve`` are the pre-trade reserves,
    ``fee_factor`` is one minus the proportional trading fee, and
    ``fixed_cost`` is denominated in units of the output token.
    """

    input_reserve: float
    output_reserve: float
    fee_factor: float = 1.0
    fixed_cost: float = 0.0

    def __post_init__(self) -> None:
        if self.input_reserve <= 0 or self.output_reserve <= 0:
            raise ValueError("reserves must be positive")
        if not 0 < self.fee_factor <= 1:
            raise ValueError("fee_factor must lie in (0, 1]")
        if self.fixed_cost < 0:
            raise ValueError("fixed_cost must be nonnegative")

    def output(self, amount: float) -> float:
        """Return output tokens received for a nonnegative input amount."""

        if amount < 0:
            raise ValueError("input amount must be nonnegative")
        effective = self.fee_factor * amount
        return self.output_reserve * effective / (
            self.input_reserve + effective
        )

    @property
    def initial_marginal_output(self) -> float:
        """Derivative of output with respect to input at zero."""

        return (
            self.output_reserve
            * self.fee_factor
            / self.input_reserve
        )


@dataclass(frozen=True)
class Route:
    """A feasible allocation and its gas-adjusted objective value."""

    allocations: Tuple[float, ...]
    gross_output: float
    fixed_cost: float

    @property
    def net_output(self) -> float:
        return self.gross_output - self.fixed_cost

    @property
    def active_indices(self) -> Tuple[int, ...]:
        return tuple(i for i, value in enumerate(self.allocations) if value > 0)


def waterfill(pools: Sequence[Pool], total_input: float) -> Tuple[float, ...]:
    """Maximize gross output over a specified collection of pools.

    Pools whose marginal output is too low can receive zero.  The returned
    allocation is the unique maximizer of the continuous concave problem.
    The common marginal value has a closed form once the positive set is
    known; the routine removes zero-flow pools until that set is consistent.
    """

    if total_input < 0:
        raise ValueError("total_input must be nonnegative")
    if not pools:
        if total_input == 0:
            return ()
        raise ValueError("positive input requires at least one pool")
    if total_input == 0:
        return tuple(0.0 for _ in pools)

    active = list(range(len(pools)))
    while True:
        numerator = sum(
            sqrt(
                pools[i].input_reserve
                * pools[i].output_reserve
                * pools[i].fee_factor
            )
            / pools[i].fee_factor
            for i in active
        )
        denominator = total_input + sum(
            pools[i].input_reserve / pools[i].fee_factor
            for i in active
        )
        marginal = (numerator / denominator) ** 2
        reduced = [
            i
            for i in active
            if pools[i].initial_marginal_output > marginal
        ]
        if reduced == active:
            break
        if not reduced:
            # At least the best marginal pool must carry positive input.
            reduced = [
                max(active, key=lambda i: pools[i].initial_marginal_output)
            ]
        active = reduced

    allocation = [0.0] * len(pools)
    for i in active:
        pool = pools[i]
        allocation[i] = (
            sqrt(
                pool.input_reserve
                * pool.output_reserve
                * pool.fee_factor
                / marginal
            )
            - pool.input_reserve
        ) / pool.fee_factor

    # Remove roundoff in the equality constraint without changing the active
    # set.  The correction is at machine precision for the closed-form solve.
    correction = total_input - sum(allocation)
    target = max(active, key=lambda i: allocation[i])
    allocation[target] += correction
    return tuple(allocation)


def evaluate_route(
    pools: Sequence[Pool], allocations: Sequence[float], zero_tol: float = 1e-12
) -> Route:
    """Evaluate a feasible route, charging gas exactly once per used pool."""

    if len(pools) != len(allocations):
        raise ValueError("pools and allocations must have the same length")
    if any(value < -zero_tol for value in allocations):
        raise ValueError("allocations must be nonnegative")

    cleaned = tuple(0.0 if abs(value) <= zero_tol else value for value in allocations)
    gross = sum(pool.output(value) for pool, value in zip(pools, cleaned))
    fixed = sum(
        pool.fixed_cost
        for pool, value in zip(pools, cleaned)
        if value > 0
    )
    return Route(cleaned, gross, fixed)


def exact_enumeration(pools: Sequence[Pool], total_input: float) -> Route:
    """Solve a small parallel-routing instance by active-set enumeration."""

    if total_input <= 0:
        raise ValueError("exact_enumeration requires positive total_input")
    if not pools:
        raise ValueError("at least one pool is required")

    best = None
    indices = range(len(pools))
    for size in range(1, len(pools) + 1):
        for selected in combinations(indices, size):
            selected_pools = [pools[i] for i in selected]
            local = waterfill(selected_pools, total_input)
            allocation = [0.0] * len(pools)
            for index, amount in zip(selected, local):
                allocation[index] = amount
            route = evaluate_route(pools, allocation)
            if best is None or route.net_output > best.net_output:
                best = route

    assert best is not None
    return best


def subset_sum_reduction(
    weights: Iterable[int], target: int
) -> Tuple[Tuple[Pool, ...], float]:
    """Construct the equal-price SUBSET-SUM reduction instance."""

    weights = tuple(weights)
    if target <= 0 or not weights or any(weight <= 0 for weight in weights):
        raise ValueError("weights and target must be positive")
    price = float((target + 1) ** 2)
    pools = tuple(
        Pool(
            input_reserve=float(weight),
            output_reserve=price * weight,
            fixed_cost=float(weight),
        )
        for weight in weights
    )
    return pools, 1.0
