"""Deterministic timing comparison for the equal-price dynamic program."""

import argparse
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.equal_price_dp import exact_integer_reserve_dp
from src.parallel_cpmm import Pool, exact_enumeration


def make_instance(count: int, seed: int) -> tuple:
    rng = random.Random(seed)
    price = 2.5
    fee_factor = 0.997
    reserves = tuple(rng.randint(1, 500) for _ in range(count))
    return tuple(
        Pool(
            float(reserve),
            price * reserve,
            fee_factor,
            rng.uniform(0.0, 15.0),
        )
        for reserve in reserves
    )


def timed(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--enumeration-max",
        type=int,
        default=16,
        help="largest pool count used for exhaustive enumeration",
    )
    args = parser.parse_args()

    print("method,pools,reserve_sum,seconds,net_output")
    for count in (8, 12, 16):
        if count > args.enumeration_max:
            continue
        pools = make_instance(count, 1000 + count)
        total_input = 100.0
        route, elapsed = timed(exact_enumeration, pools, total_input)
        print(
            f"enumeration,{count},{sum(p.input_reserve for p in pools):.0f},"
            f"{elapsed:.9f},{route.net_output:.12f}"
        )
        solution, elapsed = timed(
            exact_integer_reserve_dp, pools, total_input
        )
        print(
            f"dynamic_program,{count},"
            f"{sum(p.input_reserve for p in pools):.0f},"
            f"{elapsed:.9f},{solution.route.net_output:.12f}"
        )

    for count in (25, 50, 100):
        pools = make_instance(count, 1000 + count)
        solution, elapsed = timed(
            exact_integer_reserve_dp, pools, 100.0
        )
        print(
            f"dynamic_program,{count},"
            f"{sum(p.input_reserve for p in pools):.0f},"
            f"{elapsed:.9f},{solution.route.net_output:.12f}"
        )


if __name__ == "__main__":
    main()
