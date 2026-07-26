import itertools
import math
from fractions import Fraction
import unittest

from src.parallel_cpmm import (
    Pool,
    exact_enumeration,
    subset_sum_reduction,
    waterfill,
)


class ParallelCPMMTests(unittest.TestCase):
    def test_equal_price_waterfill_is_proportional(self) -> None:
        pools = (
            Pool(2.0, 10.0),
            Pool(3.0, 15.0),
            Pool(5.0, 25.0),
        )
        allocation = waterfill(pools, 4.0)
        self.assertEqual(len(allocation), 3)
        for amount, pool in zip(allocation, pools):
            self.assertAlmostEqual(amount, 0.4 * pool.input_reserve)

    def test_waterfill_drops_inferior_pool(self) -> None:
        pools = (
            Pool(10.0, 100.0),
            Pool(10.0, 1.0),
        )
        allocation = waterfill(pools, 1.0)
        self.assertAlmostEqual(allocation[0], 1.0)
        self.assertEqual(allocation[1], 0.0)

    def test_fixed_cost_can_exclude_a_pool(self) -> None:
        pools = (
            Pool(10.0, 100.0, fixed_cost=0.0),
            Pool(10.0, 100.0, fixed_cost=100.0),
        )
        route = exact_enumeration(pools, 2.0)
        self.assertEqual(route.active_indices, (0,))
        self.assertAlmostEqual(route.allocations[0], 2.0)

    def test_subset_sum_reduction_yes_instance(self) -> None:
        target = 8
        pools, total_input = subset_sum_reduction((3, 5, 9), target)
        route = exact_enumeration(pools, total_input)
        self.assertAlmostEqual(route.net_output, target**2)
        active_weight = sum(
            (3, 5, 9)[i] for i in route.active_indices
        )
        self.assertEqual(active_weight, target)

    def test_subset_sum_reduction_no_instance(self) -> None:
        target = 7
        weights = (3, 5, 9)
        pools, total_input = subset_sum_reduction(weights, target)
        route = exact_enumeration(pools, total_input)
        self.assertLess(route.net_output, target**2)
        self.assertFalse(
            any(
                sum(choice) == target
                for size in range(len(weights) + 1)
                for choice in itertools.combinations(weights, size)
            )
        )

    def test_subset_sum_objective_has_exact_square_gap(self) -> None:
        target = 11
        for aggregate in range(1, 30):
            price = (target + 1) ** 2
            objective = (
                Fraction(price * aggregate, aggregate + 1)
                - aggregate
            )
            gap = Fraction(target**2) - objective
            self.assertEqual(
                gap,
                Fraction((aggregate - target) ** 2, aggregate + 1),
            )
            self.assertEqual(gap == 0, aggregate == target)

    def test_route_preserves_input(self) -> None:
        pools = (
            Pool(7.0, 20.0, 0.997),
            Pool(11.0, 50.0, 0.999),
            Pool(13.0, 25.0, 0.995),
        )
        route = exact_enumeration(pools, 6.25)
        self.assertTrue(math.isclose(sum(route.allocations), 6.25))


if __name__ == "__main__":
    unittest.main()
