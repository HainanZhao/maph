import random
import unittest

from src.equal_price_dp import (
    exact_integer_reserve_dp,
    rounded_reserve_dp,
)
from src.parallel_cpmm import Pool, exact_enumeration


class EqualPriceDPTests(unittest.TestCase):
    def test_matches_enumeration_on_random_instances(self) -> None:
        rng = random.Random(20260727)
        for count in range(1, 9):
            for _ in range(20):
                price = rng.uniform(0.5, 10.0)
                fee_factor = rng.choice((0.99, 0.997, 1.0))
                pools = tuple(
                    Pool(
                        input_reserve=float(reserve),
                        output_reserve=price * reserve,
                        fee_factor=fee_factor,
                        fixed_cost=rng.uniform(0.0, 3.0),
                    )
                    for reserve in (
                        rng.randint(1, 12) for _ in range(count)
                    )
                )
                total_input = rng.uniform(0.1, 20.0)
                oracle = exact_enumeration(pools, total_input)
                dynamic = exact_integer_reserve_dp(pools, total_input)
                self.assertAlmostEqual(
                    dynamic.route.net_output,
                    oracle.net_output,
                    places=9,
                )

    def test_rounding_obeys_additive_bound(self) -> None:
        pools = (
            Pool(2.3, 11.5, 0.997, 0.1),
            Pool(4.7, 23.5, 0.997, 1.3),
            Pool(7.2, 36.0, 0.997, 0.2),
            Pool(9.9, 49.5, 0.997, 2.0),
        )
        total_input = 3.0
        quantum = 0.5
        exact = exact_enumeration(pools, total_input)
        rounded = rounded_reserve_dp(pools, total_input, quantum)
        price = 5.0
        bound = price * len(pools) * quantum
        self.assertGreaterEqual(
            rounded.route.net_output + bound + 1e-12,
            exact.net_output,
        )

    def test_rejects_heterogeneous_prices(self) -> None:
        pools = (
            Pool(2.0, 10.0),
            Pool(3.0, 18.0),
        )
        with self.assertRaises(ValueError):
            exact_integer_reserve_dp(pools, 1.0)

    def test_rejects_noninteger_exact_instance(self) -> None:
        pools = (
            Pool(2.5, 10.0),
            Pool(3.0, 12.0),
        )
        with self.assertRaises(ValueError):
            exact_integer_reserve_dp(pools, 1.0)


if __name__ == "__main__":
    unittest.main()
