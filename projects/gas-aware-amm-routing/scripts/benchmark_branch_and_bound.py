"""Compare certifying branch-and-bound with exhaustive subset enumeration."""

import argparse
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.benchmark_certificates import make_instance
from src.branch_and_bound import certifying_branch_and_bound
from src.parallel_cpmm import exact_enumeration, subset_sum_reduction


def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start


def heterogeneous_rows(trials: int, seed: int):
    rng = random.Random(seed)
    for count in (8, 10, 12):
        enumeration_seconds = 0.0
        branch_seconds = 0.0
        explored = []
        generated = []
        for _ in range(trials):
            pools, total_input = make_instance(count, rng)
            exact, elapsed = timed(
                exact_enumeration, pools, total_input
            )
            enumeration_seconds += elapsed
            result, elapsed = timed(
                certifying_branch_and_bound, pools, total_input
            )
            branch_seconds += elapsed
            if abs(result.route.net_output - exact.net_output) > 1e-8:
                raise RuntimeError("branch-and-bound disagrees with oracle")
            explored.append(result.nodes_explored)
            generated.append(result.nodes_generated)
        yield (
            "heterogeneous",
            count,
            trials,
            enumeration_seconds,
            branch_seconds,
            statistics.median(explored),
            max(explored),
            statistics.median(generated),
        )


def reduction_rows(seed: int):
    rng = random.Random(seed)
    for count in (8, 10, 12, 14, 16):
        weights = tuple(rng.randint(1, 30) for _ in range(count))
        target = sum(weights) // 2
        pools, total_input = subset_sum_reduction(weights, target)
        exact, enumeration_seconds = timed(
            exact_enumeration, pools, total_input
        )
        result, branch_seconds = timed(
            certifying_branch_and_bound, pools, total_input
        )
        if abs(result.route.net_output - exact.net_output) > 1e-7:
            raise RuntimeError("branch-and-bound disagrees with oracle")
        yield (
            "subset_sum",
            count,
            1,
            enumeration_seconds,
            branch_seconds,
            result.nodes_explored,
            result.nodes_explored,
            result.nodes_generated,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260728)
    args = parser.parse_args()
    if args.trials <= 0:
        parser.error("--trials must be positive")

    print(
        "family,pools,trials,enumeration_seconds,branch_seconds,"
        "median_nodes_explored,max_nodes_explored,median_nodes_generated"
    )
    rows = (
        *heterogeneous_rows(args.trials, args.seed),
        *reduction_rows(args.seed + 1),
    )
    for row in rows:
        print(
            f"{row[0]},{row[1]},{row[2]},"
            f"{row[3]:.9f},{row[4]:.9f},"
            f"{row[5]:.1f},{row[6]},{row[7]:.1f}"
        )


if __name__ == "__main__":
    main()
