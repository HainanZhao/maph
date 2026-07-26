"""Certifying branch-and-bound for parallel fixed-cost CPMM routing."""

from dataclasses import dataclass
import heapq
from math import fsum, inf, isfinite, nextafter, sqrt
import sys
from typing import Optional, Sequence, Tuple

from .certifying_router import (
    activation_threshold,
    dual_threshold_route,
    gross_waterfill_route,
    pool_dual_term,
    standalone_threshold_route,
)
from .parallel_cpmm import Pool, Route, evaluate_route, waterfill


@dataclass(frozen=True)
class NodeBound:
    """Lagrangian upper bound for a partially fixed activation pattern."""

    upper_bound: float
    raw_upper_bound: float
    dual_variable: float
    relaxed_allocations: Tuple[float, ...]


@dataclass(frozen=True)
class BranchAndBoundResult:
    """Best route and global certificate returned by branch-and-bound."""

    route: Route
    upper_bound: float
    nodes_explored: int
    nodes_generated: int
    nodes_pruned: int
    hit_node_limit: bool
    certified_within_tolerance: bool

    @property
    def additive_gap(self) -> float:
        return max(0.0, self.upper_bound - self.route.net_output)


@dataclass(frozen=True)
class _Node:
    included_mask: int
    excluded_mask: int
    bound: NodeBound


def _validate_masks(count: int, included_mask: int, excluded_mask: int) -> None:
    universe = (1 << count) - 1
    if included_mask < 0 or excluded_mask < 0:
        raise ValueError("activation masks must be nonnegative")
    if (included_mask | excluded_mask) & ~universe:
        raise ValueError("activation mask contains an unknown pool")
    if included_mask & excluded_mask:
        raise ValueError("included and excluded masks must be disjoint")


def _included_term(pool: Pool, dual_variable: float) -> Tuple[float, float]:
    """Return conjugate minus gas when the activation binary is fixed to one."""

    initial = pool.initial_marginal_output
    if dual_variable >= initial:
        return -pool.fixed_cost, 0.0
    if dual_variable == 0.0:
        return pool.output_reserve - pool.fixed_cost, inf

    conjugate = (
        sqrt(pool.output_reserve)
        - sqrt(
            dual_variable
            * pool.input_reserve
            / pool.fee_factor
        )
    ) ** 2
    amount = (
        sqrt(
            pool.input_reserve
            * pool.output_reserve
            * pool.fee_factor
            / dual_variable
        )
        - pool.input_reserve
    ) / pool.fee_factor
    return conjugate - pool.fixed_cost, max(0.0, amount)


def partial_lagrangian_bound(
    pools: Sequence[Pool],
    total_input: float,
    included_mask: int = 0,
    excluded_mask: int = 0,
) -> NodeBound:
    """Bound every completion of a partial pool-activation assignment.

    An included pool pays its fixed cost even if its relaxed allocation is
    zero.  A free pool may either stay off or maximize its net conjugate.
    Excluded pools contribute nothing.
    """

    if not pools:
        raise ValueError("at least one pool is required")
    if not isfinite(total_input) or total_input <= 0.0:
        raise ValueError("total_input must be positive and finite")
    _validate_masks(len(pools), included_mask, excluded_mask)

    breakpoints = set()
    for index, pool in enumerate(pools):
        bit = 1 << index
        if excluded_mask & bit:
            continue
        if included_mask & bit:
            breakpoints.add(pool.initial_marginal_output)
        else:
            threshold = activation_threshold(pool)
            if threshold > 0.0:
                breakpoints.add(threshold)

    ordered = sorted(breakpoints)
    candidates = {0.0, *ordered}
    lower = 0.0
    for upper in ordered:
        midpoint = (lower + upper) / 2.0
        active = []
        for index, pool in enumerate(pools):
            bit = 1 << index
            if excluded_mask & bit:
                continue
            threshold = (
                pool.initial_marginal_output
                if included_mask & bit
                else activation_threshold(pool)
            )
            if threshold > midpoint:
                active.append(pool)
        if active:
            coefficient = fsum(
                sqrt(
                    pool.input_reserve
                    * pool.output_reserve
                    / pool.fee_factor
                )
                for pool in active
            )
            denominator = total_input + fsum(
                pool.input_reserve / pool.fee_factor
                for pool in active
            )
            stationary = (coefficient / denominator) ** 2
            if lower <= stationary <= upper:
                candidates.add(stationary)
        lower = upper

    def evaluate(
        dual_variable: float,
    ) -> Tuple[float, float, Tuple[float, ...], float]:
        contributions = []
        allocations = []
        for index, pool in enumerate(pools):
            bit = 1 << index
            if excluded_mask & bit:
                contribution, amount = 0.0, 0.0
            elif included_mask & bit:
                contribution, amount = _included_term(pool, dual_variable)
            else:
                term = pool_dual_term(pool, dual_variable)
                contribution = term.contribution
                amount = term.maximizing_amount
            contributions.append(contribution)
            allocations.append(amount)
        summands = [dual_variable * total_input] + contributions
        value = fsum(summands)
        relaxed_total = fsum(allocations)
        mismatch = (
            abs(relaxed_total - total_input)
            if isfinite(relaxed_total)
            else inf
        )
        scale = max(1.0, fsum(abs(value) for value in summands))
        return value, mismatch, tuple(allocations), scale

    dual_variable = min(
        candidates,
        key=lambda candidate: evaluate(candidate)[:2],
    )
    raw_bound, _, allocations, scale = evaluate(dual_variable)
    margin = 128.0 * sys.float_info.epsilon * scale
    upper_bound = nextafter(raw_bound + margin, inf)
    return NodeBound(
        upper_bound,
        raw_bound,
        dual_variable,
        allocations,
    )


