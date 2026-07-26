import random
import unittest

from src.certifying_router import (
    activation_threshold,
    dual_threshold_route,
    gross_waterfill_route,
    initial_marginal_route,
    lagrangian_certificate,
    pool_dual_term,
    standalone_threshold_route,
)
from src.parallel_cpmm import Pool, exact_enumeration


class CertifyingRouterTests(unittest.TestCase):
    def test_activation_threshold_makes_net_conjugate_zero(self) -> None:
        pool = Pool(2.0, 8.0, 0.9, 2.0)
        threshold = activation_threshold(pool)
        at_threshold = pool_dual_term(pool, threshold)
        below_threshold = pool_dual_term(pool, 0.99 * threshold)
        above_threshold = pool_dual_term(pool, 1.01 * threshold)

        self.assertFalse(at_threshold.active)
        self.assertGreater(below_threshold.contribution, 0.0)
        self.assertTrue(below_threshold.active)
        self.assertEqual(above_threshold.contribution, 0.0)
        self.assertFalse(above_threshold.active)

    def test_zero_fixed_cost_certificate_is_exact(self) -> None:
        pools = (
            Pool(7.0, 20.0, 0.997),
            Pool(11.0, 50.0, 0.999),
            Pool(13.0, 25.0, 0.995),
        )
        optimum = exact_enumeration(pools, 6.25)
        certificate = lagrangian_certificate(pools, 6.25, optimum)

        self.assertAlmostEqual(
            certificate.raw_upper_bound,
            optimum.net_output,
            places=12,
        )
        self.assertAlmostEqual(certificate.additive_gap, 0.0, places=12)

    def test_certificate_bounds_random_small_instances(self) -> None:
        rng = random.Random(20260727)
        for count in range(1, 8):
            for _ in range(30):
                pools = tuple(
                    Pool(
                        input_reserve=rng.uniform(0.5, 20.0),
                        output_reserve=rng.uniform(0.5, 30.0),
                        fee_factor=rng.uniform(0.95, 1.0),
                        fixed_cost=rng.uniform(0.0, 3.0),
                    )
                    for _ in range(count)
                )
                total_input = rng.uniform(0.1, 15.0)
                optimum = exact_enumeration(pools, total_input)
                certificate = lagrangian_certificate(
                    pools, total_input, optimum
                )

                self.assertGreaterEqual(
                    certificate.upper_bound,
                    optimum.net_output,
                )
                self.assertGreaterEqual(certificate.additive_gap, 0.0)

    def test_gross_and_standalone_thresholding_can_overactivate(self) -> None:
        pools = (
            Pool(1.0, 2.0, fixed_cost=0.5),
            Pool(1.0, 2.0, fixed_cost=0.5),
        )
        optimum = exact_enumeration(pools, 1.0)
        gross = gross_waterfill_route(pools, 1.0)
        threshold = standalone_threshold_route(pools, 1.0)

        self.assertAlmostEqual(optimum.net_output, 0.5)
        self.assertAlmostEqual(gross.net_output, 1.0 / 3.0)
        self.assertEqual(threshold, gross)

    def test_dual_threshold_rounding_can_fail_at_exact_bound(self) -> None:
        pools = (
            Pool(2.0, 2.0, fixed_cost=0.25),
            Pool(2.0, 2.0, fixed_cost=0.5),
        )
        optimum = exact_enumeration(pools, 4.0)
        certificate = lagrangian_certificate(pools, 4.0, optimum)
        rounded = dual_threshold_route(pools, 4.0)

        self.assertAlmostEqual(optimum.net_output, 1.25)
        self.assertAlmostEqual(
            certificate.raw_upper_bound,
            optimum.net_output,
        )
        self.assertAlmostEqual(rounded.net_output, 13.0 / 12.0)
        self.assertLess(rounded.net_output, optimum.net_output)

    def test_initial_marginal_sorting_ignores_depth(self) -> None:
        pools = (
            Pool(1.0, 2.0),
            Pool(100.0, 190.0),
        )
        naive = initial_marginal_route(pools, 100.0)
        optimum = exact_enumeration(pools, 100.0)

        self.assertEqual(naive.active_indices, (0,))
        self.assertGreater(optimum.net_output, 40.0 * naive.net_output)


if __name__ == "__main__":
    unittest.main()
