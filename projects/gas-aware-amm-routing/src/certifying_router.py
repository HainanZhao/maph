"""Lagrangian upper bounds and deliberately simple routing heuristics.

For the fixed-charge problem

    max sum_i [f_i(x_i) - q_i 1{x_i > 0}]
        subject to x_i >= 0 and sum_i x_i = Q,

dualizing the equality constraint with ``lambda >= 0`` gives the upper
bound

    B(lambda) = lambda Q
        + sum_i max(0, sup_{x >= 0}(f_i(x) - lambda x) - q_i).

The constant-product conjugate and every activation breakpoint are
available in closed form, so the one-dimensional convex dual can be
minimized without a generic optimizer.
"""

from dataclasses import dataclass
from math import fsum, inf, isfinite, nextafter, sqrt
import sys
from typing import Optional, Sequence, Tuple

from src.parallel_cpmm import Pool, Route, evaluate_route, waterfill


@dataclass(frozen=True)
class PoolDualTerm:
    """One pool's contribution to a Lagrangian bound."""

    contribution: float
    maximizing_amount: float
    activation_threshold: float
    active: bool


@dataclass(frozen=True)
class LagrangianCertificate:
    """A minimized separable upper bound, optionally paired with a route."""

    dual_variable: float
    upper_bound: float
    raw_upper_bound: float
    roundoff_margin: float
    pool_contributions: Tuple[float, ...]
    relaxed_allocations: Tuple[float, ...]
    incumbent_net_output: Optional[float] = None

    @property
    def relaxed_total_input(self) -> float:
        return fsum(self.relaxed_allocations)

    @property
    def additive_gap(self) -> Optional[float]:
        if self.incumbent_net_output is None:
            return None
        return max(0.0, self.upper_bound - self.incumbent_net_output)


def _validate_instance(pools: Sequence[Pool], total_input: float) -> None:
    if not pools:
        raise ValueError("at least one pool is required")
    if not isfinite(total_input) or total_input <= 0:
        raise ValueError("total_input must be positive and finite")


def activation_threshold(pool: Pool) -> float:
    """Return the largest dual price at which paying this pool's gas helps.

    For ``fixed_cost >= output_reserve`` the pool is never strictly active
    in the relaxation, because even its asymptotic gross output cannot repay
    its fixed charge.
    """

    if pool.fixed_cost >= pool.output_reserve:
        return 0.0
    return (
        pool.fee_factor
        / pool.input_reserve
        * (sqrt(pool.output_reserve) - sqrt(pool.fixed_cost)) ** 2
    )


def pool_dual_term(pool: Pool, dual_variable: float) -> PoolDualTerm:
    """Evaluate one exact-real Lagrangian term in floating-point arithmetic."""

    if not isfinite(dual_variable) or dual_variable < 0:
        raise ValueError("dual_variable must be finite and nonnegative")

    threshold = activation_threshold(pool)
    if threshold == 0.0 or dual_variable >= threshold:
        return PoolDualTerm(0.0, 0.0, threshold, False)

    if dual_variable == 0.0:
        # The supremum is approached as x -> infinity.  This case is useful
        # for evaluating the endpoint B(0), although it cannot be a smooth
        # dual optimum when at least one term is strictly active.
        contribution = pool.output_reserve - pool.fixed_cost
        return PoolDualTerm(contribution, inf, threshold, True)

    conjugate = (
        sqrt(pool.output_reserve)
        - sqrt(
            dual_variable
            * pool.input_reserve
            / pool.fee_factor
        )
    ) ** 2
    contribution = conjugate - pool.fixed_cost
    if contribution <= 0.0:
        return PoolDualTerm(0.0, 0.0, threshold, False)

    amount = (
        sqrt(
            pool.input_reserve
            * pool.output_reserve
            * pool.fee_factor
            / dual_variable
        )
        - pool.input_reserve
    ) / pool.fee_factor
    return PoolDualTerm(contribution, max(0.0, amount), threshold, True)


def lagrangian_value(
    pools: Sequence[Pool], total_input: float, dual_variable: float
) -> float:
    """Evaluate a valid separable Lagrangian upper bound."""

    _validate_instance(pools, total_input)
    terms = [pool_dual_term(pool, dual_variable) for pool in pools]
    return fsum(
        [dual_variable * total_input]
        + [term.contribution for term in terms]
    )


def _dual_candidates(
    pools: Sequence[Pool], total_input: float
) -> Tuple[float, ...]:
    """Enumerate every breakpoint and feasible smooth stationary point."""

    thresholds = sorted(
        {
            threshold
            for threshold in map(activation_threshold, pools)
            if threshold > 0.0
        }
    )
    candidates = {0.0, *thresholds}

    # Between consecutive thresholds the active terms are fixed.  On such an
    # interval B'(lambda) = D - C/sqrt(lambda), whose only stationary point
    # is (C/D)^2.
    lower = 0.0
    for upper in thresholds:
        midpoint = (lower + upper) / 2.0
        active = [
            pool
            for pool in pools
            if activation_threshold(pool) > midpoint
        ]
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

    return tuple(sorted(candidates))