def _route_for_indices(
    pools: Sequence[Pool],
    total_input: float,
    selected: Sequence[int],
) -> Optional[Route]:
    if not selected:
        return None
    local = waterfill([pools[index] for index in selected], total_input)
    allocation = [0.0] * len(pools)
    for index, amount in zip(selected, local):
        allocation[index] = amount
    return evaluate_route(pools, allocation)


def _best_initial_route(
    pools: Sequence[Pool], total_input: float
) -> Route:
    candidates = [
        gross_waterfill_route(pools, total_input),
        standalone_threshold_route(pools, total_input),
        dual_threshold_route(pools, total_input),
    ]
    for index in range(len(pools)):
        route = _route_for_indices(pools, total_input, (index,))
        assert route is not None
        candidates.append(route)
    return max(candidates, key=lambda route: route.net_output)


def _relaxed_support_route(
    pools: Sequence[Pool],
    total_input: float,
    node: _Node,
) -> Optional[Route]:
    scale = max(1.0, abs(node.bound.raw_upper_bound))
    tolerance = 256.0 * sys.float_info.epsilon * scale
    selected = []
    for index, amount in enumerate(node.bound.relaxed_allocations):
        bit = 1 << index
        if node.excluded_mask & bit:
            continue
        if node.included_mask & bit or amount > tolerance:
            selected.append(index)
    return _route_for_indices(pools, total_input, selected)


def certifying_branch_and_bound(
    pools: Sequence[Pool],
    total_input: float,
    *,
    absolute_tolerance: float = 1e-10,
    relative_tolerance: float = 1e-10,
    node_limit: Optional[int] = None,
) -> BranchAndBoundResult:
    """Optimize activation with node-wise analytic Lagrangian bounds."""

    if not pools:
        raise ValueError("at least one pool is required")
    if not isfinite(total_input) or total_input <= 0.0:
        raise ValueError("total_input must be positive and finite")
    if absolute_tolerance < 0.0 or relative_tolerance < 0.0:
        raise ValueError("tolerances must be nonnegative")
    if node_limit is not None and node_limit <= 0:
        raise ValueError("node_limit must be positive")

    incumbent = _best_initial_route(pools, total_input)
    root = _Node(0, 0, partial_lagrangian_bound(pools, total_input))
    queue = [(-root.bound.upper_bound, 0, root)]
    serial = 1
    explored = 0
    generated = 1
    pruned = 0
    closed_upper = -inf
    universe = (1 << len(pools)) - 1

    def tolerance() -> float:
        return max(
            absolute_tolerance,
            relative_tolerance * max(1.0, abs(incumbent.net_output)),
        )

    while queue and (node_limit is None or explored < node_limit):
        _, _, node = heapq.heappop(queue)
        explored += 1
        if node.bound.upper_bound <= incumbent.net_output + tolerance():
            pruned += 1
            closed_upper = max(closed_upper, node.bound.upper_bound)
            continue

        candidate = _relaxed_support_route(pools, total_input, node)
        if candidate is not None and candidate.net_output > incumbent.net_output:
            incumbent = candidate

        free_mask = universe & ~(node.included_mask | node.excluded_mask)
        if free_mask == 0:
            closed_upper = max(closed_upper, node.bound.upper_bound)
            continue

        free_indices = [
            index
            for index in range(len(pools))
            if free_mask & (1 << index)
        ]
        branch_index = max(
            free_indices,
            key=lambda index: (
                node.bound.relaxed_allocations[index],
                activation_threshold(pools[index]),
                -index,
            ),
        )
        branch_bit = 1 << branch_index

        children = (
            (node.included_mask | branch_bit, node.excluded_mask),
            (node.included_mask, node.excluded_mask | branch_bit),
        )
        for included_mask, excluded_mask in children:
            if included_mask == 0 and excluded_mask == universe:
                continue
            bound = partial_lagrangian_bound(
                pools,
                total_input,
                included_mask,
                excluded_mask,
            )
            child = _Node(included_mask, excluded_mask, bound)
            generated += 1
            child_candidate = _relaxed_support_route(
                pools, total_input, child
            )
            if (
                child_candidate is not None
                and child_candidate.net_output > incumbent.net_output
            ):
                incumbent = child_candidate
            if bound.upper_bound <= incumbent.net_output + tolerance():
                pruned += 1
                closed_upper = max(closed_upper, bound.upper_bound)
                continue
            heapq.heappush(
                queue,
                (-bound.upper_bound, serial, child),
            )
            serial += 1

    open_upper = -queue[0][0] if queue else -inf
    upper_bound = max(
        incumbent.net_output,
        closed_upper,
        open_upper,
    )
    certified = upper_bound <= incumbent.net_output + tolerance()
    return BranchAndBoundResult(
        route=incumbent,
        upper_bound=upper_bound,
        nodes_explored=explored,
        nodes_generated=generated,
        nodes_pruned=pruned,
        hit_node_limit=bool(queue),
        certified_within_tolerance=certified,
    )
