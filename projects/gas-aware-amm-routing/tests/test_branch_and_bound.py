import random
import unittest

from src.branch_and_bound import (
    certifying_branch_and_bound,
    partial_lagrangian_bound,
)
from src.parallel_cpmm import Pool, exact_enumeration, waterfill


class BranchAndBoundTests(unittest.TestCase):
    @staticmethod
    def _best_compatible_binary_value(
        pools, total_input, included_mask, excluded_mask
    ) -> float:
        best = float("-inf")
        for mask in range(1, 1 << len(pools)):
            if mask & included_mask != included_mask:
                continue
            if mask & excluded_mask:
                continue
            selected = [
                index
                for index in range(len(pools))
                if mask & (1 << index)
            ]
            local_pools = [pools[index] for index in selected]
            allocation = waterfill(local_pools, total_input)
            value = sum(
                pool.output(amount)
                for pool, amount in zip(local_pools, allocation)
            ) - sum(pool.fixed_cost for pool in local_pools)
            best = max(best, value)
        return best

    def test_partial_bounds_cover_compatible_routes(self) -> None:
        pools = (
            Pool(2.0, 7.0, 0.997, 0.2),
            Pool(5.0, 12.0, 0.999, 0.7),
            Pool(9.0, 15.0, 0.995, 0.1),
        )
        total_input = 4.0

        include_first = partial_lagrangian_bound(
            pools, total_input, included_mask=0b001
        )
        compatible = self._best_compatible_binary_value(
            pools, total_input, 0b001, 0
        )
        self.assertGreaterEqual(
            include_first.upper_bound,
            compatible,
        )

        exclude_first = partial_lagrangian_bound(
            pools, total_input, excluded_mask=0b001
        )
        compatible = self._best_compatible_binary_value(
            pools, total_input, 0, 0b001
        )
        self.assertGreaterEqual(
            exclude_first.upper_bound,
            compatible,
        )

    def test_random_partial_bounds_cover_all_binary_completions(self) -> None:
        rng = random.Random(20260728)
        for count in range(2, 7):
            for _ in range(20):
                pools = tuple(
                    Pool(
                        rng.uniform(0.5, 12.0),
                        rng.uniform(0.5, 20.0),
                        rng.uniform(0.95, 1.0),
                        rng.uniform(0.0, 2.0),
                    )
                    for _ in range(count)
                )
                total_input = rng.uniform(0.1, 10.0)
                included_mask = 0
                excluded_mask = 0
                for index in range(count):
                    state = rng.randrange(3)
                    if state == 1:
                        included_mask |= 1 << index
                    elif state == 2:
                        excluded_mask |= 1 << index
                if included_mask == 0 and excluded_mask == (1 << count) - 1:
                    excluded_mask &= ~(1 << rng.randrange(count))

                bound = partial_lagrangian_bound(
                    pools,
                    total_input,
                    included_mask,
                    excluded_mask,
                )
                compatible = self._best_compatible_binary_value(
                    pools,
                    total_input,
                    included_mask,
                    excluded_mask,
                )
                self.assertGreaterEqual(bound.upper_bound, compatible)

    def test_matches_enumeration_on_random_instances(self) -> None:
        rng = random.Random(20260727)
        for count in range(1, 9):
            for _ in range(20):
                pools = tuple(
                    Pool(
                        rng.uniform(0.5, 20.0),
                        rng.uniform(0.5, 30.0),
                        rng.uniform(0.95, 1.0),
                        rng.uniform(0.0, 3.0),
                    )
                    for _ in range(count)
                )
                total_input = rng.uniform(0.1, 15.0)
                exact = exact_enumeration(pools, total_input)
                result = certifying_branch_and_bound(
                    pools, total_input
                )

                self.assertAlmostEqual(
                    result.route.net_output,
                    exact.net_output,
                    places=9,
                )
                self.assertGreaterEqual(
                    result.upper_bound + 1e-12,
                    exact.net_output,
                )
                self.assertTrue(result.certified_within_tolerance)

    def test_node_limit_preserves_global_certificate(self) -> None:
        pools = (
            Pool(1.0, 4.0, fixed_cost=0.25),
            Pool(1.0, 4.0, fixed_cost=0.5),
            Pool(2.0, 3.0, fixed_cost=0.1),
            Pool(4.0, 5.0, fixed_cost=0.2),
        )
        exact = exact_enumeration(pools, 2.0)
        result = certifying_branch_and_bound(
            pools,
            2.0,
            node_limit=1,
            absolute_tolerance=0.0,
            relative_tolerance=0.0,
        )

        self.assertTrue(result.hit_node_limit)
        self.assertGreaterEqual(result.upper_bound, exact.net_output)
        self.assertGreaterEqual(result.additive_gap, 0.0)

    def test_rejects_overlapping_partial_masks(self) -> None:
        pools = (Pool(1.0, 2.0),)
        with self.assertRaises(ValueError):
            partial_lagrangian_bound(
                pools,
                1.0,
                included_mask=1,
                excluded_mask=1,
            )


if __name__ == "__main__":
    unittest.main()