def lagrangian_certificate(
    pools: Sequence[Pool],
    total_input: float,
    incumbent: Optional[Route] = None,
) -> LagrangianCertificate:
    """Minimize the separable dual bound and optionally certify a route.

    The optimization is exact for the analytic piecewise formula, apart from
    floating-point evaluation.  ``upper_bound`` adds a small explicit
    roundoff cushion to ``raw_upper_bound``.  This is a numerical safeguard,
    not an interval-arithmetic proof for adversarial machine inputs.
    """

    _validate_instance(pools, total_input)
    if incumbent is not None:
        if len(incumbent.allocations) != len(pools):
            raise ValueError("incumbent dimension does not match pools")
        feasibility_error = abs(fsum(incumbent.allocations) - total_input)
        if feasibility_error > 1e-9 * max(1.0, total_input):
            raise ValueError("incumbent does not preserve total input")

    candidates = _dual_candidates(pools, total_input)

    def candidate_key(dual_variable: float) -> Tuple[float, float]:
        terms = [pool_dual_term(pool, dual_variable) for pool in pools]
        value = fsum(
            [dual_variable * total_input]
            + [term.contribution for term in terms]
        )
        total = fsum(term.maximizing_amount for term in terms)
        mismatch = (
            abs(total - total_input) if isfinite(total) else inf
        )
        return value, mismatch

    dual_variable = min(candidates, key=candidate_key)
    terms = tuple(pool_dual_term(pool, dual_variable) for pool in pools)
    summands = [dual_variable * total_input] + [
        term.contribution for term in terms
    ]
    raw_bound = fsum(summands)
    scale = max(1.0, fsum(abs(value) for value in summands))
    margin = 64.0 * sys.float_info.epsilon * scale
    upper_bound = nextafter(raw_bound + margin, inf)

    return LagrangianCertificate(
        dual_variable=dual_variable,
        upper_bound=upper_bound,
        raw_upper_bound=raw_bound,
        roundoff_margin=upper_bound - raw_bound,
        pool_contributions=tuple(term.contribution for term in terms),
        relaxed_allocations=tuple(term.maximizing_amount for term in terms),
        incumbent_net_output=(
            None if incumbent is None else incumbent.net_output
        ),
    )


def _best_single_pool_route(
    pools: Sequence[Pool], total_input: float
) -> Route:
    routes = []
    for index in range(len(pools)):
        allocation = [0.0] * len(pools)
        allocation[index] = total_input
        routes.append(evaluate_route(pools, allocation))
    return max(routes, key=lambda route: route.net_output)


def gross_waterfill_route(
    pools: Sequence[Pool], total_input: float
) -> Route:
    """Water-fill all pools while ignoring gas, then charge the gas."""

    _validate_instance(pools, total_input)
    return evaluate_route(pools, waterfill(pools, total_input))


def initial_marginal_route(
    pools: Sequence[Pool], total_input: float
) -> Route:
    """Send the entire trade to the best initial marginal-output pool.

    This baseline intentionally ignores both curve depth and fixed cost.
    It records the common but invalid inference that the best infinitesimal
    quote must also be the best venue for a finite trade.
    """

    _validate_instance(pools, total_input)
    index = max(
        range(len(pools)),
        key=lambda candidate: pools[candidate].initial_marginal_output,
    )
    allocation = [0.0] * len(pools)
    allocation[index] = total_input
    return evaluate_route(pools, allocation)


def standalone_threshold_route(
    pools: Sequence[Pool], total_input: float
) -> Route:
    """Use pools whose standalone Q-sized swap repays their fixed charge.

    This is a plausible but non-certifying threshold heuristic.  The active
    pools are water-filled after selection.
    """

    _validate_instance(pools, total_input)
    selected = [
        index
        for index, pool in enumerate(pools)
        if pool.output(total_input) > pool.fixed_cost
    ]
    if not selected:
        return _best_single_pool_route(pools, total_input)

    local = waterfill([pools[index] for index in selected], total_input)
    allocation = [0.0] * len(pools)
    for index, amount in zip(selected, local):
        allocation[index] = amount
    return evaluate_route(pools, allocation)


def dual_threshold_route(
    pools: Sequence[Pool], total_input: float
) -> Route:
    """Water-fill pools strictly active at the minimizing dual price.

    A tied pool has zero reduced benefit and is omitted.  This makes the
    function deterministic, but it also exposes why dual thresholding is a
    heuristic when the relaxation has a gap.
    """

    _validate_instance(pools, total_input)
    certificate = lagrangian_certificate(pools, total_input)
    scale = max(1.0, certificate.raw_upper_bound)
    tolerance = 128.0 * sys.float_info.epsilon * scale
    selected = [
        index
        for index, contribution in enumerate(
            certificate.pool_contributions
        )
        if contribution > tolerance
    ]
    if not selected:
        return _best_single_pool_route(pools, total_input)

    local = waterfill([pools[index] for index in selected], total_input)
    allocation = [0.0] * len(pools)
    for index, amount in zip(selected, local):
        allocation[index] = amount
    return evaluate_route(pools, allocation)
