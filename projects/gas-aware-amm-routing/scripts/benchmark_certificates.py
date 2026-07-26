"""Deterministic gap benchmark for certificates and routing baselines."""

import argparse
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.certifying_router import (
    dual_threshold_route,
    gross_waterfill_route,
    initial_marginal_route,
    lagrangian_certificate,
    standalone_threshold_route,
)
from src.parallel_cpmm import Pool, exact_enumeration


def make_instance(count: int, rng: random.Random) -> tuple:
    pools = []
    for _ in range(count):
        input_reserve = 10 ** rng.uniform(1.0, 3.0)
        spot_price = rng.uniform(0.7, 1.3)
        fee_factor = rng.uniform(0.995, 1.0)
        pools.append(
            Pool(
                input_reserve,
                spot_price * input_reserve,
                fee_factor,
                rng.uniform(0.0, 1.5),
            )
        )
    total_input = 10 ** rng.uniform(0.7, 2.0)
    return tuple(pools), total_input


def percentile(values: list, fraction: float) -> float:
    ordered = sorted(values)
    index = round(fraction * (len(ordered) - 1))
    return ordered[index]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260727)
    args = parser.parse_args()
    if args.trials <= 0:
        parser.error("--trials must be positive")

    rng = random.Random(args.seed)
    rows = []
    methods = {
        "dual_bound": None,
        "dual_threshold": dual_threshold_route,
        "gross_waterfill": gross_waterfill_route,
        "initial_marginal": initial_marginal_route,
        "standalone_threshold": standalone_threshold_route,
    }
    for count in (4, 6, 8):
        relative = {name: [] for name in methods}
        exact_count = 0
        for _ in range(args.trials):
            pools, total_input = make_instance(count, rng)
            optimum = exact_enumeration(pools, total_input)
            if optimum.net_output <= 0.0:
                continue
            exact_count += 1
            certificate = lagrangian_certificate(
                pools, total_input, optimum
            )
            relative["dual_bound"].append(
                certificate.additive_gap / optimum.net_output
            )
            for name, method in methods.items():
                if method is None:
                    continue
                route = method(pools, total_input)
                relative[name].append(
                    max(0.0, optimum.net_output - route.net_output)
                    / optimum.net_output
                )

        for name, values in relative.items():
            rows.append(
                (
                    name,
                    count,
                    exact_count,
                    statistics.median(values),
                    percentile(values, 0.9),
                    max(values),
                )
            )

    print(
        "method,pools,trials,median_relative_gap,"
        "p90_relative_gap,max_relative_gap"
    )
    for row in rows:
        print(
            f"{row[0]},{row[1]},{row[2]},"
            f"{row[3]:.12g},{row[4]:.12g},{row[5]:.12g}"
        )


if __name__ == "__main__":
    main()
